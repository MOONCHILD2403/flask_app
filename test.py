import requests
base = "http://127.0.0.1:5000/"

response1 = requests.post(base+"register",data={"username":"yashas","password":"pass"}).json()
print(response1)

response2 = requests.post(base+"login",data={"username":"yashas","password":"pass"}).json()
print(response2)

response3 = requests.get(base+"profile",headers={"Authorization":"Bearer "+response2["token"]}).json()
print(response3)

response4 = requests.put(base+"profile",data={"username":"randy","password":"pwd"},headers={"Authorization":"Bearer "+response2["token"]}).json()
print(response4)

response5 = requests.post(base+"analyze",data={"text":"I absolutely love the new features added to the product! They have significantly improved my user experience, and I can’t wait to see what comes next. However, I feel that the customer support could be a bit more responsive. Overall, it's a fantastic product with room for improvement."},headers={"Authorization":"Bearer "+response2["token"]}).json()
print(response5)