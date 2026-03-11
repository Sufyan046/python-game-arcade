
let currentTab = 'login';

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    setupStars();
});

// Star background animation
function setupStars() {
    const container = document.querySelector('.stars-container');
    if (!container) return;
    const fragment = document.createDocumentFragment();
    for (let i = 0; i < 80; i++) { // Reduce to 80 stars for better performance
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = `${Math.random() * 100}%`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.animationDelay = `${Math.random() * 3}s`;
        star.style.pointerEvents = 'none'; // Ensure stars themselves don't block
        fragment.appendChild(star);
    }
    container.appendChild(fragment);
}

function showTab(tab) {
    currentTab = tab;
    const tabs = document.querySelectorAll('.tab');
    const authBtn = document.getElementById('authBtn');
    const authTitle = document.getElementById('authTitle');
    const status = document.getElementById('authStatus');
    
    if (status) status.classList.add('hidden');
    
    tabs.forEach(t => t.classList.remove('active'));
    if (tab === 'login') {
        tabs[0].classList.add('active');
        authBtn.innerText = 'Enter Arcade';
        authTitle.innerText = 'Welcome Back, Player!';
    } else {
        tabs[1].classList.add('active');
        authBtn.innerText = 'Register Player';
        authTitle.innerText = 'New Recruit? Join Us!';
    }
}

async function handleAuth(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const endpoint = currentTab === 'login' ? '/api/login' : '/api/register';
    const status = document.getElementById('authStatus');

    if (status) {
        status.classList.remove('hidden');
        status.innerText = 'Processing...';
        status.style.color = 'var(--primary)';
    }

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        
        if (data.success) {
            if (currentTab === 'login') {
                window.location.href = '/'; // Redirect to main hub
            } else {
                if (status) {
                    status.innerText = "Registration successful! You can now login.";
                    status.style.color = 'var(--neon-green)';
                }
                setTimeout(() => showTab('login'), 2000);
            }
        } else {
            if (status) {
                status.innerText = data.message;
                status.style.color = '#ff4d4d';
            }
        }
    } catch (err) {
        console.error("Auth error:", err);
        if (status) {
            status.innerText = "An error occurred. Please try again.";
            status.style.color = '#ff4d4d';
        }
    }
}

async function logout() {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/login';
}

function startGame(gameType) {
    const arcadeSection = document.getElementById('arcadeSection');
    const gameSection = document.getElementById('gameSection');
    const gameDisplay = document.getElementById('gameDisplay');
    const title = document.getElementById('currentGameTitle');

    arcadeSection.classList.add('hidden');
    gameSection.classList.remove('hidden');
    gameDisplay.innerHTML = '';

    if (gameType === 'tictactoe') {
        title.innerText = 'Tic-Tac-Toe';
        initTicTacToe(gameDisplay);
    } else if (gameType === 'guessing') {
        title.innerText = 'Number Guessing';
        initGuessingGame(gameDisplay);
    } else if (gameType === 'quiz') {
        title.innerText = 'Quiz Master';
        initQuizGame(gameDisplay);
    }
}

function backToArcade() {
    const arcadeSection = document.getElementById('arcadeSection');
    const gameSection = document.getElementById('gameSection');
    gameSection.classList.add('hidden');
    arcadeSection.classList.remove('hidden');
}

async function showLeaderboard() {
    const modal = document.getElementById('leaderboardModal');
    const content = document.getElementById('leaderboardContent');
    modal.classList.remove('hidden');
    modal.style.display = 'flex'; // Explicitly set to flex
    content.innerHTML = '<div class="loader">Loading rankings...</div>';

    const games = [
        { id: 'tictactoe', name: 'Tic-Tac-Toe' },
        { id: 'guessing', name: 'Number Guessing' },
        { id: 'quiz', name: 'Quiz Master' }
    ];

    let html = '';
    for (const game of games) {
        try {
            const response = await fetch(`/api/leaderboard/${game.id}`);
            const data = await response.json();
            
            html += `
                <div class="leaderboard-section">
                    <h3>${game.name}</h3>
                    <table class="leaderboard-table">
                        <thead>
                            <tr><th>Rank</th><th>Player</th><th>Score</th></tr>
                        </thead>
                        <tbody>
                            ${data.length > 0 ? data.map((entry, i) => `
                                <tr>
                                    <td>${i + 1}</td>
                                    <td>${entry[0]}</td>
                                    <td>${entry[1]} ${game.id === 'guessing' ? 'attempts' : 'points'}</td>
                                </tr>
                            `).join('') : '<tr><td colspan="3">No rankings yet.</td></tr>'}
                        </tbody>
                    </table>
                </div>
            `;
        } catch (err) {
            console.error(`Error loading leaderboard for ${game.id}:`, err);
        }
    }
    content.innerHTML = html;
}

function closeLeaderboard() {
    const modal = document.getElementById('leaderboardModal');
    modal.classList.add('hidden');
    modal.style.display = 'none'; // Hide it
    document.getElementById('leaderboardContent').innerHTML = ''; // Clear content on close
}
