"""
Quantum-Safe Digital Time Capsule

This project demonstrates post-quantum cryptography using Kyber512 for key encapsulation
and Dilithium2 for digital signatures, combined with AES encryption for a secure time capsule.

Features:
- Generate PQC key pairs (Kyber512 + Dilithium2)
- Create encrypted capsules with time-lock
- Verify signatures and decrypt after unlock date
- CLI interface (capsule_main.py)
- GUI interface (gui_main.py)

Installation:
1. Install Python >= 3.9
2. Install dependencies: pip install -r requirements.txt
   Note: liboqs-python may require additional setup on Windows.
   If installation fails, you may need to install liboqs separately or use WSL.
3. Run CLI: python capsule_main.py
   Run GUI: python gui_main.py

Usage:
- Generate keys first
- Create a capsule with a message and unlock date
- Decrypt only after the unlock date has passed

Run Commands:

# Install dependencies
pip install -r requirements.txt

# Run CLI version
python capsule_main.py

# Run GUI version
python gui_main.py

# Test key generation (CLI)
echo "1" | python capsule_main.py

# Test capsule creation (CLI)
echo -e "2\nHello, future world!\n2035-01-01\n0" | python capsule_main.py

# Test decryption after unlock date (CLI)
echo -e "4\n1\n0" | python capsule_main.py

# Test signature verification (CLI)
echo -e "5\n1\n0" | python capsule_main.py

Security Notes:
- Kyber512 provides quantum-resistant key encapsulation
- Dilithium2 provides quantum-resistant digital signatures
- AES provides fast symmetric encryption
- Time-lock prevents early decryption

Example Run:
✅ PQC Keys generated (Kyber512 + Dilithium2)
🔒 Capsule created successfully (unlock date: 2035-01-01)
⏳ Capsule locked until unlock date
🔓 Decryption Successful — message: "Hello, future world!"
✅ Signature verified and integrity confirmed
"""