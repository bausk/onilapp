import json
from subprocess import check_output
from scripts.scriptutils.googlecreds import read_google_creds


def write_custom():
    pass


def write_variables(variables):
    with open('./zappa_settings.json', 'r') as settings_json:
        settings = json.loads(settings_json.read())
    settings['dev']['environment_variables'] = {}
    custom_vars = settings['dev']['environment_variables']
    # Write standard stuff
    for key, value in variables.items():
        custom_vars[key] = value
    # Write custom stuff
    result = check_output('aws elasticache describe-cache-clusters --show-cache-node-info', shell=True)
    data = json.loads(result)
    redis_node_url = data.get('CacheClusters')[0].get('CacheNodes')[0].get('Endpoint').get('Address')
    redis_node_port = data.get('CacheClusters')[0].get('CacheNodes')[0].get('Endpoint').get('Port')
    custom_vars['REDIS_HOST'] = "{}:{}".format(redis_node_url, redis_node_port)
    custom_vars['GSPREAD_CREDENTIALS'] = read_google_creds()
    with open('./zappa_settings.json', 'w') as outfile:
        json.dump(settings, outfile, indent=4)

if __name__ == "__main__":
    write_custom()
