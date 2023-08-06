from pathlib import Path
import numpy as np

def create_binary_array_file(name: str, n: int, type=np.float32) -> None:
    """
    This function create a binary file of an array with n items
    """
    array = np.arange(n, dtype=type)
    array.tofile(name)

def create_binary_matrix_file(name: str, rows: int, cols: int, type=np.float32) -> None:
    """
    This function create a binary file of a matrix with n rows and m columns
    """
    matrix = np.arange(rows*cols, dtype=type).reshape(rows, cols)
    matrix.tofile(name)


def average_file(file: str) -> float:
    """
    This function opens a file and returns its average
    """
    n_items = len(np.fromfile(file, dtype=np.float32))
    file_sum = sum(i for i in np.fromfile(file, dtype=np.float32))
    average = file_sum / n_items
    return average



def bin_to_txt(file: str, cols: int) -> None:
    """
    This function create a file txt from a binary file with n columns
    """
    base = Path(file).parent
    file_name = Path(file).stem

    with open(f"./{base}/{file_name}.txt", "w") as txt:
        n = np.fromfile(file, dtype=np.float32)
        for i in range(1,len(n)+1):
            txt.write(f"{str(n[i-1])} ")
            if i%cols == 0:
                txt.write("\n")

if __name__=='__main__':
    pass
