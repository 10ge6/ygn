import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

tree = ET.parse('jflap-file/your_MT.jff')
root = tree.getroot()

automaton = root.find('automaton')

dados = []

for transition in automaton.findall('transition'):
    item = {
        'to': transition.find('to').text,
        'from': transition.find('from').text
    }

    for read in transition.findall('read'):
        tape_num = read.get('tape')
        item[f'read_tape{tape_num}'] = read.text
        print(f"Read tape {tape_num}: {read.text}")

    for write in transition.findall('write'):
        tape_num = write.get('tape')
        item[f'write_tape{tape_num}'] = write.text
        print(f"Write tape {tape_num}: {write.text}")

    for move in transition.findall('move'):
        tape_num = move.get('tape')
        item[f'move_tape{tape_num}'] = move.text
        print(f"Move tape {tape_num}: {move.text}")

    dados.append(item)
    print(f"Transição adicionada: {item}")  # Debug print

print("\nTotal de transições:", len(dados))
df = pd.DataFrame(dados)
print("\nColunas do DataFrame:", df.columns)
print("\nPrimeiras linhas do DataFrame:")
print(df.head())

df.to_csv('transicoes.csv', index=False)

import matplotlib.pyplot as plt
import math


def criar_tabela_paginada(df, linhas_por_pagina=20):
    total_paginas = math.ceil(len(df) / linhas_por_pagina)

    for pagina in range(total_paginas):
        inicio = pagina * linhas_por_pagina
        fim = min((pagina + 1) * linhas_por_pagina, len(df))

        df_pagina = df.iloc[inicio:fim]

        plt.figure(figsize=(12, linhas_por_pagina * 0.5))
        plt.axis('tight')
        plt.axis('off')

        tabela = plt.table(cellText=df_pagina.values,
                           colLabels=df.columns,
                           cellLoc='center',
                           loc='center')

        tabela.auto_set_font_size(False)
        tabela.set_fontsize(9)
        tabela.scale(1.2, 1.5)

        plt.title(f'Tabela de Transições - Página {pagina + 1} de {total_paginas}')

        plt.savefig(f'tabela_transicoes_pagina_{pagina + 1}.png',
                    bbox_inches='tight',
                    dpi=300,
                    facecolor='white')
        plt.close()


criar_tabela_paginada(df, linhas_por_pagina=20)