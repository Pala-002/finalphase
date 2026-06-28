// N-Back Test Implementation (2-Back)
class NBackTest {
    constructor() {
        this.letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        this.sequence = [];
        this.trials = [];
        this.currentTrial = 0;
        this.hits = 0;
        this.errors = 0;
        this.waitingForResponse = false;
        this.stimulusStartTime = null;
        
        this.init();
    }
    
    init() {
        document.getElementById('start-nback').addEventListener('click', () => this.start());
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && this.waitingForResponse) {
                e.preventDefault();
                this.handleResponse(true);
            }
        });
    }
    
    start() {
        document.getElementById('instructions').classList.add('d-none');
        document.getElementById('test-area').classList.remove('d-none');
        this.generateSequence();
        this.nextTrial();
    }
    
    generateSequence() {
        // Generate sequence with ~30% targets
        for (let i = 0; i < 20; i++) {
            if (i >= 2 && Math.random() < 0.3) {
                // Target - repeat letter from 2 positions back
                this.sequence.push(this.sequence[i - 2]);
            } else {
                // Non-target - random letter
                this.sequence.push(this.letters[Math.floor(Math.random() * this.letters.length)]);
            }
        }
    }
    
    nextTrial() {
        if (this.currentTrial >= 20) {
            this.complete();
            return;
        }
        
        const letter = this.sequence[this.currentTrial];
        const stimulus = document.getElementById('stimulus');
        stimulus.textContent = letter;
        
        this.waitingForResponse = true;
        this.stimulusStartTime = Date.now();
        this.responded = false;
        
        document.getElementById('trial-count').textContent = this.currentTrial + 1;
        
        // Auto-hide stimulus after 500ms
        setTimeout(() => {
            stimulus.textContent = '';
            this.waitingForResponse = false;
            
            // Record as miss if target was not responded to
            const isTarget = this.currentTrial >= 2 && letter === this.sequence[this.currentTrial - 2];
            if (isTarget && !this.responded) {
                this.trials.push({ is_target: true, responded: false, correct: false });
            } else if (!isTarget && !this.responded) {
                this.trials.push({ is_target: false, responded: false, correct: true });
            }
            
            setTimeout(() => this.nextTrial(), 2500);
        }, 500);
    }
    
    handleResponse(spacePressed) {
        if (!this.waitingForResponse || !spacePressed) return;
        
        this.responded = true;
        const rt = Date.now() - this.stimulusStartTime;
        const isTarget = this.currentTrial >= 2 && 
            this.sequence[this.currentTrial] === this.sequence[this.currentTrial - 2];
        
        if (isTarget) {
            this.hits++;
            document.getElementById('hits').textContent = this.hits;
        } else {
            this.errors++;
            document.getElementById('errors').textContent = this.errors;
        }
        
        this.trials.push({
            is_target: isTarget,
            responded: true,
            response_time_ms: rt,
            correct: isTarget
        });
    }
    
    async complete() {
        document.getElementById('test-area').classList.add('d-none');
        document.getElementById('complete').classList.remove('d-none');
        
        await fetch('/cognitive/nback/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ trials: this.trials })
        });
    }
}

new NBackTest();
