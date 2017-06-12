__author__ = "Imam Omar Mochtar"
__email__ = "iomarmochtar@gmail.com"
__license__ = "GPL V.2"



import requests
import json
from pprint import pprint
from .exceptions import ZLoginFailed, ZConnectionErr, ZCommonErr
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class OZSoap(object):
	"""
	Base SOAP engine
	"""
	token = None
	soapurl = None
	isdebug = False

	username = None
	password = None

	def __init__(self, username=None, password=None, soapurl=None,
		isdebug=False, default_urn="urn:zimbraAdmin", timeout=None, zinstance=None):
		"""
		example for soapurl
		admin: https://192.168.113.75:7071/service/admin/soap
		account: https://192.168.113.75/service/soap
		"""

		if not zinstance and None in (username, password, soapurl):
			raise ZCommonErr("You must specified username, password and soapurl or zinstance to initiate object")

		self.isdebug = isdebug
		self.soapurl = soapurl
		self.default_urn = default_urn
		self.timeout = timeout

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
			token = self.token,
			soapurl = self.soapurl,
			isdebug = self.isdebug,
			username = self.username,
			password = self.password,
			default_urn = self.default_urn,
		)

	def setAttrs(self, zinstance):
		"""
		set attribute from zinstance
		"""
		attrs = zinstace.getAttrs()
		for k,v in attrs.iteritems():
			setattr(self, k, v)


	def _login(self, username, password, soap_body=None):
		"""
		Fetch token
		"""
		soapname = "Auth"
		admin_soap_body = {
			"name": [{
				"_content": username
			}],
			"password": [{
				"_content": password
			}]
		}

		body = soap_body if soap_body else admin_soap_body

		result = self.send(soapname, body)

		if not result:
			raise ZLoginFailed("Login Failed")

		self.token = result['authToken'][0]['_content']


	def printMe(self, word, isarray=False):
		"""
		Print verbose to console if isdebug is set true
		"""
		if not self.isdebug:
			return

		if not isarray:
			print word
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
			"Header": {
				"context": {
					"authToken": [{'_content':self.token} if self.token else {}],
					"nosession": {},
					"userAgent": {
						"name": "zmsoap"
					},
					"_jsns": "urn:zimbra"
				}
			},
			"Body": {"%sRequest"%soapname:body},
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

		# balikan sesuai dengan response yang diminta
		self.printMe('\nResponse BEGIN\n')
		self.printMe(body, isarray=True)
		self.printMe('\nResponse END\n')
		return body['%sResponse'%soapname]
