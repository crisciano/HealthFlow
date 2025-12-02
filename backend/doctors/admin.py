from django.contrib import admin

from .models import Doctor

# =========================================================
# 1. ADMIN PARA DOCTOR (Tabela: doctors)
# =========================================================

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Campos exibidos na lista de Médicos
    list_display = ('name', 'specialty', 'crm', 'is_active', 'created_at')
    
    # Filtros laterais
    list_filter = ('is_active', 'specialty')
    
    # Campos de busca
    search_fields = ('name', 'crm', 'specialty')
    
    # Ordem padrão
    ordering = ('name',)
    
    # Divisão dos campos na tela de edição
    fieldsets = (
        (None, {
            'fields': ('name', 'specialty', 'crm', 'is_active'),
        }),
        ('Auditoria', {
            'fields': ('created_at', 'updated_at',),
            'classes': ('collapse',),
        }),
    )
    # Campos somente leitura
    readonly_fields = ('created_at', 'updated_at',)

# admin.site.register(Doctor, DoctorAdmin)