import requests
import json


headers = {'content-type': 'application/json'}
points = [[0, 1], [1, 0], [1, 1], [2, 1], [2, 2], [3, 1]]
centroids = [[0, 0], [3,2]]

payload = {"id": "1", "action": "points", "points": points}
r = requests.post("http://localhost:50001/worker/", data=json.dumps(payload), headers=headers)
print r.content

payload = {"id": "1", "action": "centroids", "centroids": centroids}
r = requests.post("http://localhost:50001/worker/", data=json.dumps(payload), headers=headers)
print r.content

payload = {"id": "1", "action": "go"}
r = requests.post("http://localhost:50001/worker/", data=json.dumps(payload), headers=headers)
print r.content