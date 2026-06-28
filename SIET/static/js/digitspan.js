// Digit Span Test Implementation
class DigitSpanTest {
    constructor() {
        this.currentLevel = 3;
        this.maxSpan = 0;
        this.attempts = 0;
        this.testType = 'forward';
        this.currentSequence = [];
        
        this.init();
    }
    
    init() {
        document.getElementById('start-forward').addEventListener('click', () => this.start('forward'));
        document.getElementById('start-backward').addEventListener('click', () => this.start('backward'));
        document.getElementById('submit-answer').addEventListener('click', () => this.submitAnswer());
    }
    
    start(type) {
        this.testType = type;
        this.currentLevel = 3;
        this.maxSpan = 0;
        document.getElementById('instructions').classList.add('d-none');
        document.getElementById('test-area').classList.remove('d-none');
        this.nextSequence();
    }
    
    nextSequence() {
        if (this.attempts >= 2) {
            this.levelComplete();
            return;
        }
        
        this.currentSequence = [];
        for (let i = 0; i < this.currentLevel; i++) {
            this.currentSequence.push(Math.floor(Math.random() * 10));
        }
        
        const sequenceEl = document.getElementById('sequence');
        sequenceEl.textContent = this.currentSequence.join(' ');
        document.getElementById('level').textContent = this.currentLevel;
        
        setTimeout(() => {
            sequenceEl.textContent = '';
            document.getElementById('user-input').value = '';
            document.getElementById('user-input').focus();
        }, 2000);
    }
    
    submitAnswer() {
        const input = document.getElementById('user-input').value.trim();
        const userDigits = input.split(/\s+/).map(Number);
        
        let correct;
        if (this.testType === 'forward') {
            correct = JSON.stringify(userDigits) === JSON.stringify(this.currentSequence);
        } else {
            const reversed = [...this.currentSequence].reverse();
            correct = JSON.stringify(userDigits) === JSON.stringify(reversed);
        }
        
        if (correct) {
            this.maxSpan = Math.max(this.maxSpan, this.currentLevel);
        }
        
        this.attempts++;
        if (this.attempts >= 2) {
            this.levelComplete();
        } else {
            this.nextSequence();
        }
    }
    
    levelComplete() {
        if (this.maxSpan === this.currentLevel && this.currentLevel < 9) {
            this.currentLevel++;
            this.attempts = 0;
            setTimeout(() => this.nextSequence(), 500);
        } else {
            this.complete();
        }
    }
    
    async complete() {
        document.getElementById('test-area').classList.add('d-none');
        document.getElementById('complete').classList.remove('d-none');
        document.getElementById('max-span').textContent = this.maxSpan;
        
        await fetch('/cognitive/digitspan/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                [this.testType]: [{ sequence_length: this.maxSpan, correct: true }]
            })
        });
    }
}

new DigitSpanTest();
