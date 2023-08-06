Starmerx Apollo Client


Demo:

from starmerx_apollo_client.apollo_client import ApolloClient
from utils.env import env

CONFIG_URL = env.get_value('APOLLO_CONFIG_URL', default='')
APP_ID = env.get_value('APOLLO_APP_ID', default='')
APP_SECRET = env.get_value('APOLLO_APP_SECRET', default='')

a_client = ApolloClient(app_id=APP_ID, secret=APP_SECRET, config_url=CONFIG_URL)


