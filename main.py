"""
RentSmart - Gabriel Silva Santos Francisco (RA 250131)
main.py
Ponto de entrada do RentSmart: conversa com o usuário, valida as respostas,
cria os objetos e mostra o orçamento.

Execute com:  python main.py
"""
from imoveis import Apartamento, Casa, Estudio
from orcamento import Orcamento, TaxaContratual


class Interface:
    """Responsável apenas pela entrada e saída no terminal."""

    @staticmethod
    def ler_opcao(pergunta, opcoes):
        """Repete a pergunta até o usuário digitar uma das opções válidas."""
        while True:
            resposta = input(pergunta).strip().upper()
            if resposta in opcoes:
                return resposta
            print(f"  Opção inválida. Digite uma destas: {', '.join(opcoes)}")

    @staticmethod
    def ler_inteiro(pergunta, minimo, maximo):
        while True:
            texto = input(pergunta).strip()
            if texto.isdigit() and minimo <= int(texto) <= maximo:
                return int(texto)
            print(f"  Valor inválido. Digite um número inteiro entre {minimo} e {maximo}.")

    def sim_ou_nao(self, pergunta):
        return self.ler_opcao(pergunta + " (S/N): ", ["S", "N"]) == "S"

    def criar_imovel(self):
        print("\nTipos de imóvel:\n  1 - Apartamento (R$ 700,00)\n"
              "  2 - Casa (R$ 900,00)\n  3 - Estúdio (R$ 1.200,00)")
        tipo = self.ler_opcao("Escolha o tipo: ", ["1", "2", "3"])

        if tipo == "3":
            vagas = 0
            if self.sim_ou_nao("Deseja estacionamento? Pacote de 2 vagas por R$ 250,00"):
                vagas = self.ler_inteiro("Quantas vagas no total? (mínimo 2, máximo 10): ", 2, 10)
            return Estudio(vagas)

        quartos = self.ler_inteiro("Quantos quartos? (1 ou 2): ", 1, 2)
        garagem = self.sim_ou_nao("Deseja vaga de garagem? (+R$ 300,00)")
        if tipo == "1":
            criancas = self.sim_ou_nao("Possui crianças?")
            return Apartamento(quartos, garagem, criancas)
        return Casa(quartos, garagem)

    def executar(self):
        print("Bem-vindo ao RentSmart - R.M Imóveis")
        while True:
            imovel = self.criar_imovel()
            parcelas = self.ler_inteiro("Em quantas parcelas deseja pagar a taxa contratual "
                                        "de R$ 2.000,00? (1 a 5): ", 1, 5)
            orcamento = Orcamento(imovel, TaxaContratual(parcelas))
            print("\n" + orcamento.resumo())
            arquivo = orcamento.exportar_csv()
            print(f"Projeção de 12 meses salva em: {arquivo}\n")
            if not self.sim_ou_nao("Deseja fazer outro orçamento?"):
                print("Obrigado por usar o RentSmart!")
                break


if __name__ == "__main__":
    Interface().executar()
