#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, traceback, urllib, urllib2, base64, DAO, re, xlsxwriter
import unicodedata, pickle
import collections
import textwrap
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import cm
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def buildrolecaches():
    '''Construye una caché de roles,puesto y otra de grupos,puesto'''
    try:
        data = DAO.sendrequest('GET', 'role', None, 1)
        message = DAO.checkresponse(data)
        cache = {}
        cache2 = {}
        if message[0]:
            response = ElementTree.fromstring(data)
            for role in response[0].findall("role/cn"):
                print "Creating " + role.text + "..."
                data2 = DAO.sendrequest('GET', 'role/' + role.text, None, 1)
                message2 = DAO.checkresponse(data2)
                if message2[0]:
                    response2 = ElementTree.fromstring(data2)
                    father = response2[0].findall("father")
                    groupsmembers = response2[0].findall("groupsMembers")
                    if len(father) > 0 and groupsmembers > 0:
                        father = father[0]
                        if father.text != 'Recertificacion' and father.text != 'Soporte' and father.text != 'DESHABILITADOS' and father.text != 'BORRADOS' and father.text != 'Roles-Especiales' and father.text != 'WBSVision Interno':
                            groupsmembers = groupsmembers[0].text
                            # Almacena rol: grupo asociado, aplicativo
                            cache[role.text] = {"group": groupsmembers, "father": father.text}
                            # Almacena: grupo = aplicativo
                            cache2[groupsmembers] = father.text
                            print "Done."
                        else:
                            print "Skipped."
                    else:
                        print "Skipped."
                else:
                    print message[1]
            print "Salvando objeto..."
            save_obj(cache, "roles")
            save_obj(cache2, "grupos")
            print "Done."
        else:
            print message[1]
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit()




def getuserroles(userid, cache):
    '''Obtiene todos los roles del usuario devolviendo un dicionario que los contiene,
  en el que se marcan por defecto como permisos de aplicación'''
    roles = {}
    # roles = collections.OrderedDict()
    data = DAO.sendrequest('GET', 'user/' + userid, None)
    message = DAO.checkresponse(data)
    if message[0]:
        response = ElementTree.fromstring(data)
        for role in response[0][0].findall("attribute[@name='roles']"):
            # Crea una lista con los textos y su tipo
            # print role.text
            if role.text in cache:
                if cache[role.text]['father'] == 'PuestoDeTrabajo':
                    #print 'Puesto'
                    roles['Puesto'] = role.text
                roles[role.text] = cache[role.text]
    else:
        #print message[1]
        pass
    #print roles
    return roles




def rellenarUserForXLS(userid):
    print "\n\t\tGetting info forrr "+userid
    ''' Rellena los attributos rolesDefinicionPuesto, rolesDeMas y rolesDeMenos de un usuario'''
    try:
        # Cargar caches
        cache = load_obj("roles")
        gcache = load_obj("grupos")
        #print "\n\t\tbla"
        # Inicializo listas
        puestoTrabajo =""
        rolesdefinicion = []
        rolesdemas = []
        rolesdemasSinMakeUp = []
        rolesdemenosSinMakeUp = []
        rolesdemenos = []
        rolesDefSinMakeUp = []
        rolesOrdenados ={}
        # Obtener todos los roles del usuario
        uroles = collections.OrderedDict(getuserroles(userid, cache))
        # Obtener punto de decisión relacionado con el puesto de trabajo y los roles que otorga
        ordenDic = {}
        if 'Puesto' in uroles:
          print "Puesto: "+uroles['Puesto']
          for role, info in uroles.items():
            if role == 'Puesto':
              puestoTrabajo = uroles['Puesto']
              del uroles[role]
            elif info['father'] == 'PuestoDeTrabajo':
              puestoTrabajo = role
              del uroles[role]
            else:
              if info['father'] not in ordenDic:
                 ordenDic[info['father']] = [info['group']]
              else:
                 ordenDic[info['father']].append(info['group'])
        #for father, vals in ordenDic.items():
            #print father+"\t\t"+str(ordenDic[father])
        else:
            print "El usuario " + userid + " no tiene un puesto válido"
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit()
		#pass
    return puestoTrabajo, ordenDic	
    #print "\nSEGUIMOS AQUI... \n" 
    #return puestoTrabajo,  rolesDefSinMakeUp, rolesdemasSinMakeUp, rolesdemenosSinMakeUp


	
def makeXLS(uid, puesto, roles):	
    print "making xls"
    workbook = xlsxwriter.Workbook('Informe.xlsx')
    worksheet = workbook.add_worksheet()

    format1 = workbook.add_format({#'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1})
    format2 = workbook.add_format({'border':1})
    format = workbook.add_format()
    format.set_pattern(1)
    format.set_bg_color('blue')
    format.set_font_color('white')

    worksheet.write(1, 2,     "Identificador", format)
    worksheet.write(1, 3,     "Puesto", format)
    worksheet.write(1, 4,     "Aplicativo", format)
    worksheet.write(1, 5,     "Roles", format)

    worksheet.set_column(2, 2,     30)
    worksheet.set_column(3, 3,     30)
    worksheet.set_column(4, 4,     30)
    worksheet.set_column(5, 5,     30)
    x = 2
    h = x
    
    for father, vals in roles.items():
       j = len(roles[father])
       for role in roles[father]:
           worksheet.write(x, 5,     role, format2)
           
           x = x+1
       if j ==1:
          worksheet.write(x-1, 4,     father, format1)
       else:
          worksheet.merge_range(h,4,h+j-1,4, father, format1)
       h = x

    worksheet.merge_range(2,2,x-1,2, uid, format1)
    worksheet.merge_range(2,3,x-1,3, puesto, format1)
    workbook.close()	

	
def makeXLSMultiple(uids):	
	
    print "making xls"
    workbook = xlsxwriter.Workbook('Informe.xlsx')
    worksheet = workbook.add_worksheet()

    format1 = workbook.add_format({#'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1})
    format2 = workbook.add_format({'border':1})
    format = workbook.add_format()
    format.set_pattern(1)
    format.set_bg_color('blue')
    format.set_font_color('white')

    worksheet.write(1, 2,     "Identificador", format)
    worksheet.write(1, 3,     "Puesto", format)
    worksheet.write(1, 4,     "Aplicativo", format)
    worksheet.write(1, 5,     "Roles", format)

    worksheet.set_column(2, 2,     30)
    worksheet.set_column(3, 3,     30)
    worksheet.set_column(4, 4,     30)
    worksheet.set_column(5, 5,     30)
    x = 2
    h = x
    u = 2
    for uid in uids:
       print "USER "+uid
       puesto, roles = rellenarUserForXLS(uid)
       #print "puesto "+puestoTrabajo
	
	
       for father, vals in roles.items():
          j = len(roles[father])
          print father
          for role in roles[father]:
             print "\t"+role
             worksheet.write(x, 5,     role, format2)
           
             x = x+1
          if j ==1:
             worksheet.write(x-1, 4,     father, format1)
          else:
             worksheet.merge_range(h,4,h+j-1,4, father, format1)
          h = x

       worksheet.merge_range(u,2,x-1,2, uid, format1)
       worksheet.merge_range(u,3,x-1,3, puesto, format1)
       h = h+1
       x = x+1
       u = x
    workbook.close()	
	
def writer (uid):
    puestoTrabajo, rolesDic = rellenarUserForXLS(uid)
    print puestoTrabajo
    print len(rolesDic)
    for father, vals in rolesDic.items():
       print father+":"
       #print len(rolesDic)
       
       for r in rolesDic[father]:
           print "\t\t"+r	
	
    makeXLS(uid, puestoTrabajo, rolesDic)

	
	
def getAllUserForXLS():
    uids= ['raul.lopez', 'joseluis.gonzalez', 'abdel.lamouri',  'alba.pickhardt', 'alberto.ortego',\
		  'hugo.ortega', 'gestor.valida', 'gestor.recobro']
    uid1= ['raul.lopez', 'joseluis.gonzalez']
    return uids 
		
	
	
def getAllUserForXLS2():
    uids= []
    print "Actualizando todos los usuarios"
    try:
        data = DAO.sendrequest('GET', 'user', None, 0, 'branch=usuariosTFSE')
        message = DAO.checkresponse(data)
        if message[0]:
            response = ElementTree.fromstring(data)
            for child in response[0]:
                uid = child.get('uid')
                uids.append(uid)
        else:
            print message[1]
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit()
    return uids

def makeXLSAll():
    print "Starting"
    uids= getAllUserForXLS()
    makeXLSMultiple(uids)
	
def printmenu():
    print "Operaciones:"
    print "\t1.- Reconstruir indices"
    print "\t2.- Recertificar un usuario"
    print "\t3.- Rellenar atributos de permisos de un usuario"
    print "\t4.- Rellenar atributos de permisos de TODOS"
    print ""
    print "\t0.- Salir"

    op = raw_input(":-")
    try:
        op = int(op)
        if op == 1:
            print "Creando caché de roles..."
            buildrolecaches()
            print "Terminado"
            printmenu()
        elif op == 2:
            #userid = raw_input("Introduzca id de usuario a recertificar:-")
            #recertificar(userid)
            #rellenarUserForXLS(userid)
            writer('raul.lopez')
            printmenu()
        elif op == 3:
            userid = raw_input("Introduzca id de usuario a recertificar:-")
            rellenar(userid)
            printmenu()
        elif op == 4:
            #rellenarall()
            makeXLSAll()
            printmenu()
    except Exception, e:
        op = 9999
        printmenu()


# MAIN ---
try:
    printmenu()
except:
    traceback.print_exc(file=sys.stdout)
    sys.exit()
	
