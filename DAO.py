#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, urllib2, base64, ssl
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom



reload(sys)
sys.setdefaultencoding('utf8')


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def checkresponse(data):
   if data != None:
     response = ElementTree.fromstring(data)
     ele = response[0]
     if len(list(response[0])) > 0:
        ele = response[0][0]
     if ele.tag != 'error':
       return (True,"Accion realizada correctamente...")
     else:
       return (False,"Error: " + ele.text)
   else: return(False,"Error: desconocido")

def sendrequest(method, path, xmlrequest, rest=0, params=None):
  try:
    # Building the WBSVision's Rest URL
    url = 'https://0.0.0.0/resources'
    if rest == 1:
	url = url + str(rest)
    url = url + "/" + urllib2.quote(path)
    #url = url + "/" + path  
    #print url #Uncomment if you want to see url!!!
	
    if params != None:
      url = url + "?" + params

    #if (method == 'GET'):
#	url = url + xmlrequest;

 # Making the request 
    request = urllib2.Request(url)
    if xmlrequest is not None:
	if (method != 'GET'):
	    request.data=xmlrequest
    base64string = base64.encodestring('%s:%s' % ('user', 'passwd')).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)   
    request.add_header('Content-Type','text/xml;charset=UTF-8')
    request.get_method = lambda: method
    #context = ssl._create_unverified_context()
    
    # Obtaning results
    #result = urllib2.urlopen(request, context=context)
    result = urllib2.urlopen(request, context=ctx)
    data = result.read()
    return data
  except urllib2.HTTPError as e:
    print "HTTP Error: " + str(e.code)

