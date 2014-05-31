#!/bin/sh

CERT_ROOT=$1
XML_PATH=$2

if [ -z "$2" ]
then
	echo "usage: `basename $0` certificate_root_path fingerprint_xml_path"
	exit 2
fi

for CATEGORY in developer public partner platform test
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
			# Find "<CertificateDomain name="tizen-xxxxxxx">" and then add the fingerprint into the next line
			#############################################################################################################################
			#        <FingerprintSHA1>XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX:XX</FingerprintSHA1><!-- xxxxxxxxx.pem -->
			#############################################################################################################################
			/bin/sed -i "s#<CertificateDomain name=\"tizen-$CATEGORY\">.*#&\n        <FingerprintSHA1>$FINGERPRINT</FingerprintSHA1><!-- ${CERT_PATH##*/} -->#" $XML_PATH
		done
	fi
done
echo
