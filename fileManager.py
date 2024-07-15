import os
import shutil
from typing import Tuple
import pickle
import numpy as np
from Definitions.definition import ExperimentalData


class TXTFileManager:
    def __init__(self, folder: str) -> None:
        self.folder = folder

    def reset_folder(self) -> None:
        if os.path.exists(self.folder):
            shutil.rmtree(self.folder)
            print(f"The existing directory '{self.folder}' has been deleted.")

        os.makedirs(self.folder)
        print(f"The new directory '{self.folder}' has been created")
        print()
    
    def add_data_to_file(self, data: ExperimentalData, fileTXTname: str) -> None:
        file_path = os.path.join(self.folder, fileTXTname)

        try:
            with open(file_path, "wb") as file:
                pickle.dump(data, file)
                print(f"Data has been successfully saved to {file_path}")

        except Exception as e:
            print(f"Error occurred while saving data to {file_path}: {str(e)}")


    def save_data(self, name: str, data: np.ndarray):
        try: 
            np.savetxt(name, data)
            print(f"#####The data {name} is going to be saved.######")
            print(" ")

        except:
            print(f"Problem in save the data {name}.")
  
    def read_txt_file(self, file_path: str) -> ExperimentalData | None:
        try: 
            with open(file_path, 'rb',) as file:
                data: ExperimentalData = pickle.load(file) 
                return data
        
        except Exception as e: 
            print(f"Error occurred while loading data from {file_path}: {str(e)}")
            return None
  
