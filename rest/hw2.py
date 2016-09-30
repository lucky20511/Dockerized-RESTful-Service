#!/usr/bin/python

from flask import Flask, request, Response, json, abort
from sqlalchemy import *

#from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#db = SQLAlchemy(app)

#load sql db
db = create_engine('mysql://root:lucky20511@db/mysql', echo=True)
metadata = MetaData(db)

def DBGetTableByName(table_name) :
    try :
        table = Table(table_name, metadata, autoload=True)
        return True
    except :
        return False

if not DBGetTableByName('HW2'):
    sql = "CREATE TABLE `mysql`.`HW2` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,`name` TEXT,`email` TEXT,`category` TEXT,`description` TEXT,`link` TEXT,`estimated_costs` TEXT,`submit_date` TEXT,`status` TEXT,`decision_date` TEXT, PRIMARY KEY(`id`))"
    result = db.engine.execute(sql)

@app.route('/v1/expenses/<int:postID>', methods = ['GET', 'PUT', 'DELETE'])
def api_GET_PUT_DELETE(postID):
    if request.method == 'GET':

        sql = "SELECT * FROM HW2 WHERE id='%d' " %postID
        #print sql
        result = db.engine.execute(sql)

        dic = [(dict(row.items())) for row in result]
        #check if the id is valid
        print "!!!!!!%d"%len(dic)
        if len(dic) < 1: 
            abort(404)   
            #return Response(status=200, mimetype='application/json')
        #print dic[0]    
        js = json.dumps(dic[0])
        #print js


        resp = Response(js, status=200, mimetype='application/json')
        return resp


    elif request.method == 'PUT':
        #if request.headers['Content-Type'] == 'text/plain':
        #    js = request.data
        
        #check if the type is json
        #if request.headers['Content-Type'] == 'application/json':
        resp_dict = json.loads(request.data)
        #else:
        #    abort(404)

        sql = "UPDATE HW2 SET " 
        count = 0
        for i in resp_dict:
            if count != 0:
                sql = sql + ", "
            sql = sql + "%s='%s' " %(i, resp_dict[i])
            count = count + 1
            
        sql = sql + " WHERE id = '%d';" %postID
        #print sql
        result = db.engine.execute(sql)
        resp = Response(status=202)
        return resp
        


    elif request.method == 'DELETE':
        resp = Response(status=204)
        sql = "DELETE FROM HW2 WHERE id=%d;" % postID 
        result = db.engine.execute(sql)
        return resp


@app.route('/v1/expenses', methods = ['POST'])
def api_POST():
    if request.method == 'POST':    

        #if request.headers['Content-Type'] == 'text/plain':
        #   js = request.data
        #check if the type is json
        #if request.headers['Content-Type'] == 'application/json':
        resp_dict = json.loads(request.data)
        #else:
        #    abort(404)
        #print "request.data"
        #print request.data
        #print "resp_dic"
        #print resp_dict
        
        sql = "INSERT INTO HW2 (name, email, category, description, link, estimated_costs, submit_date, status, decision_date) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(resp_dict['name'], resp_dict['email'], resp_dict['category'], resp_dict['description'], resp_dict['link'], resp_dict['estimated_costs'], resp_dict['submit_date'], "pending", "")
        #print sql
        result = db.engine.execute(sql)


        sql = "SELECT * FROM HW2 WHERE name='%s' AND email = '%s' AND category='%s' AND description='%s' AND link='%s' AND estimated_costs='%s' AND submit_date='%s';" %(resp_dict['name'], resp_dict['email'], resp_dict['category'], resp_dict['description'], resp_dict['link'], resp_dict['estimated_costs'], resp_dict['submit_date'])
        result = db.engine.execute(sql)
        #print result
        
        dic = [(dict(row.items())) for row in result]
        #print dic[0]
        if len(dic) > 0:      
            js = json.dumps(dic[len(dic)-1])
        else:
            js = ""
        #print js
        #print json.loads(js)
       
        resp = Response(js, status=201, mimetype='application/json')
        print "post_response = %s" %resp
        #resp = Response(js, status=201, mimetype='application/json')
        #resp.headers['Message'] = '201 OK'
        return resp



if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=True)