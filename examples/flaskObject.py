"""
    FlaskObject
    ===========

    A microblog example application written as Flask tutorial with
    Flask and Object ORM Module (nonslite pakage)

    Emiliano A. Billi 

    Changes: 12/09/2016 Emiliano A. Billi Remplace SQLite Database with Object ORM Module (nonsqlite package)

"""


from nonsqlite.Object import Object

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

class Entry(Object):
    _db_name = 'Blog.db'
    def __init__(self):
	title = ''
	text  = ''


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='flenson',
    USERNAME='admin',
    PASSWORD='default'
))


@app.route('/')
def show_entries():
    return render_template('show_entries.html', entries=Entry.all())


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    #
    # Save Object in database    
    entry = Entry()
    entry.title = request.form['title']
    entry.text  = request.form['text']
    entry.save()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username or password'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid username or password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run('0.0.0.0', 8000)

