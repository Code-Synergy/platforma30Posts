from flask import Blueprint, request, jsonify
from . import db

workflow_bp = Blueprint('workflow', __name__)

class Workflow(db.Model):
    __tablename__ = 'workflow'

    workflow_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    def __init__(self, status):
        self.status = status

@workflow_bp.route('/', methods=['GET'])
def get_workflows():
    workflows = Workflow.query.all()
    return jsonify([w.serialize() for w in workflows])

@workflow_bp.route('/', methods=['POST'])
def add_workflow():
    data = request.get_json()
    workflow = Workflow(status=data['status'])
    db.session.add(workflow)
    db.session.commit()
    return jsonify(workflow.serialize()), 201

@workflow_bp.route('/<int:id>', methods=['PUT'])
def update_workflow(id):
    workflow = Workflow.query.get_or_404(id)
    data = request.get_json()

    workflow.status = data.get('status', workflow.status)

    db.session.commit()
    return jsonify(workflow.serialize())

@workflow_bp.route('/<int:id>', methods=['DELETE'])
def delete_workflow(id):
    workflow = Workflow.query.get_or_404(id)
    db.session.delete(workflow)
    db.session.commit()
    return '', 204
