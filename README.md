BUILT ON A CLEAN UBUNTU SERVER RUNNING 22.04 AND PYTHON 3.10 .12
You can use a requirements.txt
Or use this 

python3.10 -m pip install flask
python3.10 -m pip install tensorflow
python3.10 -m pip install pillow
python3.10 -m pip install mysql.connector
for your server conf here is a start






server {
        listen 80;
        listen [::]:80;
        server_name your.com www.your.com localhost ur.ip.add.ress;
        # enforce https
        return 301 https:// your.com $request_uri;
        }
server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name your.com www.your.com localhost ur.ip.add.ress;

        root where/your/flask/is;
        index your flask.py-file;

        access_log /var/log/nginx/access.log;
        error_log  /var/log/nginx/error.log;

        client_body_buffer_size  128k;
        client_header_buffer_size 128k;
        client_max_body_size 24m;
        large_client_header_buffers 2 128k;
        sendfile off;

        ssl_certificate /etc/letsencrypt/live/your.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/your.com/privkey.pem;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;
        ssl_ciphers "your ciphers";
        ssl_dhparam /etc/ssl/certs/dhparam.pem;
        # Add headers to serve security related headers
        add_header Access-Control-Allow-Origin "http://your.com";
        add_header Access-Control-Allow-Methods "GET, OPTIONS, DELETE, POST";
        add_header Referrer-Policy "same-origin";
        add_header Referrer-Policy "strict-origin-when-cross-origin";
        add_header Access-Control-Expose-Headers "Origin";
        add_header Access-Control-Max-Age "3600";
        add_header X-Content-Type-Options "nosniff";

        location / {
        proxy_pass http://ur.ip.add.ress:8880/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Prefix /;

         location ~ ^/index\.php$ {
                fastcgi_split_path_info ^(.+\.php)(/.+)$;
                fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
                fastcgi_index index.php;
                include fastcgi_params;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                fastcgi_intercept_errors off;
                fastcgi_buffer_size 16k;
                fastcgi_buffers 4 16k;
                fastcgi_connect_timeout 300;
                fastcgi_send_timeout 300;
                fastcgi_read_timeout 300;
                include /etc/nginx/fastcgi_params;
                try_files $uri $uri/ =404;
        }

         location ~ \.php$ {
                fastcgi_split_path_info ^(.+\.php)(/.+)$;
                fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
                fastcgi_index index.php;
                include fastcgi.conf;
        }
        location ~ \.sh {
                return 404;
        }

        location ~ /\.ht {
                deny all;
        }

        location /phpmyadmin {
                root /usr/share/;
                index index.php;
                try_files $uri $uri/ =404;
                location ~ ^/phpmyadmin/(doc|sql|setup)/ {
                deny all;
        }

        location ~ /phpmyadmin/(.+\.php)$ {
                fastcgi_pass unix:/run/php/php8.1-fpm.sock;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                include fastcgi_params;
                include snippets/fastcgi-php.conf;
        }
      }
    }
}
You will need a database-config .json
Basically 
{
        "host": "database host”,
        "user": "database username",
        "password": "password",
        "db": "database name"
}



And if your using secrets in your flask a secrets-conf.json
{
	"Secret_Key": "your log secret poassword”
}

You will need to train a model I used vgg models to train mine  and ra a 10 epoh followed by a 40 epoch training session.

If you would like to purchase the pretrained on a half of a million cards model I am open to offers on the model as well as the script I used to train said model.

the final product is here 108.61.177.88

here are some screen shots 

start page ![Screenshot 2024-01-07 at 15-10-57 Lucky Grader](https://github.com/justin-a-nobody/grader/assets/155355958/6339497f-0958-4e65-8dc1-93b99e2530a7)


Find a card to grade ![Screenshot 2024-01-07 at 15-11-56 1986 1987 FLEER BASKETBALL - YOU PICK #1 - #132 NMMT FREE SHIP eBay](https://github.com/justin-a-nobody/grader/assets/155355958/6d94c8f8-69d2-4ce7-874c-f27b32dc3ac1)

get its url ![Screenshot 2024-01-07 at 15-12-13 s-l1600 png (PNG Image 868 × 1150 pixels) — Scaled (61%)](https://github.com/justin-a-nobody/grader/assets/155355958/f1868e6b-7932-4422-b58c-41be1e4ad63f)

fill out the form then hit upload ![Screenshot 2024-01-07 at 15-13-10 Lucky Grader](https://github.com/justin-a-nobody/grader/assets/155355958/95e25e02-83de-48ce-83c2-efc31ec286d5)

Get your grade ![Screenshot 2024-01-07 at 15-13-27 Lucky Grader](https://github.com/justin-a-nobody/grader/assets/155355958/9506036e-1a87-47a2-a71a-3f2974a56a34)

