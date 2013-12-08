cp2zim
======

Seamless Cpanel to Zimbra email migration script.

This script will generate all of the commands necessary for a seemless migration of email accounts from a WHM/Cpanel server to a Zimbra Mail server. The output can then be executed in batch. 

Requires WHM root access. 

<b>This script will change all Cpanel account passwords.</b> It is recommended that you backup /etc/shadow and each account's /home/%user%/etc/%domain%/shadow file prior to execution so that you can restore the original passwords afterwards.

Tested on WHM 11.40 and Zimba Community 8.0.5.

1. Backup WHM's /etc/shadow file 
2. Configure cp2zim.py script with WHM (url, user, pass) and Zimbra (url) variables
3. Start script
4. Execute Zimbra commands on Zimbra server as zimbra user (su - zimbra)
5. Execute imapsync commands on a server with imapsync installed (be weary of cphulkd/lfd/etc!)
6. Type "yes" when mailboxes have finished synchronizing
7. Execute remaining Zimbra commands on Zimbra server as zimbra user (su - zimbra)
8. Restore /etc/shadow file on WHM server

