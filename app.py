
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from utils import user_manager, leaderboard
import os

app = Flask(__name__)
app.secret_key = "arcade_secret_key"  # Change this to a real secret key in production

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')

@app.route('/login')
def login_page():
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    success, message = user_manager.register_user(username, password)
    return jsonify({'success': success, 'message': message})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password required'}), 400
    
    success, message = user_manager.login_user(username, password)
    if success:
        session['username'] = username
    return jsonify({'success': success, 'message': message})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'success': True, 'message': 'Logged out'})

@app.route('/api/user', methods=['GET'])
def get_user():
    if 'username' in session:
        return jsonify({'username': session['username']})
    return jsonify({'username': None})

@app.route('/api/leaderboard/<game>', methods=['GET'])
def get_leaderboard(game):
    # Mapping game names to the keys used in user_manager
    game_map = {
        'tictactoe': 'Tic Tac Toe',
        'guessing': 'Number Guessing Game',
        'quiz': 'Quiz Game'
    }
    actual_game_name = game_map.get(game)
    if not actual_game_name:
        return jsonify([])
    
    top_scores = leaderboard.get_top_scores(actual_game_name)
    return jsonify(top_scores)

@app.route('/api/score', methods=['POST'])
def update_score():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.json
    game = data.get('game')
    score = data.get('score')
    action = data.get('action', 'update') # 'update' (high score) or 'increment' (total wins)
    
    game_map = {
        'tictactoe': 'Tic Tac Toe',
        'guessing': 'Number Guessing Game',
        'quiz': 'Quiz Game'
    }
    actual_game_name = game_map.get(game)
    if not actual_game_name:
        return jsonify({'success': False, 'message': 'Invalid game'}), 400

    if action == 'increment':
        user_manager.increment_score(session['username'], actual_game_name)
    else:
        user_manager.update_score(session['username'], actual_game_name, score)
        
    return jsonify({'success': True})

if __name__ == '__main__':
    if not os.path.exists("data"):
        os.makedirs("data")
    app.run(debug=True, port=5000)
