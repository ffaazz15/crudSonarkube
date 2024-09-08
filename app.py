from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# Database connection function
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="user_crud_app",
        user="postgres",
        password="123"
    )

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("INSERT INTO users (name, age, location) VALUES (%s, %s, %s) RETURNING *",
                (data['name'], data['age'], data['location']))
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_user), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

# Get a single user
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("UPDATE users SET name = %s, age = %s, location = %s WHERE id = %s RETURNING *",
                (data['name'], data['age'], data['location'], id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.clos()
    conn.close()
    if updated_user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(updated_user)

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
    deleted_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted_user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)