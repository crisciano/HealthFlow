from django.contrib import admin

from .models import Appointment

# =========================================================
# Customização para o modelo Appointment
# =========================================================

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Campos que serão exibidos na lista de consultas
    list_display = ('datetime', 'doctor', 'patient', 'status', 'created_at')
    
    # Filtros laterais
    list_filter = ('status', 'doctor', 'patient', 'datetime')
    
    # Campos de busca
    search_fields = ('reason', 'doctor__name', 'patient__name')
    
    # Ordem padrão (consultas mais próximas)
    ordering = ('datetime',)
    
    # Divisão dos campos na tela de edição
    fieldsets = (
        ('Agendamento', {
            'fields': ('doctor', 'patient', 'datetime', 'status'),
        }),
        ('Detalhes da Consulta', {
            'fields': ('reason',),
        }),
        ('Prontuário (Apenas para Médicos)', {
            'fields': ('prescription', 'notes',),
        }),
    )
    # Campos que o Django preenche automaticamente
    readonly_fields = ('created_at', 'updated_at',)


# admin.site.register(Appointment, AppointmentAdmin)