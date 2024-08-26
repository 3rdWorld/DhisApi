import base64
import json
import http.client
import os

class WebAPI:
    def __init__(self, hostAddress, intancePath, userName, password):
        
        self.httpConnection = http.client.HTTPSConnection(hostAddress)

        self.hostAddress    = hostAddress
        self.intancePath    = intancePath
        self.accessToken    = ''
        self.credentials    = f'{base64.b64encode(f"{userName}:{password}".encode('utf-8')).decode("ascii")}'
        self.accessToken    = self.getApiToken()
        
        self.resourceList   = self.getResourceList()
    #################################################################################################

    def doHttpIO(self, httpVerb, relativeURL, headers={}, body=None):
        if 'Authorization' not in headers:
            if self.accessToken != '':
                headers['Authorization'] = f'ApiToken {self.accessToken}'
            else:
                headers['Authorization'] = f'Basic {self.credentials}'

        self.httpConnection.request(httpVerb, f'{self.intancePath}{relativeURL}', headers = headers, body=body)

        return self.httpConnection.getresponse()
    #################################################################################################

    def get(self, relativeURL, headers={}, body=None):
        return self.doHttpIO('GET', relativeURL, headers, body)
    #################################################################################################

    def put(self, relativeURL, headers={}, body=None):
        return self.doHttpIO('PUT', relativeURL, headers, body)
    #################################################################################################

    def post(self, relativeURL, headers={}, body=None):
        return self.doHttpIO('POST', relativeURL, headers, body)
    #################################################################################################

    def getResourceList(self):
        httpResponse = self.get('/api/resources/')

        if(httpResponse.status != 200):
            print(f"{httpResponse.msg} {httpResponse.status}")
            return []
        else:
            return json.loads(httpResponse.read().decode('utf-8'))['resources']
    #################################################################################################
    
    def getApiToken(self):
        if os.path.exists('ApiToken.json'):
            file = open('ApiToken.json')

            data = json.load(file)
            file.close()
            print("CheckPoint :Alpha")
            return data['key']
        else:
            httpResponse = self.post('/api/apiToken/', {'Content-Type': 'application/json'}, "{}")

            if httpResponse.status == 201:
                data = json.loads(httpResponse.read().decode('utf-8'))['response']
                file = open('ApiToken.json', 'w')
                json.dump(data, file)
                file.close()
                return data['key']
            else:
                return ''
    #################################################################################################