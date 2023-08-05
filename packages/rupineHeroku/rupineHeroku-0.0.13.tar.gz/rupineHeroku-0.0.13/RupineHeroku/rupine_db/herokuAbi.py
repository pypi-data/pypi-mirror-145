import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from RupineHeroku.rupine_db import herokuDbAccess

def getAbi(connection, schema, token_address, chain_id):
    
    sql = "SELECT abi FROM {}.evm_token \
           WHERE chain_id = {} AND token_address = {}".format(schema, chain_id, token_address)
    
    result = herokuDbAccess.fetchDataInDatabase(sql, connection)    
    return result[0][0]

def updateAbi(connection, schema, abi, token_address, chain_id):
    
    sql = "UPDATE {}.evm_token \
           SET abi={} \
           WHERE chain_id = {} AND token_address = {}".format(schema, abi, chain_id, token_address)
    
    herokuDbAccess.insertDataIntoDatabase(sql, connection)    
    