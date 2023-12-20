# snmpwalk -v3 -a sha -A myauthpass -x aes -X myprivpass -l authpriv -u simon 172.18.0.1
from easysnmp import Session

session3 = Session(hostname='172.18.0.1', version=3,
                    security_level="auth_with_privacy", security_username="simon",
                    auth_protocol="SHA", auth_password="myauthpass",
                    privacy_protocol="AES", privacy_password="myprivpass")

print('snmp get:')
print(session3.get('iso.3.6.1.6.3.16.1.2.1.3.1.5.99.111.109.109.49'))

print('snmp walk:')
system_items = session3.walk("1.3.6.1.2.1.1")

for item in system_items:
    print('{oid}.{oid_index} {snmp_type} = {value}'.format(
        oid=item.oid,
        oid_index=item.oid_index,
        snmp_type=item.snmp_type,
        value=item.value)
    )