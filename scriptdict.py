## Sam :)
## Created 10-07-21

## ---- scriptdict.py ----
# 
# Provides dictionary-based access to a database of strings in a CSV file
#
# Requirements:
# - csv file with key/value pairs
#
## --------------------


import requests, csv


## ---------------------
### Dictionary Object
## ---------------------

class ScriptDict():
    def __init__(self, csv):
        self.csv = csv
        self.dict = {}
        self.LoadCSVFile(csv)
    
    def LoadCSVFile(self, filepath):

        with open(filepath, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rowCount = 0;
            for row in reader:
                if len(row) > 2 and rowCount != 0:
                    self.Add(row[0], row[1])
                rowCount += 1

    def Add(self, key, value):
        self.dict.update({key: value})

    def Remove(self, key):
        pass
    
    def Get(self, key):
        result = self.dict.get(key)
        if result:
            return result
        else:
            return "ERROR - No script key found"


if __name__ == "__main__":
    d = ScriptDict("script.csv")
    print(d.Get('SYSTEM_ONREADY'))