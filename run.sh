cron -f &
/etc/init.d/postfix start
cd app
python manage.py makemigrations
python manage.py migrate

python ini_db.py

python manage.py runserver 0.0.0.0:8002