from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for flash messages

# Home Page - Add user
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        conn.close()
        flash("User added successfully!")
        return redirect(url_for('users'))
    return render_template('index.html')

# View all users
@app.route('/users')
def users():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

# Edit user
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        new_username = request.form['username']
        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
        conn.commit()
        conn.close()
        flash("User updated successfully!")
        return redirect(url_for('users'))

    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit.html', user_id=user_id, username=user[0])

# Delete user
@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!")
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == "__main__":
    app.run()
