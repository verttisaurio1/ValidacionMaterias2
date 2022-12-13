from django.urls import path
from ValidacionMaterias import views

# Esto sirve para direccionar con el name que se le da al path
app_name = 'aplication'

urlpatterns = [
    
    path('home/',views.home ,name="home"),
    path('',views.home ,name="home"),
    path('Agregar_Plan/',views.Agregar_plan ,name="Agregar_Plan"),
    path('Agregar_Carrera/',views.Agregar_carrera ,name="Agregar_Carrera"),
    path('Agregar_Materia/',views.Agregar_materia ,name="Agregar_Materia"),
    path('Registro_Materias/',views.Registro_materias ,name="Registro_Materias"),
    path('Editar_Materia/',views.Editar_materia ,name="Editar_Materia"),
    path('Editar_Materia/',views.Editar_materia ,name="Editar_Materia"),
    path('Agregar_Carrera_Plan/',views.Agregar_Carrera_Plan,name="Agregar_Carrera_Plan"),
    path('Agregar_Materia_Plan/',views.Agregar_materia_Plan,name="Agregar_Materia_Plan"),
    
    path('Subir_Kardex/',views.Subir_Kardex,name="Subir_Kardex"),
    path('Elegir_Acreditacion/',views.Elegir_Acreditacion,name="Elegir_Acreditacion"),

    #path('vista_pdf/',views.pdf,name="vista_pdf"),

    path('test/',views.test,name="test"),

    path('fun_search/',views.fun_search_materia),
    path('fun_a_materia/',views.fun_a_materia),
    
    path('Equivalencia/',views.Equivalencia,name="Equivalencia"),
    path('Equivalencia/actualizar_Tabla_<int:idplanDE>_<int:idplanA>/',views.actualizar_Tabla,name="actualizar_Tabla"),
    path('update_Equivalencia_<int:id>_<int:idplanDE>_<int:idplanA>_<int:ban>/',views.update_Equivalencia,name='update_Equivalencia'),
    path('update_Equivalencia_elaborar_<int:id>_<int:idmat>_<int:idplanDE>_<int:idplanA>/',views.update_Equivalencia_elaborar,name='update_Equivalencia_elaborar'),
    
    #equivalencia alumno
    path('alumno_Equivalencia_<str:nombre>/',views.alumno_Equivalencia,name="alumno_Equivalencia"),
    
]