from RupineHeroku.rupine_db import herokuDbAccess

def postTaxTransaction(connection, schema, data):

    sql = "INSERT INTO {0}.tax_transaction (chain_id,chain,public_address,timestamp,block_number,transaction_hash,category,token,amount,usd_value,eur_value) \
        VALUES ({1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11})".format(
        schema,
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
        data['eur_value']
    )

    result = herokuDbAccess.insertDataIntoDatabase(sql, connection)    
    return result[0][0]

def postTaxReward(connection, schema, data):

    sql = "INSERT INTO {0}.tax_transaction (chain_id,chain,public_address,timestamp,block_number,transaction_hash,category,token,amount,usd_value,eur_value) \
        VALUES ({1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11})".format(
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

    result = herokuDbAccess.insertDataIntoDatabase(sql, connection)    
    return result[0][0]