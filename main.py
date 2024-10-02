import os
import NosisDataMiner

test = True

path = ""
if test == True: 
    base_path = os.getcwd()
    filenames = os.listdir(os.path.join(base_path, 'test_files'))

data = {}

for filename in filenames:    
    data_miner = NosisDataMiner.NosisDataMiner(os.path.join(base_path, 'test_files', filename))
    data[filename] = data_miner.get_data()



