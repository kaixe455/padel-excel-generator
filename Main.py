import pandas as pd

# Nombres de los participantes
jugadores = ['Ángel', 'Miguel', 'Claudia', 'Patricia', 'Sandra', 'Dani', 'Jose', 'Marta']

# Crear una matriz de partidos usando el método round-robin
def round_robin(players):
    if len(players) % 2:
        players.append('Descanso')  # Añadir un "Descanso" si el número de jugadores es impar
    rotation = players.copy()
    schedule = []
    for i in range(len(players) - 1):
        mid = len(players) // 2
        l1 = rotation[:mid]
        l2 = rotation[mid:]
        l2.reverse()
        round_matches = list(zip(l1, l2))
        schedule.append(round_matches)
        rotation = rotation[mid-1:mid] + rotation[:mid-1] + rotation[mid+1:] + rotation[mid:mid+1]
    return schedule

# Generar el cronograma de partidos
matches = round_robin(jugadores)

# Convertir el cronograma en el formato adecuado para el DataFrame
cronograma = []
ronda_num = 1

for ronda in matches:
    for i in range(0, len(ronda), 2):
        if i + 1 < len(ronda):
            cronograma.append([ronda_num, ronda[i][0], ronda[i][1], "", ronda[i+1][0], ronda[i+1][1], ""])
        else:
            cronograma.append([ronda_num, ronda[i][0], ronda[i][1], "", "", "", ""])
    ronda_num += 1

# Crear DataFrame para la hoja "Partidos" con el cronograma correcto
df_partidos_cronograma = pd.DataFrame(cronograma, columns=['Ronda', 'Pista 1 Jugador 1', 'Pista 1 Jugador 2', 'Resultado Pista 1', 'Pista 2 Jugador 1', 'Pista 2 Jugador 2', 'Resultado Pista 2'])

# Crear DataFrame para la hoja "Jugadores"
df_jugadores = pd.DataFrame(jugadores, columns=['Jugadores'])

# Crear DataFrame para la hoja "Clasificación"
df_clasificacion = pd.DataFrame(jugadores, columns=['Jugador'])
df_clasificacion['Partidos Jugados'] = 0
df_clasificacion['Partidos Ganados'] = 0
df_clasificacion['Partidos Perdidos'] = 0
df_clasificacion['Puntos'] = 0

# Crear el archivo Excel con el cronograma correcto
with pd.ExcelWriter('Torneo_Padel_Correcto.xlsx', engine='openpyxl') as writer:
    df_jugadores.to_excel(writer, sheet_name='Jugadores', index=False)
    df_partidos_cronograma.to_excel(writer, sheet_name='Partidos', index=False)
    df_clasificacion.to_excel(writer, sheet_name='Clasificación', index=False)
