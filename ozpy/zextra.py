from .base import OZSoap

import requests
import json
from .exceptions import ZLoginFailed, ZConnectionErr, ZCommonErr

class Zextras(OZSoap):

    def zxsend(self, soapname, body={}, urn=None):
        """
        Send & recieve soap data as JSON.
        """

        urn = urn if urn else self.default_urn

        # add urn in body
        body['_jsns'] = urn

        sendjson = {
            "Header": {
                "context": {
                    "authToken": [{'_content': self.token} if self.token else {}],
                    "nosession": {},
                    "userAgent": {
                        "name": "zmsoap"
                    },
                    "_jsns": "urn:zimbra"
                }
            },
            "Body": {"%s" % soapname: body},
            "_jsns": "urn:zimbraSoap"
        }

        self.printMe('\nRequest BEGIN\n')
        self.printMe(sendjson, isarray=True)
        self.printMe('\nRequest END\n')

        kwargs = {'verify': False}
        if self.timeout:
            kwargs['timeout'] = self.timeout

        try:
            result = requests.post(self.soapurl, json.dumps(sendjson), **kwargs).json()
        except requests.exceptions.ConnectionError, e:
            raise ZConnectionErr("Connection error: {0}".format(e))

        body = result['Body']
        # raise exception if there was an error
        if body.has_key('Fault'):
            self.printMe("FAULT: {0}".format(body), True)
            return False
        # raise ZCommonErr("Error was occur, response data: {0}".format(result))

        # return by response as its requested
        self.printMe('\nResponse BEGIN\n')
        self.printMe(body, isarray=True)
        self.printMe('\nResponse END\n')
        return body['response']


    def setConfiguration(self, type, id, paramName, value):

        data = {
            'module': 'ZxConfig',
            'action': 'setConfiguration',
            'type': type,
            'id': id,
            'values': '{"%s":{"value":%s}}"'% (paramName,value)
        }


        return self.zxsend('zextras', body=data)

    def getConfiguration(self, type, account, by = "name"):

        data = {
            'module': 'ZxConfig',
            'action': 'getConfiguration',
            'type': type,
            'by': 'name',
            'val': account,
        }

        return self.zxsend('zextras', body=data)
