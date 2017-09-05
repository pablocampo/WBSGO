#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import urllib
#from WBSVisionHandling import checkResponse, sendRequest
import sys, urllib2, base64, ssl
##import ldap
from xml.etree import ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

reload(sys)
sys.setdefaultencoding('utf8')

if hasattr(ssl, '_create_unverified_context'):
	ssl._create_default_https_context = ssl._create_unverified_context

def sendRequest(method, path, xmlrequest,host, user, passwd, rest=0):
	try:
        # Building the WBSVision's Rest URL
		url = 'https://'+host+'/resources'
		#print path
		if rest == 1:
			url = url + str(rest)
		#url = url + "/" + urllib2.quote(path) 
		url = url + "/" + path  
		print url #Uncomment if you want to see url!!!
		
    # Making the request
		request = urllib2.Request(url)
        

		if xmlrequest is not None:
			request.data=xmlrequest
		
		base64string = base64.encodestring('%s:%s' % (user, passwd)).replace('\n', '')
		request.add_header("Authorization", "Basic %s" % base64string)   
		request.add_header('Content-Type','text/xml;charset=UTF-8')
		request.add_header('Content-Type','application/xml;charset=UTF-8')
		request.add_header('Accept','text/xml;charset=UTF-8')
		request.get_method = lambda: method    
    # Obtaning results
		result = urllib2.urlopen(request)
		data = result.read()
		return data
	except urllib2.HTTPError as e:
		print "HTTP Error: " + str(e.code)

		
def checkResponse(data):
	if data != None:
		response = ET.fromstring(data)
		ele = response[0]
		if len(list(response[0])) > 0:
			ele = response[0][0]
		if ele.tag != 'error':
			return (True,"Accion realizada correctamente...")
		else:
			print ele.tag+"\n"
			return (False,"blaError: POP")
	else: return(False,"Error: desconocido")


def createGroup(groupName, description,branch,host,user,passwd):
	branch = branch.strip()
	#We make request:
	#print "\nBuilding request for "+groupName+"..."
	group_ = Element('group')
	branch_ = SubElement(group_,'branch')
	branch_.text = branch.strip()
	

	commonName_ = SubElement(group_,'commonName')
	commonName_.text = groupName.strip()

	description_ = SubElement(group_,'description')
	description_.text = unicode(description,'utf-8')
	

	xml_request = tostring(group_,'utf-8')

	#We send request:
	print "\n\nCreando grupo "+groupName+" en WBSVision...\n\n"
	print "\n\n"+xml_request+"\n\n"
	message = checkResponse(sendRequest('PUT','group',xml_request,host,user,passwd,1))
	print "\t"+message[1]

#No funciona
def modGroupAddMembers (cn, uid, host, usr, passwd):
        print "Adding members to group  "+cn+":"
        group = Element('group')

        branch_att = SubElement(group,'branch')
        branch_att.text = 'ou=deshabilitados'

        login_att = SubElement(group,'cn')
        login_att.text = cn

        lD_name  = SubElement(group,'members')
        lD_name.text=uid

        gid_ = SubElement(group,'gidNumber')
        gid_.text = '20214'


        xml_request = tostring(group,'utf-8')

        print xml_request
        message = checkResponse(sendRequest('POST', 'group/', xml_request,host, usr, passwd,1))
        print message[1]

	

def ponerDeshabilitacionPorScriptATrue (uid, host, usr, passwd):
        print "Modifying attributes for user "+uid+":"
        user = Element('user')


        atts = SubElement(user,'attributes')
        dPS_ = SubElement(atts,'atribute')
        lD_base64 = SubElement(dPS_,'base64')
        lD_base64.text = 'false'
        lD_name  = SubElement(dPS_,'name')
        lD_name.text="deshabilitacionPorScript"

        lD_name  = SubElement(dPS_,'values')
        lD_name.text="TRUE"

        login_att = SubElement(user,'login')
        login_att.text = uid

        uid_att = SubElement(user,'uid')
        uid_att.text = uid

        branch_att = SubElement(user,'branch')
        branch_att.text = 'S8'

        xml_request = tostring(user,'utf-8')

        print xml_request
        message = checkResponse(sendRequest('POST', 'user/', xml_request,host, usr, passwd,1))
        print message[1]

	
def modUserAddMembership (uid, group, host, usr, passwd):
		branch = []
		if uid.startswith('s'):
			branch = 'ou=S8'
		elif uid.startswith('x'):
			branch = 'ou=X8'
		elif uid.startswith('E'):
			branch = 'ou='+uid[0:5]
		elif uid.startswith('C'):
			branch = 'ou='+uid[0:5]
			
			
		print "Modifying attributes for uid "+uid+":"
		user = Element('user')



		atts = SubElement(user,'attributes')
		dPS_ = SubElement(atts,'atribute')
		lD_base64 = SubElement(dPS_,'base64')
		lD_base64.text = 'false'
		lD_name  = SubElement(dPS_,'name')
		lD_name.text="groupsToAdd"

		lD_name  = SubElement(dPS_,'values')
		lD_name.text=group

		login_att = SubElement(user,'login')
		login_att.text = uid

		uid_att = SubElement(user,'uid')
		uid_att.text = uid

		branch_att = SubElement(user,'branch')
		branch_att.text = branch

		xml_request = tostring(user,'utf-8')

		print xml_request
		message = checkResponse(sendRequest('POST', 'user/', xml_request,host, usr, passwd,1))
		print message[1]

#OLD	
def addUserToGroup (rama, dn, uid, nombre, roleToAddTo, host, user, passwd):
	print "Añadiendo el usuario "+uid+" al rol "+roleToAddTo+".\n"
	request = Element('request')
	usr = SubElement(request,'user')
	usr.set('branch',rama)
	usr.set('dn',dn)
	usr.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(usr,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(usr,'attribute')
	branch.set('name','branch')
	branch.text=rama

	givenName = SubElement(usr,'attribute')
	givenName.set('name','givenName')
	givenName.text=nombre

	roleToAddTo_att = SubElement(usr,'attribute')
	roleToAddTo_att.set('name','groupsToAdd')
	roleToAddTo_att.text=roleToAddTo

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, user, passwd))
	print message[1]
	
	
def notifyPasswordATrue (rama,dn,uid,nombre, host, usr, passwd):
	print "Poniendo notifyPassword a True para el usuario : " +uid+".\n"
	request = Element('request')
	user = SubElement(request,'user')
	user.set('branch',rama)
	user.set('dn',dn)
	user.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(user,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(user,'attribute')
	branch.set('name','branch')
	branch.text=rama

	givenName = SubElement(user,'attribute')
	givenName.set('name','givenName')
	givenName.text=nombre

	notifyPassword = SubElement(user,'attribute')
	notifyPassword.set('name','notifyPassword')
	notifyPassword.text="TRUE"
	
	
	xml_request = tostring(request,'utf-8')
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, usr, passwd))
	print message[1]

def getMemberUsers(branch, host, user, passwd):
	print "\nObteniendo miembros de grupos...\n"
	data = sendRequest('GET', 'group/groups/' + branch, None,host, user, passwd, 1) #get user
	response = ET.fromstring(data)
	members = []
	groups = {}
	#for dp in response[0][1]:
	#	print dp.get('name')
	for child in response[0]: #child.tag is "user"
		#print child[1].text
		#print len(child)
		for p in range (len(child)):
			if child[p].tag == 'cn':
				#print "Group: "+child[p].text
				groupName = child[p].text
			elif child[p].tag == 'members':
				#print "Member: "+child[p].text
				if groupName not in groups:
					groups[groupName] = [child[p].text]
				else:
					groups[groupName].append (child[p].text)
	return groups				
			#print "Rama: "+str(child[p].get('cn'))
		#print keys_
		#uid = properties['uid']
	
	
def getRepositories(host, user, passwd):
	print "\nObteniendo repositorios...\n"
	data = sendRequest('GET', 'repository', None,host, user, passwd, 1) #get user
	response = ET.fromstring(data)
	members = []
	repositories = {}
	#for dp in response[0][1]:
	#	print dp.get('name')
	for child in response[0]: #child.tag is "user"
		#print child[1].text
		#print len(child)
		for p in range (len(child)):
			if child[p].tag == 'cn':
				#print "Repos: "+child[p].text
				reposName = child[p].text
			if child[p].tag == 'ldapFilter':
				#print "Order: "+child[p].text
				ldapFilter =child[p].text
			if child[p].tag == 'order':
				#print "Order: "+child[p].text
				order =child[p].text
				repositories[reposName] = [order,ldapFilter]
	return repositories

			#print "Rama: "+str(child[p].get('cn'))
		#print keys_
		#uid = properties['uid']
	
	
	
def getListeners(host, user, passwd):
	print "\nObteniendo listeners...\n"
	data = sendRequest('GET', 'listener', None,host, user, passwd, 1) #get user
	response = ET.fromstring(data)
	members = []
	listeners = {}
	#for dp in response[0][1]:
	#	print dp.get('name')
	for child in response[0]: #child.tag is "user"
		#print child[1].text
		#print len(child)
		for p in range (len(child)):
			if child[p].tag == 'cn':
				#print "Listener: "+child[p].text
				listenerName = child[p].text
			if child[p].tag == 'branch':
				#print "Branch: "+child[p].text
				branch =child[p].text
				listeners[listenerName] = branch
	return listeners

			#print "Rama: "+str(child[p].get('cn'))
		#print keys_
		#uid = properties['uid']
	
	
def getOneUserApplNuevasStatus(uid, listaAppsStatus, host, user, passwd):
	properties={}
	groups =[]
	roles =[]
	print "\nObteniendo ApplXXXStatus para el usuario "+uid+"...\n"
	data = sendRequest('GET', 'user/' + uid, None,host, user, passwd, 0) #get user
	response = ElementTree.fromstring(data)
	for child in response[0]: #child.tag is "user"
		#print child.tag
		#print len(child)
		for p in range (len(child)):
			properties[child[p].get('name')] = child[p].text
			if child[p].get('name') == 'roles':
				roles.append(child[p].text.strip())
		keys_ = properties.keys()
		#print keys_
		name_at = child[0].get('name') #child[0] is at "attribute" level
		uid = properties['uid']

		listaResultadosStatus=[]
		for app in listaAppsStatus:
			if app in keys_: 
				ApplStatus =  properties[app]
				#print "here"
			else:
				ApplStatus = 'no_rellenado'
			listaResultadosStatus.append(ApplStatus)
			
	return listaResultadosStatus	

def getOneUserApplNuevasPermissions(uid, listaAppsPermissions, host, user, passwd):
	properties={}
	groups =[]
	roles =[]
	print "\nObteniendo ApplXXXXXPermissions para el usuario "+uid+"...\n"
	data = sendRequest('GET', 'user/' + uid, None,host, user, passwd, 0) #get user
	response = ElementTree.fromstring(data)
	for child in response[0]: #child.tag is "user"
		#print child.tag
		#print len(child)
		for p in range (len(child)):
			properties[child[p].get('name')] = child[p].text
			if child[p].get('name') == 'roles':
				roles.append(child[p].text.strip())
		keys_ = properties.keys()
		#print keys_
		name_at = child[0].get('name') #child[0] is at "attribute" level
		uid = properties['uid']

		listaResultadosPermissions=[]
		for app in listaAppsPermissions:
			if app in keys_: 
				ApplPermissions =  properties[app]
				#print "here"
			else:
				ApplPermissions = 'no_rellenado'
			listaResultadosPermissions.append(ApplPermissions)
			
	return listaResultadosPermissions	


def modUserAttributeApplPerms (rama, dn, uid, listaAppsPermissions, nombre, host, user, passwd):
	#Pone los atributos ApplXXXXPermisions con valor 'N/A'
	print "Modificando los atributos ApplXXXPermissions para el usuario "+uid+".\n"
	request = Element('request')
	usr = SubElement(request,'user')
	usr.set('branch',rama)
	usr.set('dn',dn)
	usr.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(usr,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(usr,'attribute')
	branch.set('name','branch')
	branch.text=rama

	givenName = SubElement(usr,'attribute')
	givenName.set('name','givenName')
	givenName.text=nombre

	for app in listaAppsPermissions:

		ApplPermissions_att = SubElement(usr,'attribute')
		ApplPermissions_att.set('name',app)
		ApplPermissions_att.text='N/A'

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, user, passwd))
	print message[1]

def modUserAttributeDelStatusApps (rama, dn, uid, listaAppsStatus, nombre, host, user, passwd):
	#Pone en blanco los atributos ApplXXXXStatus
	print "Modificando los atributos AppXXXStatus para el  usuario "+uid+".\n"
	request = Element('request')
	usr = SubElement(request,'user')
	usr.set('branch',rama)
	usr.set('dn',dn)
	usr.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(usr,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(usr,'attribute')
	branch.set('name','branch')
	branch.text=rama

	givenName = SubElement(usr,'attribute')
	givenName.set('name','givenName')
	givenName.text=nombre

	for app in listaAppsStatus:

		ApplStatus_att = SubElement(usr,'attribute')
		ApplStatus_att.set('name',app)
		ApplStatus_att.text=""

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, user, passwd))
	print message[1]


	
def modUserAttributeNoCambiosEnApps(rama, dn, uid, nombre, 	valueAtt2, host, user, passwd):	
	#Pone en blanco el atributo noCambiosenApps
	print "Modificando NoCambiosEnApps para el  usuario "+uid+".\n"
	request = Element('request')
	usr = SubElement(request,'user')
	usr.set('branch',rama)
	usr.set('dn',dn)
	usr.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(usr,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(usr,'attribute')
	branch.set('name','branch')
	branch.text=rama

	givenName = SubElement(usr,'attribute')
	givenName.set('name','givenName')
	givenName.text=nombre

	NoCambiosEnApps_att = SubElement(usr,'attribute')
	NoCambiosEnApps_att.set('name','noCambiosEnApps')
	NoCambiosEnApps_att.text=valueAtt2

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, user, passwd))
	print message[1]

	
	
	
def getOneUserAppNoCambiosEnApps(uid,host, user, passwd):
	#Devuelve el valor del atributo NoCambiosEnApps 
	properties={}
	groups =[]
	roles =[]
	print "\nObteniendo NoCambiosEnApps para el usuario "+uid+"...\n"
	data = sendRequest('GET', 'user/' + uid, None,host, user, passwd, 0) #get user
	response = ElementTree.fromstring(data)
	for child in response[0]: #child.tag is "user"
		#print child.tag
		#print len(child)
		for p in range (len(child)):
			properties[child[p].get('name')] = child[p].text
			if child[p].get('name') == 'roles':
				roles.append(child[p].text.strip())
		keys_ = properties.keys()
		#print keys_
		name_at = child[0].get('name') #child[0] is at "attribute" level
		uid = properties['uid']

		if 'noCambiosEnApps' in keys_: 
			NoCambiosEnApps =  properties['noCambiosEnApps']
			#print "here"
		else:
			NoCambiosEnApps = 'no_rellenado'

			
	return NoCambiosEnApps	



def getOneUser(uid,host, user, passwd):
	properties={}
	groups =[]
	roles =[]
	print "\nBuscando el usuario "+uid+"...\n"
	data = sendRequest('GET', 'user/' + uid, None,host, user, passwd, 0) #get user
	response = ElementTree.fromstring(data)
	for child in response[0]: #child.tag is "user"
		#print child.tag
		#print len(child)
		for p in range (len(child)):
			properties[child[p].get('name')] = child[p].text
		keys_ = properties.keys()
		#print keys_
		name_at = child[0].get('name') #child[0] is at "attribute" level
		uid = properties['uid']
		if 'primerApellido' in keys_: 
			primerApellido =  properties['primerApellido']
		else: 
			primerApellido = 'no rellenado'
		name_at2 = child[2].get('name')
		if name_at2=="givenName":
			givenName = child[2].text
		else: 
			givenName = 'no rellenado'

		name_at3 = child[3].get('name')
		#if 'puestoTrabajo'	
			
		dn = child.get('dn')
		branch = child.get('branch')

	return branch, dn, givenName	


def addUserToRole (rama, dn, uid, roleToAddTo, host, user, passwd):
	print "Añadiendo el usuario "+uid+" al rol "+roleToAddTo+".\n"
	request = Element('request')
	usr = SubElement(request,'user')
	usr.set('branch',rama)
	usr.set('dn',dn)
	usr.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(usr,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(usr,'attribute')
	branch.set('name','branch')
	branch.text=rama


	roleToAddTo_att = SubElement(usr,'attribute')
	roleToAddTo_att.set('name','roles2Add')
	roleToAddTo_att.text=roleToAddTo

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, user, passwd))
	print message[1]

	
def modifyUserOld (uid, tA, host, usr, passwd):
	print "Modifying user : " +uid+".\n"
	request = Element('request')
	user = SubElement(request,'user')
	#user.set('branch',rama)
	#user.set('dn',dn)
	user.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(user,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	#branch = SubElement(user,'attribute')
	#branch.set('name','branch')
	#branch.text=rama

	#givenName = SubElement(user,'attribute')
	#givenName.set('name','givenName')
	#givenName.text='Darío'

	tipoAlta_ = SubElement(user,'attribute')
	tipoAlta_.set('name','tipoAlta')
	tipoAlta_.text=tA

	
	xml_request = tostring(request,'utf-8')
	
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, usr, passwd))
	print message[1]

def modifyUserNew (uid,host, usr, passwd):
	print "Modifying user : " +uid+".\n"
	#request = Element('request')
	user_ = Element('user')
	#user.set('uid',uid)
	dn_ = SubElement(user_,'dn')
	dn_.text = 'uid=E1465049,ou=personas,ou=E1465,ou=entidades,dc=gid-d,dc=redsys,dc=es'
	gN = SubElement(user_,'givenName')
	gN.text = 'Pepe'
	login_ = SubElement(user_,'login')
	login_.text = 'E1465049'
	#br_ = SubElement(user_,'branch')
	#br_.text = 'E1465'
	
	
	#attr = SubElement(user_,'attributes')
	#uid_ = SubElement(attr,'attribute')
	
	#uid_.set('name','uid')
	#uid_.text=uid


	
	xml_request = tostring(user_,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('POST', 'user/', xml_request, host, usr, passwd,1))
	print message[1]

	
def getQueryMultipleUsers (host, user, passwd):
	request = Element('request')
	limit = SubElement(request,'limit')
	limit.text='1250'
	listAttr1 = SubElement(request,'listAttr')
	listAttr1.text='dn'
	listAttr2 = SubElement(request,'listAttr')
	listAttr2.text='givenname'
	listAttr4 = SubElement(request,'listAttr')
	listAttr4.text='uid'
	##listAttr3 = SubElement(request,'listAttr')
	##listAttr3.text='ultimoLoginTime'
	qFilter = SubElement(request,'queryFilter')
	cQuery = SubElement(qFilter,'conditionsQuery')
	cQuery1 = SubElement(cQuery,'conditionsQuery')
	pData1 = SubElement(cQuery1,'paramData')

	key1 = SubElement(pData1,'key')
	key1.text='ApplODINPermissions'
	type1 = SubElement(pData1,'type')
	type1.text='0'
	value1 = SubElement(pData1,'value')
	value1.text=' '
	
	#cQuery2 = SubElement(cQuery,'conditionsQuery')
	#pData2 = SubElement(cQuery2,'paramData')

	#key2 = SubElement(pData2,'key')
	#key2.text='mail'
	#type2 = SubElement(pData2,'type')
	#type2.text='0'
	#value2 = SubElement(pData2,'value')
	#value2.text='*'
	
	
	typeA = SubElement(cQuery,'type')
	typeA.text='101'
	

	xml_request = tostring(request,'utf-8')
	print xml_request
	return sendRequest('POST', 'user/searchUsers/users/entidades', xml_request, host, user, passwd,1)

	
	
def getQueryMultipleUsersUltimoLogin (host, user, passwd):
	request = Element('request')
	limit = SubElement(request,'limit')
	limit.text='1250'
	#listAttr1 = SubElement(request,'listAttr')
	#listAttr1.text='dn'
	#listAttr2 = SubElement(request,'listAttr')
	#listAttr2.text='givenname'
	listAttr4 = SubElement(request,'listAttr')
	listAttr4.text='uid'
	listAttr3 = SubElement(request,'listAttr')
	listAttr3.text='ultimoLoginTime'
	qFilter = SubElement(request,'queryFilter')
	cQuery = SubElement(qFilter,'conditionsQuery')

	cQuery1 = SubElement(cQuery,'conditionsQuery')
	pData1 = SubElement(cQuery1,'paramData')

	key1 = SubElement(pData1,'key')
	key1.text='ultimoLoginTime'
	type1 = SubElement(pData1,'type')
	type1.text='0'
	value1 = SubElement(pData1,'value')
	value1.text='*'
	
	cQuery2 = SubElement(cQuery,'conditionsQuery')
	pData2 = SubElement(cQuery2,'paramData')

	key2 = SubElement(pData2,'key')
	key2.text='loginDisabled'
	type2 = SubElement(pData2,'type')
	type2.text='0'
	value2 = SubElement(pData2,'value')
	value2.text='FALSE'
	
	
	cQuery3 = SubElement(cQuery,'conditionsQuery')
	pData3 = SubElement(cQuery3,'paramData')

	key3 = SubElement(pData3,'key')
	key3.text='NRBE'
	type3 = SubElement(pData3,'type')
	type3.text='0'
	value3 = SubElement(pData3,'value')
	value3.text='1465'
	
	
	typeA = SubElement(cQuery,'type')
	typeA.text='101'
	

	xml_request = tostring(request,'utf-8')
	print xml_request
	return sendRequest('POST', 'user/searchUsers/users/entidades', xml_request, host, user, passwd,1)

	
	
	
def modUserAttributeDelStatusApps (rama, dn, uid, nombre, attToModifiy, host, user, passwd):
	print "Modificando el Status de los apps para el  usuario "+uid+".\n"
	request = Element('request')
	usr = SubElement(request,'user')
	usr.set('branch',rama)
	usr.set('dn',dn)
	usr.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(usr,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	branch = SubElement(usr,'attribute')
	branch.set('name','branch')
	branch.text=rama

	givenName = SubElement(usr,'attribute')
	givenName.set('name','givenName')
	givenName.text=nombre

	ApplKRONOSStatus_att = SubElement(usr,'attribute')
	ApplKRONOSStatus_att.set('name','ApplKRONOSStatus')
	ApplKRONOSStatus_att.text=attToModifiy

	ApplPdEStatus_att = SubElement(usr,'attribute')
	ApplPdEStatus_att.set('name','ApplPORTALDEEMISIONStatus')
	ApplPdEStatus_att.text=attToModifiy

	ApplGATStatus_att = SubElement(usr,'attribute')
	ApplGATStatus_att.set('name','ApplGATStatus')
	ApplGATStatus_att.text=attToModifiy

	
	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request, host, user, passwd))
	print message[1]


	
###Decision Points

def dpRchApp(name_app,action,host, user, passwd):

	#We make request:
	
	dp = Element('decisionPoint')
	cn = SubElement(dp,'cn')
	cn.text = 'E-1.1.1-RCH-'+name_app
	base64 = SubElement(dp,'base64')
	base64.text ='false'
	
	branch_ = SubElement(dp,'branch')
	branch_.text ='ou=entidades'

	conditionAttributes_ = SubElement(dp,'conditionAttributes')
	conditionAttributes1 = SubElement(conditionAttributes_, 'conditionAttributes')
	
	directoryAtt_ = SubElement(conditionAttributes1, 'directoryAtt')
	directoryAtt_.text = name_app+'Status'
	name_ = SubElement(conditionAttributes1, 'name')
	name_.text = 'null'
	type_ = SubElement(conditionAttributes1, 'type')
	type_.text = 'OR'
	value_ = SubElement(conditionAttributes1, 'value')
	value_.text = 'A\/S'
	
	conditionOperations = SubElement(dp,'conditionOperations')

	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "all_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "update_user_operation"
	value = SubElement(entry,'value')
	value.text = "true"

	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "add_user_operation"
	value = SubElement(entry,'value')
	value.text = "true"

	conditionOperations1 = SubElement(dp,'condition_operations')
	
	entry = SubElement(conditionOperations1,'entry')
	key = SubElement(entry,'key')
	key.text = "all_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	
	entry = SubElement(conditionOperations1,'entry')
	key = SubElement(entry,'key')
	key.text = "update_user_operation"
	value = SubElement(entry,'value')
	value.text = "true"

	entry = SubElement(conditionOperations1,'entry')
	key = SubElement(entry,'key')
	key.text = "add_user_operation"
	value = SubElement(entry,'value')
	value.text = "true"

	
	randomAttributes = SubElement(dp,'randomAttributes')
	randomAttributes1 = SubElement(randomAttributes,'randomAttributes')
	generationType = SubElement(randomAttributes1,'generationType')
	generationType.text = '4'
	name = SubElement(randomAttributes1,'name')
	name.text = name_app+'Permissions'
	value = SubElement(randomAttributes1,'value')
	value.text = 'N/A'

	randomAttributes2 = SubElement(randomAttributes,'randomAttributes')
	generationType = SubElement(randomAttributes2,'generationType')
	generationType.text = '4'
	name = SubElement(randomAttributes2,'name')
	name.text = name_app+'Status'
	value = SubElement(randomAttributes2,'value')
	value.text = ' '

		
	saveInformation = SubElement(dp,'saveInformation')
	saveInformation.text='true'
	type_ = SubElement(dp,'type')
	type_.text = "5"

	xml_request = tostring(dp,'utf-8')
	print xml_request

	#We send request:
	sendRequest(action,'decisionPoint',xml_request,host, user, passwd, 1)



###Repositories
def createRepository(reposName, orderNr, userFilter, host,user,passwd):

	print "Creating "+'cn='+reposName+',ou=repositories,ou=configuration,dc=gid,dc=redsys,dc=es'
	##print "Creating "+'cn='+reposName+',ou=repositories,ou=configuration,dc=gid-d,dc=redsys,dc=es'
	
	repos = Element('repository')
	cn = SubElement(repos, 'cn')
	cn.text = reposName
	name = SubElement(repos, 'dn')
	name.text = 'cn='+reposName+',ou=repositories,ou=configuration,dc=gid,dc=redsys,dc=es'
	##name.text = 'cn='+reposName+',ou=repositories,ou=configuration,dc=gid-d,dc=redsys,dc=es'

	baseDn = SubElement(repos, 'baseDN')
	baseDn.text = "ou=usuarios,o=redsys"

	ip = SubElement(repos, 'ip')
	ip.text = "ldap.redsys.es"
	##ip.text = "edir-d.redsys.es"

	userLDAP = SubElement(repos, 'user')
	userLDAP.text = "cn=LDAPGdI,ou=administradores,o=redsys"
	##userLDAP.text = "cn=A9999001,ou=usuarios,o=redsys"

	ssl = SubElement(repos, 'ssl')
	ssl.text = "true"
	
	
	ldapFilter = SubElement(repos, 'ldapFilter')
	ldapFilter.text = userFilter
	
	#ldapIsNovell = SubElement(repos, 'ldapIsNovell')
	#ldapIsNovell.text = "false"
	
	
	ldapv3groupClasses = SubElement(repos, 'ldapv3groupClasses')
	ldapv3groupClasses.text = "groupOfNames"
	
	
	ldapv3userClasses = SubElement(repos, 'ldapv3userClasses')
	ldapv3userClasses.text = "inetOrgPerson,organizationalPerson,Person"
	
	order = SubElement(repos, 'order')
	order.text = orderNr

	typeL = SubElement(repos, 'type')
	typeL.text = "5"
	
	passRep = SubElement(repos, 'passRep')
	passRep.text = "VpG6SKQl0GM"
	##passRep.text = "u6qtL3Hh"

	passwordEncryption = SubElement(repos, 'passwordEncryption')
	passwordEncryption.text = "1"

	repositoryType = SubElement(repos, 'repositoryType')
	repositoryType.text = "ldap"

	portL = SubElement(repos, 'port')
	portL.text = "636"	

	notModPasswdAD = SubElement(repos, 'msadnotModifyPasswordUpdate')
	notModPasswdAD.text = "true"	
	
	
	
	bdAtts = SubElement(repos, 'bdAttributes')
	bdAtt1 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt1, 'name')
	name_.text = 'uid'
	
	bdAtt2 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt2, 'name')
	name_.text = 'cn'
	
	bdAtt3 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt3, 'name')
	name_.text = 'givenName'
	
	bdAtt4 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt4, 'name')
	name_.text = 'sn'
	
	bdAtt5 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt5, 'name')
	name_.text = 'fullName'
	
	bdAtt19 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt19, 'name')
	name_.text = 'title'
	
	bdAtt6 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt6, 'name')
	name_.text = 'carLicense'
	
	bdAtt7 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt7, 'name')
	name_.text = 'employeeNumber'
	
	bdAtt8 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt8, 'name')
	name_.text = 'employeeType'
	
	bdAtt9 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt9, 'name')
	name_.text = 'company'

	bdAtt20 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt20, 'name')
	name_.text = 'ou'
	
	bdAtt10 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt10, 'name')
	name_.text = 'mail'
	
	bdAtt11 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt11, 'name')
	name_.text = 'passwordAllowChange'
	
	bdAtt12 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt12, 'name')
	name_.text = 'passwordExpirationInterval'
	
	bdAtt13 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt13, 'name')
	name_.text = 'passwordMinimumLength'
	
	bdAtt14 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt14, 'name')
	name_.text = 'passwordRequired'
	
	bdAtt15 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt15, 'name')
	name_.text = 'passwordUniqueRequired'
	
	bdAtt16 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt16, 'name')
	name_.text = 'userPassword'
	
	bdAtt17 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt17, 'name')
	name_.text = 'loginDisabled'
	
	bdAtt18 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt18, 'name')
	name_.text = 'loginTime'
	
	bdAtt19 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt19, 'name')
	name_.text = 'lockedByIntruder'
	
	bdAtt20 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt20, 'name')
	name_.text = 'loginIntruderAttempts'

	bdAtt21 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt21, 'name')
	name_.text = 'SolicitudBaja'

	
	groupAttributes = SubElement(repos, 'groupAttributes')
	gAtt1 = SubElement(groupAttributes, 'groupAttributes')
	nameDA_ = SubElement(gAtt1, 'directoryAtt')
	nameDA_.text = 'cn'
	name_ = SubElement(gAtt1, 'name')
	name_.text = 'cn'
	
	
	userAttributes = SubElement(repos, 'userAttributes')
	uAtt1 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt1, 'directoryAtt')
	nameDA_.text = 'employeeType'
	name_ = SubElement(uAtt1, 'name')
	name_.text = 'employeeType'

	uAtt2 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt2, 'directoryAtt')
	nameDA_.text = 'mailToLDAP'
	name_ = SubElement(uAtt2, 'name')
	name_.text = 'mail'

	uAtt3 = SubElement(userAttributes, 'userAttributes')
	name_ = SubElement(uAtt3, 'name')
	name_.text = 'passwordAllowChange'
	name_ = SubElement(uAtt3, 'value')
	name_.text = 'TRUE'

	uAtt4 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt4, 'directoryAtt')
	nameDA_.text = 'ultimoLoginTime'
	name_ = SubElement(uAtt4, 'name')
	name_.text = 'loginTime'

	uAtt5 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt5, 'directoryAtt')
	nameDA_.text = 'loginDisabled'
	name_ = SubElement(uAtt5, 'name')
	name_.text = 'loginDisabled'

	uAtt6 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt6, 'directoryAtt')
	nameDA_.text = 'sn'
	name_ = SubElement(uAtt6, 'name')
	name_.text = 'sn'

	uAtt7 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt7, 'directoryAtt')
	nameDA_.text = 'ou'
	name_ = SubElement(uAtt7, 'name')
	name_.text = 'ou'

	uAtt8 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt8, 'name')
	nameDA_.text = 'passwordMinimumLength'
	name_ = SubElement(uAtt8, 'value')
	name_.text = '8'

	uAtt9 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt9, 'name')
	nameDA_.text = 'passwordRequired'
	name_ = SubElement(uAtt9, 'value')
	name_.text = 'TRUE'

	uAtt10 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt10, 'name')
	nameDA_.text = 'passwordUniqueRequired'
	name_ = SubElement(uAtt10, 'value')
	name_.text = 'TRUE'

	uAtt11 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt11, 'directoryAtt')
	nameDA_.text = 'password'
	name_ = SubElement(uAtt11, 'name')
	name_.text = 'userPassword'

	uAtt12 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt12, 'directoryAtt')
	nameDA_.text = 'givenName'
	name_ = SubElement(uAtt12, 'name')
	name_.text = 'givenName'

	uAtt13 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt13, 'name')
	nameDA_.text = 'passwordExpirationInterval'
	name_ = SubElement(uAtt13, 'value')
	name_.text = '2592000'

	uAtt14 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt14, 'directoryAtt')
	nameDA_.text = 'title'
	name_ = SubElement(uAtt14, 'name')
	name_.text = 'title'

	uAtt15 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt15, 'directoryAtt')
	nameDA_.text = 'uid'
	name_ = SubElement(uAtt15, 'name')
	name_.text = 'cn'

	uAtt16 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt16, 'directoryAtt')
	nameDA_.text = 'o'
	name_ = SubElement(uAtt16, 'name')
	name_.text = 'company'

	uAtt17 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt17, 'name')
	nameDA_.text = 'fullName'
	name_ = SubElement(uAtt17, 'value')
	name_.text = '[[[givenName]]] [[[sn]]]'

	uAtt18 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt18, 'directoryAtt')
	nameDA_.text = 'employeeNumber'
	name_ = SubElement(uAtt18, 'name')
	name_.text = 'employeeNumber'

	uAtt19 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt19, 'directoryAtt')
	nameDA_.text = 'NRBE'
	name_ = SubElement(uAtt19, 'name')
	name_.text = 'carLicense'

	uAtt20 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt20, 'directoryAtt')
	nameDA_.text = 'lockedByIntruder'
	name_ = SubElement(uAtt20, 'name')
	name_.text = 'lockedByIntruder'

	uAtt21 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt21, 'directoryAtt')
	nameDA_.text = 'loginIntruderAttempts'
	name_ = SubElement(uAtt21, 'name')
	name_.text = 'loginIntruderAttempts'

	uAtt21 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt21, 'directoryAtt')
	nameDA_.text = 'SolicitudBaja'
	name_ = SubElement(uAtt21, 'name')
	name_.text = 'SolicitudBaja'


	
	
	xml_request = tostring(repos,'utf-8')
	print xml_request
	
	message = checkResponse(sendRequest('PUT','repository',xml_request,host,user,passwd,1))

	print "\t"+message[1]
	print "\t"+str(message) 

def getRepository(reposName, host,user,passwd):	
	pass
	
def modifyRepository(reposName, orderNr, userFilter, host,user,passwd):

	print "Modifying "+'cn='+reposName+',ou=repositories,ou=configuration,dc=gid,dc=redsys,dc=es'
	##print "Creating "+'cn='+reposName+',ou=repositories,ou=configuration,dc=gid-d,dc=redsys,dc=es'
	
	repos = Element('repository')
	cn = SubElement(repos, 'cn')
	cn.text = reposName
	name = SubElement(repos, 'dn')
	name.text = 'cn='+reposName+',ou=repositories,ou=configuration,dc=gid,dc=redsys,dc=es'
	##name.text = 'cn='+reposName+',ou=repositories,ou=configuration,dc=gid-d,dc=redsys,dc=es'

	baseDn = SubElement(repos, 'baseDN')
	baseDn.text = "ou=usuarios,o=redsys"

	ip = SubElement(repos, 'ip')
	ip.text = "ldap.redsys.es"
	##ip.text = "edir-d.redsys.es"

	userLDAP = SubElement(repos, 'user')
	userLDAP.text = "cn=LDAPGdI,ou=administradores,o=redsys"
	##userLDAP.text = "cn=A9999001,ou=usuarios,o=redsys"

	ssl = SubElement(repos, 'ssl')
	ssl.text = "true"
	
	
	ldapFilter = SubElement(repos, 'ldapFilter')
	ldapFilter.text = userFilter
	
	ldapIsNovell = SubElement(repos, 'ldapIsNovell')
	ldapIsNovell.text = "false"
	
	ldapv3groupClasses = SubElement(repos, 'ldapv3groupClasses')
	ldapv3groupClasses.text = "groupOfNames"
	
	ldapv3userClasses = SubElement(repos, 'ldapv3userClasses')
	ldapv3userClasses.text = "inetOrgPerson,organizationalPerson,Person"
	
	order = SubElement(repos, 'order')
	order.text = orderNr

	typeL = SubElement(repos, 'type')
	typeL.text = "5"
	
	passRep = SubElement(repos, 'passRep')
	passRep.text = "VpG6SKQl0GM"
	##passRep.text = "u6qtL3Hh"

	passwordEncryption = SubElement(repos, 'passwordEncryption')
	passwordEncryption.text = "1"

	repositoryType = SubElement(repos, 'repositoryType')
	repositoryType.text = "ldap"

	portL = SubElement(repos, 'port')
	portL.text = "636"	

	notModPasswdAD = SubElement(repos, 'msadnotModifyPasswordUpdate')
	notModPasswdAD.text = "true"	
	
	
	
	bdAtts = SubElement(repos, 'bdAttributes')
	bdAtt1 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt1, 'name')
	name_.text = 'uid'
	
	bdAtt2 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt2, 'name')
	name_.text = 'cn'
	
	bdAtt3 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt3, 'name')
	name_.text = 'givenName'
	
	bdAtt4 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt4, 'name')
	name_.text = 'sn'
	
	bdAtt5 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt5, 'name')
	name_.text = 'fullName'
	
	bdAtt19 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt19, 'name')
	name_.text = 'title'
	
	bdAtt6 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt6, 'name')
	name_.text = 'carLicense'
	
	bdAtt7 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt7, 'name')
	name_.text = 'employeeNumber'
	
	bdAtt8 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt8, 'name')
	name_.text = 'employeeType'
	
	bdAtt9 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt9, 'name')
	name_.text = 'company'

	bdAtt20 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt20, 'name')
	name_.text = 'ou'
	
	bdAtt10 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt10, 'name')
	name_.text = 'mail'
	
	bdAtt11 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt11, 'name')
	name_.text = 'passwordAllowChange'
	
	bdAtt12 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt12, 'name')
	name_.text = 'passwordExpirationInterval'
	
	bdAtt13 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt13, 'name')
	name_.text = 'passwordMinimumLength'
	
	bdAtt14 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt14, 'name')
	name_.text = 'passwordRequired'
	
	bdAtt15 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt15, 'name')
	name_.text = 'passwordUniqueRequired'
	
	bdAtt16 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt16, 'name')
	name_.text = 'userPassword'
	
	bdAtt17 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt17, 'name')
	name_.text = 'loginDisabled'
	
	bdAtt18 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt18, 'name')
	name_.text = 'loginTime'
	
	bdAtt19 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt19, 'name')
	name_.text = 'lockedByIntruder'
	
	bdAtt20 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt20, 'name')
	name_.text = 'loginIntruderAttempts'

	bdAtt21 = SubElement(bdAtts, 'bdAttributes')
	name_ = SubElement(bdAtt21, 'name')
	name_.text = 'SolicitudBaja'

	
	groupAttributes = SubElement(repos, 'groupAttributes')
	gAtt1 = SubElement(groupAttributes, 'groupAttributes')
	nameDA_ = SubElement(gAtt1, 'directoryAtt')
	nameDA_.text = 'cn'
	name_ = SubElement(gAtt1, 'name')
	name_.text = 'cn'
	
	
	userAttributes = SubElement(repos, 'userAttributes')
	uAtt1 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt1, 'directoryAtt')
	nameDA_.text = 'employeeType'
	name_ = SubElement(uAtt1, 'name')
	name_.text = 'employeeType'

	uAtt2 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt2, 'directoryAtt')
	nameDA_.text = 'mailToLDAP'
	name_ = SubElement(uAtt2, 'name')
	name_.text = 'mail'

	uAtt3 = SubElement(userAttributes, 'userAttributes')
	name_ = SubElement(uAtt3, 'name')
	name_.text = 'passwordAllowChange'
	name_ = SubElement(uAtt3, 'value')
	name_.text = 'TRUE'

	uAtt4 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt4, 'directoryAtt')
	nameDA_.text = 'ultimoLoginTime'
	name_ = SubElement(uAtt4, 'name')
	name_.text = 'loginTime'

	uAtt5 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt5, 'directoryAtt')
	nameDA_.text = 'loginDisabled'
	name_ = SubElement(uAtt5, 'name')
	name_.text = 'loginDisabled'

	uAtt6 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt6, 'directoryAtt')
	nameDA_.text = 'sn'
	name_ = SubElement(uAtt6, 'name')
	name_.text = 'sn'

	uAtt7 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt7, 'directoryAtt')
	nameDA_.text = 'ou'
	name_ = SubElement(uAtt7, 'name')
	name_.text = 'ou'

	uAtt8 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt8, 'name')
	nameDA_.text = 'passwordMinimumLength'
	name_ = SubElement(uAtt8, 'value')
	name_.text = '8'

	uAtt9 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt9, 'name')
	nameDA_.text = 'passwordRequired'
	name_ = SubElement(uAtt9, 'value')
	name_.text = 'TRUE'

	uAtt10 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt10, 'name')
	nameDA_.text = 'passwordUniqueRequired'
	name_ = SubElement(uAtt10, 'value')
	name_.text = 'TRUE'

	uAtt11 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt11, 'directoryAtt')
	nameDA_.text = 'password'
	name_ = SubElement(uAtt11, 'name')
	name_.text = 'userPassword'

	uAtt12 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt12, 'directoryAtt')
	nameDA_.text = 'givenName'
	name_ = SubElement(uAtt12, 'name')
	name_.text = 'givenName'

	uAtt13 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt13, 'name')
	nameDA_.text = 'passwordExpirationInterval'
	name_ = SubElement(uAtt13, 'value')
	name_.text = '2592000'

	uAtt14 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt14, 'directoryAtt')
	nameDA_.text = 'title'
	name_ = SubElement(uAtt14, 'name')
	name_.text = 'title'

	uAtt15 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt15, 'directoryAtt')
	nameDA_.text = 'uid'
	name_ = SubElement(uAtt15, 'name')
	name_.text = 'cn'

	uAtt16 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt16, 'directoryAtt')
	nameDA_.text = 'o'
	name_ = SubElement(uAtt16, 'name')
	name_.text = 'company'

	uAtt17 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt17, 'name')
	nameDA_.text = 'fullName'
	name_ = SubElement(uAtt17, 'value')
	name_.text = '[[[givenName]]] [[[sn]]]'

	uAtt18 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt18, 'directoryAtt')
	nameDA_.text = 'employeeNumber'
	name_ = SubElement(uAtt18, 'name')
	name_.text = 'employeeNumber'

	uAtt19 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt19, 'directoryAtt')
	nameDA_.text = 'NRBE'
	name_ = SubElement(uAtt19, 'name')
	name_.text = 'carLicense'

	uAtt20 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt20, 'directoryAtt')
	nameDA_.text = 'lockedByIntruder'
	name_ = SubElement(uAtt20, 'name')
	name_.text = 'lockedByIntruder'

	uAtt21 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt21, 'directoryAtt')
	nameDA_.text = 'loginIntruderAttempts'
	name_ = SubElement(uAtt21, 'name')
	name_.text = 'loginIntruderAttempts'

	uAtt21 = SubElement(userAttributes, 'userAttributes')
	nameDA_ = SubElement(uAtt21, 'directoryAtt')
	nameDA_.text = 'SolicitudBaja'
	name_ = SubElement(uAtt21, 'name')
	name_.text = 'SolicitudBaja'

	xml_request = tostring(repos,'utf-8')
	print xml_request
	

	sendRequest('POST','repository',xml_request,host,user,passwd,1)
	#message = checkResponse(sendRequest('POST','repository',xml_request,host,user,passwd,1))

	#print "\t"+message[1]
	#print "\t"+str(message) 

	
def createListener (reposName, branchName, host,user,passwd):

	print "Creating "+'cn='+reposName+',ou=listeners,ou=configuration,dc=gid,dc=redsys,dc=es'
	
	listener = Element('listener')
	cn = SubElement(listener, 'cn')
	cn.text = reposName
	name = SubElement(listener, 'dn')
	name.text = 'cn='+reposName+',ou=listeners,ou=configuration,dc=gid,dc=redsys,dc=es'

	active = SubElement(listener, 'active')
	active.text = 'false'

	branch = SubElement(listener, 'branch')
	#branch.text = 'ou='+branchName+',ou=entidades'
	branch.text = 'ou='+branchName+',ou=sanitarias'

	conflictOp = SubElement(listener, 'conflictOperation')
	conflictOp.text = 'LIST_JOIN'

	ignoreEmptyQ = SubElement(listener, 'ignoreEmptyQuery')
	ignoreEmptyQ.text = 'true'

	interval = SubElement(listener, 'interval')
	interval.text = '60'

	levelToSyslog = SubElement(listener, 'levelToSyslog')
	levelToSyslog.text = '0'

	noMoveEntries = SubElement(listener, 'noMoveEntries')
	noMoveEntries.text = 'true'

	noMoveGroupEntries = SubElement(listener, 'noMoveGroupEntries')
	noMoveGroupEntries.text = 'false'

	passwordDefault = SubElement(listener, 'passwordDefault')
	passwordDefault.text = 'aA1bB2cC3dD4'

	repos = SubElement(listener, 'repository')
	repos.text = reposName

	sendToSyslog = SubElement(listener, 'sendToSyslog')
	sendToSyslog.text = 'false'

	type_ = SubElement(listener, 'type')
	type_.text = '1'
	
	update = SubElement(listener, 'update')
	update.text = 'true'
	
	
	allowOps = SubElement(listener, 'allowOperations')

	allowOps1 = SubElement(allowOps, 'allowOperations')
	allowOps1.text = 'updateAU'
	
	allowOps2 = SubElement(allowOps, 'allowOperations')
	allowOps2.text = 'updateMU'
	
	allowOps3 = SubElement(allowOps, 'allowOperations')
	allowOps3.text = 'updateMUNA'
	
	allowOps4 = SubElement(allowOps, 'allowOperations')
	allowOps4.text = 'updateEU'

	allowOpsMap = SubElement(listener, 'allowOperationsMap')

	entry1 = SubElement(allowOpsMap, 'entry')
	key1 = SubElement(entry1, 'key')
	key1.text = 'updateAU'
	val1 = SubElement(entry1, 'value')
	val1.text = 'true'
	
	entry2 = SubElement(allowOpsMap, 'entry')
	key2 = SubElement(entry2, 'key')
	key2.text = 'updateMU'
	val2 = SubElement(entry2, 'value')
	val2.text = 'true'
	
	entry3 = SubElement(allowOpsMap, 'entry')
	key3 = SubElement(entry3, 'key')
	key3.text = 'updateMUNA'
	val3 = SubElement(entry3, 'value')
	val3.text = 'true'
	
	entry4 = SubElement(allowOpsMap, 'entry')
	key4 = SubElement(entry4, 'key')
	key4.text = 'updateEU'
	val4 = SubElement(entry4, 'value')
	val4.text = 'true'
	
	
	
	xml_request = tostring(listener,'utf-8')
	print xml_request
	
	sendRequest('PUT','listener',xml_request,host,user,passwd,1)
	#message = checkResponse(sendRequest('PUT','listener',xml_request,host,user,passwd,1))

	#print "\t"+message[1]
	#print "\t"+str(message) 
	

	
def createLink(reposName, branch, host, user, passwd): # Using resources1

	print "\n\nBuilding request for "+reposName+"..."
	#request = Element('request')

	link = Element('link')
	cn = SubElement(link,'cn')
	cn.text = reposName

	name = SubElement(link, 'dn')
	name.text = 'cn='+reposName+',ou=links,ou=configuration,dc=gid,dc=redsys,dc=es'
	
	allowOperations = SubElement(link,'allowOperations')
	
	allowOperations1 = SubElement(allowOperations,'allowOperations')
	allowOperations1.text = 'updateAU'

	allowOperations2 = SubElement(allowOperations,'allowOperations')
	allowOperations2.text = 'updateMU'
	
	
	repos = SubElement(link,'repository')
	repos.text = reposName

	branches = SubElement(link,'branches')
	
		
	branch_ = SubElement(branches,'branch')
	##branch_.text = 'ou='+branch.strip()+',ou=entidades'
	branch_.text = 'ou='+branch.strip()+',ou=sanitarias'
		
	typ = SubElement(link,'type')
	typ.text = '1'

	sendToSyslog = SubElement(link,'sendToSyslog')
	sendToSyslog.text = '0'
	
	tryAllMembershipInRoleConfiguration = SubElement(link,'tryAllMembershipInRoleConfiguration')
	tryAllMembershipInRoleConfiguration.text = 'false'

	update = SubElement(link,'update')
	update.text = 'true'

	
	xml_request = tostring(link,'utf-8')
	print xml_request
	sendRequest('PUT','link',xml_request,host,user,passwd,1)
	message = checkResponse(sendRequest('PUT','link',xml_request,host,user,passwd,1))
	#print "\t"+message[1]


def delLink(reposName, host, user, passwd):
	
	
	print "Deleting link..."+reposName
	message = checkResponse(sendRequest('DELETE', 'link/' + reposName.strip(), None, host,user, passwd,1))
	print reposName + ": " + message[1]

	
	
def modODIN(dn, uid,permisoODIN):
	con = ldap.initialize('ldap://'+host+':636')
	con.simple_bind_s( dn, passwd )
	(97, [])
		
	# The dn of our existing entry/object
	user="uid="+uid+",ou=personas,ou=E1465,ou=entidades,dc=gid-d,dc=redsys,dc=es" 
	
	# Some place-holders for old and new values
	old = {"aquaStatus": ['']}
	new = {"aquaStatus":['Lectura']}

	# Convert place-holders for modify-operation using modlist-module
	ldif = modlist.modifyModlist(old,new)

	# Do the actual modification 
	con.modify_s(user,ldif)

	# Its nice to the server to disconnect and free resources when done
	con.unbind_s()
              

#modODIN(dn, 'E1465001','Lectura')

def modODIN2(uid,permisoODIN,host, user, passwd):
	rama = 'E1465'
	dn="uid="+uid+",ou=personas,ou=E1465,ou=entidades,dc=gid-d,dc=redsys,dc=es"
	nombre = 'Manuel'
	attToModifiy = permisoODIN
	modUserAttribute (rama, dn, uid, nombre, attToModifiy, host, user, passwd)

#modODIN2 ('E1465001','Lectura',host, user, passwd)

	
def ponerNuevosAppsNA(uid, host, user, passwd):	
	ftw = "/home/pablo/USR/work/USR/RedSys/log_cambio_appsnuevas.txt"
	pattern2 = '%d-%m-%Y %H:%M:%S'
	w = open(ftw, 'a')
	#w.write("\n------------------------------------------------------------------")
	valueAtt ="N/A"
	valueAtt2 =""
	branch, dn, givenName = getOneUser(uid,host, user, passwd)	
	print branch
	print dn
	print uid
	print givenName
	
	

	KRONOSPerms, PdEPerms, GATPerms = getOneUserApplNuevasPermissions(uid,host, user, passwd)
	if (KRONOSPerms == "no_rellenado"):
		modUserAttributeKRONOS (branch, dn, uid, givenName, valueAtt, host, user, passwd)
	if (PdEPerms == "no_rellenado"):
		modUserAttributePdE (branch, dn, uid, givenName, valueAtt, host, user, passwd)
	if (GATPerms == "no_rellenado"):
		modUserAttributeGAT (branch, dn, uid, givenName, valueAtt, host, user, passwd)
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime(pattern2)
		
	modUserAttributeDelStatusApps(branch, dn, uid, givenName, valueAtt2, host, user, passwd)
	modUserAttributeNoCambiosEnApps(branch, dn, uid, givenName, valueAtt2, host, user, passwd)

	ApplKRONOSStatus, ApplPdEStatus, ApplGATStatus = getOneUserApplNuevasStatus(uid,host, user, passwd)
	NoCambiosEnApps = getOneUserAppNoCambiosEnApps(uid,host, user, passwd)
	KRONOSPerms, PdEPerms, GATPerms = getOneUserApplNuevasPermissions(uid,host, user, passwd)
	
	if (KRONOSPerms ==valueAtt and PdEPerms ==valueAtt and GATPerms==valueAtt):
		w.write("\nOK. "+uid.strip()+" KRONOS: "+KRONOSPerms+"; PdE: "+PdEPerms+"; GAT: "+GATPerms+"; Status: "+ApplKRONOSStatus+" "+ApplPdEStatus+" "+ApplGATStatus+"; NoCambiosEnApps: "+NoCambiosEnApps+" "+st)
		
	else:
		w.write("\nFallo: "+uid.strip()+" KRONOS: "+KRONOSPerms+"; PdE: "+PdEPerms+"; GAT: "+GATPerms+"; Status: "+ApplKRONOSStatus+" "+ApplPdEStatus+" "+ApplGATStatus+"; NoCambiosEnApps: "+NoCambiosEnApps+" "+st)

	w.close()

	
	
def ponerAllNuevosAppsNA(uid, host, user, passwd):
	ftw = "/home/pablo/USR/work/USR/RedSys/log_cambio_appsnuevas_tpvpc.txt"
	pattern2 = '%d-%m-%Y %H:%M:%S'
	w = open(ftw, 'a')
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime(pattern2)

	
	#listaApps = ["Geminis: ", "Loki: ", "SAS: ", "SIS: ", "TPV-TP: ", "KRONOS: ", "PdE: ", "GAT: "]
	#listaAppsPermissions = ["ApplGeminisPermissions","ApplLokiPermissions","ApplSASPermissions", \
	#						"ApplSISPermissions", "ApplTPVTPPermissions", "ApplKRONOSPermissions", \
	#					   "ApplPORTALDEEMISIONPermissions", "ApplGATPermissions",]
	#listaAppsStatus = ["ApplGeminisStatus","ApplLokiStatus","ApplSASStatus", \
	#						"ApplSISStatus", "ApplTPVTPStatus", "ApplKRONOSStatus", \
	#					   "ApplPORTALDEEMISIONStatus", "ApplGATStatus",]
	listaApps = ["TPV-PC: "]
	listaAppsPermissions = ["ApplTPVPCPermissions"]
	listaAppsStatus = ["ApplTPVPCStatus"]
	valueAtt2 =""
	branch, dn, givenName = getOneUser(uid,host, user, passwd)
	print branch
	print dn
	print givenName
	Fallo =0
	ErrorEntry =""
	#Modificación de los atributos AppXXXPermissions: se ponen a 'N/A'.
	modUserAttributeApplPerms (branch, dn, uid, listaAppsPermissions, givenName, host, user, passwd)
	listaResultadosPerms = getOneUserApplNuevasPermissions(uid, listaAppsPermissions, host, user, passwd)
	for a, r in zip(listaApps,listaResultadosPerms):
		if (r != "N/A"):
			Fallo = 1
			ErrorEntry = a+" "+r
			
	#Modificación de los atributos AppXXXStatus: se ponen en blanco.
	
	modUserAttributeDelStatusApps (branch, dn, uid, listaAppsStatus, givenName, host, user, passwd)
	listaResultadosStatus = getOneUserApplNuevasStatus(uid, listaAppsStatus, host, user, passwd)
	for a, r in zip(listaApps,listaResultadosStatus):
		if (r != "no_rellenado"):
			Fallo = 1
			ErrorEntry = ErrorEntry+"; "+a+" "+r
	
	modUserAttributeNoCambiosEnApps(branch, dn, uid, givenName,	valueAtt2, host, user, passwd)
	noCambiosEnApps = getOneUserAppNoCambiosEnApps(uid,host, user, passwd)
	if (noCambiosEnApps != "no_rellenado"):
		Fallo = 1
		ErrorEntry = ErrorEntry+"; NoCambiosEnApps: "+noCambiosEnApps
	
	if (Fallo == 0):
		w.write("\nOK. "+uid.strip()+" "+st)
		
	elif (Fallo ==1):
		w.write("\nFallo: "+uid.strip()+" : "+ErrorEntry+" "+st)

	w.close()
	
####
##BRANCHES

def createBranch1(name_branch, father_branch, writeGroups, description, host, user, passwd): # Using resources1

	print "\n\nBuilding request for "+name_branch+"..."
	#request = Element('request')

	branch = Element('branch')
	cn = SubElement(branch,'cn')
	cn.text = name_branch

	name = SubElement(branch,'name')
	name.text = name_branch

	descr = SubElement(branch,'description')
	descr.text = description
	
	father = SubElement(branch,'father')
	father.text = father_branch

	writers = SubElement(branch,'writers')
	
	for w in writeGroups:
		
		writeGroups = SubElement(writers,'writeGroups')
		writeGroups.text = w.strip()
	
	
	xml_request = tostring(branch,'utf-8')
	print "\n\n"+xml_request+"\n\n"
	#sendRequest(action,'branch',xml_request,host, user, passwd, 0)
	message = checkResponse(sendRequest('PUT','branch',xml_request,host,user,passwd,1))
	print "\t"+message[1]

def editBranch(name_branch, writeGroups, host, user, passwd): # Using resources1

	print "\n\nBuilding request for "+name_branch+"..."
	#request = Element('request')

	branch = Element('branch')
	cn = SubElement(branch,'cn')
	cn.text = name_branch

	name = SubElement(branch,'name')
	name.text = name_branch

	#descr = SubElement(branch,'description')
	#descr.text = "Perfiles Área "+name_branch[len(name_branch)-1]
	
	#father = SubElement(branch,'father')
	#father.text = father_branch

	writers = SubElement(branch,'writers')
	
	for w in writeGroups:
		
		writeGroups = SubElement(writers,'writeGroups')
		writeGroups.text = w.strip()
	
	
	xml_request = tostring(branch,'utf-8')
	print "\n\n"+xml_request+"\n\n"
	#sendRequest(action,'branch',xml_request,host, user, passwd, 0)
	message = checkResponse(sendRequest('POST','branch/editBranch',xml_request,host,user,passwd,1))
	print "\t"+message[1]

