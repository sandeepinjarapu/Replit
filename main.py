from flask import Flask, render_template, request, jsonify, abort
from models import Leader, Project, Collaborator, Content
from database import db_session, init_db

app = Flask(__name__)

db_initialized = False

@app.before_request
def initialize_database():
    global db_initialized
    if not db_initialized:
        init_db()
        print("Database initialized.")
        db_initialized = True

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    leaders = Leader.query.limit(6).all()  # Limit to 6 leaders for the homepage
    return render_template('index.html', leaders=leaders)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/leaders')
def all_leaders():
    leaders = Leader.query.all()
    return render_template('leaders.html', leaders=leaders)

@app.route('/profile/<int:leader_id>')
def profile(leader_id):
    leader = Leader.query.filter(Leader.id == leader_id).first()
    if leader is None:
        abort(404)
    return render_template('profile.html', leader=leader)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    leaders = Leader.query.filter(
        (Leader.name.ilike(f'%{query}%')) | (Leader.company.ilike(f'%{query}%'))
    ).all()
    return jsonify([{'id': l.id, 'name': l.name, 'company': l.company} for l in leaders])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
