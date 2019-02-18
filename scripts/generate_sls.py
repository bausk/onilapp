import json
from subprocess import check_output
from scripts.scriptutils.googlecreds import read_google_creds


def write_custom():
    pass


def write_variables(variables):
    # Write custom stuff
    print('> Provisioning SLS variables...\n')
    custom_vars = variables.copy()
    custom_vars['GSPREAD_CREDENTIALS'] = read_google_creds()
    with open('./secrets.yml', 'w') as secrets:
        for key, value in custom_vars.items():
            secrets.write("{}: {}\n".format(key, json.dumps(value)))

if __name__ == "__main__":
    write_variables({})
