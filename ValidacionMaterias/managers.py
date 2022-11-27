from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Modelo de agente de usuarios diferente para que se manejen los 
    correos electronicos como los usuarios en el sistema.
    """
    
    def create_user(self, email, password,idDocente,NombreDocente,ApellidoPat,ApellidoMat,Cargo,**extra_fields):
        """
        Crea y guarda un usuario dados el email y contra
        """
        if not email:
            raise ValueError(_('Se debe dar un email'))
        email = self.normalize_email(email)
        user = self.model(email=email,idDocente = idDocente,NombreDocente=NombreDocente,ApellidoPat=ApellidoPat,ApellidoMat=ApellidoMat,Cargo=Cargo, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Crea y guarda un super usuario dados los datos
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)