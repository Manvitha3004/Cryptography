"""
Flask API for Quantum-Safe Digital Time Capsule

Exposes the time capsule functionality via REST API for the React frontend.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

from pqc_module import generate_keys, encapsulate_key, decapsulate_key, sign_data, verify_signature
from aes_module import encrypt_message, decrypt_message
from storage_module import save_keys, load_keys, save_capsule, load_capsule, list_capsules
from utils import is_unlocked, get_current_timestamp, validate_date

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/generate_keys', methods=['POST'])
def api_generate_keys():
    try:
        keys = generate_keys()
        save_keys(keys)
        return jsonify({"success": True, "message": "PQC Keys generated and saved!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/create_capsule', methods=['POST'])
def api_create_capsule():
    data = request.get_json()
    message = data.get('message')
    unlock_date = data.get('unlock_date')

    if not message:
        return jsonify({"success": False, "error": "Message cannot be empty."}), 400

    if not validate_date(unlock_date):
        return jsonify({"success": False, "error": "Invalid date format. Use YYYY-MM-DD."}), 400

    keys = load_keys()
    if not keys:
        return jsonify({"success": False, "error": "No keys found. Please generate keys first."}), 400

    try:
        kem_ct, aes_key = encapsulate_key(keys['kem_public'])
        ciphertext = encrypt_message(message, aes_key)
        timestamp = get_current_timestamp()
        metadata = f"{timestamp}|{unlock_date}|{ciphertext}|{kem_ct}"
        signature = sign_data(metadata, keys['sig_secret'])

        capsule = {
            "timestamp": timestamp,
            "unlock_date": unlock_date,
            "ciphertext": ciphertext,
            "kem_ct": kem_ct,
            "signature": signature
        }

        save_capsule(capsule)
        return jsonify({
            "success": True,
            "message": f"Capsule created successfully (unlock date: {unlock_date})",
            "capsule": capsule
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/capsules', methods=['GET'])
def api_list_capsules():
    try:
        capsules = list_capsules()
        capsule_list = []
        for ts in capsules:
            capsule = load_capsule(ts)
            if capsule:
                status = "unlocked" if is_unlocked(capsule['unlock_date']) else "locked"
                capsule_list.append({
                    "timestamp": ts,
                    "unlock_date": capsule['unlock_date'],
                    "status": status
                })
        return jsonify({"success": True, "capsules": capsule_list})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/decrypt_capsule', methods=['POST'])
def api_decrypt_capsule():
    data = request.get_json()
    capsule_index = data.get('capsule_index')

    if capsule_index is None or not isinstance(capsule_index, int):
        return jsonify({"success": False, "error": "Invalid capsule index."}), 400

    capsules = list_capsules()
    if capsule_index < 0 or capsule_index >= len(capsules):
        return jsonify({"success": False, "error": "Capsule index out of range."}), 400

    timestamp = capsules[capsule_index]
    capsule = load_capsule(timestamp)
    keys = load_keys()

    if not capsule or not keys:
        return jsonify({"success": False, "error": "Capsule or keys not found."}), 400

    if not is_unlocked(capsule['unlock_date']):
        return jsonify({"success": False, "error": f"Capsule locked until {capsule['unlock_date']}"}), 400

    metadata = f"{capsule['timestamp']}|{capsule['unlock_date']}|{capsule['ciphertext']}|{capsule['kem_ct']}"
    if not verify_signature(metadata, capsule['signature'], keys['sig_public']):
        return jsonify({"success": False, "error": "Signature verification failed! Capsule may be tampered."}), 400

    try:
        aes_key = decapsulate_key(keys['kem_secret'], capsule['kem_ct'])
        message = decrypt_message(capsule['ciphertext'], aes_key)
        return jsonify({
            "success": True,
            "message": "Decryption Successful!",
            "decrypted_message": message,
            "signature_verified": True
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/verify_capsule', methods=['POST'])
def api_verify_capsule():
    data = request.get_json()
    capsule_index = data.get('capsule_index')

    if capsule_index is None or not isinstance(capsule_index, int):
        return jsonify({"success": False, "error": "Invalid capsule index."}), 400

    capsules = list_capsules()
    if capsule_index < 0 or capsule_index >= len(capsules):
        return jsonify({"success": False, "error": "Capsule index out of range."}), 400

    timestamp = capsules[capsule_index]
    capsule = load_capsule(timestamp)
    keys = load_keys()

    if not capsule or not keys:
        return jsonify({"success": False, "error": "Capsule or keys not found."}), 400

    metadata = f"{capsule['timestamp']}|{capsule['unlock_date']}|{capsule['ciphertext']}|{capsule['kem_ct']}"
    verified = verify_signature(metadata, capsule['signature'], keys['sig_public'])

    return jsonify({
        "success": True,
        "verified": verified,
        "message": "Signature verified - capsule is authentic" if verified else "Signature verification failed - capsule may be tampered"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)