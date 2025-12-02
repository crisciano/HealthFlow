from django.db import models

from doctors.models import Doctor
from patients.models import Patient

# --- Choices ---
# Definindo as opções de status para a consulta
APPOINTMENT_STATUS_CHOICES = (
    ('SCHEDULED', 'Agendada'),
    ('COMPLETED', 'Realizada'),
    ('CANCELED', 'Cancelada'),
    ('RESCHEDULED', 'Reagendada'),
)

# =========================================================
# 3. ENTIDADE APPOINTMENT (Tabela: appointments)
# =========================================================

class Appointment(models.Model):
    # Chaves Estrangeiras (Regra de Negócio 1 e 2)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')

    # Data e Hora (Usando DateTimeField para simplificar a ordenação e evitar conflitos)
    datetime = models.DateTimeField(verbose_name="Data e Hora da Consulta")
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=APPOINTMENT_STATUS_CHOICES,
        default='SCHEDULED',
        verbose_name="Status da Consulta"
    )

    # Informações Adicionais
    reason = models.TextField(null=True, blank=True, verbose_name="Motivo da Consulta (Pré-consulta)")
    prescription = models.TextField(null=True, blank=True, verbose_name="Prescrição (Pós-consulta)")
    notes = models.TextField(null=True, blank=True, verbose_name="Notas do Médico")
    
    # Auditoria
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        db_table = 'appointments'
        
        # Garante que um médico não pode ter duas consultas agendadas para o mesmo horário.
        # Importante para a Regra de Negócio 1 (conflito de horários).
        unique_together = ('doctor', 'datetime',) 

    def __str__(self):
        return f"Consulta de {self.patient.name} com Dr(a). {self.doctor.name} em {self.datetime.strftime('%d/%m/%Y %H:%M')}"
