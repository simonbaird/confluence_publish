import json
import requests
from requests_kerberos import HTTPKerberosAuth

class ConfluenceSession:
    session = None

    def __init__(self, confluence_url):
        self.confluence_url = confluence_url
        self._login()

        # Usually we just need one session so do this to allow
        # casual use of the singleton pattern
        ConfluenceSession.session = self

    def get(self, url):
        return self.session.get(self._full_url(url))

    def put(self, url, data):
        return self.session.put(self._full_url(url),
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'},
            data = json.dumps(data))

    def _login(self):
        # Auth with kerberos. An auth cookie will be saved in the session.
        self.session = requests.Session()
        response = self.session.get(self._full_url("/step-auth-gss"),
            auth = HTTPKerberosAuth(mutual_authentication='DISABLED'))
        #print(response.text)
        response.raise_for_status()

    def _full_url(self, url):
        return self.confluence_url + url
