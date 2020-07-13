from objectIn import objectIn
from datetime import datetime
from random import randint
import os
import threading
from os import listdir
from os.path import isfile, isdir



dictProject = {'id': '',
               'nThreads' : 1,
               'init' : '',
               'finish' : '',
               'total_register' : 0,
               'total_page'     : 0,
               'author'         : '',
               'range'          : [],
                }

path_output = 'output/'
path_head = path_output + 'head/'
path_body = path_output + 'body/'

def checkDirs():
    if (os.path.isdir(path_output)==False):
        print('Creando Carpeta Output...')
        try:
            os.mkdir(path_output)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        print('Ok -> Carpeta Output')
    
    if (os.path.isdir(path_head)==False):
        print('Creando Carpeta Head')
        try:
            os.mkdir(path_head)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        print('Ok -> Carpeta Head')
    
    if (os.path.isdir(path_body)==False):
        print('Creando Carpeta Body')
        try:
            os.mkdir(path_body)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    else:
        print('Ok -> Carpeta Body')

def startBot(nThread, id_p, init, final, path_out):
    objT = objectIn(nThread=nThread, id_p=id_p, path_out=path_out)
    objT.setNumberPageInit(int(init))
    objT.setFinalPage(int(final))
    objT.openPage()
    objT.closeDriver()
    pass

def createProject():
    tmp_cad  = str(randint(1000, 9999))
    tmp_cad += str(datetime.now().strftime('%m%d'))
    id_p     = int(tmp_cad)
    dictProject['id'] = id_p
    print(""" 
        Comenzara la generación de un nuevo proyecto de scrap
        la clave para el nuevo proyecto es:
        id -----> {} <-----
        Ahora configuararemos algunos datos
    """.format(str(id_p))
        )
    number = True
    while(number):
        nThreads = input('Ingrese el número de hilos que desea crear: ')
        try:
            nThreads = int(nThreads)
            if nThreads <= 5:
                number = False 
            else:
                print('El entero ingresado no puede ser mayor que 5')
        except ValueError:
            print('No ha ingresado un entero')
    dictProject['nThreads'] = nThreads
    author = input('Ingresar un nombre que identifique quien realiza el scrap: ')
    dictProject['author'] = author
    print("""
            ----------- Preparando Archivos -------------
          """)
    dictProject['init'] = getDate()
    #checkeamos que existan los directorios que corresponden.
    checkDirs()
    #Creamos el directorio del proyecto en body
    final_out = path_body + tmp_cad + '/'
    try:
        print('creando la carpeta del proyecto')
        os.mkdir(path_body + tmp_cad + '/')
        for i in range(1, nThreads+1):
            os.mkdir(final_out + str(i) + '/')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    print("""
            ----------- Recogeremos datos --------------
            Lo que sigue es la recolección de datos basicos
            para que podamos generar el proyecto y empezar a trabajar
            haremos con un thread una recopilación de datos necesario
            tendras que pasar chaptchas por cada hilo... 
            ahora continuamos ...
            --------------------------------------------
    """)
    #Obtenes mos datos que necestiamos para generar los archivos 
    #base para trabajar posteriormente.

    obj1 = objectIn(nThread=1, path_out=final_out, id_p=id_p)
    dictProject['total_register'], dictProject['total_page'] = obj1.getNumberResult()
    
    
    #calcularemos los rangos donde pueden ir los distintos archivos corriendo.
    factor = int(round(dictProject['total_page'] / nThreads))
    listRange = [(1,factor)]
    for i in range(1, nThreads):
        if nThreads == i+1:
            listRange.append(((factor*i)+1, dictProject['total_page']))
        else:
            listRange.append(((factor*i)+1,(factor*i)+factor))
    dictProject['range'] = listRange
    
    print('\n Generando el archivo Cabecera')     
    writeFile(path_head + tmp_cad, str(dictProject))
    print('Desplegando hilo 1: ira desde la pagina: {} hasta la {}'.format(listRange[0][1],listRange[0][0]))
    obj1.setFinalPage(int(listRange[0][1]))
    obj1.setNumberPageInit(int(listRange[0][0]))
    print("""
            A continuación abriremos los hilos, necesitamos que resuelvan 
            todos los capthas antes de continuar
           """)
    threads= []
    for i in range(1, len(listRange)):
        print(i,'-',listRange[i], listRange[i])
        t = threading.Thread(target=startBot, args=(i+1, id_p, listRange[i][0], listRange[i][1], final_out))
        threads.append(t)
        t.start()

    obj1.openPage()
    obj1.closeDriver()
    input('Ha terminado el proceso de una, usted esta mal de la cabeza... presione enter')
    dictProject['finish'] = getDate()
    
def ls1(path):    
    return [obj for obj in listdir(path) if isfile(path + obj)]
def openProject():
    checkDirs()
    control = True
    while(control):
        print("""


                Listaremos los proyectos disponibles.
                

            """)
        
        files = ls1(path_head)
        for name in files:
            print(name)
        proj = input('Seleccione un nombre de archivo y presione enter: ')
        if os.path.isfile(path_head+proj):
            hProject = eval(openFile(path_head+proj))
            print(str(hProject))
            listRange = hProject['range']
            #controlaremos los iniciales de cada uno
            cThreads = hProject['nThreads']

            threads = []
            for i in range(1, cThreads+1):
                final_out = path_body+str(hProject['id'])+'/'
                r = int(openFile(final_out +str(i)+'/c.in')) + 1
                #nListRange.append((r, listRange[i-1][1]))
                #print(i,'-',listRange[i], listRange[i])
                t = threading.Thread(target=startBot, args=(i, hProject['id'], r, listRange[i-1][1], final_out))
                threads.append(t)
                t.start()
            control=False
        else:
            print('El nombre no es correcto')


def getDate():
    temp = datetime.now().strftime('%Y-%m-%d')
    return temp
    
def writeFile(name, text):
    file = open(name, 'w')
    file.write(text)
    file.close()

def upProject():
    print("""
        -----------------Comenzaremos a subir un proyecto -----------------
         """)


def openFile(name):
    file = open(name, 'r')
    text = file.read()
    return text
            
def main():
    again = True 
    while(again):
        print("""


                --------------------in24 Web Scrapping-------------------
                Author :    Manuel Barros  
                date:       2020-07-11
                Email:      dev.manuel.barros@gmail.com
                ----------------------------------------------------------

                Seleccionar una opción:

                1 - Crear un nuevo proyecto de scrap
                2 - Continuar un proyecto de scrap
                3 - Subir un proyecto.
                4 - Salir


        """)
        value = input("Ingrese la opción deseada y presiones 'Enter': ")
        if value == '1':
            createProject()
        if value == '2':
            openProject()
        if value == '4':
            upProject()
        if value == '4':
            again = False
            print("""Muchas gracias por probar el scrap escribime a: 
                                                    || dev.manuel.barros@gmail.com ||
                    Saludos!!!!...
                    """)

#Inicializamos el Scraper.
if __name__ == "__main__":
    main()