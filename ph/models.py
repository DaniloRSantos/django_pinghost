from django.db import models

# Create your models here.

class EnderecoBusca(models.Model):
    cep = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    @property
    def endereco_completo(self):
        return f"{self.logradouro}, {self.numero}, {self.complemento}, {self.bairro}, {self.cidade}, {self.estado}"
    
class Hosts(models.Model):
    ip_host = models.GenericIPAddressField(default='0.0.0.0')
    dns_host = models.CharField(max_length=255)
    nome_host = models.CharField(max_length= 150, null=False, blank=False)
    categoria_host = models.CharField(max_length= 150, null=False, blank=False)
    status_host = models.BooleanField(default=False)
    time_host = models.DateTimeField()
    endereco = models.ForeignKey(EnderecoBusca, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return f"Nome: {self.nome_host}, IP: {self.ip_host}, DNS: {self.dns_host}, Categoria: {self.categoria_host}, Status: {self.status_host}, Data/Hora: {self.time_host}, Endereço: {self.endereco}"
