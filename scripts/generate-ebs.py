from subprocess import check_output
import json

try:
    result = check_output('aws elasticache describe-cache-clusters --show-cache-node-info', shell=True)
    data = json.loads(result)
    redis_node_url = data.get('CacheClusters')[0].get('CacheNodes')[0].get('Endpoint').get('Address')
    redis_node_port = data.get('CacheClusters')[0].get('CacheNodes')[0].get('Endpoint').get('Port')

    redis_config_template = """
    """
except Exception as e:
    pass

options_config_template = """option_settings:
  - option_name: GSPREAD_CREDENTIALS
    value: {}"""
options_config = ""

with open('./credentials/googlekey.json', 'r') as credfile:
    key = credfile.read()
    serialized = json.dumps(json.loads(key))
    options_config = options_config_template.format(serialized)

with open('./.ebextensions/secrets.config', 'w') as configfile:
    configfile.write(options_config)
