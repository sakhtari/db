#!/bin/bash

echo "SNMP Test Skript v0.3 by Sly"
sed -i 's/mibs :/# mibs :/g' /etc/snmp/snmp.conf
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
IP=$1
User="telemetry_prd"
AES_Pass="I3e9JdQVpBtDafVI5rKSBPBGQd4Ieu0_WskKVICOsjrtKjBJR76QdwNSRG6kaarY"
SHA_Pass="vXf7YFj0goWErj4RNn2Ev0yRKEJMThUqKC_cBBabG388w5X0l7NO117gdFKM2Mm3"
oid_list="./oid_list.txt"
TimeStamp=$(date '+%F_%H.%M.%S')

if ping -c 1 $IP &> /dev/null; then
		echo "$IP ist online."
	else
		echo -e "${RED}$IP ist offline.${NC}"
		exit 1
fi
if [ -z "$oid_list" ] || [ ! -f $oid_list ]; then
	echo -e "${RED}oid_list.txt nicht gefunden.${NC}"
	exit 1
else
#	read -p "User     : " User
#	read -sp "AES Passwort : " AES_Pass
#	echo
#	read -sp "SHA Passwort : " SHA_Pass
#	echo
	[[ -e $oid_list ]] && readarray OIDs < $oid_list
	for i in ${!OIDs[@]};
	do
		printf "\rOID: "$(($i+1))"/"${#OIDs[@]}
		echo -n ${OIDs[$i]}";" >> SNMP_Output_"$IP"_"$TimeStamp".csv
		snmpget -v3 -n "" -u $User -l authPriv  -Ov -a SHA -x AES -X "$AES_Pass" -A "$SHA_Pass" -m ./DB-ROCA-MIB.mib $IP ${OIDs[$i]} >> SNMP_Output_"$IP"_"$TimeStamp".csv
	done
fi
echo ""
echo "Bericht würde erzeugt: SNMP_Output_"$IP"_"$TimeStamp".csv"
unset -v User
unset -v AES_Pass
unset -v SHA_Pass
