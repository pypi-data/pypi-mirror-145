import numpy as np

def average_file(file: str) -> float:
    """
    This function opens a file and returns its average
    """
    n_items = len(np.fromfile(file, dtype=np.float32))
    file_sum = sum(i for i in np.fromfile(file, dtype=np.float32))
    average = file_sum / n_items
    return average

if __name__=='__main__':
    pass
