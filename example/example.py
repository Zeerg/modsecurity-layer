# Started from https://waf.ninja/modsecurity-rules-verification/
import json
import os

# Mod Sec
from ModSecurity import *

def modsec(event, context):

    modsec = ModSecurity()
    rules = Rules()
    rules.loadFromUri("/opt/lib/modsec.conf")
    
    ret = rules.getParserError()
    if ret:
        print('Unable to parse rule: %s' % ret)
    
    transaction = Transaction(modsec, rules, None)
    transaction.processURI("/docs/index.html?a=SELECT * FROM", "POST", "2.0")
    transaction.processRequestHeaders()
    transaction.processRequestBody()
    intervention = ModSecurityIntervention()
    if transaction.intervention(intervention):
        return 'Blocked'
    else:
        return 'Passed'