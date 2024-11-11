#Alec Araújo da Câmara
#Fabricio da Silva Julião


class Filme:
    def __init__(self, titulo, duracao_em_minutos):
        self._titulo = titulo
        self._duracao_em_minutos = duracao_em_minutos

    def get_titulo(self):
        return self._titulo
    
    def set_titulo(self, titulo):
        self._titulo = titulo

    def get_duracao_em_minutos(self):
        return self._duracao_em_minutos

    def set_duracao_em_minutos(self, duracao_em_minutos):
        self._duracao_em_minutos = duracao_em_minutos

    def exibir_duracao_em_horas(self):
        horas = self._duracao_em_minutos // 60
        minutos = self._duracao_em_minutos % 60
        print(f"O filme {self._titulo} possui {horas} horas e {minutos} minutos de duração.")

class TestarFilme:
    @staticmethod
    def main():
        titulo = input("Digite o título do filme: ")
        duracao_em_minutos = int(input("Digite a duração do filme em minutos: "))
        
        filme = Filme(titulo, duracao_em_minutos)
        filme.exibir_duracao_em_horas()

        nova_duracao = int(input("Digite a nova duração do filme em minutos: "))
        filme.set_duracao_em_minutos(nova_duracao)
        filme.exibir_duracao_em_horas()

if __name__ :
    TestarFilme.main()
