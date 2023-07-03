from django.contrib import admin
from .models import Hosts, EnderecoBusca

class EnderecoBuscaInline(admin.StackedInline):
    model = EnderecoBusca
    fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado']
    extra = 1

class HostsAdmin(admin.ModelAdmin):
    inlines = [EnderecoBuscaInline]
    list_display = ("id", "dns_host", "nome_host", "categoria_host", "ip_host", "endereco_completo")

    def endereco_completo(self, obj):
        enderecos = obj.enderecos.all()
        return ", ".join([endereco.endereco_completo for endereco in enderecos])

admin.site.register(Hosts, HostsAdmin)
