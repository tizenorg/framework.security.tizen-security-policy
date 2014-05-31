#!/bin/sh

CERT_ROOT=$1
XML_PATH=$2

if [ -z "$2" ]
then
	echo "usage: `basename $0` certificate_root_path fingerprint_xml_path"
	exit 2
fi

for CATEGORY in platform partner public
do
	if [ -d "$CERT_ROOT/$CATEGORY" ]
	then
		echo
		echo " <<$CATEGORY>>"
		for CERT_PATH in `ls $CERT_ROOT/$CATEGORY/*.pem`
		do
			FINGERPRINT=`/usr/bin/openssl x509 -noout -fingerprint -in $CERT_PATH | cut -d '=' -f 2`
			echo "  ${CERT_PATH##*/}:"
			echo "   $FINGERPRINT"
			#############################################################################################################################
			# Find "<!-- xxxxxxx API -->" and then add the fingerprint into the next line
			#############################################################################################################################
			#            <subject><!-- xxxxxxxxx.pem -->
			#                <subject-match attr="distributor-key-root-fingerprint" func="equal">
			#                    sha-1 XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX
			#                </subject-match>
			#            </subject>
			#############################################################################################################################
			/bin/sed -i "s#<\!-- $CATEGORY API -->.*#&\n            <subject><!-- ${CERT_PATH##*/} -->\n                <subject-match attr=\"distributor-key-root-fingerprint\" func=\"equal\">\n                    sha-1 $FINGERPRINT\n                </subject-match>\n            </subject>#" $XML_PATH
		done
	fi
done
echo
