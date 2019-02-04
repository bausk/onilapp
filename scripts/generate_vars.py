import json
import os


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


def write_production(variables):
    lines = ["option_settings:"]
    variable_template = """  - option_name: {}
    value: {}"""
    for key, value in variables.items():
        lines.append(variable_template.format(key, value))
    with open('./.ebextensions/secrets.config', 'w') as configfile:
        configfile.write('\n'.join(lines))


def write_development(variables):
    for key, value in variables.items():
        os.environ[key] = value


if __name__ == '__main__':
    variables = get_variables('production')
    write_production(variables)