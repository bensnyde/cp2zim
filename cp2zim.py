# coding: utf-8
from httplib import HTTPSConnection
from base64 import b64encode
import json

# Remote WHM/Cpanel server settings
whm_url = "whm.example.com"
whm_user = "root"
whm_pass = "insert_password_here"

# Local Zimbra server settings
zimbra_url = "zimbra.example.com"

# Temporary password
tmp_pass = "insert_strong_random_password_here"

# Cpanel API Caller
def http_query(url, port, username, password, querystr):
    conn = HTTPSConnection(url, port)
    conn.request('GET', querystr, headers={'Authorization':'Basic ' + b64encode(username+':'+password).decode('ascii')})
    response = conn.getresponse()
    data = response.read()
    conn.close()
    return data

###############################################

email_accounts = []
email_domains = []

# Retrieve list of cpanel accounts
query_str = '/json-api/listaccts'
result = json.loads(http_query(whm_url, 2087, whm_user, whm_pass, query_str))

for cp_username in result["acct"]:
    username = cp_username["user"]

    # Reset cpanel account password to tmp_pass
    query_str = '/json-api/passwd?user=%s&pass=%s&db_pass_update=0' % (username, tmp_pass)
    http_query(whm_url, 2087, whm_user, whm_pass, query_str)

    # Retrieve list of email domains under cpanel account
    query_str = '/json-api/cpanel?cpanel_jsonapi_user=%s&cpanel_jsonapi_module=Email&cpanel_jsonapi_func=listmaildomains&cpanel_xmlapi_version=2&skipmain=0' % (username)
    result = json.loads(http_query(whm_url, 2087, whm_user, whm_pass, query_str))

    for domain in result["cpanelresult"]["data"]:
        # Print zmprov createdomain string
        print "zmprov createDomain %s" % domain["domain"]

        try:
                # Retrieve domain's shadow file
                queryStr = '/execute/Fileman/get_file_content?dir=/home/%s/etc/%s&file=shadow&charset=utf-8' % (username, domain["domain"])
                shadow_contents = json.loads(http_query(whm_url, 2083, username, tmp_pass, queryStr))
                shadow_accounts = shadow_contents["data"]["content"].split('\n')
        except:
                # Specified email domain has no shadow file
                break

        for account in shadow_accounts:
            shadow_vars = account.split(':')
            if len(shadow_vars)>1:
                username = shadow_vars[0]
                password = shadow_vars[1]

                # Print zmprov createaccount string
                print "zmprov  createAccount %s userPassword '{crypt}%s' displayName '%s' givenName %s" % (username, password, username, username)

                # Print imapsync string
                print "imapsync --buffersize 8192000 --nosyncacls --subscribe --syncinternaldates --host1 %s --user1 %s --password1 %s --ssl1 --port1 993 --host2 %s --user2 %s --password2 %s -ssl2 --port2 993 --noauthmd5" % (whm_url, username, password, zimbra_url, username, password)
