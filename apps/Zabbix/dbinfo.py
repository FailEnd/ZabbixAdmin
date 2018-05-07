from pymongo import MongoClient

client = MongoClient('10.101.26.43',username='root',password='monkey313',authSource='network',authMechanism='SCRAM-SHA-1')

db = client.ZabbixAdmin


def updateDataSource():
    post = {"uri": "http://10.100.18.163/zabbix/api_jsonrpc.php", "username": "admin", "password": "monkey313","token":"99e2a7a30fc07131530596ca128140ab"}
    posts = db.DataSource
    post_id = posts.insert_one(post).inserted_id
    return post_id


def findDataSource():
    posts = db.DataSource
    value = posts.find_one()
    return value
