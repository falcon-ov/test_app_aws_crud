from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text
from config import MASTER_DB, READ_REPLICA_DB

app = Flask(__name__)

# подключение к master (для записи)
master_engine = create_engine(f"mysql+pymysql://{MASTER_DB['user']}:{MASTER_DB['password']}@{MASTER_DB['host']}/{MASTER_DB['database']}")

# подключение к read replica (для чтения)
replica_engine = create_engine(f"mysql+pymysql://{READ_REPLICA_DB['user']}:{READ_REPLICA_DB['password']}@{READ_REPLICA_DB['host']}/{READ_REPLICA_DB['database']}")

# --- маршруты ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def get_todos():
    with replica_engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM todos"))
        todos = [dict(row) for row in result]
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    with master_engine.connect() as conn:
        conn.execute(text("INSERT INTO todos (title, category_id, status) VALUES (:title, :category_id, :status)"), **data)
    return jsonify({'message': 'Todo created'}), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.json
    with master_engine.connect() as conn:
        conn.execute(text("UPDATE todos SET title=:title, category_id=:category_id, status=:status WHERE id=:id"), **data, id=id)
    return jsonify({'message': 'Todo updated'})

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    with master_engine.connect() as conn:
        conn.execute(text("DELETE FROM todos WHERE id=:id"), id=id)
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
