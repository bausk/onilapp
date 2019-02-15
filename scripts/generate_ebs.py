import json
from subprocess import check_output
from scripts.scriptutils.googlecreds import read_google_creds


def write_custom():
    try:
        result = check_output('aws elasticache describe-cache-clusters --show-cache-node-info', shell=True)
        data = json.loads(result)
        redis_node_url = data.get('CacheClusters')[0].get('CacheNodes')[0].get('Endpoint').get('Address')
        redis_node_port = data.get('CacheClusters')[0].get('CacheNodes')[0].get('Endpoint').get('Port')

        redis_config_template = """option_settings:
  - option_name: REDIS_HOST
    value: {}:{}"""
        redis_config = redis_config_template.format(redis_node_url, redis_node_port)
        with open('./.ebextensions/redis.config', 'w') as configfile:
            configfile.write(redis_config)
    except Exception as e:
        pass

    options_config_template = """option_settings:
  - option_name: GSPREAD_CREDENTIALS
    value: {}"""
    serialized_creds = read_google_creds()
    options_config = options_config_template.format(serialized_creds)

    with open('./.ebextensions/gsheets.config', 'w') as configfile:
        configfile.write(options_config)


def write_variables(variables):
    lines = ["option_settings:"]
    variable_template = """  - option_name: {}
    value: {}"""
    for key, value in variables.items():
        lines.append(variable_template.format(key, value))
    with open('./.ebextensions/secrets.config', 'w') as configfile:
        configfile.write('\n'.join(lines))

if __name__ == "__main__":
    write_custom()
