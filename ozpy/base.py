__author__ = "Imam Omar Mochtar"
__email__ = "iomarmochtar@gmail.com"
__license__ = "GPL V.2"


import json
import ssl
from pprint import pprint
from .exceptions import ZLoginFailed, ZConnectionErr, ZCommonErr

py3 = False
try:
    from urllib.request import Request, urlopen, HTTPError, urlparse  # Python 3
    py3 = True
except ImportError:
    from urllib2 import Request, urlopen, HTTPError  # Python 2
    from urlparse import urlparse

# for acceptin untrusted certificate
ssl_cntx = ssl.create_default_context()
ssl_cntx.check_hostname = False
ssl_cntx.verify_mode = ssl.CERT_NONE

VERSION = 1.0


class OZInline(object):

    def __init__(self, ozsoap, req_name):
        self.ozsoap = ozsoap
        self.req_name = req_name

    def __call__(self, urn=None, **body):
        return self.ozsoap.send(self.req_name, body=body, urn=urn)


class OZSoap(object):
    """
    Base SOAP engine
    """
    token = None
    soapurl = None
    isdebug = False

    username = None
    password = None

    user_agent = 'OZPY Zimbra API Ver. {}'.format(VERSION)

    def __init__(self, username=None, password=None, soapurl=None,
                 isdebug=False, default_urn='urn:zimbraAdmin', timeout=None, zinstance=None):
        """
        example for soapurl
        admin: https://192.168.113.75:7071/service/admin/soap
        account: https://192.168.113.75/service/soap
        """

        if not zinstance and None in (username, password, soapurl):
            raise ZCommonErr('You must specified username, password and soapurl or zinstance to initiate object')

        self.isdebug = isdebug
        self.soapurl = soapurl
        self.default_urn = default_urn
        self.timeout = timeout
        self.username = username
        self.password = password

        # if zinstance instance exists then set as attrbiute
        if zinstance:
            self.setAttrs(zinstance)
        else:
            self._login(username, password)

    def getAttrs(self):
        """
        return all current object attributes
        """
        return dict(
            token=self.token,
            soapurl=self.soapurl,
            isdebug=self.isdebug,
            username=self.username,
            password=self.password,
            default_urn=self.default_urn,
        )

    def setAttrs(self, zinstance):
        """
        set attribute from zinstance
        """
        attrs = zinstance.getAttrs()
        for k, v in attrs.iteritems():
            setattr(self, k, v)

    def _login(self, username, password, soap_body=None):
        """
        Fetch token
        """
        soapname = 'Auth'
        admin_soap_body = {
            'name': [{
                '_content': username
            }],
            'password': [{
                '_content': password
            }]
        }

        body = soap_body if soap_body else admin_soap_body

        result = self.send(soapname, body)

        if not result:
            raise ZLoginFailed('Login Failed')

        self.token = result['authToken'][0]['_content']

    def printMe(self, word, isarray=False):
        """
        Print verbose to console if isdebug is set true
        """
        if not self.isdebug:
            return

        if not isarray:
            print(word)
        else:
            pprint(word)

    def send(self, soapname, body={}, urn=None):
        """
        Send & recieve soap data as JSON.
        """

        urn = urn if urn else self.default_urn

        # add urn in body
        body['_jsns'] = urn

        sendjson = {
            'Header': {
                'context': {
                    'authToken': [{'_content':self.token} if self.token else {}],
                    'nosession': {},
                    'userAgent': {
                        'name': 'zmsoap'
                    },
                    '_jsns': 'urn:zimbra'
                }
            },
            'Body': {'%sRequest'%soapname: body},
            '_jsns': 'urn:zimbraSoap'
        }

        self.printMe('\nRequest BEGIN\n')
        self.printMe(sendjson, isarray=True)
        self.printMe('\nRequest END\n')

        response = None
        try:
            request = Request(self.soapurl)
            request.add_header('Content-Type', 'application/json')
            request.add_header('User-Agent', self.user_agent)

            payload = json.dumps(sendjson)
            if py3:
                payload = bytes(payload, 'utf-8')
            response = urlopen(request, payload, context=ssl_cntx, timeout=self.timeout)
        except HTTPError as e:
            if hasattr(e, 'fp'):
                response = e.fp
            else:
                raise ZConnectionErr('Connection error: {}'.format(e))

        if not response:
            raise ZConnectionErr('Empty response returned')
        
        result = None
        try:
            result = json.loads(response.read())
        except ValueError as e:
            raise ZConnectionErr('Failed to parse response as json format: {}'.format(e))

        body = result['Body']
        # raise exception if there was an error
        if 'Fault' in body:
            self.printMe('FAULT: {0}'.format(body), True)
            return False
        # raise ZCommonErr("Error was occur, response data: {0}".format(result))

        # return by response as its requested
        self.printMe('\nResponse BEGIN\n')
        self.printMe(body, isarray=True)
        self.printMe('\nResponse END\n')
        return body['%sResponse'%soapname]

    def __getattr__(self, soapname):
        return OZInline(self, soapname)

    def __getitem__(self, soapname):
        return OZInline(self, soapname)
