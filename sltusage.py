import requests
import json

# API endpoints
API_BASE = "https://omniscapp.slt.lk/mobitelint/slt/api"
API_LOGIN = "/Account/Login"
API_USAGE = "/BBVAS/GetDashboardVASBundles?subscriberID="  # connection no
API_ACCOUNT_DETAILS = '/AccountOMNI/GetAccountDetailRequest?username='
API_SERVICE_DETAILS = '/AccountOMNI/GetServiceDetailRequest?telephoneNo='

API_HEADERS = {
    "X-IBM-Client-Id": "41aed706-8fdf-4b1e-883e-91e44d7f379b",  # hardcoded
    "Content-Type": "application/x-www-form-urlencoded"
}

class SLT:
    def __init__(self, username, password):
        self.username = username
        self.password = password 
        self.token = self.get_token()
        self.subID = self.get_id()
    
    def get_token(self):
        data = {
            "username": self.username, 
            "password": self.password, 
            "channelID": "WEB"
        }
        res = requests.post(API_BASE + API_LOGIN, data = data, headers = API_HEADERS)
        if res.status_code == 200:
            return {'Authorization' : 'bearer ' + res.json()["accessToken"]}
        
    def get_id(self):
        res1 = requests.get(
            API_BASE + API_ACCOUNT_DETAILS + self.username,
            headers = {**API_HEADERS, **self.token}
        )
        if res1.status_code != 200:
            return None
        no = res1.json()['dataBundle'][0]['telephoneno']
        res2 = requests.get(
            API_BASE + API_SERVICE_DETAILS + no,
            headers = {**API_HEADERS, **self.token}
        )
        if res2.status_code != 200:
            return None
        id = res2.json()['dataBundle']['listofBBService'][0]['serviceID']
        return id

    def get_usage(self):
        res = requests.get(
            API_BASE + API_USAGE + self.subID,
            headers = {**API_HEADERS, **self.token}
        )
        if res.status_code == 200:
            return res.json()
        