START cmd.exe /k "cd HealthNet/ & pip install Pillow & python manage.py makemigrations profiles & python manage.py makemigrations appointments & python manage.py makemigrations log & python manage.py migrate & python manage.py runserver"
Timeout 15
START "" http://127.0.0.1:8000
