from flask import Flask, request
from flask_restful import Resource, Api, reqparse, fields, marshal_with
import sqlite3 as sql
import json

app = Flask(__name__)
api = Api(app)

# define output format, it can control what can be seen by our clients
resource_fields = {
    # 'Uri': fields.String,
    'Id': fields.String,
    'Name': fields.String,
    'ItemName': fields.String,
    'ItemPrice': fields.String
    }

# Task
# shows a single task item and lets you delete a task item    
class Task(Resource):

    def __init__(self):
        #Initial reqparse.RequestParser() to help control request arguments
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(name='ItemPrice', location='json', type=str)
    

    def get(self, task_id):
        conn = sql.connect('database.db')
        cur = conn.cursor()
        cur.execute("select * from Tasks where Id=(?)", (task_id,))
        rows = cur.fetchall()
        task_list = list()
        for row in rows:
            each_task = dict()
            each_task['Id'] = row[0]
            each_task['Name'] = row[1]
            each_task['ItemName'] = row[2]
            each_task['ItemPrice'] = row[3]
            task_list.append(each_task)
        conn.close()
        return task_list
        #row = cur.fetchone()
        
        #task = dict()
        #task['Id'] = row[0]
        #task['Name'] = row[1]
        #task['ItemName'] = row[2]
        #task['ItemPrice'] = row[3]
       
        #conn.close()
        #return task

        

    #def get(self, task_id):
        #conn = sql.connect('database.db')
        #cur = conn.cursor()
        #cur.execute("SELECT COUNT(Id) FROM orders WHERE Id='r001';", (task_id,))
        #row = cur.fetchone()
        #result = row[0]
     
       
        #conn.close()
        #return {'result' : result}

    

# TaskList
# shows a list of all tasks, and lets you POST to add new tasks        
class TaskList(Resource):

    def __init__(self):
        #Initial reqparse.RequestParser() to help control request arguments
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(name='Id', location='json',required=True, type=str, help='id for this resource')
        self.parser.add_argument(name='Name', location='json', type=str)
        self.parser.add_argument(name='ItemName', location='json', type=str)
        self.parser.add_argument(name='ItemPrice', location='json', type=str)

    @marshal_with(resource_fields)
    def get(self):
        conn = sql.connect('database.db')
        cur = conn.cursor()
        cur.execute("select * from Tasks")
        rows = cur.fetchall()
        task_list = list()
        for row in rows:
            each_task = dict()
            each_task['Id'] = row[0]
            each_task['Name'] = row[1]
            each_task['ItemName'] = row[2]
            each_task['ItemPrice'] = row[3]
            task_list.append(each_task)
        conn.close()
        return task_list
    
    def post(self):
        conn = sql.connect('database.db')
        cur = conn.cursor()
        with conn:
            args = self.parser.parse_args()
            task = (args['Id'], args['Name'], args['ItemName'],args['ItemPrice'])
            cur.execute("INSERT INTO Tasks (Id,Name,ItemName,ItemPrice) VALUES (?,?,?,?)"
            , task)
            conn.commit()
        return task, 201

##
## Actually setup the Api resource routing here
##        
api.add_resource(TaskList, '/tasks')
api.add_resource(Task, '/task/<task_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)