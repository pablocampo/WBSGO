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
		#print url #Uncomment if you want to see url!!!
		
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

def getUsersLight(branch, host, user, passwd):
	users =[]
	print "Versión light (sólo uid). Buscando usuarios de la rama "+branch+"..."
	#data = DAO.sendrequest('GET', 'user', None)
	data = sendRequest('GET', 'user?limit=25000000', None,host,user,passwd)
	
	response = ET.fromstring(data)
	for child in response[0]: #child.tag is "user"
		#print child
		uid = child.get('uid')
		if child.get('branch') == branch:
			users.append(uid)
			#print uid
		#else:
			#print uid+" not in usuariosTFSE"
		#users.append(uid)
	#print len(users)
	return users	

def getOneUserSimple(uid, host, user, passwd):
	properties={}
	#print "\nBuscando el usuario "+uid+"...\n"
	if " " in uid:
		uid = uid.replace(" ","%20")
	data = sendRequest('GET', 'user/' + uid, None, host, user, passwd, 0) #get user
	response = ET.fromstring(data)
	for child in response[0]: #child.tag is "user"
		for p in range (len(child)-1):
			properties[child[p].get('name')] = child[p].text
		uid = properties['uid']
		if 'puestoTrabajo' in properties:
			puesto =  properties['puestoTrabajo']
		else:
			puesto = "empty"			
		if 'manager' in properties:
			manager =  properties['manager']
		else:
			manager = "empty"			
			
		dn = child.get('dn')
		#print '\nUsuario: ' + str(uid)+'\tPuesto: '+puesto+'\tNombre Oracle: '+nombreOracle+'\n'

	return puesto.strip(), manager.strip()


def ponerFechaAltaYFechaIncorporacionUserSingleDate (rama,dn,uid,fecha, host, usr, passwd):
	print "Modifying attributes for user "+uid+":"
	#print "Fecha alta e incorporación: "+fechaAlta
	request = Element('request')
	user = SubElement(request,'user')
	user.set('branch',rama)
	user.set('dn',dn)
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
	#givenName.text=nombre

	fechaAlta_ = SubElement(user,'attribute')
	fechaAlta_.set('name','fechaAlta')
	fechaAlta_.text=fecha

	fechaIncorporacion_ = SubElement(user,'attribute')
	fechaIncorporacion_.set('name','fechaIncorporacion')
	fechaIncorporacion_.text=fecha

	typeAssign = SubElement(user,'attribute')
	typeAssign.set('name','typeAssign')
	typeAssign.text='all'

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request,host, usr, passwd))
	print message[1]




def ponerFechaAltaYFechaIncorporacionUser (rama,dn,uid,fechas, host, usr, passwd):
	print "Modifying attributes for user "+uid+":"
	#print "Fecha alta e incorporación: "+fechaAlta
	request = Element('request')
	user = SubElement(request,'user')
	user.set('branch',rama)
	user.set('dn',dn)
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
	#givenName.text=nombre

	for f in fechas:
		print f
		fechaAlta_ = SubElement(user,'attribute')
		fechaAlta_.set('name','fechaAlta')
		fechaAlta_.text=f

		fechaIncorporacion_ = SubElement(user,'attribute')
		fechaIncorporacion_.set('name','fechaIncorporacion')
		fechaIncorporacion_.text=f
	
	typeAssign = SubElement(user,'attribute')
	typeAssign.set('name','typeAssign')
	typeAssign.text='all'

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request,host, usr, passwd))
	print message[1]


def ponerFechaAltaFechaIncorporacionYFechaBajaUser (rama,dn,uid,fechasAlta, fechasBaja, host, usr, passwd):
	print "Modifying attributes for user "+uid+":"
	#print "Fecha alta e incorporación: "+fechasAlta
	request = Element('request')
	user = SubElement(request,'user')
	user.set('branch',rama)
	user.set('dn',dn)
	user.set('uid',uid)
	#user.text=' '
	uid_ = SubElement(user,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	for fa in fechasAlta:
		
		fechaAlta_ = SubElement(user,'attribute')
		fechaAlta_.set('name','fechaAlta')
		fechaAlta_.text=fa

		fechaIncorporacion_ = SubElement(user,'attribute')
		fechaIncorporacion_.set('name','fechaIncorporacion')
		fechaIncorporacion_.text=fa
	
	for fb in fechasBaja:
		fechaBaja_ = SubElement(user,'attribute')
		fechaBaja_.set('name','fechaDeshabilitacion')
		fechaBaja_.text=fb
	
	
	typeAssign = SubElement(user,'attribute')
	typeAssign.set('name','typeAssign')
	typeAssign.text='all'

	xml_request = tostring(request,'utf-8')
	print xml_request
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request,host, usr, passwd))
	print message[1]

	
def ponerRecertificacionATrue (uid, host, usr, passwd):
	print "Modifying attributes for user "+uid+":"
	request = Element('request')
	user = SubElement(request,'user')
	#user.set('branch',rama)
	#user.set('dn',dn)
	user.set('uid',uid)
	uid_ = SubElement(user,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	recert_ = SubElement(user,'attribute')
	recert_.set('name','Recertificar')
	recert_.text="true"
	
	typeAssign = SubElement(user,'attribute')
	typeAssign.set('name','typeAssign')
	typeAssign.text='all'

	xml_request = tostring(request,'utf-8')
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request,host, usr, passwd))
	print message[1]


def vaciarRolesRecertificacion (uid, host, usr, passwd):
	print "Modifying attributes for user "+uid+":"
	request = Element('request')
	user = SubElement(request,'user')
	#user.set('branch',rama)
	#user.set('dn',dn)
	user.set('uid',uid)
	uid_ = SubElement(user,'attribute')
	uid_.set('name','uid')
	uid_.text=uid

	recert_ = SubElement(user,'attribute')
	recert_.set('name','rolesDefinicionPuesto')
	recert_.text=""
	
	recert1_ = SubElement(user,'attribute')
	recert1_.set('name','rolesDeMas')
	recert1_.text=""
	
	recert2_ = SubElement(user,'attribute')
	recert2_.set('name','rolesDeMenos')
	recert2_.text=""
	
	typeAssign = SubElement(user,'attribute')
	typeAssign.set('name','typeAssign')
	typeAssign.text='all'

	xml_request = tostring(request,'utf-8')
	message = checkResponse(sendRequest('PUT', 'user/' + uid, xml_request,host, usr, passwd))
	print message[1]


	
	

def getQueryMultipleUsers (host, user, passwd):
	request = Element('request')
	limit = SubElement(request,'limit')
	limit.text='250'
	listAttr1 = SubElement(request,'listAttr')
	listAttr1.text='dn'
	listAttr2 = SubElement(request,'listAttr')
	listAttr2.text='givenname'
	listAttr4 = SubElement(request,'listAttr')
	listAttr4.text='uid'
	qFilter = SubElement(request,'queryFilter')
	cQuery = SubElement(qFilter,'conditionsQuery')
	cQuery1 = SubElement(cQuery,'conditionsQuery')
	pData1 = SubElement(cQuery1,'paramData')

	key1 = SubElement(pData1,'key')
	key1.text='givenName'
	type1 = SubElement(pData1,'type')
	type1.text='0'
	value1 = SubElement(pData1,'value')
	value1.text='*'
	
	#cQuery2 = SubElement(cQuery,'conditionsQuery')
	#pData2 = SubElement(cQuery2,'paramData')

	#key2 = SubElement(pData2,'key')
	#key2.text='mail'
	#type2 = SubElement(pData2,'type')
	#type2.text='0'
	#value2 = SubElement(pData2,'value')
	#value2.text='*'
	
	#cQuery3 = SubElement(cQuery,'conditionsQuery')
	#pData3 = SubElement(cQuery3,'paramData')

	#key3 = SubElement(pData3,'key')
	#key3.text='memberOf'
	#type3 = SubElement(pData3,'type')
	#type3.text='0'
	#value3 = SubElement(pData3,'value')
	#value3.text='cn=SGE,ou=grupos,dc=gdi-pre,dc=mineco,dc=es'
	
	
	typeA = SubElement(cQuery,'type')
	typeA.text='101'
	

	xml_request = tostring(request,'utf-8')
	print xml_request
	return sendRequest('POST', 'user/searchUsers/users/usuariosTFSE', xml_request, host, user, passwd,1)
	

def getOneRole(r, host, user, passwd):
	#print "\nBuscando el rol "+r+"...\n"
	rolGrupoDic = {}
	if " " in r:
		r = r.replace(" ","%20")
	data = sendRequest('GET', 'role/' + r, None, host, user, passwd, 1) 
	response = ET.fromstring(data)
	#print data
	for child in response: #child.tag is "user"
		return child[0].text,child[4].text

	
	

def dpPonerPuesto(name_dp,roles2Add,name_condition_role,action,host, user, passwd):

	#We make request:
	print "\n\nBuilding request for "+name_dp+"..."
	print "\nList of roles:"
	for role in roles2Add:
		print "\t"+role
	print "\nCondition Role is:"
	print "\t"+name_condition_role
	
	dp = Element('decisionPoint')
	cn = SubElement(dp,'cn')
	cn.text = name_dp
	base64 = SubElement(dp,'base64')
	base64.text ='false'
	addUserBody = SubElement(dp,'addUserBody')
	addUserBody.text = "Se ha dado el puesto "+name_condition_role+" al usuario [[[userModified]]]"
	addUserFrom = SubElement(dp,'addUserFrom')
	addUserFrom.text = "wbsvision@es.toyota-fs.com"
	addUserSubject = SubElement(dp,'addUserSubject')
	addUserSubject.text = "Dado puesto "+name_condition_role
	comunicationRoles = SubElement(dp,'comunicationRoles')
	comunicationRol = SubElement(comunicationRoles,'comunicationRol')
	comunicationRol.text = "Confirmar-Altas"
	conditionOperations = SubElement(dp,'conditionOperations')
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "all_operation"
	value = SubElement(entry,'value')
	value.text = "true"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	conditionOperations = SubElement(dp,'conditionOperations')
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "all_operation"
	value = SubElement(entry,'value')
	value.text = "true"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"

	
	doCommit = SubElement(dp,'doCommit')
	doCommit.text = "true"
	#groupsToAddString = SubElement(dp,'groupsToAddString')
	#groupsToAddString.text = groups_string
	modifyUserBody = SubElement(dp,'modifyUserBody')
	modifyUserBody.text = "Se ha dado el puesto "+name_condition_role+" al usuario [[[userModified]]]"
	modifyUserFrom = SubElement(dp,'modifyUserFrom')
	modifyUserFrom.text = "wbsvision@es.toyota-fs.com"
	modifyUserSubject = SubElement(dp,'modifyUserSubject')
	modifyUserSubject.text = "Dado puesto "+name_condition_role
	randomAttributes = SubElement(dp,'randomAttributes')
	for rol in roles2Add:
		randomAttributes2 = SubElement(randomAttributes,'randomAttributes')
		directoryAtt = SubElement(randomAttributes2,'directoryAtt')
		directoryAtt.text = ''
		generationType = SubElement(randomAttributes2,'generationType')
		generationType.text = '4'
		name = SubElement(randomAttributes2,'name')
		name.text = 'roles2Add'
		value = SubElement(randomAttributes2,'value')
		value.text = rol+';;_;;[[[selfvalue]]]'
		#randomAttributes2.text = grupo
		#groupsMembers.text = perfil
	##Add ListasDistribucion to all
	randomAttributes2 = SubElement(randomAttributes,'randomAttributes')
	directoryAtt = SubElement(randomAttributes2,'directoryAtt')
	directoryAtt.text = ''
	generationType = SubElement(randomAttributes2,'generationType')
	generationType.text = '4'
	name = SubElement(randomAttributes2,'name')
	name.text = 'roles2Add'
	value = SubElement(randomAttributes2,'value')
	value.text = 'ListasDistribucion;;_;;[[[selfvalue]]]'

	randomAttributes2 = SubElement(randomAttributes,'randomAttributes')
	directoryAtt = SubElement(randomAttributes2,'directoryAtt')
	directoryAtt.text = ''
	generationType = SubElement(randomAttributes2,'generationType')
	generationType.text = '5'
	name = SubElement(randomAttributes2,'name')
	name.text = 'roles2Remove'
	value = SubElement(randomAttributes2,'value')
	value.text = ''
	
		
	roles = SubElement(dp,'roles')
	checkType = SubElement(roles,'checkType')
	checkType.text = '1' 
	role = SubElement(roles,'role')
	role.text = name_condition_role
	saveInformation = SubElement(dp,'saveInformation')
	saveInformation.text='true'
	type_ = SubElement(dp,'type')
	type_.text = "1"

	xml_request = tostring(dp,'utf-8')
	print xml_request

	#We send request:
	print "Creating/ modifying "+name_dp+" in WBSVision..."
#	DAO.sendrequest(action,'decisionPoint',xml_request,1)
	sendRequest(action,'decisionPoint',xml_request,host, user, passwd, 1)


def dpQuitarPuesto(name_dp,roles2Remove,name_condition_role,action,host, user, passwd):
	#We make request:
	print "\n\nBuilding request for "+name_dp+"..."
	print "\nList of roles:"
	for role in roles2Remove:
		print "\t"+role
	print "\nCondition Role is:"
	print "\t"+name_condition_role
	
	dp = Element('decisionPoint')
	cn = SubElement(dp,'cn')
	cn.text = name_dp
	addUserBody = SubElement(dp,'addUserBody')
	addUserBody.text = "Se ha quitado el puesto "+name_condition_role+" al usuario [[[userModified]]]"
	addUserFrom = SubElement(dp,'addUserFrom')
	addUserFrom.text = "wbsvision@es.toyota-fs.com"
	addUserSubject = SubElement(dp,'addUserSubject')
	addUserSubject.text = "Quitado puesto "+name_condition_role
	branch = SubElement(dp,'branch')
	branch.text = "ou=usuariosTFSE"
	comunicationRoles = SubElement(dp,'comunicationRoles')
	comunicationRol = SubElement(comunicationRoles,'comunicationRol')
	comunicationRol.text = "Confirmar-Altas"
	conditionOperations = SubElement(dp,'conditionOperations')
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "update_group_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "all_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "update_user_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "delete_group_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "add_user_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "delete_user_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "add_group_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "true"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	conditionOperations = SubElement(dp,'conditionOperations')
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "update_group_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "all_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "update_user_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "delete_group_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "add_user_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "delete_user_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "add_group_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "allocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "false"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_roles_operation"
	value = SubElement(entry,'value')
	value.text = "true"
	entry = SubElement(conditionOperations,'entry')
	key = SubElement(entry,'key')
	key.text = "deallocate_membership_operation"
	value = SubElement(entry,'value')
	value.text = "false"

	deallocateRolesOperation = SubElement(dp,'deallocateRolesOperation')
	deallocateRolesOperation.text = "true"
	deallocatedRoles = SubElement(dp,'deallocatedRoles')
	deallocatedRoles.text = name_condition_role
	
	
	doCommit = SubElement(dp,'doCommit')
	doCommit.text = "true"
	modifyUserBody = SubElement(dp,'modifyUserBody')
	modifyUserBody.text = "Se ha quitado el puesto "+name_condition_role+" al usuario [[[userModified]]]"
	modifyUserFrom = SubElement(dp,'modifyUserFrom')
	modifyUserFrom.text = "wbsvision@es.toyota-fs.com"
	modifyUserSubject = SubElement(dp,'modifyUserSubject')
	modifyUserSubject.text = "Quitado puesto "+name_condition_role
	randomAttributes = SubElement(dp,'randomAttributes')
	for rol2remove in roles2Remove:
		randomAttributes2 = SubElement(randomAttributes,'randomAttributes')
		directoryAtt = SubElement(randomAttributes2,'directoryAtt')
		directoryAtt.text = ''
		generationType = SubElement(randomAttributes2,'generationType')
		generationType.text = '4'
		name = SubElement(randomAttributes2,'name')
		name.text = 'roles2Remove'
		value = SubElement(randomAttributes2,'value')
		value.text = rol2remove+';;_;;[[[selfvalue]]]'
		#randomAttributes2.text = grupo
		#groupsMembers.text = perfil
	#roles = SubElement(dp,'roles')
	#checkType = SubElement(roles,'checkType')
	#checkType.text = '1' 
	#role = SubElement(roles,'role')
	#role.text = name_condition_role
	saveInformation = SubElement(dp,'saveInformation')
	saveInformation.text='true'
	type_ = SubElement(dp,'type')
	type_.text = "1"

	xml_request = tostring(dp,'utf-8')
	print xml_request

	#We send request:
	print "Creating/ modifying "+name_dp+" in WBSVision..."
#	DAO.sendrequest(action,'decisionPoint',xml_request,1)
	sendRequest(action,'decisionPoint',xml_request,host, user, passwd, 1)

	
def findGroupInDecisionPoint (dpName, groupNames, host, user, passwd):
	print "*"+dpName+":"
	data = sendRequest('GET', 'decisionPoint/'+dpName, None,host,user,passwd,1)
	data = data.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><response>','')
	data = data.replace('</response>','')
	#print data
	for grpN_Old in groupNames.keys():
		if grpN_Old in data:
		#if groupNames[grpN_Old] in data:
			#data = data.replace(grpN_Old,groupNames[grpN_Old])
			#print "\t"+groupNames[grpN_Old]
			
			print "\t"+grpN_Old
	
def modDecisionPoint (dpName, groupNames, host, user, passwd):
	data = sendRequest('GET', 'decisionPoint/'+dpName, None,host,user,passwd,1)
	data = data.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><response>','')
	data = data.replace('</response>','')
	#print data
	for grpN_Old in groupNames.keys():
		if grpN_Old in data:
			data = data.replace(grpN_Old,groupNames[grpN_Old])
			print data
			sendRequest('POST','decisionPoint',data,host, user, passwd, 1)
	
def modDecisionPointOld (dpName, groupNameOld, groupNameNew, host, user, passwd):
	data = sendRequest('GET', 'decisionPoint/'+dpName, None,host,user,passwd,1)
	data = data.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><response>','')
	data = data.replace('</response>','')
	#print data
	if groupNameOld in data:
		data = data.replace(groupNameOld,groupNameNew)
		print data
		sendRequest('POST','decisionPoint',data,host, user, passwd, 1)
	
	#LdD-TFSES - All Staff,LdD-TFSES - finanzas
	
def createRole(roleName,memberGroup,father_role,host,user,passwd):
	
	#We make request:
	#print "\nBuilding request for "+roleName+"..."
	role = Element('role')
	cn = SubElement(role,'cn')
	cn.text = roleName
	father = SubElement(role,'father')
	father.text = father_role
	groupsMembers = SubElement(role,'groupsMembers')
	groupsMembers.text = memberGroup

	xml_request = tostring(role,'utf-8')

	#We send request:
	print "\nCreando rol "+roleName+" en WBSVision..."
	print "\n\n"+xml_request+"\n\n"
	message = checkResponse(sendRequest('POST','role',xml_request,host,user,passwd,1))
	print "\t"+message[1]
	
#####


