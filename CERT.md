The web-configurator of pf-sense will be called on https to avoid the transmission of login-credentials in clear text. To connect over https, a verifiable certificate is needed. By default, pf-sense uses a selfsigned certificate, that could be used with web-browsers, but python-requests needs a certificate that is signed by a CA, that it can check against. Either it is a globally trusted cert (in the cert-chain of your os) or one which is signed from a local CertificateAuthority. A local CA could be created in the pf-sense web-configurator. With this CA, a certificate could be signed.

### create the CA
In the web-configurator go to ```System -> Cert Manager``` and click the add-button on the ```CAs```-tab. Give it a good descriptive name, like "my_company_pfsense-ca". Select ```Create an internal Certificate Authority```. Let ```Key length```, ```Digest Algorithm``` and ```Lifetime``` to its defaults. Fill out all the Fields for the distinguished name. You should use the same value for ```Common Name``` as you used for the descriptive name.

### download the public key and install in your browser.

In the List of CAs, export the CA cert with the left ""hand with arrow down"-icon. Save it to the local filesystem and import it to your browser.

### create the certificate

In the ```Certificates```-tab, add a new Entry. Select ```Create an internal Certificate``` as the Method. As before the descriptive name should match the common name of the certificate. Select the correct certificate authority and select ```Server Certificate``` as the certificate type. The defaults for Key length, Digest Algorithm and Lifetime are good. The distinguished name should be filled out with the information from the CA. The ```Common Name``` has to match with the url, you are reaching your pf-sense installation, e.g. ```router.example.com```. If you have some aliases for the router, you can add them at ```Alternative Names``` with the add-button. The common name itself has to be added to the SAN-List if other names are added.

### use the new certificate for the web-configurator

In ```System -> Advanced -> Admin Access```, Select ```HTTPS``` for protocoll and the new created cert in the dropdown-field "SSL Certificate" and hit "save".
