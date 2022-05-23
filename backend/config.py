# -----------------------------------------------------------
# File to load config json file 
# !IMPORTANT!: Change the 'pathProject' with the local path 
#
# (C) 2022 Marco Vannoli, Rome, Italy
# email marcovannoli@hotmial.it
# -----------------------------------------------------------

import json

# !IMPORTANT!: Change the 'pathProject' with the local path 
# ----------------------------------------------
pathProject = "D:\\test_tecnico\\test_tecnico"  # local path of project
# ----------------------------------------------

# get data from confi json file
def get_config():
        with open(pathProject+'\\config\\config.json') as config:
                data = json.load(config)
                return data
                
if __name__ == "__main__":    
    data = get_config()