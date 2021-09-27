import pandas as pd
import pickle
import json
import requests

def read_json():
    with open("payload.json",encoding = "utf-8") as json_file:
        data = json.load(json_file)
    return data
def main():
    data = read_json()
    print("before pickle file >>>>>>>>>>>>>>>>>>>>>>>")
    print(data)
    with open('project1_index_details.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


    with open('project1_index_details.pickle', 'rb') as handle:
        data1 = pickle.load(handle)

    print(data == data1)
    #with open("payload1.json") as json_file:
    #    json.dump(data1,json_file)
    print("after pickle file >>>>>>>>>>>>>>>>>>>>>>>")
    print(data1)

    payload = pickle.load(open("project1_index_details.pickle", "rb"))
    res = requests.post("http://54.89.143.10:9999/grade_index", json=payload, timeout=600)
    res = res.json()
    print("result>>>>>>>>>>>>>>>>>>>>>>>>>>.")
    print(res)




if __name__ == "__main__":
    main()