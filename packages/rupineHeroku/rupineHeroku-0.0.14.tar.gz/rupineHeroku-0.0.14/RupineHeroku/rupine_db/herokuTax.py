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
    return result[0][0]

def postTaxReward(connection, schema, data):

    query = sql.SQL("INSERT INTO {}.tax_transaction (chain_id,chain,public_address,timestamp,block_number,transaction_hash,category,token,amount,usd_value,eur_value) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)").format(sql.Identifier(schema))
        
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
    return result[0][0]