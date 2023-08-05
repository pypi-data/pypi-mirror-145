from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql

def getKeywords(connection, schema, token_address, chain_id):
    
    query = sql.SQL("SELECT keywords FROM {}.KeywordConfig \
           WHERE chain_id = %d AND token_address = %s").format(sql.Identifier(schema))
    
    params =(chain_id, token_address)
    
    result = herokuDbAccess.fetchDataInDatabase(query, params, connection)    
    return result
 
    