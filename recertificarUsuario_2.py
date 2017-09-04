#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys, traceback, urllib, urllib2, base64, DAO, re
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


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def makePDF2():
    c = canvas.Canvas("./Informe.pdf", pagesize=A4)
    doc = SimpleDocTemplate("form_letter.pdf", pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=15)
    width, height = A4
    c.setLineWidth(.3)
    c.setFont('Helvetica', 12)
    c.drawString(10, 25, "Informe Toyota")
    c.drawString(20, 45, "UID")
    c.drawString(20, 65, "puestoTrabajo")
    page_num = c.getPageNumber()
    text = "Page #%s" % page_num
    c.drawRightString(200*mm, 20*mm, text)	
    print "hostia"
    c.save()

def addPageNumber(c, doc):
    """
    Add the page number
    """
    #c.showPage()	
    logo = "./Toyota.png"
    c.drawImage(logo, 11, 275*mm, width = 40*mm, height = 20 *mm, mask='auto')
    page_num = c.getPageNumber()
    text = "%s" % page_num
    textobject2 = c.beginText()
    textobject2.setFont("Helvetica",12)
    textobject2.setTextOrigin(200*mm, 10*mm)
    textobject2.textLine(text)
    c.drawText(textobject2)	
    #c.drawRightString(200*mm, 10*mm, text)	
#    c.save()	
    print "\nhere......\n"

def addPageNumberFirstPage(c, doc):
    """
    Add the page number
    """
    title = "Informe Recertificación Usuarios TFSE"
    textobject = c.beginText()
    textobject.setFont("Helvetica-Bold",18)
    textobject.setTextOrigin(50*mm, 265*mm)
    textobject.textLine(title)
    c.drawText(textobject)	
    logo = "./Toyota.png"
    c.drawImage(logo, 11, 275*mm, width = 40*mm, height = 20 *mm, mask='auto')
    page_num = c.getPageNumber()
    text = "%s" % page_num
    textobject2 = c.beginText()
    textobject2.setFont("Helvetica",12)
    textobject2.setTextOrigin(200*mm, 10*mm)
    textobject2.textLine(text)
    c.drawText(textobject2)	
    #c.drawRightString(200*mm, 10*mm, textobject2)	
#    c.showPage()	
#    c.save()	
    print "\nhere......\n"

def makePDF(uid, puestoTrabajo, rolesPuesto, rolesDeMas, rolesDeMenos):
    c = canvas.Canvas("./Informe.pdf", pagesize=A4)
    doc = SimpleDocTemplate("./Informe_"+uid+".pdf", pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=15)
    width, height = A4
    contents = []
    logo = "./Toyota.png"
    im = Image(logo, 4 * cm, 2 * cm)
    im.hAlign = 'LEFT'
    contents.append(im)
    texto1 = "Informe Toyota"
    styles = getSampleStyleSheet()
    title = Paragraph("Informe Recertificación Usuarios TFSE", styles["Title"])

    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=14, leftIndent=60))
    styles.add(ParagraphStyle(name='Justify1', alignment=TA_JUSTIFY, fontSize=12, leftIndent=65))
    styles.add(ParagraphStyle(name='Justify2', alignment=TA_JUSTIFY, fontSize=12, textColor='black', bulletIndent=75,
                              bulletFontSize=5))
    styles.add(ParagraphStyle(name='Justify3', alignment=TA_JUSTIFY, fontSize=12, textColor='blue', bulletIndent=83))
    styles.add(ParagraphStyle(name='Justify3r', alignment=TA_JUSTIFY, fontSize=12, textColor='red', bulletIndent=83))
    valor1 = []
    ptext = '<font size=12>%s</font>' % texto1
    contents.append(title)
    contents.append(Spacer(2 * cm, 1 * cm))
    contents.append(Paragraph("<b>Identificador: " + uid + "</b>", styles["Justify"]))
    contents.append(Spacer(3 * cm, 0.5 * cm))
    contents.append(Paragraph("Puesto de trabajo: " + puestoTrabajo, styles["Justify1"]))
    contents.append(Spacer(3 * cm, 0.3 * cm))
    contents.append(
        Paragraph("El puesto de trabajo " + puestoTrabajo + " tiene los siguientes roles", styles["Justify1"]))
    contents.append(Spacer(3 * cm, 0.2 * cm))
    for rp in rolesPuesto:
        rp = re.sub('<br>', '', rp)
        if rp.startswith('-'):
            if '*' in rp:
                valor1 = rp.split('*')
                contents.append(
                    Paragraph(re.sub('-', '', valor1[0]) + ":", styles["Justify2"], bulletText="\xe2\x96\xaa"))
                contents.append(Paragraph(valor1[1], styles["Justify3"], bulletText="\xe2\x80\xa2"))
        elif rp.startswith('*'):
            contents.append(Paragraph(re.sub('\*', '', rp), styles["Justify3"], bulletText="\xe2\x80\xa2"))

    contents.append(Spacer(3 * cm, 0.5 * cm))
    contents.append(
        Paragraph("Además de los roles de puesto de trabajo, el usuario tiene los siguientes roles adicionales:",
                  styles["Justify1"]))
    contents.append(Spacer(3 * cm, 0.2 * cm))
    # valor1=[]
    for rpm in rolesDeMas:
        rpm = re.sub('<br>', '', rpm)
        if rpm.startswith('-'):
            if '*' in rpm:
                valor1 = rpm.split('*')
                contents.append(
                    Paragraph(re.sub('-', '', valor1[0]) + ":", styles["Justify2"], bulletText="\xe2\x96\xaa"))
                contents.append(Paragraph(valor1[1], styles["Justify3r"], bulletText="\xe2\x80\xa2"))
        elif rpm.startswith('*'):
            contents.append(Paragraph(re.sub('\*', '', rpm), styles["Justify3r"], bulletText='*'))

    contents.append(Spacer(3 * cm, 0.5 * cm))
    contents.append(
        Paragraph("El usuario carece de los siguientes roles que pertenecen a la definición del puesto de trabajo:",
                  styles["Justify1"]))
    contents.append(Spacer(3 * cm, 0.2 * cm))
    # valor1=[]
    for rpm in rolesDeMenos:
        # rp = re.sub('<br>', '', rp)
        # contents.append(Paragraph(rp, styles["Justify2"], bulletText='-'))
        rpm = re.sub('<br>', '', rpm)
        if rpm.startswith('-'):
            if '*' in rpm:
                valor1 = rpm.split('*')
                contents.append(
                    Paragraph(re.sub('-', '', valor1[0]) + ":", styles["Justify2"], bulletText="\xe2\x97\xbe"))
                contents.append(Paragraph(valor1[1], styles["Justify3r"], bulletText='*'))
        elif rpm.startswith('*'):
            contents.append(Paragraph(re.sub('\*', '', rpm), styles["Justify3r"], bulletText="\xe2\x80\xa2"))

    #doc.build(contents, onFirstPage=addPageNumber(c, doc), onLaterPages=addPageNumber(c,doc))
    doc.build(contents)

def getAllUserForPDF2():
    uids= ['raul.lopez', 'joseluis.gonzalez', 'abdel.lamouri', 'abid.shehzad', 'alba.pickhardt', 'alberto.ortego',\
		  'hugo.ortega', 'gestor.valida', 'gestor.recobro']
    return uids 
	
	
def getAllUserForPDF():
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


def makePDFAll():
    c = canvas.Canvas("", pagesize=A4)
    doc = SimpleDocTemplate("./Informe_.pdf", pagesize=A4,
                            rightMargin=40, leftMargin=40,
                            topMargin=100, bottomMargin=45)
    #print "BLE"	
    width, height = A4
    contents = []
    logo = "./Toyota.png"
    im = Image(logo, 4 * cm, 2 * cm)
    im.hAlign = 'LEFT'
    #contents.append(im)
    texto1 = "Informe Toyota"
    styles = getSampleStyleSheet()
    title = Paragraph("Informe Recertificación Usuarios TFSE", styles["Title"])

    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=13, leading = 20, leftIndent=55))
    styles.add(ParagraphStyle(name='Justify0', alignment=TA_JUSTIFY, fontSize=12, spaceBefore= 5, leading = 10, leftIndent=60))
    styles.add(ParagraphStyle(name='Justify1', alignment=TA_JUSTIFY, fontSize=12, spaceBefore= 20, leading = 18, leftIndent=60))
    styles.add(ParagraphStyle(name='Justify2', alignment=TA_JUSTIFY, fontSize=11, leading = 13, rightIndent=80, leftIndent = 60, backColor = '#F0F0F0', textColor='black', bulletIndent=75,
                              bulletFontSize=5))
    styles.add(ParagraphStyle(name='Justify3', alignment=TA_JUSTIFY, fontSize=11, leading = 13, borderPadding = (0,0,3,0), rightIndent=80, leftIndent = 60, backColor = '#F0F0F0',textColor='blue', bulletIndent=83))
    styles.add(ParagraphStyle(name='Justify3r', alignment=TA_JUSTIFY, fontSize=11, leading = 13, borderPadding = (0,0,3,0), rightIndent=80, leftIndent = 60, backColor = '#F0F0F0', textColor='red', bulletIndent=83))
    valor1 = []
    uidss =[]	
    #contents.append(title)
    uidss = getAllUserForPDF()
    contador = 0	
    for uidd in uidss:
		print "\n=========================================================="
		print "\n\n+Doing user ....\n"
		print "\t*UID:"+uidd
		puestoTrabajo, rolesPuesto, rolesDeMas, rolesDeMenos	= rellenarUserForPDF(uidd)
		print "\n\tPUESTO TRABAJO ES: "+puestoTrabajo
		conts = contentsForEachUserForPDF (uidd, puestoTrabajo, rolesPuesto, rolesDeMas, rolesDeMenos, styles, contador)
		print "\n\tCreada con éxito página pdf con datos del usuario... "
		contents = contents + conts
		contador = contador +1
    doc.build(contents, onFirstPage=addPageNumberFirstPage, onLaterPages=addPageNumber)
    print "\n\n\nFin de PDF .....\n"	
	
def contentsForEachUserForPDF (uid, puestoTrabajo, rolesPuesto, rolesDeMas, rolesDeMenos, styles, contador):
    contents=[]
    if contador > 0:	
	    contents.append(PageBreak())
    #contents.append(Spacer(2 * cm, 1 * cm))
    contents.append(Paragraph("Identificador: " +"<b>"+ uid + "</b>", styles["Justify"]))
    #contents.append(Spacer(3 * cm, 0.5 * cm))
    contents.append(Paragraph("Puesto de trabajo: " + "<b>"+puestoTrabajo+ "</b>", styles["Justify0"]))
    #contents.append(Spacer(3 * cm, 0.3 * cm))
    contents.append(
        Paragraph("El puesto de trabajo " + puestoTrabajo + " tiene los siguientes roles:", styles["Justify1"]))
    #contents.append(Spacer(3 * cm, 0.2 * cm))
    for rp in rolesPuesto:
        rp = re.sub('<br>', '', rp)
        if rp.startswith('-'):
            if '*' in rp:
                valor1 = rp.split('*')
                contents.append(
                    Paragraph(re.sub('-', '', valor1[0]) + ":", styles["Justify2"], bulletText="\xe2\x96\xaa"))
                contents.append(Paragraph(valor1[1], styles["Justify3"], bulletText="\xe2\x80\xa2"))
        elif rp.startswith('*'):
            contents.append(Paragraph(re.sub('\*', '', rp), styles["Justify3"], bulletText="\xe2\x80\xa2"))
        #contents.append(Spacer(3 * cm, 0.05 * cm))

    #contents.append(Spacer(3 * cm, 0.5 * cm))
    contents.append(
        Paragraph("Además de los roles de puesto de trabajo, el usuario tiene los siguientes roles:",
                  styles["Justify1"]))
    #contents.append(Spacer(3 * cm, 0.2 * cm))
    # valor1=[]
    for rpm in rolesDeMas:
        #print "SEGUIMOS"
        rpm = re.sub('<br>', '', rpm)
        if rpm.startswith('-'):
            if '*' in rpm:
                valor1 = rpm.split('*')
                contents.append(
                    Paragraph(re.sub('-', '', valor1[0]) + ":", styles["Justify2"], bulletText="\xe2\x96\xaa"))
                contents.append(Paragraph(valor1[1], styles["Justify3r"], bulletText="\xe2\x80\xa2"))
        elif rpm.startswith('*'):
            contents.append(Paragraph(re.sub('\*', '', rpm), styles["Justify3r"], bulletText='*'))

    #contents.append(Spacer(3 * cm, 0.5 * cm))
    contents.append(
        Paragraph("El usuario carece de los siguientes roles pertenecientes a la definición del puesto de trabajo:",
                  styles["Justify1"]))
    #contents.append(Spacer(3 * cm, 0.2 * cm))
    # valor1=[]
    for rpm in rolesDeMenos:
        # rp = re.sub('<br>', '', rp)
        # contents.append(Paragraph(rp, styles["Justify2"], bulletText='-'))
        rpm = re.sub('<br>', '', rpm)
        if rpm.startswith('-'):
            if '*' in rpm:
                valor1 = rpm.split('*')
                contents.append(
                    Paragraph(re.sub('-', '', valor1[0]) + ":", styles["Justify2"], bulletText="\xe2\x97\xbe"))
                contents.append(Paragraph(valor1[1], styles["Justify3r"], bulletText='*'))
        elif rpm.startswith('*'):
            contents.append(Paragraph(re.sub('\*', '', rpm), styles["Justify3r"], bulletText="\xe2\x80\xa2"))
    #print "\n\n\nRETORNAMOS CONTENTS\n\n\n"			
    return contents


def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD', unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()


def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


def setpermscontrol(uid, rolesdefinicion, rolesdemas, rolesdemenos):
    print "\nwriting data in user...\n"
    user = Element('user')
    login = SubElement(user, 'login')
    login.text = uid
    base64 = SubElement(user, 'base64')
    base64.text = 'false'
    attributes = SubElement(user, 'attributes')

    branch_att = SubElement(user,'branch')
    branch_att.text = 'usuariosTFSE'
	
    # Permisos que debería tener el puesto [[[rolesDefinicionPuesto]]]
    rolesDefinicionPuesto_ = SubElement(attributes, 'atribute')
    base64_1 = SubElement(rolesDefinicionPuesto_, 'base64')
    base64_1.text = 'false'
    name_1 = SubElement(rolesDefinicionPuesto_, 'name')
    name_1.text = 'rolesDefinicionPuesto'
    for role in rolesdefinicion:
        value = SubElement(rolesDefinicionPuesto_, 'values')
        value.text = role

    # Permisos que faltan del puesto [[[rolesDeMenos]]]
    rolesDeMenos_ = SubElement(attributes, 'atribute')
    base64_1 = SubElement(rolesDeMenos_, 'base64')
    base64_1.text = 'false'
    name_1 = SubElement(rolesDeMenos_, 'name')
    name_1.text = 'rolesDeMenos'
    for role in rolesdemenos:
        value = SubElement(rolesDeMenos_, 'values')
        value.text = role

    # Permisos adicionales no definidos en el puesto [[[rolesDeMas]]]
    rolesDeMas_ = SubElement(attributes, 'atribute')
    base64_1 = SubElement(rolesDeMas_, 'base64')
    base64_1.text = 'false'
    name_1 = SubElement(rolesDeMas_, 'name')
    name_1.text = 'rolesDeMas'
    for role in rolesdemas:
        value = SubElement(rolesDeMas_, 'values')
        value.text = role

    # Ejecutamos llamada
    xml_request = tostring(user, 'utf-8')
    message = DAO.checkresponse(DAO.sendrequest('POST', 'user/', xml_request, 1))
    print message[1]


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



def getpuntodecision(idpuesto):
    '''Obtiene el punto de decisión relacionado con el puesto dado y devuelve los roles que modifica'''
    rolelist = []
    data = DAO.sendrequest('GET', 'decisionPoint', None, 1)
    message = DAO.checkresponse(data)
    if message[0]:
        response = ElementTree.fromstring(data)
        for dp in response[0]:
            if dp.find("roles/role") != None and dp.find("roles/role").text == idpuesto and 'PonerPuesto' in dp.find(
                    "cn").text:
                for group in dp.findall("groupsToAdd"):
                    rolelist.append(group.text)
                continue
    else:
        print message[1]
    return rolelist


def tab(string, ini):
    l = len(string) - 1
    t = ini - (l / 7)
    o = ""
    while t > 0:
        o = o + "\t"
        t = t - 1
    return o


def cross(uroles, tgroups, cache, cache2):
    '''Cruza los roles del usuario (uroles - dict) con los grupos del puesto (tgroups - list)'''
    print bcolors.BOLD + "------------------------- Permisos por puesto ---------------------------"
    print "| Permiso\t\t\t\t| Aplicativo\t\t\t| "
    print "-------------------------------------------------------------------------" + bcolors.ENDC
    for perm in tgroups:
        find = False
        for role, info in uroles.items():
            if role == 'Puesto' or info['father'] == 'PuestoDeTrabajo':
                del uroles[role]
            if role != 'Puesto' and perm == info['group']:
                print bcolors.OKGREEN + "| " + perm + tab(perm, 5) + "| " + info['father'] + tab(info['father'],
                                                                                                 3) + "\t|" + bcolors.ENDC
                del uroles[role]
                find = True
                continue
        if not find:
            print bcolors.FAIL + "| " + perm + tab(perm, 5) + "| " + cache2[perm] + tab(cache2[perm],
                                                                                        4) + "|" + bcolors.ENDC
    print bcolors.BOLD + "-------------------------------------------------------------------------" + bcolors.ENDC
    print ""
    print bcolors.BOLD + bcolors.WARNING + "-------------------------- Permisos Adicionales -------------------------"
    print "| Permiso\t\t\t\t| Aplicativo\t\t\t|"
    print "-------------------------------------------------------------------------" + bcolors.ENDC + bcolors.WARNING
    for perm, value in uroles.items():
        if perm != 'Puesto':
            print "| " + value['group'] + tab(value['group'], 5) + "| " + value['father'] + tab(value['father'],
                                                                                                4) + "|"
    print "-------------------------------------------------------------------------" + bcolors.ENDC
    print ""


def recertificar(userid):
    '''Obtiene todos los permisos del usuario y los compara con los que están asociados a su puesto'''
    try:
        # Cargar caches
        c = load_obj("roles")
        g = load_obj("grupos")
        # Obtener todos los roles del usuario
        r = getuserroles(userid, c)
        # Obtener punto de decisión relacionado con el puesto de trabajo y los roles que otorga
        if 'Puesto' in r:
            rg = getpuntodecision(r['Puesto'])
            # TODO Pasar a roles
            # Cruzar e imprimir resultados
            print bcolors.OKBLUE + bcolors.BOLD + "USUARIO: " + bcolors.ENDC + bcolors.OKBLUE + userid
            print bcolors.OKBLUE + bcolors.BOLD + "PUESTO: " + bcolors.ENDC + bcolors.OKBLUE + r[
                'Puesto'] + bcolors.ENDC
            cross(r, rg, c, g)
        else:
            print bcolors.FAIL + "El usuario " + userid + " no tiene un puesto válido" + bcolors.ENDC
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit()


def rellenarall():
    print "Actualizando todos los usuarios"
    try:
        data = DAO.sendrequest('GET', 'user', None, 0, 'branch=usuariosTFSE')
        message = DAO.checkresponse(data)
        if message[0]:
            response = ElementTree.fromstring(data)
            for child in response[0]:
                uid = child.get('uid')
                print "Actualizando permisos de " + str(uid)
                rellenar(uid)
        else:
            print message[1]
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit()








def getusergroups(userid, cache, gcache):
    '''Obtiene todos los roles del usuario devolviendo un dicionario que los contiene,
  en el que se marcan por defecto como permisos de aplicación'''
    # roles = {}
    roles = collections.OrderedDict()
    # data = DAO.sendrequest('GET', 'user/' + userid, None)
    data = DAO.sendrequest('GET', 'user/memberof/' + userid, None, 1)
    message = DAO.checkresponse(data)
    if message[0]:
        print "Ha entrado por aquí"
        response = ElementTree.fromstring(data)
        # for role in response[0][0].findall("attribute[@name='cn']"):
        for role in response[0]:
            # Crea una lista con los textos y su tipo
            bla = re.sub('cn=', '', role[1].text)
            ble = re.sub(',ou=grupos,ou=usuariosTFSE,dc=wbsvision,dc=es,dc=toyota-fs,dc=com', '', bla)
            ble = re.sub(',ou=grupos,dc=wbsvision,dc=es,dc=toyota-fs,dc=com', '', ble)
            print ble
            # if role.text in cache:
            if ble in cache:
                if cache[role.text]['father'] == 'PuestoDeTrabajo':
                    # if cache[ble]['father'] == 'PuestoDeTrabajo':
                    roles['Puesto'] = role.text
                    # roles['Puesto'] = ble
                roles[role.text] = cache[role.text]
            # roles[ble] = gcache[ble]
    else:
        print message[1]
    return roles


def rellenarr(userid):
    cache = load_obj("roles")
    gcache = load_obj("grupos")
    uroles = getuserroless(userid, cache)
    # print uroles
    # print getpuntodecision(uroles['Puesto'])
    if 'Puesto' in uroles:
        # print 'Puesto es: '+uroles['Puesto']
        dpgrupos = getpuntodecision(uroles['Puesto'])
        # print len(dpgrupos)
        # print dpgrupos
        # print "bla"
        for group in dpgrupos:
            # print group
            find = False
            for role, info in uroles.items():
                # print role
                # print info
                for r in info:
                    # print role, r
                    # print cache[r]['father']
                    # if role == 'Puesto' or cache[r]['father'] == 'PuestoDeTrabajo':
                    if role == 'Puesto':
                        # puestoTrabajo = uroles[role]
                        print "Puesto de trabajo: " + uroles[role]
                        passpuestoTrabajo = uroles[role]
                    # del uroles[role]
                    elif group == info['group']:
                        '''Encontrado!'''
                        valorGrupo = ""
                        valorGrupoSinMakeUp = ""
                        if (info['father'] not in '\t'.join(rolesdefinicion)):
                            valorGrupo = "<br>-<strong>" + info[
                                'father'] + "</strong>:<br><br><pre>   *" + group + "</pre>"
                            valorGrupoSinMakeUp = "-" + info['father'] + "*" + group
                            print "father no está"
                        else:
                            valorGrupo = "<pre>   *" + group.strip() + "</pre>"
                            valorGrupoSinMakeUp = "*" + group
                            print "father está"
                        rolesDefSinMakeUp.append(valorGrupoSinMakeUp)
                        rolesdefinicion.append(valorGrupo)
                        # del uroles[role]
                        find = True
                    continue


def rellenar(userid):
    ''' Rellena los attributos rolesDefinicionPuesto, rolesDeMas y rolesDeMenos de un usuario'''
    try:
        # Cargar caches
        cache = load_obj("roles")
        gcache = load_obj("grupos")
        # Inicializo listas
        rolesdefinicion = []
        rolesdemas = []
        rolesdemasSinMakeUp = []
        rolesdemenosSinMakeUp = []
        rolesdemenos = []
        rolesDefSinMakeUp = []
        # Obtener todos los roles del usuario
        uroles = collections.OrderedDict(getuserroles(userid, cache))
        # uroles = collections.OrderedDict(getusergroups(userid,cache,gcache))
        # Obtener punto de decisión relacionado con el puesto de trabajo y los roles que otorga
        if 'Puesto' in uroles:
            dpgrupos = getpuntodecision(uroles['Puesto'])
            # print "Grupos de dp son: "+str(dpgrupos)
            dictiorddemas = {}
            for group in dpgrupos:
                find = False
                for role, info in uroles.items():
                    #if role == 'Puesto' or info['father'] == 'PuestoDeTrabajo':
                    if role == 'Puesto':
                        puestoTrabajo = uroles['Puesto']
                        print "Puesto de trabajo: " + role
                        del uroles[role]
                    elif info['father'] == 'PuestoDeTrabajo':
                        puestoTrabajo = role
                        print "Puesto de trabajo: " + role
                        del uroles[role]
                    elif group == info['group']:
                        '''Encontrado!'''
                        valorGrupo = ""
                        valorGrupoSinMakeUp = ""
                        if (info['father'] not in '\t'.join(rolesdefinicion)):
                            valorGrupo = "<br>-<strong>" + info[
                                'father'] + "</strong>:<br><br><pre>   *" + group + "</pre>"
                            valorGrupoSinMakeUp = "-" + info['father'] + "*" + group
                            print "father no está"
                        else:
                            valorGrupo = "<pre>   *" + group.strip() + "</pre>"
                            valorGrupoSinMakeUp = "*" + group
                            print "father está"
                        rolesDefSinMakeUp.append(valorGrupoSinMakeUp)
                        rolesdefinicion.append(valorGrupo)
                        del uroles[role]
                        find = True
                        continue
                if not find:
                    if (gcache[group] not in '\t'.join(rolesdemenos)):
                        rolesdemenos.append('<br>-<strong>' + gcache[
                            group] + '</strong>:<br><br><pre>   <font color="red">*' + group + '</font></pre>')
                        rolesdemenosSinMakeUp.append("-" + gcache[group] + '*' + group)
                    else:
                        rolesdemenos.append('<pre>   <font color="red">*' + group.strip() + '</font></pre>')
                        rolesdemenosSinMakeUp.append('*' + group)
            for perm, value in uroles.items():
                if perm != 'Puesto':
                    if (value['father'] not in dictiorddemas):
                        dictiorddemas[value['father']] = [value['group']]
                    else:
                        dictiorddemas[value['father']].append(value['group'])

            print dictiorddemas
            for padre, valor in dictiorddemas.items():
                for i, pos in enumerate(valor):
                    if i == 0:
                        rolesdemasSinMakeUp.append("-" + padre + '*' + pos)
                        print 'Con padre'
                    else:
                        rolesdemasSinMakeUp.append('*' + pos)
                        print "Sin padre"

            print ("POR PUESTO: ", rolesDefSinMakeUp)
            print ("FALTA: ", rolesdemenosSinMakeUp)
            print ("ADICIONALES: ", rolesdemasSinMakeUp)
            makePDF(userid, puestoTrabajo, rolesDefSinMakeUp, rolesdemasSinMakeUp, rolesdemenosSinMakeUp)

            # Guardamos resultados
            setpermscontrol(userid, rolesdefinicion, rolesdemas, rolesdemenos)
        else:
            print "El usuario " + userid + " no tiene un puesto válido"
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit()
		
def rellenarUserForPDF(userid):
    print "\n\t\tGetting info for "+userid
    ''' Rellena los attributos rolesDefinicionPuesto, rolesDeMas y rolesDeMenos de un usuario'''
    try:
        # Cargar caches
        cache = load_obj("roles")
        gcache = load_obj("grupos")
        # Inicializo listas
        puestoTrabajo =""
        rolesdefinicion = []
        rolesdemas = []
        rolesdemasSinMakeUp = []
        rolesdemenosSinMakeUp = []
        rolesdemenos = []
        rolesDefSinMakeUp = []
        # Obtener todos los roles del usuario
        uroles = collections.OrderedDict(getuserroles(userid, cache))
        # Obtener punto de decisión relacionado con el puesto de trabajo y los roles que otorga
        if 'Puesto' in uroles:
            print "\n\t\tUsuario tiene puesto...!!!!!\n"
            dpgrupos = getpuntodecision(uroles['Puesto'])
            dictiorddemas = {}
            dictiorddemenos = {}
            for group in dpgrupos:
                find = False
                for role, info in uroles.items():
                    if role == 'Puesto':
                        puestoTrabajo = uroles['Puesto']
                        del uroles[role]
                    elif info['father'] == 'PuestoDeTrabajo':
                        puestoTrabajo = role
                        del uroles[role]
                    elif group == info['group']:
                        '''Encontrado!'''
                        valorGrupo = ""
                        valorGrupoSinMakeUp = ""
                        if (info['father'] not in '\t'.join(rolesDefSinMakeUp)):
                            valorGrupoSinMakeUp = "-" + info['father'] + "*" + group
                        else:
                            valorGrupoSinMakeUp = "*" + group
                        rolesDefSinMakeUp.append(valorGrupoSinMakeUp)
                        del uroles[role]
                        find = True
                        continue
                if not find:
                    if (gcache[group] not in '\t'.join(rolesdemenosSinMakeUp)):
                        rolesdemenosSinMakeUp.append("-" + gcache[group] + '*' + group)
                    else:
                        rolesdemenosSinMakeUp.append('*' + group)
            for perm, value in uroles.items():
                if perm != 'Puesto':
                    if (value['father'] not in dictiorddemas):
                        dictiorddemas[value['father']] = [value['group']]
                    else:
                        dictiorddemas[value['father']].append(value['group'])

#            for perm, value in uroles.items():
#                if perm != 'Puesto':
#                    if (value['father'] not in dictiorddemenos):
#                        dictiorddemenos[value['father']] = [value['group']]
#                    else:
#                        dictiorddemenos[value['father']].append(value['group'])

            #print dictiorddemas
            for padre, valor in dictiorddemas.items():
                for i, pos in enumerate(valor):
                    if i == 0:
                        rolesdemasSinMakeUp.append("-" + padre + '*' + pos)
                        #print 'Con padre'
                    else:
                        rolesdemasSinMakeUp.append('*' + pos)
                        #print "Sin padre"
#            for padre, valor in dictiorddemenos.items():
#                for i, pos in enumerate(valor):
#                    if i == 0:
#                        rolesdemenosSinMakeUp.append("-" + padre + '*' + pos)
#                        #print 'Con padre'
#                    else:
#                        rolesdemenosSinMakeUp.append('*' + pos)
                        #print "Sin padre"
            #print textwrap.fill("JODER",width = 30)
            wrapper = textwrap.TextWrapper(initial_indent=' ' *20, width=140,subsequent_indent=' '*20)
            filled_text = textwrap.fill(str(rolesDefSinMakeUp),width = 30)
            #print (textwrap.indent("hostia puta",'EVEN ', predicate=should_indent))
            #print (textwrap.fill(str(rolesDefSinMakeUp),initial_indent=' '*20, subsequent_indent=' ' * 20,width = 160))
            #print wrapper.fill(str(rolesDefSinMakeUp))
            #print (str(rolesDefSinMakeUp)).ljust(100)
            print "\t\t------------------------------------"
            print "\t\tPOR PUESTO: ", "\n"+wrapper.fill(str(rolesDefSinMakeUp))
            print "\t\tFALTA: ", "\n"+wrapper.fill(str(rolesdemenosSinMakeUp))
            print "\t\tADICIONALES: ", "\n"+wrapper.fill(str(rolesdemasSinMakeUp))
            print "\t\t------------------------------------"
            #makePDF(userid, puestoTrabajo, rolesDefSinMakeUp, rolesdemasSinMakeUp, rolesdemenosSinMakeUp)

            # Guardamos resultados
            # Guardamos resultados
            #setpermscontrol(userid, rolesdefinicion, rolesdemas, rolesdemenos)
            #print "Retornado "
        else:
            print "El usuario " + userid + " no tiene un puesto válido"
    except:
        #traceback.print_exc(file=sys.stdout)
        #sys.exit()
		pass
    #return puestoTrabajo, rolesdefinicion, rolesdemas, rolesdemenos	
    #print "\nSEGUIMOS AQUI... \n" 
    return puestoTrabajo,  rolesDefSinMakeUp, rolesdemasSinMakeUp, rolesdemenosSinMakeUp

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
            userid = raw_input("Introduzca id de usuario a recertificar:-")
            recertificar(userid)
            printmenu()
        elif op == 3:
            userid = raw_input("Introduzca id de usuario a recertificar:-")
            rellenar(userid)
            printmenu()
        elif op == 4:
            #rellenarall()
            makePDFAll()
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
