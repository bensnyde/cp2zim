cp2zim
======

Seamless Cpanel to Zimbra email migration script.

This script will generate all of the commands necessary for a seemless migration of email accounts from a WHM/Cpanel server to a Zimbra Mail server. The output can then be executed in batch. 

Requires WHM root access. Note, this script will change all Cpanel account passwords. It is recommended that you backup /etc/shadow file prior and restore afterwards. 

Tested on WHM 11.40 and Zimba Community 8.0.5.

1. Backup WHM's /etc/shadow file 
2. Configure cp2zim.py script with WHM (url, user, pass) and Zimbra (url) variables
3. Run script and save the output
4. Restore /etc/shadow file on WHM server
5. Run Zimbra commands on Zimbra server as zimbra user (su - zimbra)
6. Run imapsync commands on a server with imapsync installed (be weary of cphulkd/lfd/etc!)
7. Update DNS records
