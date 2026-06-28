// Stroop Test Implementation
class StroopTest {
    constructor() {
        this.colors = ['rojo', 'azul', 'verde', 'amarillo'];
        this.colorNames = ['ROJO', 'AZUL', 'VERDE', 'AMARILLO'];
        this.trials = [];
        this.currentTrial = 0;
        this.startTime = null;
        this.results = [];
        
        this.init();
    }
    
    init() {
        document.getElementById('start-stroop').addEventListener('click', () => this.start());
        document.querySelectorAll('#color-buttons button').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleResponse(e.target.dataset.color));
        });
    }
    
    start() {
        document.getElementById('instructions').classList.add('d-none');
        document.getElementById('test-area').classList.remove('d-none');
        this.startTime = Date.now();
        this.nextTrial();
    }
    
    nextTrial() {
        if (this.currentTrial >= 20) {
            this.complete();
            return;
        }
        
        const wordIdx = Math.floor(Math.random() * 4);
        const colorIdx = Math.floor(Math.random() * 4);
        
        const stimulus = document.getElementById('stimulus');
        stimulus.textContent = this.colorNames[wordIdx];
        stimulus.style.color = this.colors[colorIdx];
        
        this.currentTrialData = {
            word: this.colors[wordIdx],
            color: this.colors[colorIdx],
            congruent: wordIdx === colorIdx,
            startTime: Date.now()
        };
        
        document.getElementById('trial-count').textContent = this.currentTrial + 1;
    }
    
    handleResponse(selectedColor) {
        const rt = Date.now() - this.currentTrialData.startTime;
        const correct = selectedColor === this.currentTrialData.color;
        
        this.results.push({
            ...this.currentTrialData,
            response: selectedColor,
            correct,
            reaction_time_ms: rt
        });
        
        this.currentTrial++;
        this.nextTrial();
    }
    
    async complete() {
        document.getElementById('test-area').classList.add('d-none');
        document.getElementById('complete').classList.remove('d-none');
        
        // Send results to server
        await fetch('/cognitive/stroop/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ trials: this.results })
        });
    }
}

new StroopTest();
