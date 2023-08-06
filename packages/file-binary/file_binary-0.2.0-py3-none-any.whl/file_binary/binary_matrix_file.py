import numpy as np

def create_binary_matrix_file(name: str, rows: int, cols: int, type=np.float32) -> None:
    """
    This function create a binary file of a matrix with n rows and m columns
    """
    matrix = np.arange(rows*cols, dtype=type).reshape(rows, cols)
    matrix.tofile(name)

if __name__=='__main__':
    pass
