
from utils import user_manager

def get_top_scores(game, limit=5):
    users = user_manager.get_users()
    scores = []
    for username, data in users.items():
        if game in data["scores"]:
            scores.append((username, data["scores"][game]))
    
    # For Number Guessing, lower is better. For others, higher is better.
    is_reverse = game != "Number Guessing Game"
    scores.sort(key=lambda x: x[1], reverse=is_reverse)
    return scores[:limit]
