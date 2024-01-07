    <script>
        function previewFile() {
            const preview = document.getElementById('image-preview');
            const file = document.querySelector('input[type=file]').files[0];
            const reader = new FileReader();

            reader.onloadend = function() {
                preview.src = reader.result;
                preview.style.display = 'block';
            }

            if (file) {
                reader.readAsDataURL(file);
            } else {
                preview.src = "";
                preview.style.display = 'none';
            }
        }

         function previewURL(input) {
            const preview = document.getElementById('image-preview');
            const url = input.value;

            if (url) {
                preview.src = url;
                preview.style.display = 'block';
            } else {
                preview.src = "";
                preview.style.display = 'none';
            }
        }
    </script>
