# coding: utf-8
from httplib import HTTPSConnection
from base64 import b64encode
import json
import os,binascii

# Remote WHM/Cpanel server settings
whm_url = "whm.example.com"
whm_user = "root"
whm_pass = "_insert_password_"

# Local Zimbra server settings
zimbra_url = "zimbra.example.com"

# Temporary password
tmp_pass = binascii.b2a_hex(os.urandom(15))

# Query CPanel API
def http_query(url, port, username, password, querystr):
    conn = HTTPSConnection(url, port)
    conn.request('GET', querystr, headers={'Authorization':'Basic ' + b64encode(username+':'+password).decode('ascii')})
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

###############################################

data = []

# Retrieve list of cpanel accounts
query_str = '/json-api/listaccts'
result = json.loads(http_query(whm_url, 2087, whm_user, whm_pass, query_str))

# Iterate through cpanel accounts
for cp_username in result["acct"]:
    # Cpanel account username
    username = cp_username["user"]  

    # Reset cpanel account password to tmp_pass
    query_str = '/json-api/passwd?user=%s&pass=%s&db_pass_update=0' % (username, tmp_pass)
    http_query(whm_url, 2087, whm_user, whm_pass, query_str)

    # Retrieve list of email domains under cpanel account
    query_str = '/json-api/cpanel?cpanel_jsonapi_user=%s&cpanel_jsonapi_module=Email&cpanel_jsonapi_func=listmaildomains&cpanel_xmlapi_version=2&skipmain=0' % (username)
    result = json.loads(http_query(whm_url, 2087, whm_user, whm_pass, query_str))

    # Iterate through email domains
    for domain in result["cpanelresult"]["data"]:
        try:
                # Retrieve domain's shadow file
                query_str = '/execute/Fileman/get_file_content?dir=/home/%s/etc/%s&file=shadow&charset=utf-8' % (username, domain["domain"])
                shadow_contents = json.loads(http_query(whm_url, 2083, username, tmp_pass, query_str))
                shadow_accounts = shadow_contents["data"]["content"].split('\n')
        except:
                # Specified domain has email accounts defined, so skip
                break

        emails = []
        # Iterate through email accounts under specified domain
        for account in shadow_accounts:
            # Parse shadow file entry for username and password
            shadow_vars = account.split(':')
            if len(shadow_vars)>1:
                email = "%s@%s" % (shadow_vars[0], domain["domain"])
                password = shadow_vars[1]

                emails.append({"email": email, "password": password})

                # Reset email account's password to temp pass
                query_str = '/json-api/cpanel?cpanel_jsonapi_user=%s&cpanel_jsonapi_module=Email&cpanel_jsonapi_func=passwdpop&cpanel_xmlapi_version=2&email=%s&domain=%s&password=%s' % (username, email, domain["domain"], tmp_pass)
                http_query(whm_url, 2087, whm_user, whm_pass, query_str)

        # Append domain and email accounts to data container
        data.append({"domain": domain["domain"], "emails": emails, "shadow": shadow_contents["data"]["content"]})

# Iterate through data container to print all zimbra createdomain strings
for domain in data:
    print "zmprov createDomain %s" % domain["domain"]

# Iterate through data container to print all zimbra createaccount strings (tmp_pass)
for domain in data:
    for email in domain["emails"]:
        print "zmprov createAccount %s '%s'" % (email["email"], tmp_pass)        

print "-------------"

# Iterate through data container to print imapsync strings (tmp_pass)
for domain in data:
    for email in domain["emails"]:
        print "imapsync --buffersize 8192000 --nosyncacls --subscribe --syncinternaldates --host1 %s --user1 %s --password1 %s --ssl1 --port1 993 --host2 %s --user2 %s --password2 %s -ssl2 --port2 993 --noauthmd5" % (whm_url, email["email"], tmp_pass, zimbra_url, email["email"], tmp_pass)       

print "-------------"

# Prompt for user input to continue 
while True:
    user_input = raw_input("Enter 'yes' when mailboxes have been synchronized: ")
    if user_input == 'yes':
        break

# Iterate through data container to restore domain's shadow file and print zimbra sp strings (encrypted pass)
for domain in data:
    for email in domain["emails"]:
        # Restore domain's shadow file
        query_str = '/execute/Fileman/save_file_content?&dir=/home/%s/etc/%s&file=shadow&from_char=utf-8&to_char=utf-8&content="%s"&fallback=0' % (username, domain["domain"], shadow_contents["data"]["content"])
        http_query(whm_url, 2087, whm_user, whm_pass, query_str)    
            
        # Print zmprov reset password  (original, encrypted password)
        print "zmprov sp %s '{crypt}%s'" % (email["email"],  email["password"]) 
