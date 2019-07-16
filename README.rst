OZPY
====

Python (2.7+ including 3.X) library for accessing Zimbra SOAP (https://wiki.zimbra.com/wiki/SOAP_API_Reference_Material_Beginning_with_ZCS_8) by using builtin Python library (no dependency required).
Currently this library split into 2 parts: Zmprov and Mailbox.

not all zmprov command(s) has been implemented, because i add them only based on customer/project needs

but you can add your own by extending **OZSoap** which is base of **Zmprov** and **Mailbox**
for example creating new COS (Class Of Service)

.. code-block:: python

	from ozpy.base import OZSoap

	class NewClass(OZSoap):

		def create_cos(self, name):
			body = {"name": [{
			  "_content": name
			}]}
			return self.send("CreateCos", body)

or directly call the soap method (by omitting Request suffix)

.. code-block:: python

	# zmsoap_obj is an instance from class OZSoap

	zmsoap_obj.CreateCos(
		name=[{"_content": "barudong"}]
	)

you can use **zmsoap** to get the parameters in soap body by using **--verbose** and **--json**

.. code-block:: bash

	zmsoap -z CreateCosRequest/name=new_cos  --json --verbose

Examples
--------

fetch all account

.. code-block:: python

	from ozpy.zmprov import Zmprov

	zmprov = Zmprov(
		username="admin@mail.com",
		password="superpassword",
		soapurl="https://192.168.113.75:7071/service/admin/soap"
	)
	print zmprov.gaa()


Sending email

.. code-block:: python

	from ozpy.mailbox import Mailbox

	mbx = Mailbox(
		username="user1@mail.com",
		password="superpassword",
		soapurl="https://192.168.113.75/service/soap"
	)
	mbx.sendMail('admin@mail.com', 'This is subject', 'Email content')
