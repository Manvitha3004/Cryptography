"""
Utils Module for Quantum-Safe Digital Time Capsule

Helper functions for time-lock checks, hashing, and validation.
"""

import datetime
import hashlib


def is_unlocked(unlock_date_str):
    """
    Check if current date is past the unlock date.
    
    Args:
        unlock_date_str (str): Unlock date in YYYY-MM-DD format
        
    Returns:
        bool: True if unlocked
    """
    try:
        unlock_date = datetime.date.fromisoformat(unlock_date_str)
        today = datetime.date.today()
        return today >= unlock_date
    except ValueError:
        return False


def get_current_timestamp():
    """
    Get current timestamp in ISO format.
    
    Returns:
        str: Current timestamp
    """
    return datetime.datetime.now().isoformat().replace(':', '-')


def hash_data(data):
    """
    Hash data using SHA256.
    
    Args:
        data (str): Data to hash
        
    Returns:
        str: Hex digest
    """
    return hashlib.sha256(data.encode()).hexdigest()


def validate_date(date_str):
    """
    Validate date string format.
    
    Args:
        date_str (str): Date in YYYY-MM-DD format
        
    Returns:
        bool: True if valid
    """
    try:
        datetime.date.fromisoformat(date_str)
        return True
    except ValueError:
        return False