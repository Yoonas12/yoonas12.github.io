from flask import Flask, request, jsonify, session, render_template
import base64
import uuid

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Simulated database
users = {
    1: {'id': 1, 'name': 'Alice', 'role': 'user'},
    2: {'id': 2, 'name': 'Bob', 'role': 'user'},
    3: {'id': 3, 'name': 'Charlie', 'role': 'admin'}
}

documents = {
    'doc1': {'id': 'doc1', 'owner_id': 1, 'content': 'Sensitive Doc for Alice'},
    'doc2': {'id': 'doc2', 'owner_id': 2, 'content': 'Sensitive Doc for Bob'},
    'doc3': {'id': 'doc3', 'owner_id': 3, 'content': 'Admin Doc for Charlie'}
}

projects = {
    1: {'id': 1, 'owner_id': 1, 'files': ['file1.txt', 'file2.txt']},
    2: {'id': 2, 'owner_id': 2, 'files': ['file3.txt']},
    3: {'id': 3, 'owner_id': 3, 'files': ['admin_file.txt']}
}

# Serve frontend
@app.route('/')
def index():
    return render_template('index.html')

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    if user_id in users:
        session['user_id'] = user_id
        session['role'] = users[user_id]['role']
        return jsonify({'message': 'Logged in', 'user_id': user_id, 'role': users[user_id]['role']})
    return jsonify({'error': 'Invalid user'}), 401

# Basic IDOR: Profile access
@app.route('/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    # Vulnerable: No check if session['user_id'] matches user_id
    if user_id in users:
        return jsonify(users[user_id])
    return jsonify({'error': 'User not found'}), 404

# Advanced IDOR: Encoded document IDs
@app.route('/document/<encoded_doc_id>', methods=['GET'])
def get_document(encoded_doc_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        doc_id = base64.urlsafe_b64decode(encoded_doc_id.encode()).decode()
        if doc_id in documents:
            # Vulnerable: No ownership check
            return jsonify(documents[doc_id])
        return jsonify({'error': 'Document not found'}), 404
    except:
        return jsonify({'error': 'Invalid document ID'}), 400

# Advanced IDOR: Indirect reference via projects
@app.route('/project/<int:project_id>/files', methods=['GET'])
def get_project_files(project_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    if project_id in projects:
        # Vulnerable: No check if session['user_id'] matches project owner
        return jsonify({'project_id': project_id, 'files': projects[project_id]['files']})
    return jsonify({'error': 'Project not found'}), 404

# Admin-only endpoint
@app.route('/admin/users', methods=['GET'])
def get_all_users():
    if 'user_id' not in session or session['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)