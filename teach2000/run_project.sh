echo "migrating"
python3 manage.py migrate
echo "starting server"
python3 manage.py runserver 0.0.0.0:8000
echo "done"