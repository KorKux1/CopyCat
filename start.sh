pip install -r requirements.txt

$env:FLASK_APP = 'main.py'
$env:FLASK_DEBUG=1
$env:FLASK_ENV="development"
flask run