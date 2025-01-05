from flask import Blueprint, request, jsonify
from models import db, Ticket

ticket_blueprint = Blueprint('tickets', __name__)

# Get all tickets
@ticket_blueprint.route('/tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([{
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "status": t.status,
        "priority": t.priority
    } for t in tickets])

# Create a new ticket
@ticket_blueprint.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    new_ticket = Ticket(
        title=data['title'],
        description=data['description'],
        priority=data.get('priority', 'Medium')
    )
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify({"message": "Ticket created", "id": new_ticket.id}), 201

# Update a ticket
@ticket_blueprint.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    data = request.json
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.status = data.get('status', ticket.status)
    ticket.priority = data.get('priority', ticket.priority)
    db.session.commit()
    return jsonify({"message": "Ticket updated"})

# Delete a ticket
@ticket_blueprint.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket deleted"})

# Test route
@ticket_blueprint.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Blueprint is working!"})
