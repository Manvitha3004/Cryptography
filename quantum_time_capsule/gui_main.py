"""
GUI Frontend for Quantum-Safe Digital Time Capsule

Tkinter-based graphical interface for the time capsule application.
"""

import tkinter as tk
from tkinter import simpledialog, messagebox

from pqc_module import generate_keys, encapsulate_key, decapsulate_key, sign_data, verify_signature
from aes_module import encrypt_message, decrypt_message
from storage_module import save_keys, load_keys, save_capsule, load_capsule, list_capsules
from utils import is_unlocked, get_current_timestamp, validate_date


class TimeCapsuleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum-Safe Digital Time Capsule")
        self.root.geometry("800x600")

        # Output text area
        self.output_text = tk.Text(root, height=25, width=90, wrap=tk.WORD)
        self.output_text.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        # Buttons
        self.btn_generate = tk.Button(button_frame, text="Generate PQC Keys", command=self.generate_keys, width=20)
        self.btn_generate.grid(row=0, column=0, padx=5, pady=5)

        self.btn_create = tk.Button(button_frame, text="Create Capsule", command=self.create_capsule, width=20)
        self.btn_create.grid(row=0, column=1, padx=5, pady=5)

        self.btn_view = tk.Button(button_frame, text="View Capsules", command=self.view_capsules, width=20)
        self.btn_view.grid(row=1, column=0, padx=5, pady=5)

        self.btn_decrypt = tk.Button(button_frame, text="Decrypt Capsule", command=self.decrypt_capsule, width=20)
        self.btn_decrypt.grid(row=1, column=1, padx=5, pady=5)

        self.btn_verify = tk.Button(button_frame, text="Verify Capsule", command=self.verify_capsule, width=20)
        self.btn_verify.grid(row=2, column=0, padx=5, pady=5)

        self.btn_clear = tk.Button(button_frame, text="Clear Output", command=self.clear_output, width=20)
        self.btn_clear.grid(row=2, column=1, padx=5, pady=5)

        self.btn_exit = tk.Button(button_frame, text="Exit", command=root.quit, width=20, bg='red', fg='white')
        self.btn_exit.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # Initial message
        self.output_text.insert(tk.END, "Welcome to Quantum-Safe Digital Time Capsule!\n")
        self.output_text.insert(tk.END, "Use the buttons above to interact with the application.\n\n")

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)

    def generate_keys(self):
        self.output_text.insert(tk.END, "🔑 Generating PQC Keys (Kyber512 + Dilithium2)...\n")
        try:
            keys = generate_keys()
            save_keys(keys)
            self.output_text.insert(tk.END, "✅ PQC Keys generated and saved!\n\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error generating keys: {e}\n\n")

    def create_capsule(self):
        message = simpledialog.askstring("Create Capsule", "Enter message:")
        if not message:
            self.output_text.insert(tk.END, "❌ Message cannot be empty.\n\n")
            return

        unlock_date = simpledialog.askstring("Create Capsule", "Enter unlock date (YYYY-MM-DD):")
        if not validate_date(unlock_date):
            self.output_text.insert(tk.END, "❌ Invalid date format. Use YYYY-MM-DD.\n\n")
            return

        keys = load_keys()
        if not keys:
            self.output_text.insert(tk.END, "❌ No keys found. Please generate keys first.\n\n")
            return

        if not is_unlocked(unlock_date):
            self.output_text.insert(tk.END, f"🔒 Capsule will be locked until {unlock_date}\n")
        else:
            self.output_text.insert(tk.END, "⚠️ Warning: Unlock date is in the past or today.\n")

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
            self.output_text.insert(tk.END, f"🔒 Capsule created successfully (unlock date: {unlock_date})\n\n")

        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error creating capsule: {e}\n\n")

    def view_capsules(self):
        capsules = list_capsules()
        if not capsules:
            self.output_text.insert(tk.END, "📭 No capsules found.\n\n")
            return

        self.output_text.insert(tk.END, "📦 Available Capsules:\n")
        for i, ts in enumerate(capsules, 1):
            capsule = load_capsule(ts)
            if capsule:
                status = "🔓 Unlocked" if is_unlocked(capsule['unlock_date']) else "🔒 Locked"
                self.output_text.insert(tk.END, f"{i}. {ts} - Unlock: {capsule['unlock_date']} ({status})\n")
        self.output_text.insert(tk.END, "\n")

    def decrypt_capsule(self):
        capsules = list_capsules()
        if not capsules:
            self.output_text.insert(tk.END, "📭 No capsules found.\n\n")
            return

        # Show capsules
        self.view_capsules()

        choice = simpledialog.askinteger("Decrypt Capsule", f"Enter capsule number to decrypt (1-{len(capsules)}):")
        if choice is None or choice < 1 or choice > len(capsules):
            self.output_text.insert(tk.END, "❌ Invalid choice.\n\n")
            return

        timestamp = capsules[choice - 1]
        capsule = load_capsule(timestamp)
        keys = load_keys()

        if not capsule or not keys:
            self.output_text.insert(tk.END, "❌ Capsule or keys not found.\n\n")
            return

        if not is_unlocked(capsule['unlock_date']):
            self.output_text.insert(tk.END, f"⏳ Capsule locked until {capsule['unlock_date']}\n\n")
            return

        metadata = f"{capsule['timestamp']}|{capsule['unlock_date']}|{capsule['ciphertext']}|{capsule['kem_ct']}"
        if not verify_signature(metadata, capsule['signature'], keys['sig_public']):
            self.output_text.insert(tk.END, "❌ Signature verification failed! Capsule may be tampered.\n\n")
            return

        try:
            aes_key = decapsulate_key(keys['kem_secret'], capsule['kem_ct'])
            message = decrypt_message(capsule['ciphertext'], aes_key)
            self.output_text.insert(tk.END, "🔓 Decryption Successful!\n")
            self.output_text.insert(tk.END, f"Message: {message}\n")
            self.output_text.insert(tk.END, "✅ Signature verified (Dilithium2)\n\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"❌ Error decrypting: {e}\n\n")

    def verify_capsule(self):
        capsules = list_capsules()
        if not capsules:
            self.output_text.insert(tk.END, "📭 No capsules found.\n\n")
            return

        # Show capsules
        self.view_capsules()

        choice = simpledialog.askinteger("Verify Capsule", f"Enter capsule number to verify (1-{len(capsules)}):")
        if choice is None or choice < 1 or choice > len(capsules):
            self.output_text.insert(tk.END, "❌ Invalid choice.\n\n")
            return

        timestamp = capsules[choice - 1]
        capsule = load_capsule(timestamp)
        keys = load_keys()

        if not capsule or not keys:
            self.output_text.insert(tk.END, "❌ Capsule or keys not found.\n\n")
            return

        metadata = f"{capsule['timestamp']}|{capsule['unlock_date']}|{capsule['ciphertext']}|{capsule['kem_ct']}"
        if verify_signature(metadata, capsule['signature'], keys['sig_public']):
            self.output_text.insert(tk.END, "✅ Signature verified - capsule is authentic\n\n")
        else:
            self.output_text.insert(tk.END, "❌ Signature verification failed - capsule may be tampered\n\n")


def main():
    root = tk.Tk()
    app = TimeCapsuleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()