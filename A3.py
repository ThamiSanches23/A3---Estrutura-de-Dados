import heapq
import networkx as nx  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from math import ceil

# Função para encontrar a menor rota logística
def logistica(grafo, inicio, destino):
    distancias = {cidade: float('inf') for cidade in grafo}
    distancias[inicio] = 0
    caminho = {cidade: None for cidade in grafo}
    visitados = set()
    fila_prioridade = [(0, inicio)]

    while fila_prioridade:
        custo_atual, cidade_atual = heapq.heappop(fila_prioridade)

        if cidade_atual in visitados:
            continue

        visitados.add(cidade_atual)

        for vizinho, peso_aresta in grafo[cidade_atual].items():
            novo_custo = custo_atual + peso_aresta
            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                caminho[vizinho] = cidade_atual
                heapq.heappush(fila_prioridade, (novo_custo, vizinho))
    
    rota = []
    cidade_atual = destino
    while cidade_atual is not None:
        rota.append(cidade_atual)
        cidade_atual = caminho[cidade_atual]
    
    rota.reverse()
    
    return distancias, rota

# Função para determinar o centro de distribuição mais próximo
def centro_distribuicao_mais_proximo(grafo, centros, destino):
    menor_distancia = float('inf')
    melhor_centro = None
    for centro in centros:
        distancias, _ = logistica(grafo, centro, destino)
        if distancias[destino] < menor_distancia:
            menor_distancia = distancias[destino]
            melhor_centro = centro
    return melhor_centro

# Função para calcular o tempo e a data estimada de entrega
def calcular_tempo_entrega(distancia):
    VELOCIDADE = 80  # km/h
    HORAS_DIA = 8  # horas por dia
    tempo_total_horas = distancia / VELOCIDADE
    dias_entrega = ceil(tempo_total_horas / HORAS_DIA)  # Arredondar para o próximo dia inteiro
    return dias_entrega

# Função para desenhar o grafo e a rota otimizada
def desenhar_grafo(grafo, rota):
    G = nx.Graph()
    
    # Adicionar arestas ao grafo
    for cidade, conexoes in grafo.items():
        for vizinho, peso in conexoes.items():
            G.add_edge(cidade, vizinho, weight=peso)

    pos = nx.spring_layout(G, seed=42)  # Layout do grafo
    pesos = nx.get_edge_attributes(G, 'weight')

    # Desenhar o grafo completo
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=8)
    
    # Destacar a rota otimizada
    rota_edges = [(rota[i], rota[i + 1]) for i in range(len(rota) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=rota_edges, edge_color='red', width=2)
    
    plt.title("Rota Logística Otimizada")
    plt.show()

# Grafo com os nomes das cidades e os pesos das arestas
grafo = {
    'Natal': {'João Pessoa': 181, 'Fortaleza': 522},
    'João Pessoa': {'Natal': 181, 'Recife': 116},
    'Recife': {'Maceió': 257, 'João Pessoa': 106},
    'Fortaleza': {'Natal': 524, 'Teresina': 599},
    'Salvador': {'Aracaju': 324, 'Brasília': 1444},
    'Maceió': {'Aracaju': 295, 'Recife': 256},
    'Aracaju': {'Salvador': 327, 'Maceió': 271},
    'São Luiz': {'Teresina': 441, 'Belém': 576},
    'Teresina': {'Fortaleza': 600, 'São Luiz': 436},
    'Belém': {'São Luiz': 576, 'Macapá': 528, 'Manaus': 2994},
    'São Paulo': {'Curitiba': 400, 'Rio de Janeiro': 446},
    'Curitiba': {'São Paulo': 399, 'Florianópolis': 308},
    'Brasília': {'Salvador': 1443, 'Goiânia': 208, 'Cuiabá': 1067},
    'Goiânia': {'Brasília': 208, 'Campo Grande': 839},
    'Campo Grande': {'Goiânia': 839, 'Cuiabá': 703},
    'Cuiabá': {'Campo Grande': 710, 'Porto Velho': 1461},
    'Porto Velho': {'Cuiabá': 1460, 'Rio Branco': 510, 'Manaus': 889},
    'Rio Branco': {'Porto Velho': 510},
    'Manaus': {'Porto Velho': 890, 'Boa Vista': 785},
    'Boa Vista': {'Manaus': 785},
    'Macapá': {'Belém': 330},
    'Rio de Janeiro': {'São Paulo': 429, 'Vitória': 521, 'Belo Horizonte': 434},
    'Belo Horizonte': {'Rio de Janeiro': 434, 'Vitória': 524},
    'Vitória': {'Rio de Janeiro': 521, 'Belo Horizonte': 524},
    'Florianópolis': {'Curitiba': 300, 'Porto Alegre': 476},
    'Porto Alegre': {'Florianópolis': 476}
}

# Lista dos centros de distribuição
centros_distribuicao = ['Belém', 'Recife', 'São Paulo', 'Curitiba']

# Dicionário de nomes das capitais (destino formatado)
capitais = {
    'Natal': 'Natal - RN',
    'João Pessoa': 'João Pessoa - PB',
    'Recife': 'Recife - PE',
    'Fortaleza': 'Fortaleza - CE',
    'Salvador': 'Salvador - BA',
    'Maceió': 'Maceió - AL',
    'Aracaju': 'Aracaju - SE',
    'São Luiz': 'São Luís - MA',
    'Teresina': 'Teresina - PI',
    'Belém': 'Belém - PA',
    'São Paulo': 'São Paulo - SP',
    'Curitiba': 'Curitiba - PR',
    'Brasília': 'Brasília - DF',
    'Goiânia': 'Goiânia - GO',
    'Campo Grande': 'Campo Grande - MS',
    'Cuiabá': 'Cuiabá - MT',
    'Porto Velho': 'Porto Velho - RO',
    'Rio Branco': 'Rio Branco - AC',
    'Manaus': 'Manaus - AM',
    'Boa Vista': 'Boa Vista - RR',
    'Macapá': 'Macapá - AP',
    'Rio de Janeiro': 'Rio de Janeiro - RJ',
    'Belo Horizonte': 'Belo Horizonte - MG',
    'Vitória': 'Vitória - ES',
    'Florianópolis': 'Florianópolis - SC',
    'Porto Alegre': 'Porto Alegre - RS'
}

# Define o destino e encontra o melhor centro de distribuição
destino = 'Goiânia'
inicio = centro_distribuicao_mais_proximo(grafo, centros_distribuicao, destino)
distancias, rota = logistica(grafo, inicio, destino)

# Calcula a data estimada de entrega
dias_entrega = calcular_tempo_entrega(distancias[destino])

# Exibe informações detalhadas
print(f"Centro de distribuição selecionado: {inicio} - {capitais[inicio]}")
print(f"Destino: {destino} - {capitais[destino]}")
print(f"Distância mínima: {distancias[destino]} km")
print(f"Melhor rota: {' -> '.join(rota)}")
print(f"Tempo estimado de entrega: {dias_entrega} dias úteis")

# Visualizar o grafo e a rota otimizada
desenhar_grafo(grafo, rota)