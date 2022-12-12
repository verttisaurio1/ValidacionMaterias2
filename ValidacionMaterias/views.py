from django.template import Context ,Template
from pickle import GET
from django.shortcuts import render , HttpResponse ,redirect
from ValidacionMaterias.models import Materia,PlanEstudio,Etapa,TipoMateria,Carrera,PlanEstudioCarrera,PlanEstudioCarreraMateria,RegistroEquivalenciaComparativa
import pandas as pd
import xlrd
 
# Create your views here.
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
        return render(request,"ValidacionMaterias/Subir_Kardex.html",context)
    elif request.method == 'POST':
        if 'boton_subir' in request.POST:
            return render(request,"ValidacionMaterias/Subir_Kardex.html",context)
        elif 'document' in request.FILES:
            archivo = request.FILES['document']
            print("tengo un archivo")
            name = archivo.name
            handle_file(archivo,name)
            

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
 

def alumno_Equivalencia(request):
    
    idpcDE = 4
    idpcA = 3

    kardex=leer_kardex('ValidacionMaterias/static/ValidacionMaterias/Kardex/prueba.xls')

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

    if len(mnp) == 0:
        context= {
            
            "nombre":kardex['nombre'],
            "ap_pat":kardex['ap_pat'],
            "ap_mat":kardex['ap_mat'],
            "carrera":kardex['carrera'],
            "matricula":matricula,
            "planDe":kardex['plan'],
            "equivalencia":alumno_equivalencia
        }


    else:
        context= {
            "nombre":kardex['nombre'],
            "ap_pat":kardex['ap_pat'],
            "ap_mat":kardex['ap_mat'],
            "carrera":kardex['carrera'],
            "matricula":matricula,
            "planDe":kardex['plan'],
            "equivalencia":alumno_equivalencia,
            "mnp":mnp
        }
    

    

    return render(request,"ValidacionMaterias/Alumno_Equiavalencia.html",context)
    

    
