import numpy as np

def create_binary_array_file(name: str, n: int, type=np.float32) -> None:
    """
    This function create a binary file of an array with n items
    """
    array = np.arange(n, dtype=type)
    array.tofile(name)

if __name__=='__main__':
    pass
