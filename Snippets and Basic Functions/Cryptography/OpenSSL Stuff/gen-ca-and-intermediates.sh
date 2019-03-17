#!/bin/sh

echo "Please follow instructions during execution of this script"

echo "########## Creating CA ##########"
openssl ecparam -name prime256v1 -genkey -noout -out ca-key.pem
echo "Created CA key..."
openssl req -new -key ca-key.pem -out ca-request.csr -sha256
echo "Created CA CSR..."
openssl req -x509 -sha256 -days 365 -key ca-key.pem -in ca-request.csr -out ca-cert.pem
echo "Created CA Certificate..."

echo "########## Intermediate Node 1 - PC ##########"
openssl ecparam -name prime256v1 -genkey -noout -out pc-key.pem
echo "Created PC key..."
openssl req -new -key pc-key.pem -out pc-request.csr -sha256
echo "Created PC CSR..."
openssl x509 -req -sha256 -days 365 -in pc-request.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out pc-cert.pem
echo "Created PC Certificate..." 

echo "########## Intermediate Node 2 - Gateway ##########"
openssl ecparam -name prime256v1 -genkey -noout -out gw-key.pem
echo "Created GW key..."
openssl req -new -key gw-key.pem -out gw-request.csr -sha256
echo "Created GW CSR..."
openssl x509 -req -sha256 -days 365 -in gw-request.csr -CA ca-cert.pem -CAkey ca-key.pem -CAcreateserial -out gw-cert.pem
echo "Created GW Certificate..."

echo "########## Convert PEM certs to DER format ##########"
openssl x509 -outform der -in ca-cert.pem -out ca-cert.der
openssl x509 -outform der -in pc-cert.pem -out pc-cert.der
openssl x509 -outform der -in gw-cert.pem -out gw-cert.der
echo "Created DER certificates..."

echo "Script executed successfully...check folder for files...Goodbye!"
