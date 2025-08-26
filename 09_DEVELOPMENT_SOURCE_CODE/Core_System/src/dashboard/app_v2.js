// MWRASP Dashboard v2 - Interactive Control System

// Global State
let dashboardState = {
    agents: {
        total: 127,
        active: 127,
        hibernating: 0,
        suspicious: 0,
        generation: 3
    },
    protocols: {
        quantumDefense: true,
        behavioralCrypto: true,
        temporalFrag: true,
        evolutionMode: true
    },
    securityLevel: 'SECRET',
    threatLevel: 0.35,
    responseTime: 87,
    threatsBlocked: 1247,
    fragments: {
        active: 847,
        reconstructionRate: 99.8,
        avgLifetime: 94
    },
    network: {
        clusters: 8,
        intelligenceLevel: 'NETWORK'
    },
    verification: {
        inProgress: false,
        progress: 0,
        results: []
    }
};

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeWebSocket();
    initializeControls();
    initializeCharts();
    startRealtimeUpdates();
    animateNetworkVisualization();
});

// WebSocket Connection for Real-time Updates
let ws = null;

function initializeWebSocket() {
    // Use ws:// for HTTP or wss:// for HTTPS
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.hostname}:8000/ws`;
    
    try {
        ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            console.log('Connected to MWRASP Command Center');
            updateSystemStatus('QUANTUM DEFENSE ACTIVE', 'active');
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            handleRealtimeUpdate(data);
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            updateSystemStatus('CONNECTION ERROR', 'error');
        };
        
        ws.onclose = () => {
            console.log('Disconnected from MWRASP Command Center');
            updateSystemStatus('RECONNECTING...', 'warning');
            setTimeout(initializeWebSocket, 5000);
        };
    } catch (error) {
        console.error('Failed to connect WebSocket:', error);
    }
}

// Initialize Controls
function initializeControls() {
    // Protocol Toggles
    document.getElementById('quantum-defense').addEventListener('change', (e) => {
        dashboardState.protocols.quantumDefense = e.target.checked;
        sendProtocolUpdate('quantum-defense', e.target.checked);
    });
    
    document.getElementById('behavioral-crypto').addEventListener('change', (e) => {
        dashboardState.protocols.behavioralCrypto = e.target.checked;
        sendProtocolUpdate('behavioral-crypto', e.target.checked);
    });
    
    document.getElementById('temporal-frag').addEventListener('change', (e) => {
        dashboardState.protocols.temporalFrag = e.target.checked;
        sendProtocolUpdate('temporal-frag', e.target.checked);
    });
    
    document.getElementById('evolution-mode').addEventListener('change', (e) => {
        dashboardState.protocols.evolutionMode = e.target.checked;
        sendProtocolUpdate('evolution-mode', e.target.checked);
    });
    
    // Security Level Selector
    document.getElementById('security-level').addEventListener('change', (e) => {
        dashboardState.securityLevel = e.target.value;
        updateSecurityLevel(e.target.value);
    });
    
    // Agent Selector
    document.getElementById('agent-selector').addEventListener('change', (e) => {
        if (e.target.value !== 'Select Agent...') {
            loadAgentDetails(e.target.value);
        }
    });
}

// Send Protocol Update
function sendProtocolUpdate(protocol, enabled) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
            type: 'protocol_update',
            protocol: protocol,
            enabled: enabled
        }));
    }
    
    addActivityItem(
        enabled ? 'success' : 'warning',
        `Protocol ${protocol} ${enabled ? 'enabled' : 'disabled'}`,
        enabled ? 'fa-check' : 'fa-times'
    );
}

// Update Security Level
function updateSecurityLevel(level) {
    const agentCounts = {
        'UNCLASSIFIED': { min: 10, max: 20 },
        'CONFIDENTIAL': { min: 50, max: 100 },
        'SECRET': { min: 200, max: 500 },
        'TOP_SECRET': { min: 1000, max: 2000 },
        'QUANTUM_CLASSIFIED': { min: 5000, max: null }
    };
    
    const range = agentCounts[level];
    
    // Trigger agent scaling
    if (dashboardState.agents.total < range.min) {
        spawnAgents(range.min - dashboardState.agents.total);
    }
    
    addActivityItem('info', `Security level changed to ${level}`, 'fa-shield-alt');
}

// Agent Headcount
function runAgentHeadcount() {
    const modal = document.getElementById('verification-modal');
    modal.classList.add('active');
    
    // Start headcount
    let verified = 0;
    const total = dashboardState.agents.total;
    
    document.getElementById('total-agents').textContent = total;
    
    const interval = setInterval(() => {
        verified += Math.floor(Math.random() * 10) + 5;
        if (verified >= total) {
            verified = total;
            clearInterval(interval);
            
            // Show results
            const suspicious = Math.floor(Math.random() * 3);
            dashboardState.agents.suspicious = suspicious;
            
            const results = document.getElementById('verification-results');
            results.innerHTML = `
                <div class="verification-summary">
                    <h3>Headcount Complete</h3>
                    <div class="headcount-results">
                        <div class="result-item">
                            <span class="result-label">Total Agents</span>
                            <span class="result-value">${total}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Verified</span>
                            <span class="result-value success">${total - suspicious}</span>
                        </div>
                        <div class="result-item">
                            <span class="result-label">Suspicious</span>
                            <span class="result-value danger">${suspicious}</span>
                        </div>
                    </div>
                </div>
            `;
            
            if (suspicious > 0) {
                addActivityItem('warning', `${suspicious} suspicious agents detected during headcount`, 'fa-exclamation');
            }
        }
        
        document.getElementById('verify-count').textContent = verified;
        document.getElementById('verification-progress').style.width = `${(verified / total) * 100}%`;
    }, 100);
}

// Agent Verification
function initiateVerification() {
    const modal = document.getElementById('verification-modal');
    modal.classList.add('active');
    startVerification();
}

function startVerification() {
    dashboardState.verification.inProgress = true;
    dashboardState.verification.progress = 0;
    
    const total = dashboardState.agents.total;
    let verified = 0;
    let impostors = [];
    
    const interval = setInterval(() => {
        verified++;
        
        // Simulate behavioral verification
        const confidence = Math.random();
        if (confidence < 0.02) { // 2% impostor rate for demo
            impostors.push({
                agent: `AGENT_${verified.toString().padStart(3, '0')}`,
                confidence: confidence,
                anomalies: ['protocol_sequence_mismatch', 'behavioral_deviation']
            });
        }
        
        dashboardState.verification.progress = (verified / total) * 100;
        document.getElementById('verify-count').textContent = verified;
        document.getElementById('verification-progress').style.width = `${dashboardState.verification.progress}%`;
        
        if (verified >= total) {
            clearInterval(interval);
            dashboardState.verification.inProgress = false;
            displayVerificationResults(impostors);
        }
    }, 50);
}

function displayVerificationResults(impostors) {
    const results = document.getElementById('verification-results');
    
    if (impostors.length === 0) {
        results.innerHTML = `
            <div class="verification-success">
                <i class="fas fa-check-circle"></i>
                <h3>All Agents Verified</h3>
                <p>No impostors detected. All behavioral signatures match expected patterns.</p>
            </div>
        `;
    } else {
        let impostorList = impostors.map(imp => `
            <div class="impostor-item">
                <span class="impostor-id">${imp.agent}</span>
                <span class="impostor-confidence">Confidence: ${(imp.confidence * 100).toFixed(1)}%</span>
                <div class="impostor-anomalies">
                    ${imp.anomalies.map(a => `<span class="anomaly-tag">${a}</span>`).join('')}
                </div>
            </div>
        `).join('');
        
        results.innerHTML = `
            <div class="verification-warning">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>${impostors.length} Potential Impostors Detected</h3>
                <div class="impostor-list">
                    ${impostorList}
                </div>
            </div>
        `;
    }
}

function quarantineSuspicious() {
    if (dashboardState.agents.suspicious > 0) {
        addActivityItem('danger', `${dashboardState.agents.suspicious} agents quarantined`, 'fa-lock');
        dashboardState.agents.active -= dashboardState.agents.suspicious;
        dashboardState.agents.suspicious = 0;
        updateAgentCount();
    }
    closeVerificationModal();
}

// Emergency Protocol
function emergencyProtocol() {
    document.getElementById('emergency-modal').classList.add('active');
}

function activateEmergency() {
    // Get selected options
    const options = document.querySelectorAll('.emergency-option input:checked');
    const protocols = Array.from(options).map(opt => opt.nextElementSibling.textContent);
    
    // Activate emergency measures
    dashboardState.securityLevel = 'QUANTUM_CLASSIFIED';
    dashboardState.threatLevel = 0.9;
    
    // Update UI
    document.getElementById('security-level').value = 'QUANTUM_CLASSIFIED';
    document.querySelector('.threat-fill').style.width = '90%';
    
    // Spawn emergency agents
    spawnAgents(50, 'EMERGENCY_RESPONSE');
    
    // Log activation
    protocols.forEach(protocol => {
        addActivityItem('danger', `Emergency: ${protocol}`, 'fa-shield-alt');
    });
    
    closeEmergencyModal();
    
    // Flash warning
    document.body.style.animation = 'emergency-flash 0.5s';
    setTimeout(() => {
        document.body.style.animation = '';
    }, 500);
}

// Spawn Agents
function spawnAgents(count, specialization = 'AUTO') {
    for (let i = 0; i < count; i++) {
        setTimeout(() => {
            dashboardState.agents.total++;
            dashboardState.agents.active++;
            updateAgentCount();
            
            const specs = ['DEFENDER', 'MONITOR', 'ANALYZER', 'QUANTUM_SPECIALIST', 'BEHAVIORAL_ANALYST'];
            const spec = specialization === 'AUTO' ? specs[Math.floor(Math.random() * specs.length)] : specialization;
            
            addActivityItem('info', `New agent spawned: ${spec}_${dashboardState.agents.total}`, 'fa-robot');
        }, i * 100);
    }
}

// Load Agent Details
function loadAgentDetails(agentId) {
    // Simulate loading agent details
    const details = {
        status: 'ACTIVE',
        generation: Math.floor(Math.random() * 3) + 1,
        specialization: ['Quantum Defense', 'Behavioral Analysis', 'Network Monitor'][Math.floor(Math.random() * 3)],
        trustScore: (0.8 + Math.random() * 0.2).toFixed(2),
        relationships: Math.floor(Math.random() * 60) + 20,
        packetRhythm: `[${Math.floor(Math.random() * 50) + 50}, ${Math.floor(Math.random() * 50) + 50}, ${Math.floor(Math.random() * 100) + 100}]ms`,
        bufferPreference: (1.0 + Math.random() * 0.5).toFixed(1) + 'x',
        hashTruncation: Math.floor(Math.random() * 8) + 8 + ' chars'
    };
    
    // Update UI
    const detailsContainer = document.getElementById('agent-details');
    detailsContainer.innerHTML = `
        <div class="detail-group">
            <span class="detail-label">Status</span>
            <span class="detail-value status-active">${details.status}</span>
        </div>
        <div class="detail-group">
            <span class="detail-label">Generation</span>
            <span class="detail-value">${details.generation}</span>
        </div>
        <div class="detail-group">
            <span class="detail-label">Specialization</span>
            <span class="detail-value">${details.specialization}</span>
        </div>
        <div class="detail-group">
            <span class="detail-label">Trust Score</span>
            <span class="detail-value">${details.trustScore}</span>
        </div>
        <div class="detail-group">
            <span class="detail-label">Relationships</span>
            <span class="detail-value">${details.relationships} Active</span>
        </div>
        <div class="behavioral-signature">
            <h4>Behavioral Signature</h4>
            <div class="signature-item">
                <span>Packet Rhythm</span>
                <span class="signature-value">${details.packetRhythm}</span>
            </div>
            <div class="signature-item">
                <span>Buffer Preference</span>
                <span class="signature-value">${details.bufferPreference}</span>
            </div>
            <div class="signature-item">
                <span>Hash Truncation</span>
                <span class="signature-value">${details.hashTruncation}</span>
            </div>
        </div>
    `;
}

// Real-time Updates
function startRealtimeUpdates() {
    // Update stats every second
    setInterval(() => {
        // Response time fluctuation
        dashboardState.responseTime = Math.max(50, Math.min(400, 
            dashboardState.responseTime + (Math.random() - 0.5) * 10));
        document.getElementById('response-time').textContent = `${Math.round(dashboardState.responseTime)}μs`;
        
        // Threats blocked increment
        if (Math.random() > 0.7) {
            dashboardState.threatsBlocked++;
            document.getElementById('threats-blocked').textContent = 
                dashboardState.threatsBlocked.toLocaleString();
        }
        
        // Fragment updates
        updateFragments();
        
        // Random activity
        if (Math.random() > 0.8) {
            generateRandomActivity();
        }
    }, 1000);
    
    // Evolution updates every 30 seconds
    setInterval(() => {
        if (dashboardState.protocols.evolutionMode && Math.random() > 0.5) {
            evolveAgents();
        }
    }, 30000);
}

// Update Fragments
function updateFragments() {
    const fragments = document.querySelectorAll('.fragment');
    fragments.forEach(frag => {
        const ttl = parseInt(frag.dataset.ttl) - Math.floor(Math.random() * 10);
        frag.dataset.ttl = ttl;
        
        if (ttl <= 0) {
            frag.className = 'fragment expired';
        } else if (ttl < 30) {
            frag.className = 'fragment expiring';
        } else {
            frag.className = 'fragment active';
        }
    });
    
    // Respawn expired fragments
    fragments.forEach(frag => {
        if (frag.classList.contains('expired') && Math.random() > 0.5) {
            frag.dataset.ttl = Math.floor(Math.random() * 50) + 50;
            frag.className = 'fragment active';
        }
    });
}

// Evolve Agents
function evolveAgents() {
    const evolutionChance = Math.random();
    
    if (evolutionChance > 0.7) {
        // Spawn new specialist
        dashboardState.agents.total++;
        dashboardState.agents.active++;
        updateAgentCount();
        
        addActivityItem('info', `Evolution: New specialist agent spawned`, 'fa-dna');
    } else if (evolutionChance > 0.4) {
        // Agent hibernation
        if (dashboardState.agents.active > 50) {
            dashboardState.agents.active--;
            dashboardState.agents.hibernating++;
            updateAgentCount();
            
            addActivityItem('info', `Agent entered hibernation for resource optimization`, 'fa-moon');
        }
    }
}

// Generate Random Activity
function generateRandomActivity() {
    const activities = [
        { type: 'success', text: 'Behavioral authentication successful', icon: 'fa-check' },
        { type: 'success', text: 'Quantum threat neutralized', icon: 'fa-shield-alt' },
        { type: 'warning', text: 'Protocol sequence anomaly detected', icon: 'fa-exclamation' },
        { type: 'info', text: 'Agent relationship established', icon: 'fa-link' },
        { type: 'info', text: 'Handshake evolution completed', icon: 'fa-handshake' },
        { type: 'success', text: 'Fragment reconstruction successful', icon: 'fa-puzzle-piece' }
    ];
    
    const activity = activities[Math.floor(Math.random() * activities.length)];
    addActivityItem(activity.type, activity.text, activity.icon);
}

// Add Activity Item
function addActivityItem(type, text, icon) {
    const feed = document.getElementById('activity-feed');
    const time = new Date().toLocaleTimeString('en-US', { hour12: false });
    
    const item = document.createElement('div');
    item.className = `activity-item ${type}`;
    item.innerHTML = `
        <span class="activity-time">${time}</span>
        <span class="activity-icon"><i class="fas ${icon}"></i></span>
        <span class="activity-text">${text}</span>
    `;
    
    feed.insertBefore(item, feed.firstChild);
    
    // Limit feed items
    while (feed.children.length > 10) {
        feed.removeChild(feed.lastChild);
    }
}

// Update Agent Count
function updateAgentCount() {
    document.getElementById('agent-count').textContent = dashboardState.agents.active;
}

// Update System Status
function updateSystemStatus(text, status) {
    const statusText = document.querySelector('.status-text');
    const statusIndicator = document.querySelector('.status-indicator');
    
    statusText.textContent = text;
    statusIndicator.className = `status-indicator ${status}`;
}

// Handle Real-time Updates
function handleRealtimeUpdate(data) {
    switch (data.type) {
        case 'agent_update':
            dashboardState.agents = data.agents;
            updateAgentCount();
            break;
        case 'threat_detected':
            dashboardState.threatsBlocked++;
            document.getElementById('threats-blocked').textContent = 
                dashboardState.threatsBlocked.toLocaleString();
            addActivityItem('warning', `Threat detected: ${data.threat}`, 'fa-exclamation-triangle');
            break;
        case 'evolution_event':
            addActivityItem('info', `Evolution: ${data.event}`, 'fa-dna');
            break;
    }
}

// Network Visualization
function animateNetworkVisualization() {
    const canvas = document.getElementById('network-canvas');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    function resizeCanvas() {
        canvas.width = canvas.offsetWidth;
        canvas.height = canvas.offsetHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Node class
    class Node {
        constructor(x, y, type) {
            this.x = x;
            this.y = y;
            this.type = type;
            this.radius = type === 'cluster' ? 8 : 4;
            this.connections = [];
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.color = this.getColor();
        }
        
        getColor() {
            const colors = {
                'defender': '#3B82F6',
                'monitor': '#10B981',
                'analyzer': '#F59E0B',
                'quantum': '#00D4FF',
                'behavioral': '#7C3AED',
                'cluster': '#EF4444'
            };
            return colors[this.type] || '#9CA3AF';
        }
        
        update() {
            this.x += this.vx;
            this.y += this.vy;
            
            // Bounce off walls
            if (this.x < this.radius || this.x > canvas.width - this.radius) {
                this.vx *= -1;
            }
            if (this.y < this.radius || this.y > canvas.height - this.radius) {
                this.vy *= -1;
            }
            
            // Keep in bounds
            this.x = Math.max(this.radius, Math.min(canvas.width - this.radius, this.x));
            this.y = Math.max(this.radius, Math.min(canvas.height - this.radius, this.y));
        }
        
        draw() {
            // Draw connections
            this.connections.forEach(other => {
                ctx.beginPath();
                ctx.moveTo(this.x, this.y);
                ctx.lineTo(other.x, other.y);
                ctx.strokeStyle = 'rgba(0, 212, 255, 0.1)';
                ctx.stroke();
            });
            
            // Draw node
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
            
            if (this.type === 'cluster') {
                ctx.strokeStyle = this.color;
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        }
    }
    
    // Create nodes
    const nodes = [];
    const types = ['defender', 'monitor', 'analyzer', 'quantum', 'behavioral', 'cluster'];
    
    for (let i = 0; i < 50; i++) {
        const type = types[Math.floor(Math.random() * types.length)];
        const node = new Node(
            Math.random() * canvas.width,
            Math.random() * canvas.height,
            type
        );
        nodes.push(node);
    }
    
    // Create connections
    nodes.forEach(node => {
        const connectionCount = node.type === 'cluster' ? 5 : 2;
        for (let i = 0; i < connectionCount; i++) {
            const other = nodes[Math.floor(Math.random() * nodes.length)];
            if (other !== node && !node.connections.includes(other)) {
                node.connections.push(other);
            }
        }
    });
    
    // Animation loop
    function animate() {
        ctx.fillStyle = 'rgba(10, 14, 27, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        nodes.forEach(node => {
            node.update();
            node.draw();
        });
        
        requestAnimationFrame(animate);
    }
    
    animate();
}

// Initialize Charts
function initializeCharts() {
    // Performance chart
    const perfCanvas = document.getElementById('performance-chart');
    if (perfCanvas) {
        const ctx = perfCanvas.getContext('2d');
        
        // Simple line chart
        const data = [];
        for (let i = 0; i < 20; i++) {
            data.push(Math.random() * 100);
        }
        
        function drawChart() {
            ctx.clearRect(0, 0, perfCanvas.width, perfCanvas.height);
            ctx.strokeStyle = '#00D4FF';
            ctx.lineWidth = 2;
            ctx.beginPath();
            
            data.forEach((value, index) => {
                const x = (index / data.length) * perfCanvas.width;
                const y = perfCanvas.height - (value / 100) * perfCanvas.height;
                
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            
            ctx.stroke();
        }
        
        setInterval(() => {
            data.shift();
            data.push(Math.random() * 100);
            drawChart();
        }, 1000);
        
        drawChart();
    }
    
    // Threat radar
    const radarCanvas = document.getElementById('threat-radar');
    if (radarCanvas) {
        const ctx = radarCanvas.getContext('2d');
        const centerX = radarCanvas.width / 2;
        const centerY = radarCanvas.height / 2;
        const radius = Math.min(centerX, centerY) - 20;
        
        function drawRadar() {
            ctx.clearRect(0, 0, radarCanvas.width, radarCanvas.height);
            
            // Draw rings
            for (let i = 1; i <= 3; i++) {
                ctx.beginPath();
                ctx.arc(centerX, centerY, (radius / 3) * i, 0, Math.PI * 2);
                ctx.strokeStyle = 'rgba(55, 65, 81, 0.5)';
                ctx.stroke();
            }
            
            // Draw axes
            for (let i = 0; i < 6; i++) {
                const angle = (Math.PI * 2 / 6) * i;
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.lineTo(
                    centerX + Math.cos(angle) * radius,
                    centerY + Math.sin(angle) * radius
                );
                ctx.strokeStyle = 'rgba(55, 65, 81, 0.5)';
                ctx.stroke();
            }
            
            // Draw threat levels
            const threats = [
                Math.random() * 0.8,
                Math.random() * 0.6,
                Math.random() * 0.4,
                Math.random() * 0.7,
                Math.random() * 0.5,
                Math.random() * 0.3
            ];
            
            ctx.beginPath();
            threats.forEach((threat, index) => {
                const angle = (Math.PI * 2 / 6) * index - Math.PI / 2;
                const x = centerX + Math.cos(angle) * radius * threat;
                const y = centerY + Math.sin(angle) * radius * threat;
                
                if (index === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }
            });
            ctx.closePath();
            ctx.fillStyle = 'rgba(0, 212, 255, 0.2)';
            ctx.fill();
            ctx.strokeStyle = '#00D4FF';
            ctx.stroke();
        }
        
        setInterval(drawRadar, 2000);
        drawRadar();
    }
}

// Modal Controls
function closeVerificationModal() {
    document.getElementById('verification-modal').classList.remove('active');
}

function closeEmergencyModal() {
    document.getElementById('emergency-modal').classList.remove('active');
}

function openAgentVerification() {
    runAgentHeadcount();
}

function openSettings() {
    // Settings implementation
    console.log('Settings panel not yet implemented');
}

function toggleFullscreen() {
    if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
    } else {
        document.exitFullscreen();
    }
}

function refreshNetwork() {
    animateNetworkVisualization();
    addActivityItem('info', 'Network topology refreshed', 'fa-sync');
}

function toggleNetworkView() {
    // Toggle between different network views
    console.log('Network view toggle not yet implemented');
}

function toggleEvolutionView() {
    // Toggle evolution view
    console.log('Evolution view toggle not yet implemented');
}

function exportResults() {
    // Export verification results
    const results = {
        timestamp: new Date().toISOString(),
        agents: dashboardState.agents,
        verification: dashboardState.verification
    };
    
    const blob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `mwrasp-verification-${Date.now()}.json`;
    a.click();
}

// CSS Animation for emergency
const style = document.createElement('style');
style.textContent = `
@keyframes emergency-flash {
    0%, 100% { filter: brightness(1); }
    50% { filter: brightness(1.2) hue-rotate(-10deg); }
}
`;
document.head.appendChild(style);