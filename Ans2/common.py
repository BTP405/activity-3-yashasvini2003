# common.py
import pickle

def serialize(data):
    """Serialize data to bytes using pickle."""
    return pickle.dumps(data)

def deserialize(data_bytes):
    """Deserialize bytes back to original data using pickle."""
    return pickle.loads(data_bytes)
