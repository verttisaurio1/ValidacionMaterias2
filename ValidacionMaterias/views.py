from django.template import Context ,Template
from pickle import GET
from django.shortcuts import render , HttpResponse ,redirect
from ValidacionMaterias.models import Materia,PlanEstudio,Etapa,TipoMateria,Carrera,PlanEstudioCarrera,PlanEstudioCarreraMateria
import pandas

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