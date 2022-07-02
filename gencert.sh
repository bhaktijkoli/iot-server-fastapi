#! /bin/bash
mkdir -p certs
echo 'basicConstraints=CA:true' > certs/android_options.txt
openssl genrsa -out certs/private.key 2048
openssl req -new -days 3650 -key certs/private.key -out certs/CA.pem
openssl x509 -req -days 3650 -in certs/CA.pem -signkey certs/private.key -extfile ./certs/android_options.txt -out certs/CA.crt
openssl x509 -inform PEM -outform DER -in certs/CA.crt -out certs/CA.der.crt
rm certs/android_options.txt