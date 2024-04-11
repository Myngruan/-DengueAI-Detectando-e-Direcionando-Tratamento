# Base de dados de pessoas com dengue
pessoas_dengue = {
    'Pessoa1': {'latitude': 40.7128, 'longitude': -74.0060},  # Exemplo de coordenadas para Nova York
    'Pessoa2': {'latitude': 34.0522, 'longitude': -118.2437},  # Exemplo de coordenadas para Los Angeles
    # Adicione mais pessoas conforme necessário
}

# Base de dados de hospitais
hospitais = {
    'Hospital1': {'latitude': 41.8781, 'longitude': -87.6298},  # Exemplo de coordenadas para Chicago
    'Hospital2': {'latitude': 37.7749, 'longitude': -122.4194},  # Exemplo de coordenadas para São Francisco
    # Adicione mais hospitais conforme necessário
}
import math

def heuristic(node, values):
    # Calcular a distância euclidiana entre a pessoa com dengue (node) e o hospital (values)
    pessoa_lat = pessoas_dengue[node]['latitude']
    pessoa_lon = pessoas_dengue[node]['longitude']
    hospital_lat = values['latitude']
    hospital_lon = values['longitude']
    distance = math.sqrt((pessoa_lat - hospital_lat) ** 2 + (pessoa_lon - hospital_lon) ** 2)
    return distance

def astar(start, end):
    path = {}
    distance = {}
    q = priorityQueue()
    q.push(start, 0)
    distance[start] = 0
    path[start] = None
    expandedList = []
    while not q.isEmpty():
        current = q.pop()
        expandedList.append(current)
        if current == end:
            break
        for hospital, coords in hospitais.items():
            g_cost = distance[current] + heuristic(current, coords)
            if hospital not in distance or g_cost < distance[hospital]:
                distance[hospital] = g_cost
                f_cost = g_cost + heuristic(hospital, hospitais[end])
                q.push(hospital, f_cost)
                path[hospital] = current
    printoutput(start, end, path, distance, expandedList)

def printoutput(start, end, path, distance, expandedList):
    print("Caminho mais curto de", start, "para", end, ":", end=" ")
    current = end
    while current != start:
        print(current, "<-", end=" ")
        current = path[current]
    print(start)
    print("Distância total:", distance[end])
    print("Nós expandidos:", expandedList)
# Exemplo de uso
if __name__ == "__main__":
    makedict()  # Não será mais necessário se você estiver lendo dados de uma base de dados
    pessoa = 'Pessoa1'  # Escolha uma pessoa com dengue
    hospital_mais_proximo = 'Hospital1'  # Escolha o hospital mais próximo
    astar(pessoa, hospital_mais_proximo)
