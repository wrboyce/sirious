#!/usr/bin/env zsh


# Feel free to change any of these defaults
countryName="UK"
stateOrProvinceName="England"
localityName=""
organizationName="Will Boyce"
organizationalUnitName=""
commonName="Sirious"
emailAddress=""

## Do not edit below here!

mkdir -p ssl
mkdir -p demoCA/{certs,crl,newcerts,private}
touch demoCA/index.txt
echo 01 > demoCA/crtnumber

CAREQARGS="${countryName}\n${stateOrProvinceName}\n${localityName}\n${organizationName}\n${organizationalUnitName}\n${commonName}\n${emailAddress}\n\n\n"
echo -n $CAREQARGS | openssl req -new -keyout demoCA/private/cakey.pem -out demoCA/careq.pem -passin pass:1234 -passout pass:1234
openssl ca -create_serial -passin pass:1234 -out ssl/ca.pem -outdir demoCA/newcerts -days 1095 -batch -keyfile demoCA/private/cakey.pem -selfsign -extensions v3_ca -infiles demoCA/careq.pem

CRTREQARGS="${countryName}\n${stateOrProvinceName}\n${localityName}\n${organizationName}\n${organizationalUnitName}\nguzzoni.apple.com\n${emailAddress}\n\n\n"
echo $CRTREQARGS | openssl req -new -keyout demoCA/newkey.pem -out demoCA/newreq.pem -days 1095 -passin pass:1234 -passout pass:1234

openssl ca -policy policy_anything -out ssl/server.crt -passin pass:1234 -keyfile demoCA/private/cakey.pem -cert ssl/ca.pem -infiles demoCA/newreq.pem
openssl rsa -in demoCA/newkey.pem -out ssl/server.key -passin pass:1234

rm -rf demoCA/
