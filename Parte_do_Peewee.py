from peewee import *
from datetime import *

meu_bd = SqliteDatabase("os_dados_nos_perseguem.db")

class BaseGeral(Model):

    class Meta:
        database = meu_bd

class Paciente(BaseGeral):

    nome_pac = CharField()
    dt_nasc_pac = DateField()
    cpf_pac = CharField()

    def __str__(self):
        return self.nome_pac

class Medico(BaseGeral):

    nome_med = CharField()
    cpf_med = CharField()
    taxa_suce = CharField()

    def __str__(self):
        return self.nome_med

class Tipo_Sang(BaseGeral):

    tipo_sang = CharField()
    sang_dispo = BooleanField()

    def __str__(self):
        return f"Tipo do Sangue: {self.tipo_sang}\nO Sangue está disponível: {self.sang_dispo}"

class Transfussao(BaseGeral):

    paciente_t = ForeignKeyField(Paciente)
    data_hora = DateTimeField()
    tipo_sang_t = ForeignKeyField(Tipo_Sang)
    medico_t = ForeignKeyField(Medico)

    def __str__(self):
        return f"{self.id}"

    # def __iter__(self):

    #     self.a = self.id
    #     return self

    # def __next__(self):
    #     x = self.a
    #     return x

meu_bd.connect()
meu_bd.create_tables([Paciente, Medico, Tipo_Sang, Transfussao])
