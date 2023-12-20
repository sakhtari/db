from pysnmp.hlapi import *
import pysnmp.hlapi as hlapi

iterator = getCmd(
    SnmpEngine(),
    UsmUserData('simon', 'myauthpass', 'myprivpass',
                authProtocol= hlapi.usmHMACSHAAuthProtocol,
                privProtocol=hlapi.usmAesCfb256Protocol),
    UdpTransportTarget(('172.18.0.1', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('NOTIFICATION-LOG-MIB', '1.3.6.1.2.1.92.1.1.1.0', 0))
)


errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(errorIndication)

elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))