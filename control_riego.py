import pygame
import time
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema de Riego con Lógica Difusa")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (180, 180, 180)

# Definición de la lógica difusa
temperatura = ctrl.Antecedent(np.arange(-10, 41, 1), 'temperatura')
riego = ctrl.Consequent(np.arange(0, 101, 1), 'riego')

# Definir conjuntos difusos
temperatura['baja'] = fuzz.trimf(temperatura.universe, [-10, 0, 15])
temperatura['media'] = fuzz.trimf(temperatura.universe, [10, 18, 25])
temperatura['alta'] = fuzz.trimf(temperatura.universe, [20, 40, 40])

riego['bajo'] = fuzz.trimf(riego.universe, [0, 0, 40])
riego['medio'] = fuzz.trimf(riego.universe, [30, 50, 70])
riego['alto'] = fuzz.trimf(riego.universe, [60, 100, 100])

# Reglas de riego
rule1 = ctrl.Rule(temperatura['baja'], riego['bajo'])
rule2 = ctrl.Rule(temperatura['media'], riego['medio'])
rule3 = ctrl.Rule(temperatura['alta'], riego['alto'])

# Crear el sistema de control
riego_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
riego_simulador = ctrl.ControlSystemSimulation(riego_ctrl)

# Configuración de velocidad (lenta, normal, rápida)
velocidades = [2, 1, 0.5]  
indice_velocidad = 1  
boton_presionado = False  

# Función para determinar si es de día o de noche
def es_dia(hora):
    return 6 <= hora < 18

# Generar temperatura realista según el horario
def generar_temperatura(hora):
    if es_dia(hora):
        return 18 + np.abs(np.sin(time.time() / 5) * 20)  
    else:
        return 5 + np.abs(np.sin(time.time() / 5) * 10)  

# Dibujar la planta
def dibujar_planta():
    pygame.draw.rect(screen, BROWN, (340, 450, 120, 80))  
    pygame.draw.line(screen, GREEN, (400, 450), (400, 300), 10)  
    pygame.draw.ellipse(screen, GREEN, (360, 320, 40, 30))  
    pygame.draw.ellipse(screen, GREEN, (400, 320, 40, 30))  
    pygame.draw.circle(screen, RED, (400, 290), 20)  

# Dibujar el sol o la luna
def dibujar_sol_o_luna(hora):
    if es_dia(hora):
        pygame.draw.circle(screen, YELLOW, (700, 100), 50)  
    else:
        pygame.draw.circle(screen, GRAY, (700, 100), 50)  

# Dibujar el termómetro y la temperatura
def dibujar_termometro(temp):
    pygame.draw.rect(screen, BLACK, (50, 100, 40, 200))  
    pygame.draw.rect(screen, RED, (50, 300 - int(temp * 5), 40, int(temp * 5)))  
    pygame.draw.circle(screen, RED, (70, 320), 20)  
    font = pygame.font.Font(None, 36)
    texto_temp = font.render(f"Temp: {int(temp)}°C", True, BLACK)
    screen.blit(texto_temp, (50, 50))  

# Dibujar la bomba de agua y la manguera con leyenda
def dibujar_bomba():
    pygame.draw.rect(screen, BLACK, (100, 450, 80, 60))  
    pygame.draw.line(screen, BLACK, (180, 480), (300, 480), 10)  
    font = pygame.font.Font(None, 24)
    texto_bomba = font.render("Bomba de Agua", True, BLACK)
    screen.blit(texto_bomba, (90, 520))  

# Dibujar el botón de velocidad
def dibujar_boton():
    global boton_presionado
    color_boton = DARK_GRAY if boton_presionado else LIGHT_GRAY  
    pygame.draw.rect(screen, color_boton, (300, 550, 200, 40), border_radius=10)
    font = pygame.font.Font(None, 36)
    texto_boton = font.render(f"<| {['Lento', 'Normal', 'Rápido'][indice_velocidad]} |>", True, BLACK)
    screen.blit(texto_boton, (315, 560))  

# Dibujar gotas de agua si la bomba está regando
def dibujar_riego(nivel_riego):
    if nivel_riego > 50:
        for i in range(5):
            pygame.draw.circle(screen, BLUE, (300 + i * 20, 480 - i * 10), 6)  

# Mostrar la hora y si es día o noche
def mostrar_hora(hora):
    font = pygame.font.Font(None, 36)
    texto_hora = font.render(f"Hora: {hora}:00", True, BLACK)
    texto_dia_noche = font.render("Día" if es_dia(hora) else "Noche", True, BLACK)
    screen.blit(texto_hora, (600, 500))
    screen.blit(texto_dia_noche, (600, 530))

# Simulación del sistema
running = True
hora = 0
while running:
    screen.fill(WHITE)

    # Obtener la temperatura simulada según el horario
    temperatura_actual = generar_temperatura(hora)

    # Calcular el riego con la lógica difusa
    riego_simulador.input['temperatura'] = temperatura_actual
    riego_simulador.compute()
    nivel_riego = riego_simulador.output['riego']

    # Dibujar elementos
    dibujar_sol_o_luna(hora)
    dibujar_planta()
    dibujar_termometro(temperatura_actual)
    dibujar_bomba()
    dibujar_boton()
    mostrar_hora(hora)

    # Indicar si la bomba está regando
    font = pygame.font.Font(None, 36)
    texto_estado = font.render("Regando" if nivel_riego > 50 else "No Regando", True, BLUE if nivel_riego > 50 else BLACK)
    screen.blit(texto_estado, (300, 460))

    # Dibujar las gotas de agua si la bomba está regando
    dibujar_riego(nivel_riego)

    pygame.display.flip()
    time.sleep(velocidades[indice_velocidad])
    hora = (hora + 1) % 24  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 300 <= x <= 500 and 550 <= y <= 590:
                boton_presionado = True
        elif event.type == pygame.MOUSEBUTTONUP:
            boton_presionado = False
            indice_velocidad = (indice_velocidad + 1) % 3  

pygame.quit()
