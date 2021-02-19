import os
def remove_out_files():
    out_path = "out//"
    for filename in os.listdir(out_path):
        file_path = os.path.join(out_path, filename)
        os.remove(file_path)