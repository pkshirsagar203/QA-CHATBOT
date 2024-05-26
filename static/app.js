async function generateQuestion() {
    const topic = document.getElementById("topic").value;
    const response = await fetch('/generate-question', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ topic: topic })
    });
    const data = await response.json();
    document.getElementById("questionText").innerText = data.question;
}

async function submitAnswer() {
    const question = document.getElementById("questionText").innerText;
    const userAnswer = document.getElementById("userAnswer").value;
    const response = await fetch('/verify-answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question, answer: userAnswer })
    });
    const data = await response.json();
    document.getElementById("feedbackText").innerText = data.feedback;
}
