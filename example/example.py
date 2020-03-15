import json
import os


def modsec(event, context):
    os.environ['LD_LIBRARY_PATH'] = "/opt/lib"
    from ModSecurity import ModSecurity
    from ModSecurity import Rules
    from ModSecurity import Transaction
    modsec = ModSecurity()
    print(modsec.whoAmI())
    rules = Rules()

    rules.loadFromUri("/opt/lib/basic_rules.conf")
    print(rules.getParserError())

    transaction = Transaction(modsec, rules)
    print(transaction.processURI("http://www.modsecurity.org/test?key1=value1&key2=value2&key3=value3&test=args&test=test", "GET", "2.0"))