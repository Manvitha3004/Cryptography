"""
Storage Module for Quantum-Safe Digital Time Capsule

Handles saving and loading keys and capsules using JSON files.
"""

import json
import os
from datetime import datetime


KEYS_FILE = "data/keys/user_keys.json"
CAPSULES_DIR = "data/capsules/"


def save_keys(keys):
    """
    Save PQC keys to file.
    
    Args:
        keys (dict): Keys dictionary from generate_keys()
    """
    os.makedirs(os.path.dirname(KEYS_FILE), exist_ok=True)
    with open(KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)
        f.flush()  # Ensure data is written to disk
        os.fsync(f.fileno())  # Force write to disk


def load_keys():
    """
    Load PQC keys from file.
    
    Returns:
        dict: Keys dictionary or None if file doesn't exist
    """
    if not os.path.exists(KEYS_FILE):
        return None
    try:
        with open(KEYS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading keys: {e}")
        return None


def save_capsule(capsule_data):
    """
    Save capsule data to file.
    
    Args:
        capsule_data (dict): Capsule dictionary
    """
    os.makedirs(CAPSULES_DIR, exist_ok=True)
    timestamp = capsule_data['timestamp']
    filename = f"capsule_{timestamp}.json"
    filepath = os.path.join(CAPSULES_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(capsule_data, f, indent=2, ensure_ascii=False)
        f.flush()  # Ensure data is written to disk
        os.fsync(f.fileno())  # Force write to disk


def load_capsule(timestamp):
    """
    Load capsule data from file.
    
    Args:
        timestamp (str): Capsule timestamp
        
    Returns:
        dict: Capsule data or None if not found
    """
    filename = f"capsule_{timestamp}.json"
    filepath = os.path.join(CAPSULES_DIR, filename)
    
    if not os.path.exists(filepath):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading capsule {timestamp}: {e}")
        return None


def list_capsules():
    """
    List all capsule timestamps.
    
    Returns:
        list: List of timestamps
    """
    if not os.path.exists(CAPSULES_DIR):
        os.makedirs(CAPSULES_DIR, exist_ok=True)
        return []
    
    capsules = []
    try:
        for filename in os.listdir(CAPSULES_DIR):
            if filename.startswith("capsule_") and filename.endswith(".json"):
                timestamp = filename[8:-5]  # Remove "capsule_" and ".json"
                capsules.append(timestamp)
    except OSError as e:
        print(f"Error listing capsules: {e}")
        return []
    
    return sorted(capsules)