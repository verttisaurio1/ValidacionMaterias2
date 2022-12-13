from django.db import models
from re import A
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

from django.utils.translation import gettext_lazy as _

# Create your models here.
class PlanEstudio(models.Model):
    idPlanEstudio = models.AutoField(primary_key=True)
    NombrePlanEstudio=models.CharField(max_length=10,blank=False)
    Estatus = models.BooleanField(blank=False)
    def __str__(self):
        return f"{self.NombrePlanEstudio}"

class Carrera(models.Model):
    idCarrera= models.AutoField(primary_key=True)
    ClaveCarrera= models.IntegerField(blank=False)
    NombreCarrera= models.CharField(max_length=50,blank=False)
    Estatus= models.BooleanField(blank=False)
    def __str__(self):
        return f"{self.NombreCarrera}"

class TipoMateria(models.Model):
    idTipoMateria = models.AutoField(primary_key=True)
    NombreMateria= models.CharField(max_length=20,blank=False)

class Etapa(models.Model):
    idEtapa = models.AutoField(primary_key=True)
    NombreEtapa= models.CharField(max_length=20,blank=False)

class Materia(models.Model):
    idMateria = models.AutoField(primary_key=True)
    ClaveMateria= models.IntegerField(blank=False)
    NombreMateria= models.CharField(max_length=20,blank=False)
    Creditos= models.IntegerField(blank=False)

class PlanEstudioCarrera(models.Model):
    idPlanEstudioCarrera = models.AutoField(primary_key=True)
    idPlanEstudio= models.ForeignKey(PlanEstudio,blank=False,on_delete=models.CASCADE)
    idCarrera= models.ForeignKey(Carrera,blank=False,on_delete=models.CASCADE)

class PlanEstudioCarreraMateria(models.Model):
    idPlanEstudioCarreraMateria = models.AutoField(primary_key=True)
    idPlanEstudioCarrera= models.ForeignKey(PlanEstudioCarrera,blank=False,on_delete=models.CASCADE)
    idMateria= models.ForeignKey(Materia,blank=False,on_delete=models.CASCADE)
    idTipoMateria= models.ForeignKey(TipoMateria,blank=False,on_delete=models.CASCADE)
    idEtapa= models.ForeignKey(Etapa,blank=False,on_delete=models.CASCADE)
    #Semestre= models.CharField(max_length=20,blank=False)
    Estatus= models.BooleanField(blank=False)

class RegistroEquivalenciaComparativa(models.Model):
    idRegistroEquivalenciaComparativa = models.AutoField(primary_key=True)
    idMateriaDe = models.IntegerField(blank=False)
    idMateriaA = models.IntegerField(blank=False)

class DetalleAcreditacion(models.Model):
    idDetalleAcreditacion = models.AutoField(primary_key=True)
    idPlanEstudioCarreraMateriaDE= models.ForeignKey(PlanEstudioCarreraMateria,blank=False,on_delete=models.CASCADE)
    CalificacionDE= models.FloatField(blank=False)
    TipodeExamenDE=models.CharField(max_length=10,blank=False)
    PeriodoDE=models.CharField(max_length=10,blank=False)
    #idPlanEstudioCarreraMateriaA= models.ForeignKey(PlanEstudioCarreraMateria,blank=False,on_delete=models.CASCADE)
    CalificacionA= models.FloatField(blank=False)
    TipodeExamenA=models.CharField(max_length=10,blank=False)
    PeriodoA=models.CharField(max_length=10,blank=False)

class Alumno(models.Model):
    idAlumno = models.AutoField(primary_key=True)
    idCarrera=models.ForeignKey(Carrera,blank=False,on_delete=models.CASCADE)
    Matricula= models.IntegerField(blank=False)
    NombreAlum= models.CharField(max_length=25,blank=False)
    PaternoAlum= models.CharField(max_length=25,blank=False)
    MaternoAlum= models.CharField(max_length=25,blank=False)
    
class Usuario(AbstractUser):
    
    idDocente = models.IntegerField(primary_key=True)
    username = None
    
    #hago el campo de email requerido y unico 
    email = models.EmailField(_('email address'), unique=True)
    #hacemos que el campo de usuario utilice el email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['idDocente','NombreDocente','ApellidoPat','ApellidoMat','Cargo']
    
    
    NombreDocente= models.CharField(max_length=40,blank=False)
    ApellidoPat= models.CharField(max_length=40,blank=False)
    ApellidoMat= models.CharField(max_length=40,blank=False)
    Cargo= models.CharField(max_length=100,blank=False)
    
    #todos los objetos de la clase vienen del Usermanager
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.idDocente}"



class UniversidadExterior(models.Model):
    idUniversidadExterior = models.AutoField(primary_key=True)
    NombreUniversidad= models.CharField(max_length=30,blank=False)

class AlumnoExterior(models.Model):
    idAlumnoExterior = models.AutoField(primary_key=True)
    idCarrera = models.ForeignKey(Carrera,blank=False,on_delete=models.CASCADE)
    Matricula= models.IntegerField(blank=False)
    NombreAlum= models.CharField(max_length=25,blank=False)
    PaternoAlum= models.CharField(max_length=25,blank=False)
    MaternoAlum= models.CharField(max_length=25,blank=False)
    idUniversidadExterior = models.ForeignKey(UniversidadExterior,blank=False,on_delete=models.CASCADE)

class DictamenE(models.Model):
    idDictamenE = models.AutoField(primary_key=True)
    idAlumnoExterior = models.ForeignKey(AlumnoExterior,blank=False,on_delete=models.CASCADE)
    idInfoDocente = models.ForeignKey(Usuario,blank=False,on_delete=models.CASCADE)
    Fecha = models.DateField()
    PlanEstudioDe= models.CharField(max_length=20,blank=False)
    CarreraDE= models.CharField(max_length=20,blank=False)
    idPlanEstudioCarrera =models.ForeignKey(PlanEstudioCarrera,blank=False,on_delete=models.CASCADE)

class DetalleEquivalencia(models.Model):
    idDetalleEquivalenciaE = models.AutoField(primary_key=True)
    ClaveMatDe= models.IntegerField(blank=False)
    NombreMatDE= models.CharField(max_length=25,blank=False)
    CalificacionMatDE= models.FloatField(blank=False)
    TipoDeExamenDE= models.CharField(max_length=10,blank=False)
    CreditosMatDE= models.IntegerField(blank=False)
    PeriodoDE= models.CharField(max_length=10,blank=False)
    idPlanEstudioCarreraMateria = models.ForeignKey(PlanEstudioCarreraMateria,blank=False,on_delete=models.CASCADE)
    CalificacionA= models.FloatField(blank=False)
    TipoDeExamenA= models.CharField(max_length=10,blank=False)
    PeriodoA= models.CharField(max_length=10,blank=False)

class DictamenEDetalleEquivalencia(models.Model):
    idDictamenEDetalleEquivalencia = models.AutoField(primary_key=True)
    idDictamenE = models.ForeignKey(DictamenE,blank=False,on_delete=models.CASCADE)
    idDetalleEquivalencia = models.ForeignKey(DetalleEquivalencia,blank=False,on_delete=models.CASCADE)

class DictamenA(models.Model):  
    idDictamenA = models.AutoField(primary_key=True)
    idAlumno = models.ForeignKey(Alumno,blank=False,on_delete=models.CASCADE)
    idInfoDocente = models.ForeignKey(Usuario,blank=False,on_delete=models.CASCADE)
    Fecha = models.DateField()
    idPlanEstudioCarreraDE = models.ForeignKey(PlanEstudioCarrera,blank=False,on_delete=models.CASCADE)
    #idPlanEstudioCarreraA = models.ForeignKey(PlanEstudioCarrera,blank=False,on_delete=models.CASCADE)
    
class DictamenADetalleAcreditacion(models.Model): 
    idDictamenADetalleAcreditacion = models.AutoField(primary_key=True)

    idDictamenA = models.ForeignKey(DictamenA,blank=False,on_delete=models.CASCADE)
    idDetalleAcreditacion = models.ForeignKey(DetalleAcreditacion,blank=False,on_delete=models.CASCADE)