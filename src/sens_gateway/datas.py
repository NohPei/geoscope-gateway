import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import time


class data_collection:
    def __init__(self):

        self.API_ENDPOINT = "https://api.smartcity.kmitl.io/api/v1/collections/"
        self.API_KEY = ""
        self.API_SECRET = ""
        self.HEADERS = {'Authorization': self.API_SECRET}

    def setSecret(self, API_SECRET):
        self.API_SECRET = API_SECRET
        self.HEADERS = {'Authorization': self.API_SECRET}

    def setKey(self, KEY):
        self.API_KEY = KEY

    # This "Retry Function" code base on https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    def session_retry(retries=3,
                      backoff_factor=0.3,
                      status_forcelist=(500, 502, 504),
                      session=None):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def send(self, payload):
        status = 0
        try:
            session = requests.Session()
            session.headers.update(self.HEADERS)
            res = self.session_retry(session=session).post(f'{self.API_ENDPOINT}{self.API_KEY}', headers=self.HEADERS,
                                                           data=json.dumps(payload))
            status = res.status_code
        finally:
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            if status == 200:
                print(f'> Push data: Done. \tstatus: {status} ##{t}')
            else:
                print(f'> Push data: Failed. \tstatus: {status} ##{t}')


def main():
    API_KEY = "sc-739aeac3-b37e-4c57-aaa7-119e400637d8"
    API_SECRET = "eyJkYXRhIjoiOXp5VnFpWFNpOEc0YnBXNWxlRXJWeGlCUk81TG50cVBLU0pOOEh6WmM4cWxYbnQ0SlJGSHRzTm9VUEhmUnN4WWZNYXBpUG96QmNDUTlPQXFJRHVjLXRiTFFwNGx1VVYwRl94UGE3QnUtVVJCS0dXbVdKSVg4OWkzWmNYUjY3elFyVFZOZHBYZENzektPT05RaGJCbW5HY3lydUV0dFEtOUlxcUVrTEhLbGlDMUlRcGRmMUFiR1lvX2hkMGY1VnFsbmRaMmd3dG81YWVTYTRqQXdzZDhRZUtETnp6V1RFTkh4aFdLM05mMnAtamdyLXgxUlBFWVdkb0tWV0EwRDIwZUZJVmhYLVZZZnJUUGtBT3NER1hfamJaQ094enlodE5CZFUzMG94WjZRUHVBcVVMOE1RaXQwT2VJdXlTNmktX0QiLCJrZXkiOiJKam9zYjVuSTU3OHlSdGljMlN5R3VZYUdPZWJjbUxSTXlNcmxvN2R4UWQ3QnFBaU9wdldSTXhDOHA0ZG5DaXg1TDdnc05GSUNQSF9CMXdKZFRZTldnQWFkckdxbkIyQXVoUG0zS2FtTzRRT0t2NHNXbURZMm5oalJZekZ2bEVsbmhOeVRUOVlQOUk0eDZVLVVDNXh1WF9nZ1FSN3cwVnRuM2JaVlRZTUs3bUxDQlY2LUpRR3RUa0dKQy1aYTRTdGdHVGU5UGZwUVY2Uld1c250TklsUVpNTnp4VFI5Y2xQcTc1RGFKTVg2ZHhkblczSG4yRDZKYy1KM0NONkU5UElZV0RSRDdXQk4ycVlaVjF4cl9Ub2RfcVVpT0xPSHl0X2gyRVE5ckR5aGxZd0lFVHFLa0I4QW5GLUhGYTFoSzZ3MVdvYXBZTk5HMTVFS056NjhaR2NmX2c9PSJ9"
    payload = {
        "lng": 0,
        "data": "[0]",
        "uuid": "TEST",
        "lat": 0,
        "ts": 1
    }
    test_datas = data_collection()
    test_datas.setKey(API_KEY)
    test_datas.setSecret(API_SECRET)
    test_datas.send(payload)


if __name__ == '__main__':
    main()
