mkdir output
pipenv lock -r > requirements.txt
pip install -r requirements.txt --no-deps -t output
zip -r output.zip output
