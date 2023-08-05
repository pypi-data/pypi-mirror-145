import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from RupineHeroku.rupine_db import herokuDbAccess

def getKeywords(connection, schema, token_address, chain_id):
    
    sql = "SELECT keywords FROM {}.KeywordConfig \
           WHERE chain_id = {} AND token_address = {}".format(schema, chain_id, token_address)
    
    result = herokuDbAccess.fetchDataInDatabase(sql, connection)    
    return result[0][0]
 
    