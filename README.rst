OZPY
====

Python library for accessing Zimbra SOAP.
Currently this library split into 2 parts: Zmprov and Mailbox.


Example
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
