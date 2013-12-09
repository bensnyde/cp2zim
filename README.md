cp2zim
======

Seamless Cpanel to Zimbra email migration script.

This script will generate all of the commands necessary for a seemless migration of email accounts from a WHM/Cpanel server to a Zimbra Mail server. The output can then be executed in batch. 

Requires WHM root access. 

<b>This script will temporarily change all Cpanel account passwords.</b> It is recommended that you backup /etc/shadow and each account's /home/%user%/etc/%domain%/shadow file prior to execution so that you can restore the original passwords afterwards.

Tested on WHM 11.40 and Zimba Community 8.0.5.

1. Backup WHM's /etc/shadow file 
2. Configure cp2zim.py script with WHM (url, user, pass) and Zimbra (url) variables
3. Start script
<pre># python cp2zim.py</pre>
4. Execute Zimbra commands on Zimbra server as zimbra user (su - zimbra)
<pre>
zmprov createDomain example.com
zmprov createDomain another.com
...
zmprov createAccount john@example.com fdsaf83432980fASF
zmprov createAccount bill@example.com fdsaf83432980fASF
...
</pre>
5. Execute imapsync commands on a server with imapsync installed (be weary of cphulkd/lfd/etc!)
<pre>
imapsync --buffersize 8192000 --nosyncacls --subscribe --syncinternaldates --host1 whm.example.com --user1 john@example.com --password1 fdsaf83432980fASF --ssl1 --port1 993 --host2 zimbra.example.com --user2 john@example.com --password2 fdsaf83432980fASF -ssl2 --port2 993 --noauthmd5
imapsync --buffersize 8192000 --nosyncacls --subscribe --syncinternaldates --host1 whm.example.com --user1 bill@example.com --password1 fdsaf83432980fASF --ssl1 --port1 993 --host2 zimbra.example.com --user2 bill@example.com --password2 fdsaf83432980fASF -ssl2 --port2 993 --noauthmd5
...
</pre>
6. Type "yes" when mailboxes have finished synchronizing
<pre>
  Enter 'yes' when mailboxes have been synchronized: yes
</pre>
7. Execute remaining Zimbra commands on Zimbra server as zimbra user (su - zimbra)
<pre>
zmprov sp john@example.com '{crypt}$1$YaLAzauW$0qwVVISHblDE3Igx6HDic.'
zmprov sp bill@example.com '{crypt}$1$.bQzN12k$sMCyw4IBMFrTCvkiPBu8H/'
</pre>
8. Restore /etc/shadow file on WHM server
