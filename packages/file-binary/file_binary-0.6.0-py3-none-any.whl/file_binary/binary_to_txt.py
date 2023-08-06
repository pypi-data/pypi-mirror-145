from pathlib import Path
import numpy as np



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