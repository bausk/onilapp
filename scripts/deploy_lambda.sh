pipenv shell
pipenv lock -r > requirements.txt
python scripts/generate_vars.py
zappa deploy