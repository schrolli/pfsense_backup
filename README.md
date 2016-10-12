This script requests the pf-sense configuration from its web-configurator and saves it in a file on the local filesystem. It could be configured, if old files should be deleted after successful download of the current config. This could be handy if the folder is backed up daily with history, so no excess space is used.

# Installation

This script needs some packages, that are normally not installed:

Install apt-package for Ubuntu or Debian:
```bash
apt-get install python3-requests python3-lxml
```

On other Distributions install them with ``pip``:
```bash
pip3 install requests lxml
```

# Provisions

## SSL-Certificate
The web-configurator of pf-sense will be called on https to avoid the transmission of login-credentials in clear text. To connect over https, a verifiable certificate is needed. By default, pf-sense uses a selfsigned certificate, that could be used with web-browsers, but python-requests needs a certificate that is signed by a CA, that it can check against. Either it is a globally trusted cert (in the cert-chain of your os) or one which is signed from a local CertificateAuthority. A local CA could be created in the pf-sense web-configurator. With this CA, a certificate could be signed.

How this is done is explained in ```CERT.md```.

## Special User for Backups

For security reasons, create a seperate user that has only rights to download backups in ```System -> User Manager -> Users```. Give it a name, e.g. ```backup``` and a strong password. It does not need to be in a group. Save the new user and directly re-edit it. Now an ```Effective Privilege``` could be added. To retrieve backups, the ```WebCfg - Diagnostics: Backup/restore page``` privilege is needed.

# Configuration

This script expects its configuration-file at ```/etc/pfsense_backup/config.json```. You could provide another filepath with the optional argument ```-c```. A default config-file is provided in ```config.json.default```. It uses a slightly adapted version of json: you could use ```//``` and ```/* */``` for comments and commas after the last element in dicts and lists are valid.

## The configuration parameters in details:

#### host
String. Hostname or IP-Address of the pf-sense instance.

#### user
String. Username for login.

#### password
String. Password for the user.

#### dest_dir
String. Absolute Directorypath. Folder in which the downloaded configuration should be saved.

#### file_prefix
String. The filename of the saved files is built from this prefix, a datecode in the format "YYYY-mm-dd_HHMMSS" and the file extension ".xml".

#### ssl_certs
String. Absolute Filepath. Path to the root-certificate to check the server-certificate against. Alternatively, ```ssl_certs``` could be set to ```true``` to use the certificate storage provided by the os.

#### remove_old_files
Boolean. If set to ```true```, old files in the ``dest_dir``-folder, which have ```file_prefix``` as a substring, will be deleted after the new backup is saved.

# Todo

* backup rrd as config-option
* add logging
