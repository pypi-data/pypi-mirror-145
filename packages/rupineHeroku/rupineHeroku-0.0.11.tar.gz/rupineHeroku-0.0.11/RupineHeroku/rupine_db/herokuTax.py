from RupineHeroku.rupine_db import herokuDbAccess

def postTaxTransaction(connection, schema, data):

    sql = """INSERT INTO %s.tax_transaction (chain_id,chain,public_address,timestamp,block_number,transaction_hash,category,token,amount,usd_value,eur_value)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    params = (schema,
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
    result = herokuDbAccess.insertDataIntoDatabase(sql, params, connection)    
    return result[0][0]

def postTaxReward(connection, schema, data):

    sql = """INSERT INTO %s.tax_transaction (chain_id,chain,public_address,timestamp,block_number,transaction_hash,category,token,amount,usd_value,eur_value) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
    params = (
        schema,
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

    result = herokuDbAccess.insertDataIntoDatabase(sql, params, connection)    
    return result[0][0]