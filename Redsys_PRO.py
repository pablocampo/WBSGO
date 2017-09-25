#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re, sys, os, time, datetime, calendar, urllib2, base64, \
Redsys_Funciones
from datetime import timedelta
from datetime import datetime as dt

from xml.etree import ElementTree
from xml.dom import minidom
#from termcolor import colored
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from Redsys_Funciones import *



T = True
F = False

delete_users= F
getApps= F
modRepos = F
compararOrigYDestin = F
addRepos = F
addListener = F
addLink = F
deleteLink = F
ad_user_to_role = F
add_dp_rch = F
mod_users = F
mod_user = F
desh_users = F
edit_branch = F
create_branch = F
create_group = F
add_to_group = F
reactivar_usuarios = F

if reactivar_usuarios:
	#users = ['E1465933']
	#users = ['E1465932']
	#users=['E6858100','E6100999','E6100128','E6100088','E3067005','E3060003','E3058105','E2095087']
	#users=['E2095084','E2095076','E2095009','e1465802','E1465764','E1465763','E1465651','E1465570']
	#users=['E1465169','E1465161','E1465034','E1465007','E0237069','e0237026','E0216002','E0182704']
	#users=['E0182347','E0182291','E0182193','E0128024','E0081524','E0081521','E0078001','E0075948']
	#users=['E0075770','E0075349','E0075250','e0075067','E0075057','E0049E46','e0049978','E0049794']
	#users=['E0049738','E0019127','e0019122','E0019017']
	#users=['e1465802','e0237026','e0075067','e0049978']
	for u in users:
		#ponerReactivarATrue (u, host, user, passwd)	
		pass
		
if add_to_group:
	##users = ['E0019002']#,
	##users = ['E0019003','E0019005','E0019006','E0019010','E0019017','E0019069']
	##users=['E0019109'] #,
	##users=['E0049002']#,
	##users= ['E0049042','E0049166','E0049362','E0049700','E0049701']
	##users=['E0049707','E0049731','E0049903','E0049B29','E0049B34','E0061001','E0061002']
	users = ['E0061003','E0061005','E0061006','E0061008','E0073011','E0073019','E0073677',\
			 'E0075015','E0075017','E0075018','E0075021','E0075066','E0075069','E0075083',\
			 'E0075199','E0075211','E0075254','E0075357','E0075748','E0075769','E0075902',\
			 'E0081007','E0081008','E0081009','E0081022','E0081032','E0081084','E0081206',\
			 'E0081327','E0128005','E0128047','E0128048','E0130002','E0130008','E0131009',\
			 'E0131010','E0131011','E0138002','E0152100','E0182002','E0182029','E0182070',\
			 'E0182097','E0182112','E0182113','E0182132','E0182133','E0182135','E0186002',\
			 'E0198002','E0198028','E0216001','E0216002','E0216013','E0216014','E0225001',\
			 'E0234006','E0234008','E0235006','E0239001','E1465015','E1465060','E1465117',\
			 'E1465123','E1465205','E1465271','E1465364','E1465708','E1491019',\
			 'E1491035','E1525001','E2038022','E2038639','E2056001','E2095002','E2095006',\
			 'E2095011','E2100002','E2100003','E2100036','E2100038','E2100077','E2100084',\
			 'E2100222','E2100238','E2100296','E2100300','E3001002','E3001005','E3025012',\
			 'E3025042','E3035002','E3035011','E3058002','E3058003','E3058006','E6100006',\
			 'E6100024','E6100030','E6100060','E6100064','E6100127','E6858080','E6858105',\
			 'E8814057','E8814059','E8814086','E9920001','E9920004','E9922001','E9922005',\
			 'E9922009']
	group = 'ReseteoDelegadoPassword'
	for u in users:
		print "\n\nAñadiendo "+u+" a grupo "+group
	
		#modUserAddMembership (u, group, host, user, passwd)

if create_group:
	groups = ['InterlocutoresC0090', \
				   'InterlocutoresC0100', 'InterlocutoresC0130', 'InterlocutoresC0180', 'InterlocutoresC0210', \
				   'InterlocutoresC0260', 'InterlocutoresC0330', 'InterlocutoresC0440', 'InterlocutoresC0460', \
				   'InterlocutoresC0520', 'InterlocutoresC0550', 'InterlocutoresC0560', 'InterlocutoresC0600', \
				   'InterlocutoresC0640', 'InterlocutoresC0680', 'InterlocutoresC0690', 'InterlocutoresC0700', \
				   'InterlocutoresC0750', 'InterlocutoresC0770', 'InterlocutoresC0790', 'InterlocutoresC0820', \
				   'InterlocutoresC0840', 'InterlocutoresC0850']
	
	#groupName = 'InterlocutoresC0090'
	for g in groups:
		description = g[:14]+' cía '+g[14:]
		print "Creando grupo "+g+ " : "+description
		createGroup(g, description,g[14:],host,user,passwd)

if create_branch:
	#branches = ['C0100', 'C0130', 'C0180', 'C0210', 'C0260', 'C0330', \
	branches = ['C0260', 'C0330', \
			  'C0440', 'C0460', 'C0520', 'C0560', 'C0600', \
			  'C0640', 'C0770', 'C0790', 'C0820', 'C0840', 'C0850']

	#descriptions = ['Mapfre Familiar', 'FIATC', 'Asefa', 'AFEMEFA', 'M. G. Catalunya', 'SF Salud', \
	descriptions = ['M. G. Catalunya', 'SF Salud', \
				   ' I.M.Q.', 'Adeslas SegurCaixa', 'Mutua Manresana', 'Mutua de Terrassa', 'Agrupació Mutua', \
				   'Amsyr', 'H.N.A.', 'H.N.A. S.C.', 'Caser', 'A.X.A. - Winterthur', 'Cigna']

	
	for b, d in zip(branches, descriptions):
		print "Creating branch " + b+ " : "+d
	#father_branch = 
		createBranch1(b, 'sanitarias', '',  d, host, user, passwd)
		
if edit_branch:
	branches = [ 'C0070', 'C0090', 'C0100', 'C0130', 'C0180', 'C0210', 'C0260', 'C0330', \
			  'C0440', 'C0460', 'C0520', 'C0560', 'C0600', \
			  'C0640', 'C0770', 'C0790', 'C0820', 'C0840', 'C0850']
	branchess = ['C0002']
	for b in branches:
		print "Updating branch "+b
		writeGroups = ['Interlocutores'+b]	
		editBranch(b, writeGroups, host, user, passwd)	
		
	#name_branch='deshabilitados'
	#father_branch = 
	#writeGroups = ['grpEnt_E1465','grpEnt_E0049', 'InterlocutoresC0002', 'InterlocutoresC0070', 'InterlocutoresC0090', \
	#			   'InterlocutoresC0100', 'InterlocutoresC0130', 'InterlocutoresC0180', 'InterlocutoresC0210', \
	#			   'InterlocutoresC0260', 'InterlocutoresC0330', 'InterlocutoresC0440', 'InterlocutoresC0460', \
	#			   'InterlocutoresC0520', 'InterlocutoresC0550', 'InterlocutoresC0560', 'InterlocutoresC0600', \
	#			   'InterlocutoresC0640', 'InterlocutoresC0680', 'InterlocutoresC0690', 'InterlocutoresC0700', \
	#			   'InterlocutoresC0750', 'InterlocutoresC0770', 'InterlocutoresC0790', 'InterlocutoresC0820', \
	#			   'InterlocutoresC0840', 'InterlocutoresC0850']
	

if desh_users:

	pvalidez = timedelta(days=91)
	data = getQueryMultipleUsersUltimoLogin (host, user, passwd)

	hoy = dt.now()

	response = ElementTree.fromstring(data)

	for i in range (len(response[0])):
		print response[0][i][0][1][2].text
		print response[0][i][0][0][2].text

		if response[0][i][0][0][1].text == 'uid' and \
			response[0][i][0][1][1].text == 'ultimoLoginTime':

			print "Ahora: "+dt.strftime(dt.now(), "%Y-%m-%d %H:%M:%S")
			if dt.strptime(response[0][i][0][1][2].text[:14], "%Y%m%d%H%M%S") + pvalidez < dt.now():
				print "período excedido"
				print "fecha último login + período de validez: "+str(dt.strptime(response[0][i][0][1][2].text[:14], "%Y%m%d%H%M%S")+pvalidez)


	

if compararOrigYDestin:
	orig = []
	dest = []
	file_to_read_orig = '/home/pablo/USR/work/USR/RedSys/santanderOrig.txt'
	f_orig = open(file_to_read_orig, 'r')

	
	file_to_read = '/home/pablo/USR/work/USR/RedSys/santanderDest.txt'
	f_dest = open(file_to_read, 'r')
	for l_d in f_dest:
		dest.append(l_d.strip())
	
	lista_usuarios = f_orig
	for l in lista_usuarios:
		if l.strip() not in dest:
			print l+" not in dest"

#branch, dn, givenName = getOneUser("E1465950",host, user, passwd)

#print dn

#uid = "E1465099"
#branch, dn, fechaBaja, givenName, primerApellido, puesto, departamento, responsable, groups, roles = getOneUser(uid,host, user, passwd)

#NoCambiosEnApps = getOneUserAppNoCambiosEnApps(uid,host, user, passwd)
#print NoCambiosEnApps
#modUserAttributeNoCambiosEnApps(branch, dn, uid, givenName, "", host, user, passwd)
#NoCambiosEnApps = getOneUserAppNoCambiosEnApps(uid,host, user, passwd)
#print NoCambiosEnApps


#lista_usuarios = getUsersLight(host, user, passwd)

#print len(lista_usuarios)

#dn = "uid=Administrador,ou=personas,dc=gid,dc=redsys,dc=es"
#dn = "uid=Administrador,ou=personas,dc=gid-d,dc=redsys,dc=es"

if mod_user:
	#dn ='uid=E1465171,ou=personas,ou=E1465,ou=entidades,dc=gid-d,dc=redsys,dc=es'
	uid = 'E1465171'
	tipoAlta = ''
	rama ='E1465'
	
	#modifyUser2 ('E1465049',host, user, passwd)
	#modifyUserOld (uid, tipoAlta, host, user, passwd)
	#modifyUserOld (rama, dn,uid, host, user, passwd)
	
	#print getQueryMultipleUsers (host, user, passwd)


if mod_users:
	file_to_read = '/home/pablo/USR/work/USR/RedSys/AppsEnBlanco/YEMANJA_.csv'
	f = open(file_to_read, 'r')
	lista_usuarios = f
	for l in lista_usuarios:
		#dn, givenName, uid = l.strip().split(';')
		#branch = uid[0:5]
		
		#print dn, givenName, uid, branch
		print l.strip()
		#modifyUserOld (l.strip(), '', host, user, passwd)
	
	#modifyUser2 ('E1465049',host, user, passwd)
	#modifyUserOld (rama, dn,uid, host, user, passwd)
	#modifyUserOld (rama, dn,uid, host, user, passwd)
	
	#print getQueryMultipleUsers (host, user, passwd)

if add_dp_rch:
	
	name_app = 'ApplVIGIA'
	
	#dpRchApp(name_app,'PUT',host, user, passwd)

if ad_user_to_role:
	
	dn = 'uid=E1465B58,ou=personas,ou=E1465,ou=entidades,dc=gid-d,dc=redsys,dc=es'
	uid = 'E1465B58'
	roleToAddTo = 'ResponsableApplPORTALDEEMISION'
	
#	roles= ['InterlocutorRedsys', 'ResponsableApplCANALES', \
#		   'ResponsableApplVIGIA', 'ResponsableApplODIN', 'ResponsableApplGAT', \
#		   'ResponsableApplKRONOS', 'ResponsableGAFW', 'ResponsablewApplGenesis',\
#		   'ResponsableApplSIS', 'ResponsableApplSAS', 'ResponsableApplTPVPC', \
#		   'ResponsablePPII', 'ResponsableusuariosSIRE', 'ResponsableApplGestionEntidades', \
#		   'ResponsableApplGeminis', 'ResponsableApplLoki', 'ResponsableusuariosHERMES', \
#		   'ResponsableApplPORTALDEEMISION']
	
#	for roleToAddTo in roles:
	#addUserToRole ('E1465', dn, uid, roleToAddTo, host, user, passwd)	

	
if delete_users:
	#file_to_read = "/home/pablo/USR/RedSys/users_1465_PRE_VISION.txt"
	#file_to_read = "/home/pablo/USR/RedSys/users_1465_nnn.txt"

	f = open(file_to_read, 'r')

	lista_usuarios = f

	for l in lista_usuarios:
		print l.strip()
		#deleteUser(l,host,user,passwd)
	f.close()


	
if getApps:

	file_to_read = "/home/pablo/USR/work/USR/RedSys/usuarios_PRO_nn.txt"

	f = open(file_to_read, 'r')

	lista_usuarios = f

	for l in lista_usuarios:
		print l.strip()
		#ponerAllNuevosAppsNA(l.strip(), host, user, passwd)
	f.close()

if modRepos:

	repositorios = ["LDAP-SAN-C0130"]
	branches = ["C0130"]
	orderNr = 104
		
	#reposName = "LDAP-PRO-Read-Sabadell"

	#userFilter = 'cn=E0081*'
	for reposName, branch in zip(repositorios, branches):
		print "Modifying: "+reposName, branch, 'cn='+branch+'*'
		modifyRepository(reposName, str(orderNr),'cn='+branch+'*', host,user,passwd)	
	
	##56 repos, 53 listeners
	
	#repositorios = ["LDAP-PRO-Read-CR-JAEN", "LDAP-PRO-Read-CR-GALEGA", \
	#				"LDAP-PRO-Read-CR-TENERIFE", "LDAP-PRO-Read-CR-TERUEL", \
	#				"LDAP-PRO-Read-CR-TOLEDO", "LDAP-PRO-Read-CR-ZAMORA", \
	#			    "LDAP-PRO-Read-CR-BAENA", "LDAP-PRO-Read-CR-LALCUDIA"]
	








if addRepos:
	
#	repositorios = ["LDAP-PRO-Read-CR-CANETEDLTORRES", "LDAP-PRO-Read-CR-SISIDRO", \
#					"LDAP-PRO-Read-CR-ALCORA", "LDAP-PRO-Read-CR-ADAMUZ", \
#					"LDAP-PRO-Read-CR-ALGEMESI", "LDAP-PRO-Read-CR-CASASIBANEZ", \
#				    "LDAP-PRO-Read-CR-SANJOSEALMASSORA", "LDAP-PRO-Read-CR-ONDA", \
#				   	"LDAP-PRO-Read-CR-BETXI", "LDAP-PRO-Read-CR-VILLAMALEA", \
#					"LDAP-PRO-Read-CR-ALBAL", "LDAP-PRO-Read-CAJAPOPULARVALENCIANA", \
#					"LDAP-PRO-Read-CR-BENICARLO", "LDAP-PRO-Read-CR-COVESVINROMA", \
#					"LDAP-PRO-Read-CR-VINAROZ", "LDAP-PRO-Read-CR-DELSUR", \
#					"LDAP-PRO-Read-GLOBALCAJA", "LDAP-PRO-Read-BANTIERRA"]
#	repositorios = ["LDAP-PRO-Read-BES", "LDAP-PRO-Read-EVO", \
#					"LDAP-PRO-Read-FIARE", "LDAP-PRO-Read-CAIXAPOLLENSA", \
#					"LDAP-PRO-Read-CR-INGENIEROS", "LDAP-PRO-Read-MONEYEXCHANGE"]
	#orderNr = 90	#Sanitarias desde 100. última entidad 89???

#	branches = ["E3104", "E3111",  "E3113", "E3115", "E3117", "E3127", "E3130", "E3134", \
#			    "E3138", "E3144", "E3150", "E3159", "E3162", "E3166", "E3174", "E3187", \
#				"E3190", "E3191"]
#	branches = ["E0131", "E0239", "E1550", "E2056", "E3025", "E6812"]


	#repositorios = ["LDAP-PRO-Read-ComerciaGPBrasil"]
	#repositorios = ["LDAP-PRO-Read-Wizink"]	
	#branches = ["E6100"]
	#branches = ["E0229"]

#	repositorios = ["LDAP-PRO-Read-Santander", "LDAP-PRO-Read-OpenBank"]
	#branches = ["E0049", "E0073"]
	
	
	#repositorios = ["LDAP-PRO-Read-BCC"]
	#branches = ["E0240"]

	#####Sanitarias PRE#####
	#repositorios = ["LDAP-SAN-Alianca-n"]
	#branches = ["C0002"]
	orderNr = 120 # último 119
	#repositorios = ["LDAP-SAN-C0130"]
	#branches = ["C0130"]

	##repositorios = ["LDAP-PRO-Read-SCF"]
	##branches = ["E0224"]
	#repositorios = ["LDAP-PRO-Read-Pecunpay","LDAP-PRO-Read-Almendralejo"]
	#branches = ["E6707", "E3001"]

	#repositorios = ["LDAP-SAN-C0180","LDAP-SAN-C0210","LDAP-SAN-C0260"]
	#branches = ["C0180","C0210","C0260"]

	#repositorios = ["LDAP-SAN-C0520","LDAP-SAN-C0560","LDAP-SAN-C0600"]
	#branches = ["C0520","C0560","C0600"]

	#repositorios = ["LDAP-SAN-C0640","LDAP-SAN-C0770","LDAP-SAN-C0790"]
	#branches = ["C0640","C0770","C0790"]
	
	repositorios = ["LDAP-SAN-C0820","LDAP-SAN-C0840","LDAP-SAN-C0850"]
	branches = ["C0820","C0840","C0850"]
	
	for reposName, branch in zip(repositorios, branches):
		print reposName, branch, 'cn='+branch+'*', orderNr
		createRepository(reposName, str(orderNr), 'cn='+branch+'*', host,user,passwd)	
		createListener (reposName, branch, host,user,passwd)
		orderNr = orderNr + 1
		

if addLink:
	#repositorios = ["LDAP-PRO-Read-CR-JAEN", "LDAP-PRO-Read-CR-GALEGA", \
	#				"LDAP-PRO-Read-CR-TENERIFE", "LDAP-PRO-Read-CR-TERUEL", \
	#				"LDAP-PRO-Read-CR-TOLEDO", "LDAP-PRO-Read-CR-ZAMORA", \
	#			    "LDAP-PRO-Read-CR-BAENA", "LDAP-PRO-Read-CR-LALCUDIA", \
	#			   "LDAP-PRO-Read-CR-NUEVACARTEYA"]

	#branches = ["E3067", "E3070",  "E3076", "E3080", "E3081", "E3085", "E3089", "E3096", \
	#		   "E3098"]

#	repositorios = ["LDAP-PRO-Read-CR-CANETEDLTORRES", "LDAP-PRO-Read-CR-SISIDRO", \
#					"LDAP-PRO-Read-CR-ALCORA", "LDAP-PRO-Read-CR-ADAMUZ", \
#					"LDAP-PRO-Read-CR-ALGEMESI", "LDAP-PRO-Read-CR-CASASIBANEZ", \
#				    "LDAP-PRO-Read-CR-SANJOSEALMASSORA", "LDAP-PRO-Read-CR-ONDA", \
#				   	"LDAP-PRO-Read-CR-BETXI", "LDAP-PRO-Read-CR-VILLAMALEA", \
#					"LDAP-PRO-Read-CR-ALBAL", "LDAP-PRO-Read-CAJAPOPULARVALENCIANA", \
#					"LDAP-PRO-Read-CR-BENICARLO", "LDAP-PRO-Read-CR-COVESVINROMA", \
#					"LDAP-PRO-Read-CR-VINAROZ", "LDAP-PRO-Read-CR-DELSUR", \
#					"LDAP-PRO-Read-GLOBALCAJA", "LDAP-PRO-Read-BANTIERRA"]

#	branches = ["E3104", "E3111",  "E3113", "E3115", "E3117", "E3127", "E3130", "E3134", \
#			    "E3138", "E3144", "E3150", "E3159", "E3162", "E3166", "E3174", "E3187", \
#				"E3190", "E3191"]

	#repositorios = ["LDAP-PRO-Read-BES", "LDAP-PRO-Read-EVO", \
	#				"LDAP-PRO-Read-FIARE", "LDAP-PRO-Read-CAIXAPOLLENSA", \
	#				"LDAP-PRO-Read-CR-INGENIEROS", "LDAP-PRO-Read-MONEYEXCHANGE"]
	#branches = ["E0131", "E0239", "E1550", "E2056", "E3025", "E6812"]



	#repositorios = ["LDAP-PRO-Read-ComerciaGPBrasil"]
	
	#branches = ["E6100"]

	#repositorios = ["LDAP-PRO-Read-Wizink"]	
	#branches = ["E0229"]

	#repositorios = ["LDAP-PRO-Read-Santander", "LDAP-PRO-Read-OpenBank"]
	#branches = ["E0049", "E0073"]
	#repositorios = ["LDAP-PRO-Read-BCC"]
	#branches = ["E0240"]
	
	###repositorios = ["LDAP-PRO-Read-SCF"]
	###branches = ["E0224"]
	#####Sanitarias #####
	###repositorios = ["LDAP-SAN-Alianca-n"]
	###branches = ["C0002"]
	
	##repositorios = ["LDAP-PRO-Read-Pecunpay","LDAP-PRO-Read-Almendralejo"]
	##branches = ["E6707", "E3001"]
	
	#repositorios = ["LDAP-SAN-C0070"]
	#branches = ["C0070"]
	#repositorios = ["LDAP-SAN-C0090"]
	#branches = ["C0090"]
	#repositorios = ["LDAP-SAN-C0100"]
	#branches = ["C0100"]
	#repositorios = ["LDAP-SAN-C0130"]
	#branches = ["C0130"]
	#repositorios = ["LDAP-PRO-Read-Pecunpay","LDAP-PRO-Read-Almendralejo"]
	#branches = ["E6707", "E3001"]

	#repositorios = ["LDAP-SAN-C0180","LDAP-SAN-C0210","LDAP-SAN-C0260"]
	#branches = ["C0180","C0210","C0260"]

	#repositorios = ["LDAP-SAN-C0330","LDAP-SAN-C0440","LDAP-SAN-C0460"]
	#branches = ["C0330","C0440","C0460"]

	#repositorios = ["LDAP-SAN-C0520","LDAP-SAN-C0560","LDAP-SAN-C0600"]
	#branches = ["C0520","C0560","C0600"]

	#repositorios = ["LDAP-SAN-C0640","LDAP-SAN-C0770","LDAP-SAN-C0790"]
	#branches = ["C0640","C0770","C0790"]
	
	#repositorios = ["LDAP-SAN-C0820","LDAP-SAN-C0840","LDAP-SAN-C0850"]
	#branches = ["C0820","C0840","C0850"]
	
	for reposName, branch in zip(repositorios, branches):
		print reposName, branch

		createLink(reposName, branch, host, user, passwd)
		
		
if deleteLink:
	
	reposName = "LDAP-PRO-Read-CREDITANDORRA"
	#delLink(reposName, host, user, passwd)

if addListener:

	reposName = "LDAP-PRO-Read-BARCLAYCARDPLC"
	branch = 'E0152'
	
	#createListener (reposName, branch, host,user,passwd)
	