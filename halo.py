from ozpy.zmprov import Zmprov 

zmprov = Zmprov(
    username="zimbra",
    password="tkn94v98Zb",
    soapurl="https://192.168.113.129/service/soap"
)
print( zmprov.gaa() )

