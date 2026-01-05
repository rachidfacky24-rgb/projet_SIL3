from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    space TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS spaces (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT
                )''')
    # Insert sample data
    c.execute("INSERT OR IGNORE INTO spaces VALUES (1, 'Salle Informatique', 'Espace pour cours d''informatique')")
    c.execute("INSERT OR IGNORE INTO spaces VALUES (2, 'Laboratoire Sciences', 'Espace pour expériences scientifiques')")
    c.execute("INSERT OR IGNORE INTO spaces VALUES (3, 'Salle de Formation', 'Espace pour formations professionnelles')")
    c.execute("INSERT OR IGNORE INTO spaces VALUES (4, 'Atelier Technique', 'Espace pour travaux pratiques')")

    c.execute("INSERT OR IGNORE INTO users VALUES (1, 'Alice Dupont', 'formateur', 'Salle Informatique')")
    c.execute("INSERT OR IGNORE INTO users VALUES (2, 'Bob Martin', 'etudiant', 'Salle Informatique')")
    c.execute("INSERT OR IGNORE INTO users VALUES (3, 'Charlie Brown', 'technicien', 'Salle Informatique')")
    c.execute("INSERT OR IGNORE INTO users VALUES (4, 'Diana Prince', 'formateur', 'Laboratoire Sciences')")
    c.execute("INSERT OR IGNORE INTO users VALUES (5, 'Eve Wilson', 'etudiant', 'Laboratoire Sciences')")
    c.execute("INSERT OR IGNORE INTO users VALUES (6, 'Frank Miller', 'technicien', 'Laboratoire Sciences')")
    c.execute("INSERT OR IGNORE INTO users VALUES (7, 'Grace Lee', 'formateur', 'Salle de Formation')")
    c.execute("INSERT OR IGNORE INTO users VALUES (8, 'Henry Ford', 'etudiant', 'Salle de Formation')")
    c.execute("INSERT OR IGNORE INTO users VALUES (9, 'Ivy Chen', 'technicien', 'Atelier Technique')")
    c.execute("INSERT OR IGNORE INTO users VALUES (10, 'Jack Sparrow', 'administrateur', 'Salle Informatique')")
    c.execute("INSERT OR IGNORE INTO users VALUES (11, 'Kate Bishop', 'secretaire', 'Salle de Formation')")
    c.execute("INSERT OR IGNORE INTO users VALUES (12, 'Liam Neeson', 'etudiant', 'Laboratoire Sciences')")
    c.execute("INSERT OR IGNORE INTO users VALUES (13, 'Mia Khalifa', 'etudiant', 'Salle Informatique')")
    c.execute("INSERT OR IGNORE INTO users VALUES (14, 'Noah Centineo', 'technicien', 'Salle de Formation')")

    conn.commit()
    conn.close()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM spaces")
    spaces = c.fetchall()
    spaces_data = []
    for space in spaces:
        space_id, space_name, space_desc = space
        c.execute("SELECT * FROM users WHERE space = ?", (space_name,))
        users = c.fetchall()
        spaces_data.append({
            'id': space_id,
            'name': space_name,
            'description': space_desc,
            'users': users
        })
    conn.close()
    return render_template('dashboard.html', spaces=spaces_data)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        space = request.form['space']
        conn = sqlite3.connect('pedagogical_system.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, role, space) VALUES (?, ?, ?)", (name, role, space))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute("SELECT name FROM spaces")
    spaces = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('add_user.html', spaces=spaces)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        space = request.form['space']
        conn = sqlite3.connect('pedagogical_system.db')
        c = conn.cursor()
        c.execute("UPDATE users SET name = ?, role = ?, space = ? WHERE id = ?", (name, role, space, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    c.execute("SELECT name FROM spaces")
    spaces = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('edit_user.html', user=user, spaces=spaces)

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/edit_space/<int:space_id>', methods=['GET', 'POST'])
def edit_space(space_id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = sqlite3.connect('pedagogical_system.db')
        c = conn.cursor()
        c.execute("UPDATE spaces SET name = ?, description = ? WHERE id = ?", (name, description, space_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute("SELECT * FROM spaces WHERE id = ?", (space_id,))
    space = c.fetchone()
    conn.close()
    return render_template('edit_space.html', space=space)

@app.route('/delete_space/<int:space_id>')
def delete_space(space_id):
    conn = sqlite3.connect('pedagogical_system.db')
    c = conn.cursor()
    c.execute("DELETE FROM spaces WHERE id = ?", (space_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
