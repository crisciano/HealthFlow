from django.contrib import admin

from .models import Patient

# =========================================================
# 2. ADMIN PARA PATIENT (Tabela: patients)
# =========================================================

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de Pacientes
    list_display = ('name', 'cpf', 'phone', 'birthdate', 'created_at')
    
    # Filtros laterais
    list_filter = ('birthdate',)
    
    # Campos de busca
    search_fields = ('name', 'cpf', 'phone')
    
    # Ordem padrão
    ordering = ('name',)
    
    # Divisão dos campos na tela de edição
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('name', 'cpf', 'birthdate',),
        }),
        ('Contato e Endereço', {
            'fields': ('phone', 'address',),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',),
        }),
    )
    # Campos somente leitura
    readonly_fields = ('created_at', 'updated_at',)

# admin.site.register(Patient, PatientAdmin)