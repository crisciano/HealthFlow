from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Validador para garantir que o CRM tem um formato padrão
crm_validator = RegexValidator(
    regex=r'^\d{4,10}[/][A-Z]{2}$', # Exemplo: 12345/SP
    message='O CRM deve estar no formato número/Estado (e.g., 12345/SP).',
    code='invalid_crm'
)

# =========================================================
# 1. ENTIDADE DOCTOR (Tabela: doctors)
# =========================================================

class Doctor(models.Model):
    # Liga o perfil do médico ao usuário do Django para login
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    
    # Campos obrigatórios (*)
    name = models.CharField(max_length=150, verbose_name="Nome Completo")
    specialty = models.CharField(max_length=100, verbose_name="Especialidade")
    crm = models.CharField(
        max_length=15, 
        unique=True, 
        validators=[crm_validator],
        verbose_name="Registro CRM"
    )
    
    # Auditoria e Controle
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        # O Django cria a tabela 'app_doctor' por padrão. Você pode definir o nome da tabela no DB.
        db_table = 'doctors' 

    def __str__(self):
        return f"Dr(a). {self.name} ({self.specialty})"