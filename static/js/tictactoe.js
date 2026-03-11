
function initTicTacToe(container) {
    let currentPlayer = 'X';
    let board = ['', '', '', '', '', '', '', '', ''];
    let gameActive = true;

    const gameHTML = `
        <div class="tictactoe-container">
            <div id="tictactoeStatus" class="status-msg">Player ${currentPlayer}'s Turn</div>
            <div class="tictactoe-grid">
                ${[0,1,2,3,4,5,6,7,8].map(i => `<div class="tictactoe-cell" data-index="${i}"></div>`).join('')}
            </div>
            <button class="btn-primary mt-4" id="resetBtn">Reset Game</button>
        </div>
    `;
    container.innerHTML = gameHTML;

    const cells = container.querySelectorAll('.tictactoe-cell');
    const status = container.querySelector('#tictactoeStatus');
    const resetBtn = container.querySelector('#resetBtn');

    cells.forEach(cell => {
        cell.addEventListener('click', (e) => handleCellClick(e));
    });

    resetBtn.addEventListener('click', () => resetGame());

    function handleCellClick(e) {
        const index = e.target.getAttribute('data-index');
        if (board[index] !== '' || !gameActive) return;

        board[index] = currentPlayer;
        e.target.innerText = currentPlayer;
        e.target.classList.add(currentPlayer === 'X' ? 'neon-blue' : 'neon-purple');

        if (checkWin()) {
            status.innerText = `Player ${currentPlayer} Wins!`;
            gameActive = false;
            saveWin();
        } else if (board.every(cell => cell !== '')) {
            status.innerText = "It's a Draw!";
            gameActive = false;
        } else {
            currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
            status.innerText = `Player ${currentPlayer}'s Turn`;
        }
    }

    function checkWin() {
        const winPatterns = [
            [0,1,2], [3,4,5], [6,7,8], // rows
            [0,3,6], [1,4,7], [2,5,8], // cols
            [0,4,8], [2,4,6]           // diags
        ];
        return winPatterns.some(pattern => {
            return pattern.every(index => board[index] === currentPlayer);
        });
    }

    async function saveWin() {
        // Since we are playing locally, the "currentPlayer" who wins 
        // will get their score updated if they match the logged in user
        // For simplicity, we'll increment the score of the currently logged in user
        try {
            await fetch('/api/score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game: 'tictactoe', action: 'increment' })
            });
        } catch (err) {
            console.error("Error saving score:", err);
        }
    }

    function resetGame() {
        currentPlayer = 'X';
        board = ['', '', '', '', '', '', '', '', ''];
        gameActive = true;
        status.innerText = `Player ${currentPlayer}'s Turn`;
        cells.forEach(cell => {
            cell.innerText = '';
            cell.classList.remove('neon-blue', 'neon-purple');
        });
    }
}
