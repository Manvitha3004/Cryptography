# Safe Digital Time Capsule

A **post-quantum secure** digital time capsule that lets you encrypt a message (or file) today and ensure it can **only be opened after a specified future date** — even in a world with powerful quantum computers.

Built with NIST-approved **post-quantum cryptography**:
- **Kyber512** – Quantum-resistant key encapsulation (KEM)
- **Dilithium2** – Quantum-resistant digital signatures
- **AES-256-GCM** – Fast and secure symmetric encryption
- **Time-lock puzzle** – Prevents decryption before the unlock date

Multiple interfaces:
- Modern **Web UI** (React + Flask)
- Interactive **CLI**
- Simple **GUI** (Tkinter)

Perfect for long-term secrets, wills, predictions, love letters to your future self, or blockchain-free timestamped messages.

---

### Features

- Fully quantum-resistant encryption & signing
- Enforced time-lock (cannot decrypt early, even with private keys)
- Sign & verify message authenticity
- Store text or files
- Three ways to interact: Web, GUI, CLI
- No blockchain, no third-party, 100% offline-capable

---

### Installation

#### Prerequisites
- Python ≥ 3.9
- Node.js ≥ 14
- Git

#### 1. Clone the repository
```bash
git clone https://github.com/yourusername/quantum-time-capsule.git
cd quantum-time-capsule
2. Install Python dependencies
Bashpip install -r requirements.txt
Windows users: liboqs-python may require extra steps.
If installation fails → use WSL2 (recommended) or pre-built wheels from https://github.com/open-quantum-safe/liboqs-python
3. Install frontend (React)
Bashcd frontend
npm install
cd ..

Running the Application
Option 1: Web Interface (Recommended)
Bash# Terminal 1 – Start Flask backend
python api.py

# Terminal 2 – Start React frontend
cd frontend && npm start
Then open → http://localhost:3000
Option 2: Desktop GUI
Bashpython gui_main.py
Option 3: Command Line Interface
Bashpython capsule_main.py

Quick CLI Test (Instant Demo)
Bash# 1. Generate keys
echo "1" | python capsule_main.py

# 2. Create a capsule (unlocks on Jan 1, 2035)
echo -e "2\nHello from the past! Quantum computers are here.\n2035-01-01\n0" | python capsule_main.py

# 3. Try to decrypt now → Will fail (too early)
echo -e "4\n1\n0" | python capsule_main.py

# 4. After 2035 → Same command will succeed
# → "Hello from the past! Quantum computers are here."


Component Algorithm Security Level Quantum Resistant?Key ExchangeKyber512~AES-128 equivalentYesDigital SignatureDilithium2EUF-CMA secureYesEncryptionAES-256-GCMVery highNo (but protected by Kyber)Time LockDelay functionConfigurable difficultyYes

Project Structure
text├── api.py                  # Flask backend (REST API)
├── capsule_core.py         # Core crypto logic
├── capsule_main.py         # CLI interface
├── gui_main.py             # Tkinter GUI
├── frontend/               # React web app
├── keys/                   # Generated keys (gitignored)
├── capsules/               # Encrypted capsules (gitignored)
└── requirements.txt

Contributing
Contributions are welcome! Feel free to:

Improve the UI/UX
Add more PQC algorithms (Falcon, SPHINCS+, etc.)
Add file attachment support
Dockerize the app

Just fork → make changes → open a PR

License
MIT License – feel free to use, modify, and distribute
