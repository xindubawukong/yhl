import pymongo

conn = pymongo.MongoClient("127.0.0.1",27017)
db = conn.biocad
db.register.remove()
db.setting.remove()
db.vistor.remove()
db.st1.remove()
db.st2.remove()
db.st3.remove()
db.st4.remove()
db.st5.remove()
db.st6.remove()
db.st7.remove()
db.st8.remove()
db.st9.remove()
db.st10.remove()
db.setting.insert({"maxid":0})
db.st1.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st2.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st3.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st4.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st5.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st6.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st7.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st8.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st9.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.st10.insert({"vistorid":0,"dataid":0,"pid":0,"pos_x":0,"pos_y":0})
db.register.insert({"user":"airfan","password":"123456","vistorid":0});
db.vistor.insert({"vistorid":0,"pn":0});
db.device1.remove()
db.flow1.remove()
db.control1.remove()
db.device2.remove()
db.device3.remove()
db.device4.remove()
db.device5.remove()
db.device6.remove()
db.device7.remove()
db.device8.remove()
db.device9.remove()
db.device10.remove()
db.flow2.remove()
db.flow3.remove()
db.flow4.remove()
db.flow5.remove()
db.flow6.remove()
db.flow7.remove()
db.flow8.remove()
db.flow9.remove()
db.flow10.remove()
db.control2.remove()
db.control3.remove()
db.control4.remove()
db.control5.remove()
db.control6.remove()
db.control7.remove()
db.control8.remove()
db.control9.remove()
db.control10.remove()