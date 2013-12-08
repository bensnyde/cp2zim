cp2zim
======

Seemless Cpanel to Zimbra email migration script.

1. SSH to WHM server and backup /etc/shadow file 
2. Configure script with whm (url, user, pass) and zimbra (url) variables
3. Run script and save the output
4. Restore /etc/shadow file on WHM server
5. Run Zimbra commands on Zimbra server as zimbra user
6. Run imapsync commands on a server with imapsync installed (be weary of cphulkd/lfd/etc!)
7. Update DNS records
