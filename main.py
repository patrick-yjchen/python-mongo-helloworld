from bottle import route, run, template
import ConfigParser
import json
import pymongo
import sys

cfg = ConfigParser.RawConfigParser()
if len(sys.argv) < 2:
    print "Usage: {} config.cfg".format(sys.argv[0])
    exit(-1)
cfg.read(sys.argv[1])

mongoClient = pymongo.MongoClient(cfg.get('Setting', 'MONGO_HOST'), cfg.getint('Setting', 'MONGO_PORT'))
mongoDB = mongoClient.mongoHelloWorld
userCollection = mongoDB.users

@route('/inc/<name>')
def index(name):
    u = userCollection.find_and_modify({'_id':name}, {'$inc': {'cnt':1}}, upsert=True)
    return """<b>User {} has visisted {} times.</b>""".format(name, u.get('cnt', 0))

run(host='0.0.0.0', port=cfg.get('Setting', 'SERVER_PORT'))
