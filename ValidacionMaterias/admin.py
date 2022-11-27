from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Usuario, Materia,Etapa,TipoMateria

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = ('email', 'is_staff', 'is_active','NombreDocente','ApellidoPat','ApellidoMat','Cargo','idDocente')
    list_filter = ('email', 'is_staff', 'is_active','NombreDocente','ApellidoPat','ApellidoMat','Cargo','idDocente')
    fieldsets = (
        (None, {'fields': ('email', 'password','NombreDocente','ApellidoPat','ApellidoMat','Cargo','idDocente')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','NombreDocente','ApellidoPat','ApellidoMat','Cargo','idDocente')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    
class MateriaInline(admin.StackedInline):
    model = Materia
    extra = 1    
    
class CourseAdmin(admin.ModelAdmin):
    inlines = [MateriaInline]
    list_display = ('idMateria','ClaveMateria','NombreMateria','Creditos')
    list_filter = ['idMateria']
    search_fields = ['NombreMateria','idMateria']    


admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Materia)
admin.site.register(Etapa)
admin.site.register(TipoMateria)
