from os import environ as env

from dotenv import load_dotenv


def token_loader():
    load_dotenv()
    if bool(env['INVEST_TOKEN']):
        return env['INVEST_TOKEN']
    else:
        print('Token is not exist!')
        return None
