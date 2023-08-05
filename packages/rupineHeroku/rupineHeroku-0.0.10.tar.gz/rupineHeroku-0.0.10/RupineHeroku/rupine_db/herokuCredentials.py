from ntpath import join
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from RupineHeroku.rupine_db import herokuDbAccess


def getCredential(connection, schema, chain_id):
    
    username = getCredential(connection, schema, 'ankr_prod', 'USERNAME', chain_id)
    password = getCredential(connection, schema, 'ankr_prod', 'PASSWORD', chain_id)

    return ':'.join([username,password])

def getCredential(connection, schema, credential_name, credential_type, chain_id):
    
    sql = 'SELECT credentials_value \
           FROM {}.credentials \
           WHERE credentials_name = \'{}\' AND  credentials_type = \'{}\' AND chain_id = {};'.format(schema, credential_name, credential_type, chain_id)
    
    retVal = herokuDbAccess.fetchDataInDatabase(sql, connection)
    return retVal[0][0]
    