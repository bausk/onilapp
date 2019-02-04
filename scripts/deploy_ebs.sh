pipenv shell
python scripts/generate-ebs.py
python scripts/generate_vars.py
eb deploy development