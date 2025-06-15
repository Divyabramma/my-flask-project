@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!")
    return redirect(url_for('users'))

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
