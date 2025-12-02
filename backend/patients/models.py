from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Validador para garantir que o CPF tem 11 dígitos
cpf_validator = RegexValidator(
    regex=r'^\d{11}$', 
    message='O CPF deve conter exatamente 11 dígitos.',
    code='invalid_cpf'
)

# =========================================================
# 2. ENTIDADE PATIENT (Tabela: patients)
# =========================================================

class Patient(models.Model):
    # Liga o perfil do paciente ao usuário do Django para login
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', null=True, blank=True)
    
    # Campos obrigatórios (*)
    name = models.CharField(max_length=150, verbose_name="Nome Completo")
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[cpf_validator],
        verbose_name="CPF"
    )
    phone = models.CharField(
        max_length=15, 
        verbose_name="Telefone", 
        help_text="Ex: 51998765432"
    )

    has_partner = models.BooleanField(default=False, verbose_name="Possui Convênio Médico?")
    
    # Campos opcionais
    birthdate = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    address = models.TextField(null=True, blank=True, verbose_name="Endereço Completo")
    
    # Auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        db_table = 'patients'

    def __str__(self):
        return self.name
