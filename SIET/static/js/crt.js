// Cognitive Reflection Test Handler
document.addEventListener('DOMContentLoaded', function() {
    const answers = {};
    const startTime = {};
    
    document.querySelectorAll('.crt-option').forEach(btn => {
        btn.addEventListener('click', function() {
            const qId = this.dataset.question;
            const answer = this.dataset.answer;
            
            // Record answer and timing
            answers[qId] = answer;
            if (!startTime[qId]) startTime[qId] = Date.now();
            
            // Visual feedback
            document.querySelectorAll(`[data-question="${qId}"]`).forEach(b => {
                b.classList.remove('btn-primary');
                b.classList.add('btn-outline-primary');
            });
            this.classList.remove('btn-outline-primary');
            this.classList.add('btn-primary');
        });
    });
    
    document.getElementById('submit-crt').addEventListener('click', async function() {
        const crtAnswers = [];
        const correctAnswers = ['$0.05', '5 minutos', '47 días'];
        
        for (let i = 1; i <= 3; i++) {
            crtAnswers.push({
                answer: answers[i] || '',
                response_time_ms: startTime[i] ? Date.now() - startTime[i] : 0
            });
        }
        
        const response = await fetch('/cognitive/crt/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ answers: crtAnswers })
        });
        
        const result = await response.json();
        if (result.success) {
            document.getElementById('crt-container').classList.add('d-none');
            document.getElementById('result').classList.remove('d-none');
            document.getElementById('crt-score').textContent = result.score;
        }
    });
});
