from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import datetime
import apin24

class objectIn():

    __url_base = 'https://www.inmuebles24.com/'
    __dict_url = {'venta_casa' : 'casas-en-venta.html', 'venta_depto' : 'departamentos-en-venta.html',
                  'venta_terreno' : 'terrenos-en-venta.html', 'in24' : 'inmuebles.html' }

    
    __final_dict = {}
    __tmp_dict = {}


    __values = ['postingId', 
                'postingCode', 
                'title', 
                #'prices',
                'descriptionNormalized',
                'generatedTitle',
                'pictures',
                'reserved',
                'mainFeatures',
                'url',
                'postingLocation',
                'priceOperationTypes',
                #'status',
                'postingType',
                'publication',
                'realEstateType',
                ]

    __actual_page = 1
    __list_of_register = []
    __t = 0
    __number_of_result = 0
    __number_of_pages = 0
    __number_init_page = 0
    __number_for_page = 20
    __final_page = 0
    __debug = False
    __actual_select_url = ''
    __driver = 0
    __id_p = ''
    __result_actual_page = ''
    __path_output = ''

    def __init__(self, nThread, id_p, path_out='', debug=False):
        """__init__ Inicializa el objeto.

        Args:
            id_p (str) : número identificatorio de Id
            nThread (int): El número de hilo que esta corriendo
            path_out (str, optional) : salida donde iran los archivos generados.
            debug (bool, optional): Si esta en modo debug, en general es 
            util porque guarda archivos con los resultados. Defaults to False.
        """
        self.__t = nThread
        self.__debug = debug
        self.__id_p = id_p
        self.__path_output = path_out + str(nThread) + "/"
        self.__driver = webdriver.Chrome(ChromeDriverManager().install())


    def setFinalPage(self, final_page):
        """setFinalPage

        Args:
            final_page (int): la ultima pagina a la que debe llegar

        Returns:
            bool : si devuelve True es que se pudo setear el valor.
            False en caso contrario.
        """
        if isinstance(final_page, int):
            self.__final_page= final_page
            return True
        else:
            return False


    def getNumberResult(self):
        """getNumbreResult -> obtenemos los datos que hay
        para realizar el scaping
        Returns:
            (int, int) : (numero de resultados, numero de paginas ) 
        """
        url = self.__url_base + self.__dict_url['in24']
        self.__driver.get(url)
        input('Presione enter luego de verificar el captcha...')
        self.__driver.get(url)
        time.sleep(5)
        #cargamos el contenido de la primer pagina.
        self.__result_actual_page = self.__driver.page_source
        #-------------------------------------------------------
        cons_string = 'const totalPosting'
        #Buscaremos el valor de cons_string y separaremos el texto. quedandonos
        #con la parte posterior a esa constante.
        tmp_cad = self.__result_actual_page.split(cons_string)[1]
        #Iniciaremos un resporte desde "=" hasta ";" y desaparecen esos valores y los espacios
        #en blanco.
        tmp_cad = tmp_cad[tmp_cad.find("=")+1:tmp_cad.find(';')].strip()
        #realizamos una limpieza sobre la cadena, quitando las comas.
        tmp_cad = tmp_cad.replace(",","")
        #quitamos los ' para finalmente quede un número, por las dudas quitamos espacios en blanco
        tmp_cad = tmp_cad.replace("'","").strip()
        self.__number_of_result = int(tmp_cad)
        self.__number_of_pages = round(self.__number_of_result / self.__number_for_page) + 1
        print('------------------------------------------------------------------------')
        print('El número de resultado es: {} registros.'.format(self.__number_of_result))
        print('El número de paginas es: {} paginas.\n'.format(self.__number_of_pages))
        print('------------------------------------------------------------------------')
        return (self.__number_of_result, self.__number_of_pages)



    def openPage(self):
        url = self.__url_base + self.__dict_url['in24']
        if self.__number_init_page != 1:
             url = url.split('.html')[0] + '-pagina-{}.html'.format(str(self.__number_init_page))
        else:
            self.__actual_page = self.__number_init_page
        self.__driver.get(url)
        input('Presione enter luego de verificar el captcha... t:{}'.format(self.__t))
        self.__driver.get(url)
        time.sleep(5)
        #cargamos el contenido de la primer pagina.
        self.__result_actual_page = self.__driver.page_source
        #debug
        if self.__debug == True:
            self.__saveFile('./result.txt', self.__result_actual_page)
        #obtener el número de registros disponibles
        self.__get_dict()
        for page in range(self.__number_init_page, self.__final_page+1):
            print('thread: {} - i - {} f - {} - url: {}'.format(self.__t,
                                                                self.__number_init_page,
                                                                self.__final_page+1,
                                                                page))
            self.__actual_page = page
            elemt = self.__driver.find_elements_by_class_name('pag-go-next')[0]
            elemt.click()
            time.sleep(2)
            self.__driver.refresh()
            time.sleep(3)
            self.__result_actual_page = self.__driver.page_source
            if self.__debug == True:
                self.__saveFile('basic_scrap' + str(page) + '.txt', self.__result_actual_page)
            self.__get_dict()          
        if self.__debug == True:
            self.__saveFile('final_dict'+ str(page) +'.txt', str(self.__final_dict))
        return True

    def setNumberPageInit(self,page):
        if isinstance(page, int):
            self.__number_init_page = page
            return True
        else:
            return False

    def setNumberForPage(self, pages):
        if isinstance(pages, int):
            self.__number_for_page = pages
            return True
        else:
            return False
    
    def closeDriver(self):
        self.__driver.close()


    def getCategories(self):
        return self.__dict_url


    def __saveFinalDict(self):
        cont = 0
        #empezamos a recorrer el dict temporal
        for key, value in self.__tmp_dict.items():
            #Creamos un dict temporal 
            tmp_dict = {}
            #Recorremos los valores completos
            for k,v in self.__tmp_dict[key].items():
                if k in self.__values:
                    tmp_dict[k] = v
            #Si esta en desarrollo lo filtramos Es lo único que filtramos por el momento.
            #if tmp_dict['postingType'] == 'DEVELOPMENT':
            #    pass
            #else:
                #Caso contrario agramos el diccionario.
            if self.__debug == True:
                self.__saveFile('dict'+str(cont)+'.txt', str(tmp_dict))
                cont +=1
            self.__final_dict[value[self.__values[0]]] = self.__clearDict(tmp_dict)
        if self.__debug == True:
            self.__saveFile(self.__path_output + str(self.__actual_page) + '.in', str(self.__final_dict))
        apin24.saveR(self.__final_dict)
        self.__saveFile(self.__path_output + 'c.in', str(self.__actual_page))
        self.__final_dict = {}
        self.__tmp_dict = {}



    def __saveFile(self, name_file, text):
        #Agregamos un archivo para que nos quede el backup
        if self.__debug == True:
            name_file = './debug/' + name_file
        file = open(name_file, 'w')
        file.write(text)
        file.close()

    def __get_dict(self):
        #primer delimitador, a partir de line1 estan todos los datos que necesitamos.
        line1 = "const listPostings = ["
        #Dividimos y tomamos el restante.
        subString = self.__result_actual_page.split(line1)[1]
        #llegamos al final separado po } ]; y tomamos la parte anterior pero bolsamos 
        #agregar el  '}' al fina para que quede como corresponde
        subString = subString.split("} ];")[0] + "}"
        subString = subString.replace("null,", "\"\",") #remplazamos valores null, por "," 
        subString = subString.replace("null"," \"\" ")  #ahora solamente null por ""
        subString = subString.replace(" false", "\"False\"") #para que python no chille false x False
        subString = subString.replace(" true", "\"True\"") #para que python no chille true x True
        #partimos desde la cadena que sigue que denota cada uno de los caracteres
        posicion = subString.split("""{
  "postingId" : """)
        #Comenzamos a recorrer desde la posición 1 el primero esta vacio.
        for i in range(1, len(posicion)):
            #para para que quede completo volvemos a agregar la primer parte
            posicion[i] = "{ \"postingId\" : " + posicion[i]
            #Si es el ultimo no tiene coma al final
            if len(posicion) - 1 == i:
                #si entro aqui es el último caracter
                self.__tmp_dict[i-1] = json.loads(posicion[i])
            else:
                #si entro aqui no es el ultimo y termina en  '}, '
                self.__tmp_dict[i-1] = json.loads(posicion[i][:-2])

        self.__saveFinalDict()
        self.__result_actual_page = ''

    def __clearDict(self, n):
        dict_db = {}
        #diccionarios
        main = {}
        location = {}
        prices = {}
        features = {}
        description = {}

        main['postingId']       = str(n['postingId'])
        main['postingCode']     = str(n['postingCode'])
        main['title']           = str(n['title'])
        main['url']             = str(n['url'])
        main['reserved']        = False if n['reserved']=='False' else True
        main['status_online']   = True
        
        main['type_prop']        = str(n['realEstateType']['name'])
        main['id_scrap'] = str(self.__id_p)
        main['publication_null_date'] = '1900-01-01'
        #obtenemos fecha de publicacion
        tmp = n['publication']['firstDateOnline']
        tmp = str(tmp['yearOfEra']) + "-" + str(tmp['monthOfYear']) + "-" + str(tmp['dayOfMonth'])
        main['publication_date'] = tmp 


        
        #Direccion
        tmp = n['postingLocation']
        if 'name' in tmp['address']:
            location['address'] = tmp['address']['name']
        else:
            location['addresses'] = tmp['address']
        location['postingId'] = main['postingId']
        location['zone'] = ''
        location['city']  = ''
        location['province'] = ''
        location['country'] = 'Mexico'
        for k, v in tmp['location'].items():    
            if k == 'name':
                location['zone'] = v
            if k == 'parent':
                for k1, v1, in v.items():
                    if k1 == 'name':
                        location['city'] = v1
                    if k1 == 'parent':
                        for k2, v2 in v1.items():
                            if k2 == 'name':
                                location['province'] = v2
                            if k2 == 'parent':
                                if isinstance(v2, dict):
                                    for k3, v3 in v2.items():
                                        if k3 == 'name':
                                            location['country'] = v3
        #if 'geolocation' in tmp
        main['lat']             = 0
        main['lon']             = 0
        if 'geolocation' in tmp['postingGeolocation']:
            main['lat'] = tmp['postingGeolocation']['geolocation']['latitude']
            main['lon'] = tmp['postingGeolocation']['geolocation']['longitude']
        #main['status_online'] = if(n['status']=='ONLINE')    
        main['postingType'] = n['postingType']
        
        tmp = 0
        #PRICES
        tmp2 = n['priceOperationTypes']
        prices['expenses'] = 0
        if 'expenses' in tmp2:
            prices['expenses'] = tmp['expenses']
        main['renta'] =False
        main['sale'] = False
        main['tmp_rent'] = False

        #Prices
        prices['renta_price'] = 0
        prices['sale_price'] = 0
        prices['renta_currency'] = 'MN'
        prices['sale_currency'] = 'MN'
        prices['tmp_rent'] = 0
        prices['tmp_rent_currency'] = 'MN'
        for item in tmp2:
            iTipo = []
            iPrecio = []
            for k, v in item.items():
                if k == 'operationType':
                    if v['name'] == 'Venta':
                        iTipo.append('Venta')
                    if v['name'] == 'Renta':
                        iTipo.append('Renta')
                    if v['name'] == 'Temporal/Vacacional':
                        iTipo.append('Temporal/Vacacional')
                if k == 'prices':
                    iPrecio.append([v[0]['amount'], v[0]['currency']])
            for i in range(0, len(iTipo)):
                if iTipo[i] == 'Venta':
                    main['sale'] = True
                    prices['sale_price'] = float(iPrecio[i][0])
                    prices['sale_currency'] = iPrecio[i][1]
                    prices['sale_update_field'] = datetime.now().strftime('%Y-%m-%d')
                if iTipo[i] == 'Renta':
                    main['renta'] = True
                    prices['renta_price'] = float(iPrecio[i][0])
                    prices['renta_currency'] = iPrecio[i][1]
                    prices['renta_update_field'] = datetime.now().strftime('%Y-%m-%d')
                if iTipo[i] == 'Temporal/Vacacional':
                    main['tmp_rent'] = True
                    prices['tmp_renta_price'] = float(iPrecio[i][0])
                    prices['tmp_renta_currency'] = iPrecio[i][1]
                    prices['tmp_renta_update_field'] = datetime.now().strftime('%Y-%m-%d')
                

        tmp2 = 0
        prices['postingId'] = main['postingId']
        #Features
        tmp3 = n['mainFeatures']
        
        features_dict = {'CFT2' : 'rooms',
                        'CFT3' : 'bath_room',
                        'CFT4' : 'half_bath_room',
                        'CFT7' : 'parking',
                        'CFT5' : 'antiquity'}
        
        for k, v in features_dict.items():
            features[v] = 0
            if k in tmp3:
                if k == 'CFT5':
                    if tmp3[k]['value'] == 'A estrenar':
                        tmp3[k]['value'] = -1
                    if tmp3[k]['value'] == 'En construcción':
                        tmp3[k]['value'] = -2
                features[v] = int(tmp3[k]['value'])
        
        features['postingId'] = main['postingId']
        features['plot_size'] = 0
        features['measure_plot_size'] = 'm²'
        features['build_size']= 0
        features['measure_build_size'] = 'm²' 
        #print(features)       
        if 'CFT100' in tmp3:
            features['plot_size'] = int(tmp3['CFT100']['value'])
            features['measure_plot_size'] = tmp3['CFT100']['measure']
        if 'CFT101' in tmp3:
            features['build_size'] = int(tmp3['CFT101']['value'])
            features['measure_build_size'] = tmp3['CFT101']['measure']
        tmp3 = 0
        #Pictures
        tmp4 = n['pictures']

        #description
        description['postingId'] = main['postingId']
        description['description'] = str(n['descriptionNormalized'])
        description['generatedTitle']  = str(n['generatedTitle'])
        
        tmpDict = { }
        listPictures = []
        for tmpPicture in tmp4:
            tmpDict['postingId'] = main['postingId']
            tmpDict['url100x75'] = tmpPicture['url100x75']
            tmpDict['url360x266'] = str(tmpPicture['url360x266'])
            tmpDict['url1200x1200'] = str(tmpPicture['url1200x1200'])
            tmpDict['title'] = str(tmpPicture['title'])
            listPictures.append(tmpDict)
        dict_db['inmuebles'] = main
        dict_db['prices'] = prices 
        dict_db['location'] = location
        dict_db['features'] = features
        dict_db['description'] = description
        dict_db['pictures'] = listPictures
        return dict_db