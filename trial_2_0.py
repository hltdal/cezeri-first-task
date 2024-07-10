import pandas as pd
import json
import time

with open("files.csv","r") as f:
    data=pd.read_csv(f)

#data.to_json("data.json", orient="records", lines=True)
for i in range(100):
    with open("data.json","a") as file:
        json.dump(data[i:i+1].to_dict(),file)
        file.write("\n")
    #time.sleep(0.5)
file.close()
