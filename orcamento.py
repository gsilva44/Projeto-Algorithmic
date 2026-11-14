"""
RentSmart - Gabriel Silva Santos Francisco (RA 250131)
orcamento.py
Classes do contrato: taxa contratual, orçamento e exportação em CSV.
"""
import csv


def moeda(valor):
    """Formata um número no padrão brasileiro: R$ 1.234,56"""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


class TaxaContratual:
    """Taxa de contrato de R$ 2.000,00, parcelável em até 5 vezes.
    Fica separada do aluguel para não serem confundidos."""

    VALOR = 2000.00
    MAX_PARCELAS = 5

    def __init__(self, parcelas=1):
        if not 1 <= parcelas <= self.MAX_PARCELAS:
            raise ValueError(f"A taxa pode ser paga em 1 a {self.MAX_PARCELAS} parcelas.")
        self.parcelas = parcelas

    def valor_parcela(self):
        return round(self.VALOR / self.parcelas, 2)

    def parcela_do_mes(self, mes):
        """Valor da taxa cobrado no mês informado (1 a 12)."""
        if mes > self.parcelas:
            return 0.0
        # A última parcela absorve eventuais centavos do arredondamento
        if mes == self.parcelas:
            return round(self.VALOR - self.valor_parcela() * (self.parcelas - 1), 2)
        return self.valor_parcela()


class Orcamento:
    """Junta um imóvel e uma taxa contratual e gera o resumo e a projeção."""

    MESES = 12

    def __init__(self, imovel, taxa):
        self.imovel = imovel
        self.taxa = taxa
        self.aluguel_mensal = imovel.calcular_aluguel()

    def projecao(self):
        """Lista com um dicionário por mês: aluguel, parcela da taxa e total."""
        linhas = []
        for mes in range(1, self.MESES + 1):
            parcela = self.taxa.parcela_do_mes(mes)
            linhas.append({
                "mes": mes,
                "aluguel": self.aluguel_mensal,
                "parcela_taxa": parcela,
                "total": round(self.aluguel_mensal + parcela, 2),
            })
        return linhas

    def resumo(self):
        linhas = ["=" * 52, "        RENTSMART - ORÇAMENTO DE LOCAÇÃO", "=" * 52,
                  f"Imóvel: {self.imovel.descricao()}", "",
                  "Composição do aluguel mensal:"]
        for descricao, valor in self.imovel.itens:
            linhas.append(f"  {descricao:<36}{moeda(valor):>14}")
        linhas += ["-" * 52,
                   f"  {'ALUGUEL MENSAL':<36}{moeda(self.aluguel_mensal):>14}", "",
                   "Taxa contratual (cobrada à parte do aluguel):",
                   f"  Valor total{'':<25}{moeda(self.taxa.VALOR):>14}",
                   f"  Parcelamento: {self.taxa.parcelas}x de {moeda(self.taxa.valor_parcela())}",
                   "",
                   f"Total no 1º ano (12 aluguéis + taxa): "
                   f"{moeda(sum(l['total'] for l in self.projecao()))}",
                   "=" * 52]
        return "\n".join(linhas)

    def exportar_csv(self, caminho="orcamento_12_meses.csv"):
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel (R$)", "Parcela taxa contratual (R$)", "Total do mês (R$)"])
            for l in self.projecao():
                escritor.writerow([l["mes"], *(f"{l[c]:.2f}".replace(".", ",")
                                               for c in ("aluguel", "parcela_taxa", "total"))])
        return caminho
