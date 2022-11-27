from django.urls import path
from ValidacionMaterias import views

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

    path('test/',views.test,name="test"),
    path('fun_search/',views.fun_search_materia),
    path('fun_a_materia/',views.fun_a_materia),
    

]