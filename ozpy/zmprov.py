from .base import OZSoap
from .exceptions import ZLoginFailed, ZConnectionErr, ZCommonErr


class Zmprov(OZSoap):
	"""
	zmprov command line wrapper through soap
	"""

	def gadl(self, exclude=[]):
		"""
		Get all disribution list
		"""
		head = 'GetAllDistributionLists'
		data = {}

		result = self.send(head, data)
		return [x['name'] for x in result['dl'] if x['name'] not in exclude_dist ]

	"""
	# gdlm(distname, searchdata['search'], searchdata['page'])
	def gdlm(self, distname, search, page):


		head = 'GetDistributionList'
		data = {
			"dl": [{
				"by": "name",
				"_content": distname
			}]
		}
		urn = "urn:zimbraAdmin"

		members = []
		result = self.send(head, data, urn)

		try:
			dlmlist = result['dl'][0]['dlm']
			return paginate(dlmlist, '_content', search, page)
			# return [ x['_content'] for x in result['dl'][0]['dlm'] ]
		except:
			return None
	"""

	def rdlm(self, distid, members):
		"""
		Remove distribution list member
		"""

		head = 'RemoveDistributionListMember'

		data = {
			'id': distid,
			'dlm': [{'_content':x} for x in members ]
		}

		return self.send(head, data)

	def adlm(self, distid, members):
		"""
		Add distribution list member
		"""

		head = 'AddDistributionListMember'

		data = {
			'id': distid,
			'dlm': [{'_content':x} for x in members ]
		}

		return self.send(head, data)

	def ra(self, accountid, newname):
		"""
		Rename account
		"""

		data = {
			'id': accountid,
			'newName': newname
		}

		return self.send('RenameAccount', data)

	def ma(self, accountid, attribute, value=None):
		"""
		Modify user attribute(s)
		"""
		data = {
			'id': accountid,
			'a':{'n': attribute, '_content': value}
		}

		# jika tidak ada value berarti akan dihapus
		if not value: del data['a']['_content']

		return self.send('ModifyAccount', data)

	def aaa(self, accountid, newalias):
		"""
		Add account alias
		"""
		data = {
			'id': accountid,
			'alias': newalias
		}

		return self.send('AddAccountAlias', data)

	def raa(self, accountid, alias):
		"""
		Remove account alias
		"""
		data = {
			"id": accountid,
			"alias": alias
		}

		return self.send('RemoveAccountAlias', data)

	def gdlcheck(self, distname):
		"""
		Get distribution list id
		"""

		head = 'GetDistributionList'
		data = {
			"dl": [{
				"by": "name",
				"_content": distname
			}]
		}

		result = self.send(head, data)

		if result:
			return result['dl'][0]['id']

		return False

	def ga(self, account):
		"""
		Get account
		"""

		head = 'GetAccount'
		data = {
			'account': {
				'by': 'name',
				"_content": account
			}
		}

		result = self.send(head, data)

		if result:
			return result['account'][0]['a']

		return False


	def cdl(self, distname):
		"""
		Create distribution list
		"""

		head = 'CreateDistributionList'
		data = {
			'name': distname,
			'a': {
				"n": "zimbraMailStatus",
			}
		}

		result = self.send(head, data)

		if result:
			return True

		return False

	def ddl(self, distname):
		"""
		Delete distribution list
		"""

		# fetch distribution list ID based on dist name
		dlid = self.gdlcheck(distname)

		if not dlid:
			return False

		head = 'DeleteDistributionList'
		data = {
			'id': dlid
		}

		result = self.send(head, data)

		if result:
			return True

		return False

	def ca(self, name, password, attrs=[]):
		"""
		Create account
		"""

		head = "CreateAccount"
		data = {
			"name": name,
			"password": password,
			"a": attrs
		}
		return self.send(head, data)

	def da(self, name):
		"""
		Delete Account
		"""

		acc = self.ga(name)
		if not acc:
			raise ZCommonErr("User {0} not found".format(name))

		zimbraId = None
		for data in acc:
			if data['n'] != 'zimbraId': continue
			zimbraId = data['_content']
			break

		head = "DeleteAccount"
		data = {
			"id": zimbraId
		}

		return self.send(head, data)

	def gac(self, shortd=False):
		"""
		Get All COS
		@shortd: fetch name only
		"""
		result = self.send("GetAllCos")
		if not shortd: return result
		take = []
		for x in result['cos']:
			del x['a']
			take.append( x )
		return take

	def mc(self, cosid, attr, value):
		"""
		Modify COS
		"""

		data = {
			'id': [{
				'_content': cosid
			}],
			'a':{'n': attr, '_content': value}
		}

		return self.send("ModifyCos", data)


	def gc(self, cosid, attrs=None):
		"""
		Get COS based on COS ID
		"""
		params = {
			"cos": {
					"by": "id",
					"_content": cosid
				}
			}
		if attrs:
			params["attrs"] = attrs

		return self.send("GetCos", params)

	def gaa(self, search='', uid=False, limit=0, offset=0):
		"""
		Get All Accouunt
		"""

		head = 'SearchDirectory'
		data = {
			'sortBy': 'name',
			'limit': limit,
			'offset' : offset,
			'sortAscending': 1,
			'attrs' : '',
			# hanya mendapatkan normal account
			"query": "(&(!(zimbraIsSystemAccount=TRUE)))"
		}

		if search:
			data['query'] = 'mail=*{0}*'.format(search)

		members = []

		result = self.send(head, data)

		if not result:
			return []

		if result.has_key('account'):
			for member in result['account']:
				if uid:
					data = {
						'name': member['name'],
						'uid': member['id']
					}
				else:
					data = member['name']

				members.append(data)

		return members

		# untuk prevpage

		# if page * settings.TOTAL_CONTENT_PER_PAGE > settings.TOTAL_CONTENT_PER_PAGE:
		# 	prevpage = False
		# else:
		# 	prevpage = True

		# nextpage = not result['more']

		# if result['searchTotal'] == 0 or len(members) == 0:
		# 	prevpage = True
		# 	nextpage = True

		# return {'members': members, 'nextpage': nextpage, 'prevpage': prevpage }
