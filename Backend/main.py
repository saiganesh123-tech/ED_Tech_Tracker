from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for tracking educational resources
resources = [
    {"id": 1, "name": "Python Basics", "type": "Course", "progress": 50},
    {"id": 2, "name": "Data Science Handbook", "type": "Book", "progress": 20},
]
@app.route('/resources/search', methods=['GET'])
def search_resources():
    query = request.args.get('q', '').lower()
    filtered_resources = [r for r in resources if query in r["name"].lower()]
    return jsonify(filtered_resources)
@app.route('/')
def home():
    return "Welcome to the Edtech Tracker API!"

@app.route('/resources', methods=['GET'])
def get_resources():
    return jsonify(resources)

@app.route('/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if resource:
        return jsonify(resource)
    return jsonify({"error": "Resource not found"}), 404

@app.route('/resources', methods=['POST'])
def add_resource():
    new_resource = request.json
    new_resource["id"] = len(resources) + 1
    resources.append(new_resource)
    return jsonify(new_resource), 201

@app.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if resource:
        updates = request.json
        resource.update(updates)
        return jsonify(resource)
    return jsonify({"error": "Resource not found"}), 404

@app.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    global resources
    resources = [r for r in resources if r["id"] != resource_id]
    return jsonify({"message": "Resource deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)