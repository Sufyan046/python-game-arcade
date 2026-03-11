
function initQuizGame(container) {
    const questions = [
        {
            question: "What is the capital of France?",
            options: ["Berlin", "Madrid", "Paris", "Rome"],
            answer: "Paris"
        },
        {
            question: "What is 2 + 2?",
            options: ["3", "4", "5", "6"],
            answer: "4"
        },
        {
            question: "What is the largest planet in our solar system?",
            options: ["Earth", "Jupiter", "Mars", "Saturn"],
            answer: "Jupiter"
        }
    ];

    let currentQuestion = 0;
    let score = 0;

    function renderQuestion() {
        if (currentQuestion < questions.length) {
            const q = questions[currentQuestion];
            const shuffledOptions = [...q.options].sort(() => Math.random() - 0.5);
            
            container.innerHTML = `
                <div class="quiz-container">
                    <p class="quiz-progress">Question ${currentQuestion + 1} of ${questions.length}</p>
                    <h3 class="quiz-question">${q.question}</h3>
                    <div class="quiz-options">
                        ${shuffledOptions.map(option => `
                            <button class="quiz-option" onclick="checkQuizAnswer('${option}', '${q.answer}')">${option}</button>
                        `).join('')}
                    </div>
                </div>
            `;
        } else {
            showFinalScore();
        }
    }

    window.checkQuizAnswer = (selected, correct) => {
        if (selected === correct) {
            score++;
            alert("Correct!");
        } else {
            alert(`Incorrect! The correct answer was ${correct}.`);
        }
        currentQuestion++;
        renderQuestion();
    };

    async function showFinalScore() {
        container.innerHTML = `
            <div class="quiz-container text-center">
                <h2>Quiz Complete!</h2>
                <p class="final-score">Your Score: ${score} / ${questions.length}</p>
                <button class="btn-primary" onclick="initQuizGame(document.getElementById('gameDisplay'))">Try Again</button>
            </div>
        `;
        saveScore(score);
    }

    async function saveScore(score) {
        try {
            await fetch('/api/score', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ game: 'quiz', score: score, action: 'update' })
            });
        } catch (err) {
            console.error("Error saving score:", err);
        }
    }

    renderQuestion();
}
