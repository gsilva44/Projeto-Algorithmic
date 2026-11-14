# RentSmart — Sistema de Orçamento de Locação (R.M Imóveis)

Aluno: **Gabriel Silva Santos Francisco** — RA **250131**
Disciplina: Algorithmic Thinking & Introduction to Object-Oriented Programming

Aplicação em Python que calcula o orçamento mensal de locação de apartamentos, casas e estúdios
aplicando as regras comerciais da R.M Imóveis, mostra um resumo detalhado e gera um arquivo CSV
com a projeção dos 12 primeiros meses de contrato.

## Requisitos
- Python 3.8 ou superior (não usa bibliotecas externas).

## Como executar
```bash
git clone <link-do-seu-repositorio>
cd rentsmart
python main.py
```
Responda às perguntas no terminal. Ao final, o orçamento aparece na tela e o arquivo
`orcamento_12_meses.csv` é criado na mesma pasta (abre direto no Excel, separador `;`).

## Estrutura
| Arquivo | Conteúdo |
|---|---|
| `main.py` | Classe `Interface`: perguntas, validação das entradas e fluxo principal |
| `imoveis.py` | Classes `Imovel`, `Residencial`, `Apartamento`, `Casa`, `Estudio` |
| `orcamento.py` | Classes `TaxaContratual` e `Orcamento` (resumo e exportação CSV) |
| `orcamento_12_meses.csv` | Exemplo de saída gerada |

## Regras implementadas
| Imóvel | Base | Adicionais | Desconto |
|---|---|---|---|
| Apartamento | R$ 700 | 2 quartos +R$ 200; garagem +R$ 300 | 5% se não tiver crianças (após adicionais) |
| Casa | R$ 900 | 2 quartos +R$ 250; garagem +R$ 300 | — |
| Estúdio | R$ 1.200 | pacote 2 vagas R$ 250; +R$ 60 por vaga extra | — |

Taxa contratual: R$ 2.000,00 em 1 a 5 parcelas, cobradas nos primeiros meses e mostradas
separadas do aluguel.

## Exemplo
Apartamento, 2 quartos, com garagem, sem crianças, taxa em 3x:
```
Aluguel-base (Apartamento)    R$ 700,00
Adicional 2 quartos           R$ 200,00
Vaga de garagem               R$ 300,00
Desconto 5% (sem crianças)    R$ -60,00
ALUGUEL MENSAL              R$ 1.140,00
Taxa contratual: 3x de R$ 666,67
```
