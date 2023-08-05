import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import json
from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql

def getToken(connection, schema, chain_id, token_address):
    
    query = "SELECT * FROM %s.token WHERE chain_id = %s AND token_address = '%s';"
    
    result = herokuDbAccess.fetchDataInDatabase(query, [sql.Identifier(schema),chain_id,token_address], connection)    
    return result[0][0]

def getTokenWithoutName(connection, schema, chain_id, gteCreatedAt):
    
    query = "SELECT * FROM %s.evm_token WHERE chain_id = %s AND name = 'n/a' AND created_at >= %s"
    
    result = herokuDbAccess.fetchDataInDatabase(query, [sql.Identifier(schema),chain_id,gteCreatedAt], connection)    
    return result[0][0]

def getTokenWN(connection, schema, chain_id, gteCreatedAt):
    
    query = "SELECT * FROM %s.evm_token WHERE chain_id = %s AND name = 'n/a' AND created_at >= %s"
    
    result = herokuDbAccess.fetchDataInDatabase(query, [sql.Identifier(schema),chain_id,gteCreatedAt], connection)    
    return result[0][0]