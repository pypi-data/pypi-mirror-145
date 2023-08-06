from RupineHeroku.rupine_db import herokuDbAccess
from psycopg2 import sql

def postTaxTransaction(connection, schema, data):

    query = sql.SQL("INSERT INTO {}.tax_transaction (chain_id,chain,public_address,timestamp,block_number,transaction_hash,category,token,amount,usd_value,eur_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
    params = (
        data['chain_id'],
        data['chain'],
        data['public_address'],
        data['timestamp'],
        data['block_number'],
        data['transaction_hash'],
        data['category'],
        data['token'],
        data['amount'],
        data['usd_value'],
        data['eur_value'])
    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result

def getTaxTransaction(connection, schema, token:str=None, timestamp:int=0, posNegAll:str='all'):
    '''
    Parameters:
        - token: String of Token, e.g. URHT, DUSD-URTH, etc. Default is None
        - timestamp: all data with timestamp gte. Default is 0
        - posNegAll: "positive", "negative" or "all". is Amount gte 0, lt 0 or everything. Default is 'all'
    '''
    conditions = ""
    params = []
    if token != None:
        conditions = conditions + " AND token = %s"
        params.append(token)
    
    if posNegAll == 'positive':
        conditions = conditions + " AND amount >= 0"
    elif posNegAll == 'negative':
        conditions = conditions + " AND amount < 0"
 
    query = sql.SQL("SELECT * FROM {}.tax_transaction WHERE 1=1 AND timestamp >= %s" + conditions).format(sql.Identifier(schema))
    result = herokuDbAccess.fetchDataInDatabase(query, [timestamp,*params], connection)    
       
    return result


def postTaxReward(connection, schema, data):

    query = sql.SQL("INSERT INTO {}.tax_reward (chain_id,chain,public_address,timestamp,category,token,amount,usd_value,eur_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
        
    params = (
        data['chain_id'],
        data['chain'],
        data['public_address'],
        data['timestamp'],
        data['category'],
        data['token'],
        data['amount'],
        data['usd_value'],
        data['eur_value']
    )

    result = herokuDbAccess.insertDataIntoDatabase(query, params, connection)    
    return result