import locale

def formatar_moeda(valor):
    if isinstance(valor, (int, float)):
        return locale.currency(valor, grouping=True)
    return "Valor inválido"
