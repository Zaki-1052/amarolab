import pickle
import os

def load_pkl(path, filename):
    """
    Load data from a pickle file if it exists, otherwise return None.
    
    Args:
        path (str): Directory path containing the pickle file
        filename (str): Name of the pickle file (with or without .pkl extension)
        
    Returns:
        object: Contents of the pickle file if it exists, None otherwise
        
    Raises:
        FileNotFoundError: If the directory path does not exist
    """
    # Ensure path exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory not found: {path}")
        
    # Ensure filename has .pkl extension
    if not filename.endswith('.pkl'):
        filename += '.pkl'
    
    file_path = os.path.join(path, filename)
    
    # Check if file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    else:
        print(f"Pickle file not found: {file_path}")
        return None
    
def save_pkl(data, path, filename):
    """
    Save data to a pickle file in the specified path.
    Args:
        data: Data to be pickled
        path (str): Directory path to save the pickle file
        filename (str): Name of the pickle file (should end in .pkl)
    Returns:
        str: Path to the saved pickle file
    """
    # Ensure filename has .pkl extension
    if not filename.endswith('.pkl'):
        filename += '.pkl'
        
    # Create directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)
        
    # Full path to save file
    save_path = os.path.join(path, filename)
    
    # Save the pickle file
    with open(save_path, 'wb') as f:
        pickle.dump(data, f)
        
    return save_path