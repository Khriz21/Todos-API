import re
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/datas'
mongo = PyMongo(app)
CORS(app)

db = mongo.db.todos

@app.route('/todos')
def get_todos():
    todos = []
    for doc in db.find():
        todos.append({
            "_id": str(ObjectId(doc['_id'])),
            "title": doc['title'],
            "description": doc['description'],
            "done": doc['done']
        })
    return jsonify(todos)
        
@app.route('/todos', methods=['POST'])
def add_todo():   
    id = db.insert({
        "title": request.json['title'],
        "description": request.json['description'],
        "done": False
    })
    return jsonify(str(ObjectId(id)))
    
@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        "title": request.json['title'],
        "description": request.json['description']
    }})
    
    return "tarea actualizada"

@app.route('/todos/<id>', methods= ['DELETE'])
def delete_todo(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Tarea eliminada'})

@app.route('/todos/done/<id>', methods=['PUT'])
def check_done(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        "done": request.json['done']
    }})
    return 'Received'
    
if __name__ == '__main__':
    app.run(debug=True ,host='192.168.1.31',port=5000)
    
