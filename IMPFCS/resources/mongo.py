from pymongo import *
import json
################################################
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017
MONGO_USER = ""
MONGO_PASS = ""
################################################

class MongoClient(object):
	"""docstring for  MongoClient"""
	def __init__(self,
				 host=MONGO_HOST,
                 port=MONGO_PORT,
                 username=MONGO_USER,
                 password=MONGO_PASS):
		self.db = Connection(host, port)["IMPFCS_database"]
		self.db.mans.ensure_index('s_id', unique=True);

	def get_doc_by_id(self, doc_type, _id):
		return self.db[doc_type].find_one(dict(_id=_id))

	def insert_doc(self, doc_type, doc):
		_id = self.db[doc_type].insert(doc)
		return _id

	def get_doc_by_name(self, doc_type, name):
		return self.db[doc_type].find_one(dict(name=name))

	def get_doc_by_student_id(self, doc_type, s_id):
		return self.db[doc_type].find_one(dict(s_id=s_id))

	def get_doc_by_team(self, doc_type, team):
		g = self.db[doc_type].find(dict(team=team))
		lists = []
		for each in g:
			lists.append(each)
		return lists

	def remove_doc_by_name(self, doc_type, name):
		return self.db[doc_type].remove(dict(name=name))

	def update_doc_by_s_id(self, s_id, doc_type, change_type, change):
		return self.db[doc_type].update(dict(s_id=s_id),  {'$set':{change_type:change}})

'''
MClient = MongoClient()
post = {
	"team" : "AA",
	"title" : "captain",
	"t_name" : "xxx",
	"coach" : "xxx",
	"name" : "xxx",
	"gender" : "male",
	"birthday" : ["1999", "1", "1"],
	"pos" : {"department":"cs", "class" : "23"} ,
	"s_id" : "20111111113",
	"rank" : {"GPA" : "90", "ranking" : "10", "total" : "40"},
	"telephone" : "18811333333",
	"email" : "askd@gmail.com",
	"Address" :	"zijing2#",
	"social_work" : "dsada"
}
post1 = {
	"team" : "AA",
	"title" : "captain",
	"t_name" : "xxx",
	"coach" : "xxx",
	"name" : "xxx",
	"gender" : "male",
	"birthday" : ["1999", "1", "1"],
	"pos" : {"department":"cs", "class" : "23"} ,
	"s_id" : "20111111112",
	"rank" : {"GPA" : "90", "ranking" : "10", "total" : "40"},
	"telephone" : "18811333333",
	"email" : "askd@gmail.com",
	"Address" :	"zijing2#",
	"social_work" : "dsada"
}

MClient.insert_doc("man1", post)
MClient.insert_doc("man1", post1)

print MClient.get_doc_by_team("man1", "AA")
'''

'''
client = MongoClient()
db = client.test_database
collection = db.test_collection

post = {
	"team" : "A",
	"title" : "captain",
	"t_name" : "xxx",
	"coach" : "xxx",
	"name" : "xxx",
	"gender" : "male",
	"birthday" : ["1999", "1", "1"],
	"pos" : {"department":"cs", "class" : "23"} ,
	"s_id" : "20111111111",
	"rank" : {"GPA" : "90", "ranking" : "10", "total" : "40"},
	"telephone" : "18811333333",
	"email" : "askd@gmail.com",
	"Address" :	"zijing2#",
	"social_work" : "dsada"
}


posts = db.post1
post_id = posts.insert(post)

'''
