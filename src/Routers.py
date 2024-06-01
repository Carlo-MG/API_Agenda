from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src import db
from src.Models import Task
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@main.route('/task', methods=['POST'])
@jwt_required()
def new_task():
    data = request.get_json()
    user_id = get_jwt_identity()
    due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    task = Task(title=data['title'], due_date=due_date, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@main.route('/task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != get_jwt_identity():
        return jsonify({"message": "Permission denied"}), 403
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
