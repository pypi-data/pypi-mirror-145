from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql

def getToken(connection, schema, chain_id, token_address):
    
    query = sql.SQL("SELECT * FROM {}.token WHERE chain_id = %s AND token_address = %s").format(sql.Identifier(schema))
    
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,token_address], connection)    
    return result

def getTokenWithoutName(connection, schema, chain_id, gteCreatedAt):
    
    query = sql.SQL("SELECT * FROM {}.evm_token WHERE chain_id = %s AND name = 'n/a' AND created_at >= %s").format(sql.Identifier(schema))
    
    result = herokuDbAccess.fetchDataInDatabase(query, [chain_id,gteCreatedAt], connection)    
    return result