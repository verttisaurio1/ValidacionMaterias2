from django.template import Context ,Template
from pickle import GET
from django.shortcuts import render , HttpResponse ,redirect
from ValidacionMaterias.models import Materia,PlanEstudio,Etapa,TipoMateria,Carrera,PlanEstudioCarrera,PlanEstudioCarreraMateria,RegistroEquivalenciaComparativa
import pandas as pd
import xlrd
from fpdf import FPDF 
from datetime import date
from datetime import datetime
from django.http import FileResponse 
# Create your views here.

def current_date_format(date):
    #definir fecha actual
     months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
     day = date.day
     month = months[date.month - 1]
     year = date.year
     messsage = "{} de {} del {}".format(day, month, year)

     return messsage






context = Context({"resp": " "})
def home(request):
    return render(request,"ValidacionMaterias/home.html")

def Agregar_plan(request):
    context = {}
    if request.method == 'GET':
            return render(request,"ValidacionMaterias/Agregar_Plan.html",context)
    elif request.method == 'POST':
        if PlanEstudio.objects.filter(NombrePlanEstudio=(request.POST["nombre_plan"])):
            context = { "resp" : "Este Plan ya esta registrada"}
            return render(request,"ValidacionMaterias/Agregar_Plan.html",context)

        planE = PlanEstudio(NombrePlanEstudio = request.POST['nombre_plan'], Estatus = True)
        planE.save()
        context = { "resp" : "Registrado Correctamente"}
        return render(request,"ValidacionMaterias/Agregar_Plan.html",context)  
        
        
        
def Agregar_carrera(request):
    context = {}
    if request.method == 'GET':
            return render(request,"ValidacionMaterias/Agregar_Carrera.html",context)
    elif request.method == 'POST':
        
        if Carrera.objects.filter(ClaveCarrera=(request.POST["clave_Carrera"])):
            context = { "resp" : "Esta Clave ya esta registrada"}
            return render(request,"ValidacionMaterias/Agregar_Carrera.html",context)
        carrera = Carrera(ClaveCarrera = request.POST['clave_Carrera'], NombreCarrera = request.POST['nombre_Carrera'], Estatus = True)
        carrera.save()
        context = { "resp" : "Registrado Correctamente"}
        return render(request,"ValidacionMaterias/Agregar_Carrera.html",context)



def Agregar_Carrera_Plan(request):
    context = {}
    carreras= Carrera.objects.all()
    planes= PlanEstudio.objects.all()
    if request.method == 'GET':
            
        return render(request,"ValidacionMaterias/Agregar_Carrera_Plan.html",{"carreras":carreras ,"planes":planes})
    elif request.method == 'POST':
        EstudioCarera = PlanEstudioCarrera(idCarrera_id = request.POST['select_carrera'], idPlanEstudio_id = request.POST['select_plan'])
        EstudioCarera.save()
        return render(request,"ValidacionMaterias/Agregar_Carrera_Plan.html",{"carreras":carreras ,"planes":planes,"resp":"Registrado Correctamente"})

def Agregar_materia_Plan(request):
    context = {}
    etapas = Etapa.objects.all()
    tipos = TipoMateria.objects.all()
    planes = PlanEstudio.objects.all()
    carreras = Carrera.objects.all()
    planescarrera = PlanEstudioCarrera.objects.all()
    
    context['etapas'] = etapas
    context['tipos'] = tipos
    context['planes'] = planes
    context['carreras'] = carreras
    context['planescarrera'] = planescarrera

    
    if request.method == 'GET':
        return render(request,"ValidacionMaterias/Agregar_Materia_Plan.html",context)
        
    elif request.method == 'POST':
        if 'submit_search' in request.POST:
            clave = request.POST["clave"]
            try:
                materia = Materia.objects.get(ClaveMateria = clave)
                context['materia'] = materia
                context['alerta'] = 'bien'
            except Materia.DoesNotExist:
                context['alerta'] = 'mal'
                
            
            return render(request,"ValidacionMaterias/Agregar_Materia_Plan.html",context)
        
        elif 'submit_plan' in request.POST:
            idPlanEstudioCarrera = request.POST['planes']
            planEstudioCarrera = PlanEstudioCarrera.objects.get(idPlanEstudioCarrera = idPlanEstudioCarrera)
            
            idMateria= request.POST['display_id']
            materia1 = Materia.objects.get(idMateria = idMateria)
            
            idTipoMateria =request.POST['tipo']
            tipoMateria = TipoMateria.objects.get(idTipoMateria = idTipoMateria)
            
            idEtapa =request.POST['etp']
            etapa = Etapa.objects.get(idEtapa = idEtapa)
            
            Estatus = True
            materia_plan = PlanEstudioCarreraMateria(idPlanEstudioCarrera=planEstudioCarrera, idMateria=materia1, idTipoMateria=tipoMateria,idEtapa=etapa, Estatus=Estatus)
            materia_plan.save()
        return render(request,"ValidacionMaterias/Agregar_Materia_Plan.html",context)
    

        

def Agregar_materia(request):
    return render(request,"ValidacionMaterias/Agregar_Materia.html")

def Registro_materias(request):
    return render(request,"ValidacionMaterias/Registro_Materias.html")

def Editar_materia(request):
    return render(request,"ValidacionMaterias/Editar_Materia.html")


    

def Subir_Kardex(request):
    context = {}
    if request.method == 'GET':
        context['bandera'] = False
        return render(request,"ValidacionMaterias/Subir_Kardex.html",context)
    elif request.method == 'POST':
        if 'boton_subir' in request.POST:
            #añadimos datos subidos al contexto y mandamos a la siguiente vista
            context['nombre'] = request.POST['nombre']
            context['ap_pat'] = request.POST['ap_pat']
            context['ap_mat'] = request.POST['ap_mat']
            context['carrera'] = request.POST['carrera']
            context['matricula'] = request.POST['matricula']
            context['plan_de_estudios'] = request.POST['plan_de_estudios']
            context['archivo'] = request.POST['archivo']
            print(context)
            #reemplazar este return por el de la siguiente vista
            #return redirect('alumno_Equivalencia/',context)
            return redirect('aplication:alumno_Equivalencia',nombre=str(context['archivo']),n_alum=str(context['nombre']),ap_p_alum=str(context['ap_pat']),ap_m_alum=str(context['ap_mat']))
            #return render(request,"ValidacionMaterias/Alumno_Equivalencia.html",context)
        elif 'document' in request.FILES:
            archivo = request.FILES['document']
            print("tengo un archivo")
            name = archivo.name
            handle_file(archivo,name)
            kardex = leer_kardex('ValidacionMaterias/static/ValidacionMaterias/Kardex/' +name)
            context['nombre']= kardex['nombre']
            context['ap_pat']= kardex['ap_pat']
            context['ap_mat']= kardex['ap_mat']
            context['carrera']= kardex['carrera']
            context['matricula']= kardex['matricula']
            context['plan_de_estudios']= kardex['plan']
            context['archivo'] = name
            context['bandera'] = True
                
            items = []
            for llave in kardex['materias']:
                contenido = kardex['materias'][llave]
                if(len(contenido)>7):
                    an_item = dict(clave=contenido[0],materia=contenido[1],creditos=contenido[2],tipo=contenido[3],calif=contenido[4],fecha=contenido[5],periodo=contenido[7])
                else:    
                    an_item = dict(clave=contenido[0],materia=contenido[1],creditos=contenido[2],tipo=contenido[3],calif=contenido[4],fecha=contenido[5],periodo=contenido[6])
                items.append(an_item)   
            
            context['materias'] = items
            return render(request,"ValidacionMaterias/Subir_Kardex.html",context)


def Elegir_Acreditacion(request):
    return render(request,"ValidacionMaterias/Elegir_Acreditacion.html")



def prueba(request):
    return render(request,"ValidacionMaterias/prueba.html")

def fun_a_materia(request):
    if Materia.objects.filter(ClaveMateria=(request.GET["clave"])):
        context = { "resp" : "Esta clave ya esta registrada"}
        return render(request,"ValidacionMaterias/Agregar_Materia.html",context)
    context = { "resp" : "Registrado Correctamente"}
    materia= Materia(ClaveMateria= request.GET["clave"],NombreMateria=request.GET["nombre"],Creditos=request.GET["creditos"])
    materia.save()
    return render(request,"ValidacionMaterias/Agregar_Materia.html",context)

def fun_search_materia(request):
    if Materia.objects.filter(ClaveMateria=(request.POST["clav"])):
        materia=Materia.objects.get(ClaveMateria=(request.POST["clav"]))
        return render(request,"ValidacionMaterias/Agregar_Plan.html",materia)
    

def test(request):
    context = {}
    planestudio = PlanEstudio.objects.all()
    carreras = Carrera.objects.all()
    Relacion = PlanEstudioCarrera.objects.all()
    
    materias = Materia.objects.all() 
    relacionMaterias = PlanEstudioCarreraMateria.objects.all()
    
    context["planestudio"] = planestudio
    context["carreras"]   = carreras
    context["Relacion"] = Relacion    
    context["materias"] = materias    
    context["relacionMaterias"] = relacionMaterias    

    
    return render(request,"ValidacionMaterias/test.html",context)

def handle_file(file, name):
    with open('ValidacionMaterias/static/ValidacionMaterias/Kardex/' + name,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def leer_kardex(archivo):
    kardex = {}
    wb = archivo
    documento = xlrd.open_workbook(wb, encoding_override='ISO-8859-1')
    sh = documento.sheet_by_index(0)

    #obtener nombre
    nombre_completo = pd.read_excel(documento, skiprows=9 - 1, usecols='I', nrows=1, header=None, names=["Value"]).iloc[0]["Value"]
    

    #separar nombre 
    lista = nombre_completo.split(" ")
    ap_mat = lista.pop()
    ap_pat = lista.pop()
    nombre = ""
    nombre = " ".join(lista)

    #obtener carrera
    carrera = pd.read_excel(documento, skiprows=7 - 1, usecols='I', nrows=1, header=None, names=["Value"]).iloc[0]["Value"]
    

    #obtener matricula
    matricula = pd.read_excel(documento, skiprows=9 - 1, usecols='G', nrows=1, header=None, names=["Value"]).iloc[0]["Value"]


    #obtener plan de estudios
    plan_de_estudios = pd.read_excel(documento, skiprows=9 - 1, usecols='AR', nrows=1, header=None, names=["Value"]).iloc[0]["Value"]

    contador_ciclo = 0
    contador_renglon = 0
    contador_columna = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
                    'AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM','AN','AO','AP','AQ','AR','AS','AT')
    materias={}
    while contador_ciclo < sh.nrows:
        renglon = str(pd.read_excel(documento, skiprows=contador_ciclo, usecols='A', nrows=1, header=None, names=["Value"]).iloc[0]["Value"])
        if(renglon != "nan"):
            lista = []
            for columna in contador_columna:
                contenido = str(pd.read_excel(documento, skiprows=contador_ciclo, usecols=columna, nrows=1, header=None, names=["Value"]).iloc[0]["Value"])
                if(contenido != "nan"):
                    lista.append(contenido)
            
            if(lista[4].isnumeric()):
                if(int(lista[4])>60):
                    materias[contador_renglon] = lista
                    contador_renglon = contador_renglon + 1
            else:
                if(lista[4] not in ("NP","SD")):
                    materias[contador_renglon] = lista
                    contador_renglon = contador_renglon + 1
        contador_ciclo = contador_ciclo + 1
    
    #aqui en teoria hay que meter los datos al diccionario kardex
    #seria algo como  kardex["cosa"] = cosa
    kardex['nombre'] = nombre
    kardex['ap_pat'] = ap_pat
    kardex['ap_mat'] = ap_mat
    kardex['carrera'] = carrera
    kardex['matricula'] = matricula
    kardex['plan'] = plan_de_estudios
    kardex['materias'] = materias
    #finalmente regresamos el diccionario con un return kardex
    return kardex




# guarda el las materias asosiados a plan estudio carrera del registro de equivalencia para moder mostrar a las tablas y tener accesoa los datos
class Registro_Materias:
    def __init__(self,id,mde,ma):
        self.id=id
        self.mde=mde
        self.ma=ma

# Asigna un sin equivalencia a las materias del plan estudio carrera seleccionada a donde se dirige
def Equivalencia(request):
    carrera_planListadas = PlanEstudioCarrera.objects.all()
    
    if request.method =="POST":
         
        
        #Datos del desplegable plan estudio carrera "DE"
        carrera_planDE = request.POST['planCarreraDe']
        
        #Datos del desplegable plan estudio carrera "A"
        carrera_planA = request.POST['planCarreraA']

        # verifica si los datos no son los mismos
        if  int(carrera_planDE) == int(carrera_planA):
             return render(request,"ValidacionMaterias/Equivalencia.html",{"cpl":carrera_planListadas,"cpDE":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=carrera_planDE),"cpA":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=carrera_planA)})
        
        #Todos los registros de las tablas comparativas
        registros = RegistroEquivalenciaComparativa.objects.all()

        # lista donde se guardaran todos id que ya estan asociados 
        datos_Equivalencia = []

        #Filtrar datos de los registros con respecto a los planes de estudio carrera seleccionados
        for r in registros:
            materiaDe = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaDe)
            materiaA = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaA)
            
           #filtra los datos de los planes estudio carrera seleccionados a los registros
            if int(materiaDe.idPlanEstudioCarrera.idPlanEstudioCarrera) == int(carrera_planDE) and int(materiaA.idPlanEstudioCarrera.idPlanEstudioCarrera) ==  int(carrera_planA):
                # Se guardaran todos los ids que coinsidan
                datos_Equivalencia.append(int(materiaDe.idPlanEstudioCarreraMateria))

        # filtra las materias de plan estudio carrera DE
        materiasDe = PlanEstudioCarreraMateria.objects.filter(idPlanEstudioCarrera=carrera_planDE)
        # filtra las materias de plan estudio carrera A
        materiasA = PlanEstudioCarreraMateria.objects.filter(idPlanEstudioCarrera=carrera_planA)
        
        ##### Dame el id que contega la clave 0 osea sin equivalencia de el plan estudio carrera DE
        clave = 1
        for m in materiasA:
            if int(m.idMateria.ClaveMateria) == 0:
                clave = m.idPlanEstudioCarreraMateria
        if clave == 1:
            return render(request,"ValidacionMaterias/Equivalencia.html",{"cpl":carrera_planListadas,"cpDE":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=carrera_planDE),"cpA":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=carrera_planA)})

        # si los datos de los planes estudio carrera seleccionados a los registros es igual a cero asigna a todos los datos un sin equivalencia
        if len(datos_Equivalencia) == 0:
            for m in materiasDe:
                    if int(m.idMateria.ClaveMateria) != 0:
                       
                        reg = RegistroEquivalenciaComparativa(idMateriaDe=m.idPlanEstudioCarreraMateria,idMateriaA=clave)
                        reg.save()
        else:
            # de lo contrario verifica a cuales les puedes asignar un sin equivalencia para no afectar el registro anterior
            for m in materiasDe:
                if int(m.idPlanEstudioCarreraMateria) not in datos_Equivalencia:
                    if int(m.idMateria.ClaveMateria) != 0:
                        reg = RegistroEquivalenciaComparativa(idMateriaDe=m.idPlanEstudioCarreraMateria,idMateriaA=clave)
                        reg.save()
 
        return redirect('aplication:actualizar_Tabla',idplanDE = carrera_planDE,idplanA = carrera_planA)
                  
    return render(request,"ValidacionMaterias/Equivalencia.html",{"cpl":carrera_planListadas})



def actualizar_Tabla(request,idplanDE,idplanA):

    materiasDE = PlanEstudioCarreraMateria.objects.filter(idPlanEstudioCarrera=idplanDE)
    for m in materiasDE:
        if int(m.idMateria.ClaveMateria) == 0:
            clave = m.idPlanEstudioCarreraMateria

    #Todos los registros de las tablas comparativas
    registros = RegistroEquivalenciaComparativa.objects.all()

    #listas donde se guardaran las materias de donde proviene, a donde va y su respectivo identificador de equivalencia

    datos_Equivalencia = []

    #Filtrar datos de los registros con respecto a los planes de estudio carrera seleccionados
    for r in registros:
        materiaDe = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaDe)
        materiaA = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaA)
            
        if int(materiaDe.idPlanEstudioCarrera.idPlanEstudioCarrera) == int(idplanDE) and int(materiaA.idPlanEstudioCarrera.idPlanEstudioCarrera) ==  int(idplanA) :
            
            # Se guardara el objeto para tener acceso al: identificador del registro, su materiaDE y su materiaA
            datos_Equivalencia.append(Registro_Materias(r.idRegistroEquivalenciaComparativa,materiaDe,materiaA))

 
    return render(request,"ValidacionMaterias/Actualizar_tablas.html",{"Registro_Equivalencias": datos_Equivalencia,"idplanDE":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=idplanDE),"idplanA":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=idplanA)})

def update_Equivalencia(request,id,idplanDE,idplanA,ban):
    
    materias = PlanEstudioCarreraMateria.objects.filter(idPlanEstudioCarrera=idplanA)
    # bandera donde identifica que la materia seleccionada no esta repetida
    if ban == 0:
        return render(request,"ValidacionMaterias/Editar_equivalencia.html",{"id_registro":id,"idplanDE":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=idplanDE),"idplanA":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=idplanA),"materias":materias})
    
    # bandera donde identifica que la materia seleccionada esta repetida
    if ban == 1:
        return render(request,"ValidacionMaterias/Editar_equivalencia.html",{"id_registro":id,"idplanDE":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=idplanDE),"idplanA":PlanEstudioCarrera.objects.get(idPlanEstudioCarrera=idplanA),"materias":materias,"mensaje":"Esta materia ya se encuentra en la equivalencia se leccione otra porfavor"})

def update_Equivalencia_elaborar(request,id,idmat,idplanDE,idplanA):

    registros = RegistroEquivalenciaComparativa.objects.all()

    materiasA = PlanEstudioCarreraMateria.objects.filter(idPlanEstudioCarrera=idplanA)
    for m in materiasA:
        if int(m.idMateria.ClaveMateria) == 0:
            clave = m.idPlanEstudioCarreraMateria

    for r in registros:
        materiaDe = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaDe)
        materiaA = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaA)
            
        if int(materiaDe.idPlanEstudioCarrera.idPlanEstudioCarrera) == int(idplanDE) and int(materiaA.idPlanEstudioCarrera.idPlanEstudioCarrera) ==  int(idplanA):
            if int(r.idRegistroEquivalenciaComparativa) != int(id): #no tomes encuenta el registro seleccionado
                if int(clave) != int(materiaA.idPlanEstudioCarreraMateria): # no tomes en cuenta los sin equivalencia ya que estos si se pueden repetir
                    if int(materiaA.idPlanEstudioCarreraMateria) == int(idmat): # si una de las materias de los registros guardados es igual a la que quieres adjuntar, mandara un mensaje de error
                        return redirect('aplication:update_Equivalencia',id=id,idplanDE=idplanDE,idplanA=idplanA,ban=1) 

    # en el caso que no se hiciera el redirect anterior,"Elabora la edicion de la equivalencia"  
    id_registro = id
    registro= RegistroEquivalenciaComparativa.objects.get(idRegistroEquivalenciaComparativa=id_registro)
    registro.idMateriaA=int(idmat)
    registro.save()
   
    # redireccioname a las tablas de equivalencia
    return redirect('aplication:actualizar_Tabla',idplanDE=idplanDE,idplanA= idplanA)



class datos_materias:
    def __init__(self,mde,ma,examen,cali,periodo):
        
        self.mde = mde
        self.ma = ma
        self.examen = examen
        self.cali = cali
        self.periodo = periodo

class materias_no_plan:
    def __init__(self,clave,nombre,creditos,examen,cali,periodo):
        
        self.clave = clave
        self.nombre = nombre
        self.creditos = creditos
        self.examen = examen
        self.cali = cali
        self.periodo = periodo
 

def alumno_Equivalencia(request,nombre,n_alum,ap_p_alum,ap_m_alum):
    auxpc = PlanEstudioCarrera.objects.all()
    carrera_planListadasA = []
    carrera_planListadasDE = auxpc
    for cp in auxpc:
        
        carreras = PlanEstudioCarreraMateria.objects.filter(idPlanEstudioCarrera=cp.idPlanEstudioCarrera)
        for m in carreras:
            if int(m.idMateria.ClaveMateria) == 0:
                carrera_planListadasA.append(cp)
    if request.method =="POST":
        if 'pdf' in request.POST: # boton generar pdf
            print('*******pdf******')
            doc_pdf = open('ValidacionMaterias/static/ValidacionMaterias/pdfs/' + request.POST["archivo_pdf"], 'rb')

            return FileResponse(doc_pdf)
        else:
            carrera_planListadas = PlanEstudioCarrera.objects.all()
            #Datos del desplegable plan estudio carrera "DE"
            idpcDE = request.POST['planCarreraDe']
        
            #Datos del desplegable plan estudio carrera "A"
            idpcA = request.POST['planCarreraA']
            kardex=leer_kardex('ValidacionMaterias/static/ValidacionMaterias/Kardex/'+ nombre)

            #Todos los registros de las tablas comparativas
            registros = RegistroEquivalenciaComparativa.objects.all()

            # lista donde se guardaran todos id que ya estan asociados 
            datos_Equivalencia = []

            #Filtrar datos de los registros con respecto a los planes de estudio carrera seleccionados
            for r in registros:
                materiaDe = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaDe)
                materiaA = PlanEstudioCarreraMateria.objects.get(idPlanEstudioCarreraMateria=r.idMateriaA)
                
                #filtra los datos de los planes estudio carrera seleccionados a los registros
                if int(materiaDe.idPlanEstudioCarrera.idPlanEstudioCarrera) == int(idpcDE) and int(materiaA.idPlanEstudioCarrera.idPlanEstudioCarrera) ==  int(idpcA):
                    # Se guardaran todos los ids que coinsidan
                    datos_Equivalencia.append(Registro_Materias(r.idRegistroEquivalenciaComparativa,materiaDe,materiaA))
                    

            materias = kardex['materias'].values()
            alumno_equivalencia = []
            claves = []
            mnp = []

            for m in materias:
                for e in datos_Equivalencia:
                    if len(m) == 7:
                        if int(m[0]) == int(e.mde.idMateria.ClaveMateria): 
                            alumno_equivalencia.append(datos_materias(e.mde,e.ma,m[3],m[4],m[6]))
                            claves.append(int(m[0]))
                    elif len(m) == 8:
                        if int(m[0]) == int(e.mde.idMateria.ClaveMateria): 
                            alumno_equivalencia.append(datos_materias(e.mde,e.ma,m[3],m[4],m[7])) 
                            claves.append(int(m[0]))
            for m in materias:
                if int(m[0]) not in claves:
                
                    if len(m) == 7:
                        mnp.append(materias_no_plan(m[0],m[1],m[2],m[3],m[4],m[6]))
                    elif len(m) == 8:
                        mnp.append(materias_no_plan(m[0],m[1],m[2],m[3],m[4],m[7]))

            matricula = kardex['matricula']
            
            aux= matricula[2:] 
            matricula= aux[0] +  aux[2:] 
            plande= PlanEstudioCarrera.objects.get(idPlanEstudioCarrera =idpcDE) # filtra datos 
            plana = PlanEstudioCarrera.objects.get(idPlanEstudioCarrera =idpcA) # filtra datos
            if len(mnp) == 0:
                context= {
                    "cplDE":carrera_planListadasDE,
                    "cplA":carrera_planListadasA,
                    "nombre":kardex['nombre'],
                    "ap_pat":kardex['ap_pat'],
                    "ap_mat":kardex['ap_mat'],
                    "carrera":kardex['carrera'],
                    "matricula":matricula,
                    "planDe":kardex['plan'],
                    "equivalencia":alumno_equivalencia,
                    "ban":True,
                    "idplanDE":plande,
                    "idplanA":plana
    
                }


            else:
                context= {
                    "cplDE":carrera_planListadasDE,
                    "cplA":carrera_planListadasA,
                    "nombre":kardex['nombre'],
                    "ap_pat":kardex['ap_pat'],
                    "ap_mat":kardex['ap_mat'],
                    "carrera":kardex['carrera'],
                    "matricula":matricula,
                    "planDe":kardex['plan'],
                    "equivalencia":alumno_equivalencia, # lista de todas las materias equivalentes
                    "mnp":mnp,  # lista de materias que no estan en el plan 
                    "ban":True,
                    "idplanDE":plande,
                    "idplanA":plana
                }

                nombre_pdf = n_alum # nombre del alumno ap_p_alum,ap_m_alum
                ap_pat_pdf = ap_p_alum # apellido pat del alumno
                ap_mat_pdf = ap_m_alum # apellido mat del alumno
                matricula_pdf = matricula # matricula del alumno
                tablas_equivalencia_pdf = alumno_equivalencia # materias del alumno y sus equivalencias
                tablas_no_plan_pdf = mnp # materias que no se encuentran en el plan
                nombre_carrera_de_pdf = plande.idCarrera.NombreCarrera # nombre de la carrera DE
                nombre_carrera_a_pdf  = plana.idCarrera.NombreCarrera   # nombre de la carrera A
                plan_estudio_de_pdf =   plande.idPlanEstudio.NombrePlanEstudio  # plan de estudio DE
                plan_estudio_a_pdf =   plande.idPlanEstudio.NombrePlanEstudio   # plan de estudio A

                #preparo datos
                nombre_comp = f"{nombre_pdf}  {ap_pat_pdf}  {ap_mat_pdf}"
                lista_listas = []
                for e in tablas_equivalencia_pdf:
                    lista_datos = [str(e.mde.idMateria.ClaveMateria), str(e.mde.idMateria.NombreMateria), str(e.cali), str(e.examen), str(e.mde.idMateria.Creditos),str(e.periodo),    
                    str(e.ma.idMateria.ClaveMateria), str(e.ma.idMateria.NombreMateria), str(e.cali), str(e.examen), str(e.ma.idMateria.Creditos), str(e.periodo)]   
                    lista_listas.append(lista_datos)                                     
                for m in tablas_no_plan_pdf:
                    lista_datos = [str(m.clave), str(m.nombre), str(m.cali), str(m.examen), str(m.creditos), str(m.periodo), str(m.clave), 
                                   str(m.nombre), str(m.cali), str(m.examen), str(m.creditos), str(m.periodo)]
                    lista_listas.append(lista_datos)
                TABLE_COL_NAMES = ("Clave","Materia","Calif","Exa","Cred","Periodo","Clave","Materia","Calif","Exa","Cred","Periodo")    
                COLUMN_WIDTH =    (10,        40,      11,     10,   9,     15,       10,     40,       11,    10,   9,     15)   
                    
                #aqui se genera el pdf
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Times", size=8)
                line_height = pdf.font_size * 3.5
                col_width = pdf.epw / 12  # distribute content evenly
                spacing=3
                print(col_width)
                print(pdf.epw)
                
                
                #header
                pdf.set_xy(50,0.0)
                pdf.set_font('Arial','',16)
                pdf.cell(w=100,h=50,align= 'C',txt='Universidad Autonoma de Baja California \n  ',border=0)
                pdf.set_xy(48,10)
                pdf.cell(w=100,h=50,align= 'C',txt='Facultad de Ingenieria Arquitectura y Diseño ',border=0)
                pdf.set_font('Arial','',12)
                pdf.set_xy(10,35)
                pdf.cell(w=100,h=50,align= 'L',txt='A quien corresponda ',border=0)

                pdf.set_xy(0,45)
                pdf.cell(w=210,h=50,txt=' Por medio de la presente solicito de la manera más atenta se haga la acreditación de las asignaturas que se ',border=0)
                pdf.set_xy(0,50)
                pdf.cell(w=210,h=50,txt=f' menciona en el cuadro del alumno {nombre_comp} con matrícula {matricula_pdf} del plan de estudios',border=0)
                pdf.set_xy(0,55)
                pdf.cell(w=210,h=50,txt=f'{plan_estudio_de_pdf} de {nombre_carrera_de_pdf}',border=0)
                #pdf.fecha()
                now = datetime.now()
                today= current_date_format(now)
                pdf.set_xy(100,25)
                pdf.set_font('Arial','',12)
                pdf.cell(w=100,h=50,align= 'R',txt='Ensenada,Baja California a '+today,border=0)

                
                
                
                #body
                pdf.set_font("Times", size=8)
                pdf.set_y(90)
                def render_table_header():
                    pdf.set_font(style="B")  # enabling bold text
                    contador = 0 
                    for col_name in TABLE_COL_NAMES:
                        pdf.cell(COLUMN_WIDTH[contador], line_height, col_name, border=1)
                        contador+=1
                    pdf.ln(line_height)
                    pdf.set_font(style="")  # disabling bold text
                render_table_header()
                for row in lista_listas:
                    if pdf.will_page_break(line_height):
                        render_table_header()
                    contador2=0
                    for datum in row:
                        pdf.multi_cell(COLUMN_WIDTH[contador2], line_height,align='C', txt=datum, border=1, ln=3, max_line_height=pdf.font_size)
                        #pdf.cell(COLUMN_WIDTH[contador2], line_height, datum, border=1)
                        contador2+=1
                    pdf.ln(line_height)
                    
                    
                #pdf.footer()
                pdf.set_font('Arial','',12)
                pdf.cell(w=100,h=25,align= 'L',txt='Sin más por el momento quedo a sus apreciables órdenes para cualquier aclaración ',border=0)
                y = pdf.get_y()
                print(y) 
                pdf.set_line_width(0.2)
                pdf.set_draw_color(r=0, g=0, b=0)
                pdf.line(x1=30, y1=y+50, x2=90, y2=y+50)
                pdf.line(x1=110, y1=y+50, x2=170, y2=y+50)
                
                pdf.set_xy(45,y+50)
                pdf.cell(w=30,h=12,align= 'C',txt='Nombre de Acreditador',border=0)
                pdf.ln(5)
                pdf.set_x(45)
                pdf.cell(w=30,h=12,align= 'C',txt='Cargo',border=0)
                pdf.ln(5)
                pdf.set_x(45)
                pdf.cell(w=30,h=12,align= 'C',txt='Carrera',border=0)
                
                pdf.set_xy(125,y+50)
                pdf.cell(w=30,h=12,align= 'C',txt='Nombre de Subdirector',border=0)
                pdf.ln(5)
                pdf.set_x(125)
                pdf.cell(w=30,h=12,align= 'C',txt='Cargo',border=0)
                pdf.ln(5)
                pdf.set_x(125)
                pdf.cell(w=30,h=12,align= 'C',txt='Carrera',border=0)
                
                
                
                archivo_pdf = matricula_pdf + "_pdf.pdf"
                pdf.output('ValidacionMaterias/static/ValidacionMaterias/pdfs/' + archivo_pdf,dest='f')
                context['archivo_pdf'] = archivo_pdf

            return render(request,"ValidacionMaterias/Alumno_Equiavalencia.html",context)
    context = {"cplDE":carrera_planListadasDE,"cplA":carrera_planListadasA,}
    return render(request,"ValidacionMaterias/Alumno_Equiavalencia.html",context)
    

