import os

os.system("python manage.py db init")
os.system("python manage.py db migrate")
os.system("python manage.py db upgrade")
