"""
Main CLI for Quantum-Safe Digital Time Capsule

Command-line interface for managing PQC keys and time capsules.
"""

import sys
from datetime import datetime

from pqc_module import generate_keys, encapsulate_key, decapsulate_key, sign_data, verify_signature
from aes_module import generate_aes_key, encrypt_message, decrypt_message
from storage_module import save_keys, load_keys, save_capsule, load_capsule, list_capsules
from utils import is_unlocked, get_current_timestamp, validate_date


def print_menu():
    """Display main menu."""
    print("\n==== Quantum Time Capsule ====")
    print("1. Generate PQC Keys")
    print("2. Create Capsule")
    print("3. View Capsules")
    print("4. Decrypt Capsule")
    print("5. Verify Capsule")
    print("0. Exit")


def generate_keys_option():
    """Generate and save PQC keys."""
    print("🔑 Generating PQC Keys (Kyber512 + Dilithium2)...")
    try:
        keys = generate_keys()
        save_keys(keys)
        print("✅ PQC Keys generated and saved!")
    except Exception as e:
        print(f"❌ Error generating keys: {e}")


def create_capsule_option():
    """Create a new time capsule."""
    keys = load_keys()
    if not keys:
        print("❌ No keys found. Please generate keys first.")
        return
    
    print("📝 Creating new capsule...")
    
    # Get user input
    message = input("Enter message: ").strip()
    if not message:
        print("❌ Message cannot be empty.")
        return
    
    unlock_date = input("Enter unlock date (YYYY-MM-DD): ").strip()
    if not validate_date(unlock_date):
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return
    
    if not is_unlocked(unlock_date):
        print(f"🔒 Capsule will be locked until {unlock_date}")
    else:
        print("⚠️  Warning: Unlock date is in the past or today.")
    
    try:
        # Generate AES key (Kyber shared secret)
        kem_ct, aes_key = encapsulate_key(keys['kem_public'])
        
        # Encrypt message
        ciphertext = encrypt_message(message, aes_key)
        
        # Prepare metadata for signing
        timestamp = get_current_timestamp()
        metadata = f"{timestamp}|{unlock_date}|{ciphertext}|{kem_ct}"
        
        # Sign metadata
        signature = sign_data(metadata, keys['sig_secret'])
        
        # Create capsule
        capsule = {
            "timestamp": timestamp,
            "unlock_date": unlock_date,
            "ciphertext": ciphertext,
            "kem_ct": kem_ct,
            "signature": signature
        }
        
        save_capsule(capsule)
        print(f"🔒 Capsule created successfully (unlock date: {unlock_date})")
        
    except Exception as e:
        print(f"❌ Error creating capsule: {e}")


def view_capsules_option():
    """List all capsules."""
    capsules = list_capsules()
    if not capsules:
        print("📭 No capsules found.")
        return
    
    print("📦 Available Capsules:")
    for i, ts in enumerate(capsules, 1):
        capsule = load_capsule(ts)
        if capsule:
            status = "🔓 Unlocked" if is_unlocked(capsule['unlock_date']) else "🔒 Locked"
            print(f"{i}. {ts} - Unlock: {capsule['unlock_date']} ({status})")


def decrypt_capsule_option():
    """Decrypt a capsule."""
    capsules = list_capsules()
    if not capsules:
        print("📭 No capsules found.")
        return
    
    view_capsules_option()
    
    try:
        choice = int(input("Enter capsule number to decrypt: ")) - 1
        if choice < 0 or choice >= len(capsules):
            print("❌ Invalid choice.")
            return
    except ValueError:
        print("❌ Invalid input.")
        return
    
    timestamp = capsules[choice]
    capsule = load_capsule(timestamp)
    keys = load_keys()
    
    if not capsule or not keys:
        print("❌ Capsule or keys not found.")
        return
    
    # Check unlock date
    if not is_unlocked(capsule['unlock_date']):
        print(f"⏳ Capsule locked until {capsule['unlock_date']}")
        return
    
    # Verify signature
    metadata = f"{capsule['timestamp']}|{capsule['unlock_date']}|{capsule['ciphertext']}|{capsule['kem_ct']}"
    if not verify_signature(metadata, capsule['signature'], keys['sig_public']):
        print("❌ Signature verification failed! Capsule may be tampered.")
        return
    
    try:
        # Decapsulate AES key
        aes_key = decapsulate_key(keys['kem_secret'], capsule['kem_ct'])
        
        # Decrypt message
        message = decrypt_message(capsule['ciphertext'], aes_key)
        
        print("🔓 Decryption Successful!")
        print(f"Message: {message}")
        print("✅ Signature verified (Dilithium2)")
        
    except Exception as e:
        print(f"❌ Error decrypting: {e}")


def verify_capsule_option():
    """Verify a capsule's signature."""
    capsules = list_capsules()
    if not capsules:
        print("📭 No capsules found.")
        return
    
    view_capsules_option()
    
    try:
        choice = int(input("Enter capsule number to verify: ")) - 1
        if choice < 0 or choice >= len(capsules):
            print("❌ Invalid choice.")
            return
    except ValueError:
        print("❌ Invalid input.")
        return
    
    timestamp = capsules[choice]
    capsule = load_capsule(timestamp)
    keys = load_keys()
    
    if not capsule or not keys:
        print("❌ Capsule or keys not found.")
        return
    
    metadata = f"{capsule['timestamp']}|{capsule['unlock_date']}|{capsule['ciphertext']}|{capsule['kem_ct']}"
    if verify_signature(metadata, capsule['signature'], keys['sig_public']):
        print("✅ Signature verified - capsule is authentic")
    else:
        print("❌ Signature verification failed - capsule may be tampered")


def main():
    """Main CLI loop."""
    print("Welcome to Quantum-Safe Digital Time Capsule!")
    
    while True:
        print_menu()
        try:
            choice = input("Choose option: ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                generate_keys_option()
            elif choice == "2":
                create_capsule_option()
            elif choice == "3":
                view_capsules_option()
            elif choice == "4":
                decrypt_capsule_option()
            elif choice == "5":
                verify_capsule_option()
            else:
                print("❌ Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()