<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LexAI | Schweizer Anwaltsprüfungssimulator</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f9f9fb;
            --bg-tertiary: #f1f1f4;
            --text-primary: #111111;
            --text-secondary: #666666;
            --text-muted: #999999;
            --accent: #1c2d42;
            --accent-light: #e8ecef;
            --border-color: #e5e5e7;
            --success: #2e7d32;
            --error: #c62828;
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: var(--font-main); background-color: var(--bg-primary); color: var(--text-primary); line-height: 1.6; -webkit-font-smoothing: antialiased; }
        header { border-bottom: 1px solid var(--border-color); padding: 1.5rem 2rem; display: flex; justify-content: space-between; align-items: center; background: var(--bg-primary); position: sticky; top: 0; z-index: 100; }
        .logo { font-weight: 700; font-size: 1.25rem; letter-spacing: -0.02em; text-transform: uppercase; }
        .logo span { font-weight: 300; color: var(--text-secondary); }
        main { max-width: 1200px; margin: 0 auto; padding: 2rem; min-height: calc(100vh - 74px); }
        .hidden { display: none !important; }
        .card { background: var(--bg-primary); border: 1px solid var(--border-color); padding: 2.5rem; margin-bottom: 2rem; border-radius: 0px; }
        h1, h2, h3 { font-weight: 600; letter-spacing: -0.01em; margin-bottom: 1.5rem; }
        h1 { font-size: 2rem; }
        h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; color: var(--text-secondary); }
        input[type="text"], input[type="password"], select, textarea { width: 100%; padding: 0.8rem 1rem; border: 1px solid var(--border-color); background: var(--bg-secondary); font-family: var(--font-main); font-size: 1rem; color: var(--text-primary); transition: border-color 0.2s ease; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: var(--text-primary); background: var(--bg-primary); }
        .btn { display: inline-block; padding: 0.8rem 2rem; font-family: var(--font-main); font-size: 0.95rem; font-weight: 500; text-decoration: none; cursor: pointer; transition: all 0.2s ease; border: 1px solid var(--text-primary); background: transparent; color: var(--text-primary); }
        .btn-primary { background: var(--text-primary); color: var(--bg-primary); }
        .btn-primary:hover { background: var(--accent); border-color: var(--accent); }
        .btn-secondary:hover { background: var(--bg-secondary); }
        .grid-cantons { display: grid; grid-template-columns: repeat(auto-fill, minmax(70px, 1fr)); gap: 0.5rem; margin-bottom: 1.5rem; }
        .canton-chip { border: 1px solid var(--border-color); padding: 0.5rem; text-align: center; cursor: pointer; font-weight: 500; font-size: 0.9rem; background: var(--bg-secondary); }
        .canton-chip.active { background: var(--text-primary); color: var(--bg-primary); border-color: var(--text-primary); }
        .grid-fields { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
        .checkbox-card { border: 1px solid var(--border-color); padding: 1rem; cursor: pointer; display: flex; align-items: center; background: var(--bg-secondary); }
        .checkbox-card input { margin-right: 1rem; transform: scale(1.2); }
        .checkbox-card.active { border-color: var(--text-primary); background: var(--bg-primary); }
        .simulation-container { display: flex; flex-direction: column; height: calc(100vh - 200px); min-height: 500px; }
        .sim-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 1rem; border-bottom: 1px solid var(--border-color); margin-bottom: 1rem; }
        .timer-badge { font-family: monospace; font-size: 1.2rem; font-weight: 600; }
        .progress-bar-container { width: 100%; height: 3px; background: var(--bg-tertiary); margin-bottom: 1.5rem; }
        .progress-bar { height: 100%; width: 0%; background: var(--text-primary); transition: width 0.4s ease; }
        .chat-feed { flex-grow: 1; overflow-y: auto; padding-right: 1rem; margin-bottom: 1.5rem; }
        .message { margin-bottom: 2rem; max-width: 85%; animation: fadeIn 0.3s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        .message-meta { font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; color: var(--text-secondary); }
        .message-text { background: var(--bg-secondary); padding: 1.2rem 1.5rem; border-left: 3px solid var(--text-muted); font-size: 1rem; }
        .msg-commission { margin-right: auto; }
        .msg-commission .message-text { border-left-color: var(--accent); background: var(--bg-secondary); }
        .msg-user { margin-left: auto; max-width: 80%; }
        .msg-user .message-text { border-left: none; border-right: 3px solid var(--text-primary); background: var(--bg-primary); text-align: left; border: 1px solid var(--border-color); }
        .input-area { display: flex; gap: 1rem; align-items: flex-end; background: var(--bg-primary); padding-top: 1rem; border-top: 1px solid var(--border-color); }
        .input-wrapper { flex-grow: 1; position: relative; }
        .speech-indicator { position: absolute; right: 15px; top: 50%; transform: translateY(-50%); width: 10px; height: 10px; background: var(--error); border-radius: 50%; animation: pulse 1.2s infinite; }
        @keyframes pulse { 0% { transform: translateY(-50%) scale(0.9); opacity: 0.6; } 50% { transform: translateY(-50%) scale(1.3); opacity: 1; } 100% { transform: translateY(-50%) scale(0.9); opacity: 0.6; } }
        .control-btns { display: flex; gap: 0.5rem; }
        .btn-icon { padding: 0.8rem; display: flex; align-items: center; justify-content: center; width: 48px; height: 48px; }
        .feedback-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; }
        .grade-box { border: 2px solid var(--text-primary); text-align: center; padding: 3rem 1rem; }
        .grade-num { font-size: 5rem; font-weight: 700; line-height: 1; margin-bottom: 0.5rem; }
        .metric-card { border-bottom: 1px solid var(--border-color); padding: 1rem 0; }
        .metric-title { font-weight: 600; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
        #toast { position: fixed; bottom: 2rem; right: 2rem; background: var(--text-primary); color: var(--bg-primary); padding: 1rem 2rem; font-size: 0.9rem; z-index: 1000; animation: fadeIn 0.2s ease; }
    </style>
</head>
<body>

    <header>
        <div class="logo">LexAI <span>// Anwaltsprüfung</span></div>
        <div id="user-status-bar" style="font-size: 0.9rem;">
            <span id="status-user-name">API nicht verbunden</span> | <a href="#" onclick="logout()" style="color: var(--text-primary);">Trennen</a>
        </div>
    </header>

    <main>
        <div id="toast" class="hidden"></div>

        <div id="view-auth" class="view">
            <div class="card" style="max-width: 550px; margin: 4rem auto;">
                <h2>API-Konfiguration</h2>
                <p style="color: var(--text-secondary); margin-bottom: 2rem; font-size: 0.95rem;">
                    Bitte hinterlegen Sie Ihren gültigen Anthropic API-Key, um den Simulator zu nutzen. 
                    Ihr Key wird nur lokal in Ihrem Browser gespeichert und verschlüsselt an Anthropic gesendet.
                </p>
                
                <div class="form-group" style="margin-bottom: 2rem;">
                    <label for="api-key">Anthropic API-Key (Claude)</label>
                    <input type="password" id="api-key" placeholder="sk-ant-...">
                </div>

                <div style="display: flex; gap: 1rem; flex-direction: column;">
                    <button class="btn btn-primary" onclick="handleLogin()">Speichern & Fortfahren</button>
                </div>
            </div>
        </div>

        <div id="view-config" class="view hidden">
            <h1>Konfiguration der Prüfungssimulation</h1>
            
            <div class="card">
                <h2>1. Kantonale Jurisdiktion bestimmen</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1rem; font-size: 0.9rem;">
                    Wählen Sie den Kanton aus. Dies beeinflusst das kantonale Verfahrensrecht.
                </p>
                <div class="grid-cantons" id="canton-selector"></div>
            </div>

            <div class="card">
                <h2>2. Prüfungsfächer & Materielles Recht</h2>
                <div class="grid-fields">
                    <div class="checkbox-card active" onclick="toggleLawField(this, 'Zivilrecht')">
                        <input type="checkbox" value="Zivilrecht" checked>
                        <div><strong>Zivilrecht</strong> <span style="display:block; font-size:0.8rem; color:var(--text-secondary);">ZGB, OR</span></div>
                    </div>
                    <div class="checkbox-card" onclick="toggleLawField(this, 'Strafrecht')">
                        <input type="checkbox" value="Strafrecht">
                        <div><strong>Strafrecht</strong> <span style="display:block; font-size:0.8rem; color:var(--text-secondary);">StGB</span></div>
                    </div>
                    <div class="checkbox-card" onclick="toggleLawField(this, 'Verwaltungsrecht')">
                        <input type="checkbox" value="Verwaltungsrecht">
                        <div><strong>Öffentliches Recht</strong> <span style="display:block; font-size:0.8rem; color:var(--text-secondary);">VwVG, BV</span></div>
                    </div>
                    <div class="checkbox-card" onclick="toggleLawField(this, 'SchKG')">
                        <input type="checkbox" value="SchKG">
                        <div><strong>SchKG</strong> <span style="display:block; font-size:0.8rem; color:var(--text-secondary);">Betreibung & Konkurs</span></div>
                    </div>
                    <div class="checkbox-card active" onclick="toggleLawField(this, 'ZPO')">
                        <input type="checkbox" value="ZPO" checked>
                        <div><strong>Zivilprozessrecht</strong> <span style="display:block; font-size:0.8rem; color:var(--text-secondary);">ZPO</span></div>
                    </div>
                    <div class="checkbox-card" onclick="toggleLawField(this, 'StPO')">
                        <input type="checkbox" value="StPO">
                        <div><strong>Strafprozessrecht</strong> <span style="display:block; font-size:0.8rem; color:var(--text-secondary);">StPO</span></div>
                    </div>
                </div>
            </div>

            <div class="grid-fields" style="grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));">
                <div class="card">
                    <h2>3. Prüfungsmodus</h2>
                    <div class="form-group">
                        <select id="select-mode" onchange="toggleDuoInfo()">
                            <option value="solo">Solo-Modus</option>
                            <option value="duo">Duo-Modus (Mitkandidat)</option>
                        </select>
                    </div>
                    <p id="duo-info" style="font-size:0.85rem; color:var(--text-secondary);" class="hidden">
                        * Im Duo-Modus agiert Claude zusätzlich als zweiter Prüfling.
                    </p>
                </div>

                <div class="card">
                    <h2>4. Parameter</h2>
                    <div class="form-group">
                        <select id="select-input">
                            <option value="text">Tastatur (Chat)</option>
                            <option value="speech">Sprache (Mikrofon)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <select id="select-difficulty">
                            <option value="standard">Standard</option>
                            <option value="rigoros">Rigoros</option>
                        </select>
                    </div>
                </div>
            </div>

            <div style="text-align: right; margin-top: 1rem;">
                <button class="btn btn-primary" style="padding: 1rem 3rem; font-size: 1.1rem;" onclick="startExamSession()">Simulation starten</button>
            </div>
        </div>

        <div id="view-exam" class="view hidden">
            <div class="simulation-container">
                <div class="sim-header">
                    <div>
                        <span id="badge-canton" style="background:var(--text-primary); color:var(--bg-primary); padding:0.2rem 0.6rem; font-weight:700; margin-right: 0.5rem;">ZH</span>
                        <span id="badge-mode" style="text-transform:uppercase; font-size:0.85rem; letter-spacing:0.05em; font-weight:600;">SIMULATION</span>
                    </div>
                    <div class="timer-badge" id="exam-timer">20:00</div>
                </div>

                <div class="progress-bar-container"><div class="progress-bar" id="exam-progress"></div></div>
                <div class="chat-feed" id="chat-feed-container"></div>

                <div class="input-area">
                    <div class="input-wrapper">
                        <textarea id="user-chat-input" rows="2" placeholder="Argumentation eingeben... (Ctrl+Enter zum Senden)"></textarea>
                        <div id="mic-active-pulse" class="speech-indicator hidden"></div>
                    </div>
                    <div class="control-btns">
                        <button id="btn-toggle-mic" class="btn btn-secondary btn-icon" onclick="toggleSpeech()">🎤</button>
                        <button class="btn btn-primary" onclick="processUserResponse()">Senden</button>
                        <button class="btn btn-secondary" onclick="terminateSessionPrompt()" style="border-color:var(--error); color:var(--error);">Beenden</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="view-feedback" class="view hidden">
            <h1>Auswertung</h1>
            <div class="feedback-grid">
                <div>
                    <div class="grade-box">
                        <div class="metric-title">Gesamtnote</div>
                        <div class="grade-num" id="eval-grade">-</div>
                        <div style="font-weight: 600;" id="eval-result-text">Wird berechnet...</div>
                    </div>
                    <br>
                    <button class="btn btn-primary" style="width: 100%;" onclick="resetToConfig()">Neue Simulation</button>
                </div>
                <div class="card">
                    <div class="metric-card"><div class="metric-title">1. Korrektheit</div><p id="eval-correctness" style="font-size:0.95rem;"></p></div>
                    <div class="metric-card"><div class="metric-title">2. Vernetzung</div><p id="eval-networking" style="font-size:0.95rem;"></p></div>
                    <div class="metric-card"><div class="metric-title">3. Rhetorik & Tempo</div><p id="eval-speed" style="font-size:0.95rem;"></p></div>
                    <div class="metric-card" style="border-bottom:none;"><div class="metric-title">4. Verbesserungsvorschläge</div><p id="eval-suggestions" style="font-size:0.95rem; white-space: pre-line;"></p></div>
                </div>
            </div>
        </div>
    </main>

    <script>
        const cantons = ['AG', 'AI', 'AR', 'BE', 'BL', 'BS', 'FR', 'GE', 'GL', 'GR', 'JU', 'LU', 'NE', 'NW', 'OW', 'SG', 'SH', 'SO', 'SZ', 'TG', 'TI', 'UR', 'VD', 'VS', 'ZG', 'ZH'];
        
        let state = {
            apiKey: '',
            config: { canton: 'ZH', fields: ['Zivilrecht', 'ZPO'], mode: 'solo', inputType: 'text', difficulty: 'standard' },
            session: { active: false, timeLeft: 1200, timerInterval: null, history: [], questionCount: 0, maxQuestions: 4 }
        };

        let speechRecognition = null; let isListening = false;
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechObj = window.SpeechRecognition || window.webkitSpeechRecognition;
            speechRecognition = new SpeechObj();
            speechRecognition.continuous = true; speechRecognition.interimResults = true; speechRecognition.lang = 'de-CH'; 
            speechRecognition.onresult = (e) => {
                let finalTranscript = '';
                for (let i = e.resultIndex; i < e.results.length; ++i) { if (e.results[i].isFinal) finalTranscript += e.results[i][0].transcript; }
                if(finalTranscript) document.getElementById('user-chat-input').value += finalTranscript + ' ';
            };
            speechRecognition.onerror = () => { showToast("Spracherkennungsfehler."); stopListeningMode(); };
        }

        function toggleSpeech() {
            if (!speechRecognition) return showToast("Spracheingabe nicht unterstützt.");
            if (isListening) stopListeningMode();
            else {
                try { speechRecognition.start(); isListening = true; document.getElementById('mic-active-pulse').classList.remove('hidden'); document.getElementById('btn-toggle-mic').style.background = 'var(--accent-light)'; } catch(e){}
            }
        }
        function stopListeningMode() { if (speechRecognition && isListening) { speechRecognition.stop(); isListening = false; document.getElementById('mic-active-pulse').classList.add('hidden'); document.getElementById('btn-toggle-mic').style.background = 'transparent'; } }
        function speak(text) { if ('speechSynthesis' in window) { const u = new SpeechSynthesisUtterance(text.replace(/[*#_]/g, '')); u.lang = 'de-DE'; window.speechSynthesis.speak(u); } }

        window.onload = () => { buildCantonSelector(); loadStateFromLocalStorage(); };
        function showToast(msg) { const t = document.getElementById('toast'); t.innerText = msg; t.classList.remove('hidden'); setTimeout(() => t.classList.add('hidden'), 4000); }
        function switchView(viewId) { document.querySelectorAll('.view').forEach(v => v.classList.add('hidden')); document.getElementById(viewId).classList.remove('hidden'); window.scrollTo(0,0); }

        function buildCantonSelector() {
            const container = document.getElementById('canton-selector');
            cantons.forEach(c => {
                const chip = document.createElement('div');
                chip.className = `canton-chip ${c === state.config.canton ? 'active' : ''}`;
                chip.innerText = c;
                chip.onclick = () => { document.querySelectorAll('.canton-chip').forEach(el => el.classList.remove('active')); chip.classList.add('active'); state.config.canton = c; saveStateToLocalStorage(); };
                container.appendChild(chip);
            });
        }

        function toggleLawField(element, fieldName) {
            const ev = window.event; const checkbox = element.querySelector('input');
            if (ev && ev.target !== checkbox) checkbox.checked = !checkbox.checked;
            if (checkbox.checked) { element.classList.add('active'); if(!state.config.fields.includes(fieldName)) state.config.fields.push(fieldName); } 
            else { element.classList.remove('active'); state.config.fields = state.config.fields.filter(f => f !== fieldName); }
            saveStateToLocalStorage();
        }

        function toggleDuoInfo() { state.config.mode = document.getElementById('select-mode').value; document.getElementById('duo-info').classList.toggle('hidden', state.config.mode !== 'duo'); }

        function handleLogin() {
            const key = document.getElementById('api-key').value.trim();
            if(!key) return showToast("Bitte API-Key eingeben.");
            state.apiKey = key; document.getElementById('status-user-name').innerText = "API Verbunden";
            switchView('view-config'); saveStateToLocalStorage();
        }

        function logout() { state.apiKey = ''; document.getElementById('api-key').value = ''; document.getElementById('status-user-name').innerText = "API nicht verbunden"; saveStateToLocalStorage(); switchView('view-auth'); }

        function saveStateToLocalStorage() { localStorage.setItem('lexai_state', JSON.stringify({ config: state.config, apiKey: state.apiKey })); }
        function loadStateFromLocalStorage() {
            const data = localStorage.getItem('lexai_state');
            if(data) {
                const parsed = JSON.parse(data); state.config = parsed.config;
                if(parsed.apiKey) { state.apiKey = parsed.apiKey; document.getElementById('api-key').value = state.apiKey; document.getElementById('status-user-name').innerText = "API Verbunden"; switchView('view-config'); }
                document.getElementById('select-mode').value = state.config.mode; document.getElementById('select-input').value = state.config.inputType; document.getElementById('select-difficulty').value = state.config.difficulty; toggleDuoInfo();
            }
        }

        function startExamSession() {
            if(!state.apiKey) return switchView('view-auth');
            if(state.config.fields.length === 0) return showToast("Bitte Rechtsgebiet wählen.");
            state.session.active = true; state.session.timeLeft = state.config.difficulty === 'rigoros' ? 900 : 1200; state.session.questionCount = 0; state.session.history = [];
            document.getElementById('badge-canton').innerText = state.config.canton; document.getElementById('chat-feed-container').innerHTML = '';
            switchView('view-exam'); startTimer(); triggerAIQuestionGeneration(true);
        }

        function startTimer() {
            clearInterval(state.session.timerInterval);
            state.session.timerInterval = setInterval(() => {
                state.session.timeLeft--;
                const m = Math.floor(state.session.timeLeft / 60); const s = state.session.timeLeft % 60;
                document.getElementById('exam-timer').innerText = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
                if(state.session.timeLeft <= 0) { clearInterval(state.session.timerInterval); terminateSession(); }
            }, 1000);
        }

        async function triggerAIQuestionGeneration(isFirstQuestion, userText = "") {
            state.session.questionCount++;
            document.getElementById('exam-progress').style.width = `${(state.session.questionCount / state.session.maxQuestions) * 100}%`;
            if (state.session.questionCount > state.session.maxQuestions) return terminateSession();
            appendLoadingIndicator();
            try {
                const response = await callClaudeAPI(userText, isFirstQuestion);
                removeLoadingIndicator();
                appendMessage("Kommission (KI)", response, "commission");
                if(state.config.inputType === 'speech') speak(response);
                state.session.history.push({ role: "assistant", content: response });
            } catch (error) {
                removeLoadingIndicator(); showToast("API Fehler: " + error.message); state.session.questionCount--; 
            }
        }

        async function callClaudeAPI(userText, isFirstQuestion) {
            let roleInstruction = state.config.mode === 'duo' ? "Du simulierst Vorsitzenden UND Mitkandidat (Müller). Mache deutlich wer spricht." : "Du bist der Vorsitzende.";
            const systemPrompt = `Du bist die Prüfungskommission der Schweizer Anwaltsprüfung Kanton ${state.config.canton}.
            Aufgaben:
            - Erfinde realistische Prüfungsfälle basierend auf echten Gerichtsurteilen (Rechtsgebiete: ${state.config.fields.join(', ')}).
            - Prüfe präzise, hake nach. Sprache: Schweizer Hochdeutsch. Modus: ${state.config.mode}. Schwierigkeit: ${state.config.difficulty}.
            - ${roleInstruction}
            ${isFirstQuestion ? "Beginne mit Begrüssung und erstem Sachverhalt." : "Bewerte die Antwort. Stelle dann eine Rückfrage oder wechsle den Fall."}`;

            const messages = state.session.history.map(h => ({ role: h.role, content: h.content }));
            if(userText) messages.push({ role: "user", content: userText });
            else if(isFirstQuestion) messages.push({ role: "user", content: "Ich bin bereit." });

            const payload = { model: 'claude-3-5-sonnet-20241022', max_tokens: 1024, system: systemPrompt, messages: messages };
            
            // Versuch 1: Direkter Fetch (funktioniert wenn CORS-Erweiterung aktiv ist oder auf bestimmten Hosts)
            let response;
            try {
                response = await fetch('https://api.anthropic.com/v1/messages', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'x-api-key': state.apiKey, 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
                    body: JSON.stringify(payload)
                });
            } catch (e) {
                // Versuch 2: Fallback über allOrigins Proxy (Zuverlässiger für GitHub Pages ohne Erweiterung)
                const proxyUrl = 'https://api.allorigins.win/raw?url=';
                response = await fetch(proxyUrl + encodeURIComponent('https://api.anthropic.com/v1/messages'), {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'x-api-key': state.apiKey, 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
                    body: JSON.stringify(payload)
                });
            }

            if (!response.ok) throw new Error(`API Fehler ${response.status}`);
            const data = await response.json(); return data.content[0].text;
        }

        function processUserResponse() {
            const inputEl = document.getElementById('user-chat-input'); const text = inputEl.value.trim();
            if(!text) return; stopListeningMode(); appendMessage("Sie", text, "user"); state.session.history.push({ role: "user", content: text }); inputEl.value = ''; triggerAIQuestionGeneration(false, text);
        }

        document.getElementById('user-chat-input').addEventListener('keydown', (e) => { if (e.ctrlKey && e.key === 'Enter') processUserResponse(); });

        function appendMessage(sender, text, roleClass) {
            const container = document.getElementById('chat-feed-container'); const msgDiv = document.createElement('div'); msgDiv.className = `message msg-${roleClass}`;
            msgDiv.innerHTML = `<div class="message-meta">${sender} • ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div><div class="message-text">${text}</div>`;
            container.appendChild(msgDiv); container.scrollTop = container.scrollHeight;
        }

        function appendLoadingIndicator() {
            const container = document.getElementById('chat-feed-container'); const loader = document.createElement('div'); loader.id = 'ai-loader';
            loader.innerHTML = `<div style="padding:1rem; font-style:italic; color:var(--text-secondary);">KI generiert...</div>`; container.appendChild(loader); container.scrollTop = container.scrollHeight;
        }
        function removeLoadingIndicator() { const loader = document.getElementById('ai-loader'); if(loader) loader.remove(); }

        function terminateSessionPrompt() { if(confirm("Prüfung abbrechen und auswerten?")) terminateSession(); }

        async function terminateSession() {
            clearInterval(state.session.timerInterval); stopListeningMode(); appendLoadingIndicator(); switchView('view-feedback');
            try {
                const evalPrompt = `Werte den Chat aus. JSON Format: {"grade": "X.X", "correctness": "...", "networking": "...", "speed": "...", "suggestions": "..."}. Schweizer Notenskala (1-6). NUR validen JSON zurückgeben.`;
                const response = await callClaudeAPI(evalPrompt, false);
                const cleanJson = response.substring(response.indexOf('{'), response.lastIndexOf('}') + 1); const evalObj = JSON.parse(cleanJson);
                document.getElementById('eval-grade').innerText = evalObj.grade || "-";
                document.getElementById('eval-result-text').innerText = parseFloat(evalObj.grade) >= 4.0 ? "BESTANDEN" : "NICHT BESTANDEN";
                document.getElementById('eval-correctness').innerText = evalObj.correctness || "-"; document.getElementById('eval-networking').innerText = evalObj.networking || "-"; document.getElementById('eval-speed').innerText = evalObj.speed || "-"; document.getElementById('eval-suggestions').innerText = evalObj.suggestions || "-";
            } catch (e) {
                showToast("Auswertungsfehler."); document.getElementById('eval-grade').innerText = "N/A";
            }
            removeLoadingIndicator(); state.session.active = false; saveStateToLocalStorage();
        }
        function resetToConfig() { switchView('view-config'); }
    </script>
</body>
</html>
