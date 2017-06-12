__author__ = "Imam Omar Mochtar"
__email__ = "iomarmochtar@gmail.com"
__license__ = "GPL"

from .base import OZSoap

class Mailbox(OZSoap):
	"""
	managing mailbox soap
	"""

	def __init__(self, *args, **kwargs):

		default_urn = "urn:zimbraAccount"
		super(Mailbox, self).__init__(default_urn=default_urn, *args, **kwargs)


	def _login(self, username, password):
		"""
		Override login method, inject with client soap login body
		"""

		client_soap_body = {
			"account": {
				"by": "name",
				"_content": username
			},
			"password": {
				"_content": password
			}
		}

		return super(Mailbox, self)._login(username, password, client_soap_body)


	def sendMail(self, to, subject, body):
		"""
		Send email request
		"""
		soapname = "SendMsg"
		urn = "urn:zimbraMail"
		body = {
			"m":{
				"e":[
					{
						"t": "t",
						"a": to,
						"add": "0"
					},
				],
				"su":{
					"_content": subject
				},
				"mp":[
					{
						"ct":"text/plain",
						"content":{
							"_content": body
						}
					}
				]
			}
		}
		return self.send(soapname, body, urn)


	def getMailbox(self, query="in:\"inbox\"", offset=0, limit=1, timezone="Asia/Jakarta"):
		"""
		Get mailbox content requests
		"""
		soapname = "Search"
		urn = "urn:zimbraMail"
		body = {
			"sortBy": "dateDesc",
			"tz": {
				"id": timezone
			},
			"locale": {
				"_content": "en_US"
			},
			"offset": offset,
			"limit": limit,
			"query": query,
			"types": "conversation",
			"fetch": 1,
			"html": 1
		}

		return self.send(soapname, body, urn)
