"""
Export all project data from DB to backup files
"""

import json
from bson.objectid import ObjectId

from consys._db import get_db
from libdev.cfg import cfg


db = get_db(
    cfg('mongo.host', 'db'),
    cfg('project_name'),
    cfg('mongo.user'),
    cfg('mongo.pass'),
)


dbs = [collection['name'] for collection in db.list_collections()]

for db_name in dbs:
    with open(f'/backup/{db_name}.txt', 'w', encoding='utf-8') as file:
        for i in db[db_name].find():
            if isinstance(i['_id'], ObjectId):
                del i['_id']
            print(json.dumps(i, ensure_ascii=False), file=file)

    print(f'✅\t{db_name}')
