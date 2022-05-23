from pymongo import MongoClient
from gridfs import GridFS

class mongoModel:
    def __init__(self):
        self.connect('localhost', 27017)
        self.set_db('colearner')
        self.set_gridfs()

    def connect(self, host, port):
        if isinstance(port, str):
            port=int(port)
        self.client = MongoClient(host,port)
    
    def set_db(self, name):
        self.db = self.client[name]
    
    def set_gridfs(self, prefix='fs'):
        self.fs = GridFS(self.db, prefix)
    
    def put_file(self, uid, data, file_info):
        try:
            if data != None:
                fileid = self.put_file_to_fs(data)
                file_info["fileid"] = fileid
            
            filelist = self.db.users.find_one({'uid':uid})["files"]
            file_info["id"] = len(filelist)
            filelist.append(file_info)
            self.db.users.update_one({'uid':uid}, {'$set':{'files':filelist}})
            return True
        except:
            return False
        
    def put_file_to_fs(self, data):
        return self.fs.put(data)

    def get_file_from_fs(self, fileid):
        out = self.fs.get(fileid)
        return out.read()

    def get_file(self, uid, id):
        return self.get_user(uid)["files"][int(id)]

    def get_files(self, uid, parent):
        if self.get_user(uid) is not None:
            files = self.get_user(uid)["files"]
            return [i for i in files if i is not None and i["parent"] == int(parent)]
        else:
            return False

    def get_user(self, uid):
        self.users = self.db['users']
        return self.users.find_one({"uid" : uid})

    def set_user(self, user_info):
        self.users.insert_one(user_info)
    
    