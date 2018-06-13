import pymongo
a=1
curvistorid = 1
if a==1:	
	up_file = open('all.txt')
        conn = pymongo.MongoClient("127.0.0.1",27017)
        db = conn.biocad
        lines = up_file.readline()
        lines = up_file.readline()
        ss = lines.split(" ")
        num = 0
        if ss[0] =='device':
                num = int(ss[1])
                if num==None    or num<=0:
			print "sd"
        else:
        i=0
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                i=i+1
                db.device1.insert({"vistorid":curvistorid,"p0":int(sss[0]),"p1":int(sss[1]),"p2":int(sss[2]),"p3":int(sss[3]),"p4":int(sss[4])})
        lines = up_file.readline()
        num = 0
	ss = lines.split(" ")
        if ss[0]=='path':
                num = int(ss[1])
        i = 0
        a=1
	print "g"
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                t = 1
                while t<len(sss)-1:
                        ssss = sss[t].split(",")
                        ssss1 = ssss[0].split("(")
                        ssss2 = ssss[1].split(")")
                        db.flow1.insert({"vistorid":curvistorid,"order":a,"px":int(ssss1[1]),"py":int(ssss2[0]),"psid":i})
                        t=t+1
                        a=a+1
                i = i+1
        lines = up_file.readline()
        num = 0
        ss = lines.split(" ")
        if ss[0]=='control':
         	num = int(ss[1])
                if num==None or num<=0:
                        db.flow1.remove()
                        db.device1.remove()
                        
        else:
                db.device1.remove()
                db.flow1.remove()
                
        i = 0
        a=1
        while i<num:
                lines = up_file.readline()
                sss = lines.split(" ")
                t = 1
                while t<len(sss)-1:
                        ssss = sss[t].split(",")
                        ssss1 = ssss[0].split("(")
                        ssss2 = ssss[1].split(")")
                        db.control1.insert({"vistorid":curvistorid,"order":a,"px":int(ssss1[1]),"py":int(ssss2[0]),"psid":i})
                        t=t+1
                        a=a+1
                i = i+1
	up_file.close()
