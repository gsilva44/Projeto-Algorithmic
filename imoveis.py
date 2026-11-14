"""
RentSmart - Gabriel Silva Santos Francisco (RA 250131)
imoveis.py
Classes que representam os tipos de imóveis da R.M Imóveis.

Cada imóvel sabe calcular o próprio aluguel mensal. A classe base Imovel
guarda o que é comum a todos (tipo, aluguel-base e a lista de itens do
orçamento) e as subclasses implementam apenas as regras específicas.
"""


class Imovel:
    """Classe base (genérica) de um imóvel para locação."""

    TIPO = "Imóvel"
    ALUGUEL_BASE = 0.0

    def __init__(self, quartos=1):
        self.quartos = quartos
        self.itens = []          # lista de (descrição, valor) que formam o aluguel

    # ---- métodos comuns a todos os imóveis --------------------------------
    def _adicionar_item(self, descricao, valor):
        self.itens.append((descricao, valor))

    def calcular_aluguel(self):
        """Monta a lista de itens e devolve o aluguel mensal final.

        Segue sempre a mesma sequência (Template Method):
        1) aluguel-base  2) adicionais  3) descontos
        """
        self.itens = []
        self._adicionar_item(f"Aluguel-base ({self.TIPO})", self.ALUGUEL_BASE)
        self._aplicar_adicionais()
        self._aplicar_descontos()
        return round(sum(valor for _, valor in self.itens), 2)

    # ---- pontos que cada subclasse personaliza -----------------------------
    def _aplicar_adicionais(self):
        pass

    def _aplicar_descontos(self):
        pass

    def descricao(self):
        return f"{self.TIPO} - {self.quartos} quarto(s)"


class Residencial(Imovel):
    """Comportamento compartilhado por Casa e Apartamento:
    podem ter 2 quartos e uma vaga de garagem (R$ 300,00)."""

    ADICIONAL_2_QUARTOS = 0.0
    VALOR_GARAGEM = 300.00

    def __init__(self, quartos=1, garagem=False):
        if quartos not in (1, 2):
            raise ValueError("Casas e apartamentos podem ter 1 ou 2 quartos.")
        super().__init__(quartos)
        self.garagem = garagem

    def _aplicar_adicionais(self):
        if self.quartos == 2:
            self._adicionar_item("Adicional 2 quartos", self.ADICIONAL_2_QUARTOS)
        if self.garagem:
            self._adicionar_item("Vaga de garagem", self.VALOR_GARAGEM)

    def descricao(self):
        garagem = "com garagem" if self.garagem else "sem garagem"
        return f"{super().descricao()}, {garagem}"


class Apartamento(Residencial):
    TIPO = "Apartamento"
    ALUGUEL_BASE = 700.00
    ADICIONAL_2_QUARTOS = 200.00
    PERCENTUAL_DESCONTO = 0.05

    def __init__(self, quartos=1, garagem=False, possui_criancas=True):
        super().__init__(quartos, garagem)
        self.possui_criancas = possui_criancas

    def _aplicar_descontos(self):
        # 5% sobre o aluguel já com os adicionais, para quem não tem crianças
        if not self.possui_criancas:
            subtotal = sum(valor for _, valor in self.itens)
            desconto = round(subtotal * self.PERCENTUAL_DESCONTO, 2)
            self._adicionar_item("Desconto 5% (sem crianças)", -desconto)

    def descricao(self):
        criancas = "com crianças" if self.possui_criancas else "sem crianças"
        return f"{super().descricao()}, {criancas}"


class Casa(Residencial):
    TIPO = "Casa"
    ALUGUEL_BASE = 900.00
    ADICIONAL_2_QUARTOS = 250.00


class Estudio(Imovel):
    TIPO = "Estúdio"
    ALUGUEL_BASE = 1200.00
    PACOTE_VAGAS = 2
    VALOR_PACOTE = 250.00
    VALOR_VAGA_EXTRA = 60.00

    def __init__(self, vagas=0):
        if vagas < 0:
            raise ValueError("O número de vagas não pode ser negativo.")
        super().__init__(quartos=1)
        self.vagas = vagas

    def _aplicar_adicionais(self):
        # Qualquer vaga contrata o pacote de 2; o que passar de 2 é "extra".
        if self.vagas > 0:
            self._adicionar_item("Pacote estacionamento (2 vagas)", self.VALOR_PACOTE)
            extras = max(0, self.vagas - self.PACOTE_VAGAS)
            if extras:
                self._adicionar_item(f"Vagas adicionais ({extras} x R$ 60,00)",
                                     extras * self.VALOR_VAGA_EXTRA)

    def descricao(self):
        return f"{self.TIPO}, {self.vagas} vaga(s) de estacionamento"
