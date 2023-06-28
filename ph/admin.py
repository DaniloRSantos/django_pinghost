from django.contrib import admin  # Importa o módulo admin do Django

from .models import EnderecoBusca, Hosts  # Importa as classes EnderecoBusca e Hosts do arquivo models.py

# Define uma classe inline para exibição e edição de objetos EnderecoBusca relacionados ao modelo Hosts na interface de administração
class EnderecoBuscaInline(admin.StackedInline):
    model = EnderecoBusca  # Define o modelo com o qual a classe inline está relacionada
    fields = ['logradouro', 'numero', 'complemento', 'bairro', 'cidade', 'estado']  # Define os campos a serem exibidos e editados
    extra = 1  # Define o número de formulários extras em branco a serem exibidos

# Define uma classe para personalizar a exibição e comportamento do modelo Hosts na interface de administração
class HostsAdmin(admin.ModelAdmin):
    inlines = [EnderecoBuscaInline]  # Define a lista de classes inlines a serem exibidas para o modelo Hosts
    exclude = ['status_host','time_host']

# Registra o modelo Hosts na interface de administração, usando a classe HostsAdmin para personalizar sua exibição e comportamento
admin.site.register(Hosts, HostsAdmin)
