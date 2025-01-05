from flask import Blueprint, request, jsonify
from models import db, Ticket

# Initialize the blueprint
ticket_blueprint = Blueprint('tickets', __name__)

# Get all tickets
@ticket_blueprint.route('/tickets', methods=['GET'])
def get_tickets():
    """
    Fetch all tickets from the database.
    """
    tickets = Ticket.query.all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "priority": t.priority
        }
        for t in tickets
    ])

# Create a new ticket
@ticket_blueprint.route('/tickets', methods=['POST'])
def create_ticket():
    """
    Create a new ticket with provided data.
    """
    data = request.json

    # Validation
    if not data.get('title') or not data.get('description'):
        return jsonify({"error": "Title and description are required"}), 400
    if data.get('priority') and data['priority'] not in ['Low', 'Medium', 'High']:
        return jsonify({"error": "Priority must be Low, Medium, or High"}), 400

    # Create the ticket
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
    """
    Update an existing ticket with new data.
    """
    data = request.json
    ticket = Ticket.query.get_or_404(ticket_id)

    # Validation
    if data.get('priority') and data['priority'] not in ['Low', 'Medium', 'High']:
        return jsonify({"error": "Priority must be Low, Medium, or High"}), 400

    # Update the ticket fields
    ticket.title = data.get('title', ticket.title)
    ticket.description = data.get('description', ticket.description)
    ticket.status = data.get('status', ticket.status)
    ticket.priority = data.get('priority', ticket.priority)
    db.session.commit()
    return jsonify({"message": "Ticket updated"})

# Delete a ticket
@ticket_blueprint.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    """
    Delete a ticket by its ID.
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket deleted"})

# Test route
@ticket_blueprint.route('/test', methods=['GET'])
def test_route():
    """
    Simple route to test if the blueprint is working.
    """
    return jsonify({"message": "Blueprint is working!"})
