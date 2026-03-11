
function initGuessingGame(container) {
    let secretNum = Math.floor(Math.random() * 100) + 1;
    let attempts = 0;
    let gameActive = true;

    const gameHTML = `
        <div class="guessing-container">
            <p>I'm thinking of a number between 1 and 100.</p>
            <p id="guessingStatus" class="status-msg">Make your first guess!</p>
            <div class="input-group">
                <input type="number" id="guessInput" placeholder="Enter number" min="1" max="100">
            </div>
            <button class="btn-primary" id="guessBtn">Submit Guess</button>
            <button class="btn-secondary hidden mt-4" id="playAgainBtn">Play Again</button>
        </div>
    `;
    container.innerHTML = gameHTML;

    const input = container.querySelector('#guessInput');
    const guessBtn = container.querySelector('#guessBtn');
    const status = container.querySelector('#guessingStatus');
    const playAgainBtn = container.querySelector('#playAgainBtn');

    guessBtn.addEventListener('click', () => {
        if (!gameActive) return;
        const guess = parseInt(input.value);
        if (isNaN(guess) || guess < 1 || guess > 100) {
            alert("Please enter a valid number between 1 and 100.");
            return;
        }

        attempts++;
        if (guess < secretNum) {
            status.innerText = "Too Low! Try again.";
            status.style.color = "var(--neon-blue)";
        } else if (guess > secretNum) {
            status.innerText = "Too High! Try again.";
            status.style.color = "var(--neon-purple)";
        } else {
            status.innerText = `CORRECT! You found it in ${attempts} attempts.`;
            status.style.color = "var(--neon-green)";
            gameActive = false;
            playAgainBtn.classList.remove('hidden');
            saveScore(attempts);
        }
        input.value = '';
        input.focus();
    });

    playAgainBtn.addEventListener('click', () => {
        secretNum = Math.floor(Math.random() * 100) + 1;
        attempts = 0;
        gameActive = true;
        status.innerText = "Make your first guess!";
        status.style.color = "var(--text-light)";
        playAgainBtn.classList.add('hidden');
    });

    async function saveScore(score) {
        try {
            await fetch('/api/score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game: 'guessing', score: score, action: 'update' })
            });
        } catch (err) {
            console.error("Error saving score:", err);
        }
    }
}
