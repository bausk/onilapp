import json
import os
import sys 
sys.path.append('.')
from scripts.scriptutils.googlecreds import read_google_creds
from scripts import generate_ebs, generate_lambda, generate_sls
from backend.secrets import SECRETS


def get_variables(*envs):
    variables = {}
    for env in envs:
        try:
            with open('./credentials/variables.{}.json'.format(env), 'r') as varfile:
                json_string = varfile.read()
                json_variables = json.loads(json_string)
                for entry in json_variables:
                    key = entry.get('key', None)
                    value = entry.get('value', '')
                    if key:
                        variables[key] = value
        except Exception:
            pass
    return variables


def write_development(variables):
    for key, value in variables.items():
        os.environ[key] = value
    serialized_creds = read_google_creds()
    os.environ[SECRETS.GOOGLE_CRED.value] = serialized_creds


if __name__ == '__main__':
    variables = get_variables('production')
    generate_ebs.write_variables(variables)
    generate_lambda.write_variables(variables)
    variables = get_variables('slslambda')
    generate_sls.write_variables(variables)
