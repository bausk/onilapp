pipenv shell
pipenv lock -r > requirements.txt
python scripts/generate_ebs.py
python scripts/generate_vars.py
eb deploy development