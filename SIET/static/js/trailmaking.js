// Trail Making Test Implementation
class TrailMakingTest {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.nodes = [];
        this.currentNode = 0;
        this.startTime = null;
        this.timerInterval = null;
        this.version = 'A';
        
        this.init();
    }
    
    init() {
        document.getElementById('start-version-a').addEventListener('click', () => this.start('A'));
        document.getElementById('start-version-b').addEventListener('click', () => this.start('B'));
    }
    
    start(version) {
        this.version = version;
        document.getElementById('instructions').classList.add('d-none');
        document.getElementById('test-area').classList.remove('d-none');
        
        this.canvas = document.getElementById('trail-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        
        this.generateNodes();
        this.draw();
        this.startTime = Date.now();
        this.timerInterval = setInterval(() => {
            const elapsed = ((Date.now() - this.startTime) / 1000).toFixed(1);
            document.getElementById('time').textContent = elapsed;
        }, 100);
    }
    
    generateNodes() {
        this.nodes = [];
        const count = this.version === 'A' ? 15 : 13; // Numbers 1-15 or 1-7 + A-G
        const padding = 50;
        
        for (let i = 0; i < count; i++) {
            let label;
            if (this.version === 'A') {
                label = (i + 1).toString();
            } else {
                label = i % 2 === 0 ? ((i / 2) + 1).toString() : String.fromCharCode(65 + Math.floor(i / 2));
            }
            
            this.nodes.push({
                x: padding + Math.random() * (this.canvas.width - 2 * padding),
                y: padding + Math.random() * (this.canvas.height - 2 * padding),
                label: label,
                connected: false
            });
        }
        
        this.currentNode = 0;
    }
    
    draw() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections
        this.ctx.strokeStyle = '#007bff';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        for (let i = 0; i < this.nodes.length; i++) {
            if (this.nodes[i].connected && i > 0 && this.nodes[i-1].connected) {
                this.ctx.moveTo(this.nodes[i-1].x, this.nodes[i-1].y);
                this.ctx.lineTo(this.nodes[i].x, this.nodes[i].y);
            }
        }
        this.ctx.stroke();
        
        // Draw nodes
        this.nodes.forEach(node => {
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, 20, 0, Math.PI * 2);
            this.ctx.fillStyle = node.connected ? '#28a745' : '#fff';
            this.ctx.fill();
            this.ctx.strokeStyle = '#333';
            this.ctx.stroke();
            
            this.ctx.fillStyle = '#000';
            this.ctx.font = '16px Arial';
            this.ctx.textAlign = 'center';
            this.ctx.textBaseline = 'middle';
            this.ctx.fillText(node.label, node.x, node.y);
        });
    }
    
    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const targetNode = this.nodes[this.currentNode];
        const dist = Math.sqrt((x - targetNode.x) ** 2 + (y - targetNode.y) ** 2);
        
        if (dist < 30) {
            targetNode.connected = true;
            this.currentNode++;
            this.draw();
            
            if (this.currentNode >= this.nodes.length) {
                this.complete();
            }
        }
    }
    
    async complete() {
        clearInterval(this.timerInterval);
        const finalTime = ((Date.now() - this.startTime) / 1000).toFixed(1);
        
        document.getElementById('test-area').classList.add('d-none');
        document.getElementById('complete').classList.remove('d-none');
        document.getElementById('final-time').textContent = finalTime;
        
        await fetch('/cognitive/trailmaking/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ['version_' + this.version.toLowerCase()]: {
                    time_ms: parseInt(finalTime * 1000),
                    errors: 0,
                    completed: true,
                    path_efficiency: 1.0
                }
            })
        });
    }
}

new TrailMakingTest();
