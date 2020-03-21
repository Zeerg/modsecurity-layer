# Pull from https://waf.ninja/modsecurity-rules-verification/
import json
import os

# Mod Sec
from ModSecurity import *

def modsec(event, context):

    modsec = ModSecurity()
    rules = Rules()
    rules.load('''SecRuleEngine On
    SecDebugLog /tmp/debug.log
    SecDebugLogLevel 9
    SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:941011,phase:1,pass,nolog,skipAfter:END-REQUEST-941-APPLICATION-ATTACK-XSS"
    SecRule TX:EXECUTING_PARANOIA_LEVEL "@lt 1" "id:941012,phase:2,pass,nolog,skipAfter:END-REQUEST-941-APPLICATION-ATTACK-XSS"
    SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/|REQUEST_COOKIES_NAMES|REQUEST_HEADERS:User-Agent|REQUEST_HEADERS:Referer|ARGS_NAMES|ARGS|XML:/* "@rx (?i)[<＜]script[^>＞]*[>＞][\s\S]*?" "id:1,phase:2,deny,deny,t:none,status:403"
    ''')
    
    ret = rules.getParserError()
    if ret:
        print('Unable to parse rule: %s' % ret)
    
    transaction = Transaction(modsec, rules, None)
    transaction.processURI("/docs/index.html?a=<script>alert(1)</script>&q=test", "GET", "1.1")
    transaction.processRequestHeaders()
    transaction.processRequestBody()
    intervention = ModSecurityIntervention()
    if transaction.intervention(intervention):
        return 'Blocked'
    else:
        return 'Passed'