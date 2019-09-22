from flask import Flask
from sqlalchemy import create_engine
from flask_restful import Resource, Api
from flask_jsonpify import jsonify

db_connect = create_engine("sqlite:///chinook.db")
app = Flask(__name__)
api = Api(app)


class Employees(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM employees")
        return {"employees": [i[0] for i in query.cursor.fetchall()]}


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT trackid, name, composer, unitprice from tracks;")
        result = {"data": [dict(zip(query.keys(), i)) for i in query.cursor]}
        return jsonify(result)


class EmployeesName(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute(f"SELECT * FROM employees WHERE employeeid ={employee_id}")
        result = {"data": [dict(zip(query.keys(), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Employees, "/employees")
api.add_resource(Tracks, "/tracks")
api.add_resource(EmployeesName, "/employees/<employee_id>")

if __name__ == "__main__":
    app.run(port="5002")
