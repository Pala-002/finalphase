// RED-TIC Questionnaire Handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('redtic-form');
    const loading = document.getElementById('loading');
    
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const answers = {};
            const timing = {};
            const formData = new FormData(form);
            
            for (let [key, value] of formData.entries()) {
                if (key.startsWith('q')) {
                    const qId = key.substring(1);
                    answers[qId] = parseInt(value);
                    timing[qId] = performance.now(); // Simple timing
                }
            }
            
            // Show loading
            loading.classList.remove('d-none');
            form.classList.add('d-none');
            
            try {
                const response = await fetch('/evaluation/redtic/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrf_token]')?.value || ''
                    },
                    body: JSON.stringify({ answers, timing })
                });
                
                const result = await response.json();
                if (result.success) {
                    window.location.href = result.redirect_url;
                } else {
                    alert('Error al enviar respuestas');
                    location.reload();
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error de conexión');
                location.reload();
            }
        });
    }
});
