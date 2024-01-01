from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import shutil
from PIL import Image,  ImageEnhance
import mysql.connector
import json
import requests

# GPU Configuration
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except RuntimeError as e:
        print(e)

# Load the trained model
model_path = 'path to your best_model.keras'
model = tf.keras.models.load_model(model_path)

app = Flask(__name__)

@app.route('/card_grader')
def card_grader():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/enter')
def enter():
    return render_template('enter.html')


app.config['UPLOAD_FOLDER'] = 'static/imgs'
app.config['WATERMARKED_FOLDER'] = 'static/watermarked'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}




# Load database configuration
with open('path to your database config file') as config_file:
    app.config['DB_CONFIG'] = json.load(config_file)

with open('path to yoiur config file') as config_file:
    app.config['SITE_CONF'] = json.load(config_file)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_next_number():
    counter_file = 'path to your counter.txt'
    if not os.path.exists(counter_file):
        with open(counter_file, 'w') as file:
            file.write('0')
        return 1

    with open(counter_file, 'r') as file:
        number = int(file.read().strip())

    with open(counter_file, 'w') as file:
        file.write(str(number + 1))

    return number + 1
    
def apply_watermark(image_path, watermark_image_path=None, opacity=0.66):
    image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA") if watermark_image_path else None

    # Resize image and 224watermark
    image = image.resize((500, 750), Image.Resampling.LANCZOS)
    if watermark:
        watermark = watermark.resize((200, 200), Image.Resampling.LANCZOS)

        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)

        # Calculate position for watermark
        watermark_position = (image.width - watermark.width - 10, image.height - watermark.height - 10)

        # Paste watermark onto the image
        image.paste(watermark, watermark_position, watermark)

        # Save the watermarked image
        watermarked_image_name = os.path.basename(image_path)
        watermarked_image_path = os.path.join(app.config['WATERMARKED_FOLDER'], watermarked_image_name)
        image = image.convert("RGB")  # Convert back to RGB to save in JPG format
        image.save(watermarked_image_path)
        return watermarked_image_path
    else:
        return image_path

def save_upload_details(filename, watermarked_image_path, grade, card_number, card_maker, card_player, card_year, card_type, image_url, spec_info):
    grade = int(grade) if isinstance(grade, np.int64) else grade
    card_year = int(card_year) if isinstance(card_year, np.int64) else card_year

    conn = mysql.connector.connect(**app.config['DB_CONFIG'])
    cursor = conn.cursor()
    query = """
    INSERT INTO uploads (filename, watermarked_image_path, grade, card_number, card_maker, card_player, card_year, card_type, image_url, spec_info)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (filename, watermarked_image_path, grade, card_number, card_maker, card_player, card_year, card_type, image_url, spec_info))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        image_url = request.form.get('image_url')
        if file and file.filename != '' and allowed_file(file.filename):
            next_number = get_next_number()
            extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{next_number}.{extension}"

            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

        elif image_url:
            # Download and process the image from the URL
            try:
                responce = requests.get(image_url)
                responce.raise_for_status()

                next_number = get_next_number()
                extension = image_url.rsplit('.', 1)[1].lower()
                filename = f"{next_number}.{extension}"

                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                with open(save_path, 'wb') as f:
                    f.write(responce.content)
            except requests.exceptions.RequestException as e:
                # Handle any errors that occur during download
                print(f"Error downloading image: {e}")
                return render_template('error.html', error_message="Error downloading image.")

        else:
            # No file or URL provided
            return redirect(request.url)

         # Apply watermark
        watermarked_image_path = apply_watermark(save_path, 'static/wm.png')

        # Process the image for grading
        relative_image_path, grade = grade_card(save_path)

        # Extract additional form data
        image_url = request.form.get('image_url')
        card_number = request.form.get('card_number')
        card_maker = request.form.get('card_maker')
        card_player = request.form.get('card_player')
        card_year = request.form.get('card_year')
        card_type = request.form.get('card_type')
        spec_info = request.form.get('spec_info')


        # Save upload details to database with additional data
        uploader_ip = request.remote_addr
        save_upload_details(filename, watermarked_image_path, grade, card_number, card_maker, card_player, card_year, card_type, image_url, spec_info)

        return render_template('results.html', image_path=watermarked_image_path, grade=grade)

    return render_template('index.html')

def preprocess_image(image_path, target_size=(250, 350)):
    image = load_img(image_path, target_size=target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image /= 255.0
    return image


def grade_card(image_path):
    processed_image = preprocess_image(image_path)
    prediction = model.predict(processed_image)
    grade = np.argmax(prediction, axis=1)[0]
    
    if grade == 0:
        grade = 10

    if grade ==1:
        grade = 10

    grade_folder = f"imgs"
    new_filename = f"grade_{grade}_{os.path.basename(image_path)}"
    grade_folder_path = os.path.join(app.config['UPLOAD_FOLDER'], grade_folder)
    if not os.path.exists(grade_folder_path):
        os.makedirs(grade_folder_path)
    new_file_path = os.path.join(grade_folder_path, new_filename)
    shutil.move(image_path, new_file_path)

    return os.path.join(grade_folder, new_filename), grade

if __name__ == '__main__':
    app.run(host='your.ip.add.ress', port=8880, debug=True)
