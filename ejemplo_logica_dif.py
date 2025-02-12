import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import matplotlib.pyplot as plt

# 1️⃣ Definir las variables difusas
servicio = ctrl.Antecedent(np.arange(0, 11, 1), 'servicio')
comida = ctrl.Antecedent(np.arange(0, 11, 1), 'comida')
propina = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

# 2️⃣ Definir las funciones de pertenencia
servicio['malo'] = fuzz.trimf(servicio.universe, [0, 0, 5])
servicio['regular'] = fuzz.trimf(servicio.universe, [0, 5, 10])
servicio['bueno'] = fuzz.trimf(servicio.universe, [5, 10, 10])

comida['mala'] = fuzz.trimf(comida.universe, [0, 0, 5])
comida['regular'] = fuzz.trimf(comida.universe, [0, 5, 10])
comida['buena'] = fuzz.trimf(comida.universe, [5, 10, 10])

propina['baja'] = fuzz.trimf(propina.universe, [0, 0, 13])
propina['media'] = fuzz.trimf(propina.universe, [0, 13, 25])
propina['alta'] = fuzz.trimf(propina.universe, [13, 25, 25])

# 3️⃣ Definir las reglas difusas
regla1 = ctrl.Rule(servicio['malo'] | comida['mala'], propina['baja'])
regla2 = ctrl.Rule(servicio['regular'], propina['media'])
regla3 = ctrl.Rule(servicio['bueno'] | comida['buena'], propina['alta'])

# 4️⃣ Crear el sistema de control difuso
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3])
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# 5️⃣ Función para convertir la entrada del usuario a un valor de 0 a 10
def convertir_a_rango(valor):
    if valor == 1:  # Malo
        return 2  
    elif valor == 2:  # Regular
        return 5  
    elif valor == 3:  # Bueno
        return 8  
    else:
        return None  

# 6️⃣ Capturar entradas del usuario con validación
while True:
    try:
        servicio_usuario = int(input("🛎️ Clasifique el servicio (1=Malo, 2=Regular, 3=Bueno): "))
        if servicio_usuario not in [1, 2, 3]:
            raise ValueError("⚠️ Ingrese solo 1, 2 o 3.")
        break
    except ValueError as e:
        print(e)

while True:
    try:
        comida_usuario = int(input("🍽️ Clasifique la comida (1=Mala, 2=Regular, 3=Buena): "))
        if comida_usuario not in [1, 2, 3]:
            raise ValueError("⚠️ Ingrese solo 1, 2 o 3.")
        break
    except ValueError as e:
        print(e)

while True:
    try:
        monto_factura = float(input("💰 Ingrese el monto total de la factura: $"))
        if monto_factura <= 0:
            raise ValueError("⚠️ El monto de la factura debe ser mayor a 0.")
        break
    except ValueError as e:
        print(e)

# Convertir a valores en la escala difusa
servicio_valor = convertir_a_rango(servicio_usuario)
comida_valor = convertir_a_rango(comida_usuario)

# 7️⃣ Evaluar el sistema con los valores convertidos
sistema.input['servicio'] = servicio_valor
sistema.input['comida'] = comida_valor
sistema.compute()
propina_porcentaje = sistema.output['propina']

# 8️⃣ Calcular montos finales
monto_propina = (propina_porcentaje / 100) * monto_factura
total_pagar = monto_factura + monto_propina

# 9️⃣ Explicación detallada de la decisión
print("\n📊 Evaluación del Sistema de Propinas 📊")
print(f"- Servicio recibido: {servicio_valor}/10 ({'Malo' if servicio_usuario == 1 else 'Regular' if servicio_usuario == 2 else 'Bueno'})")
print(f"- Comida recibida: {comida_valor}/10 ({'Mala' if comida_usuario == 1 else 'Regular' if comida_usuario == 2 else 'Buena'})")

# Calcular el grado de pertenencia de las entradas
serv_malo = fuzz.interp_membership(servicio.universe, servicio['malo'].mf, servicio_valor)
serv_regular = fuzz.interp_membership(servicio.universe, servicio['regular'].mf, servicio_valor)
serv_bueno = fuzz.interp_membership(servicio.universe, servicio['bueno'].mf, servicio_valor)

comida_mala = fuzz.interp_membership(comida.universe, comida['mala'].mf, comida_valor)
comida_regular = fuzz.interp_membership(comida.universe, comida['regular'].mf, comida_valor)
comida_buena = fuzz.interp_membership(comida.universe, comida['buena'].mf, comida_valor)

print("\n🔍 Grado de pertenencia de las entradas:")
print(f"  - Servicio malo: {serv_malo:.2f}")
print(f"  - Servicio regular: {serv_regular:.2f}")
print(f"  - Servicio bueno: {serv_bueno:.2f}")

print(f"  - Comida mala: {comida_mala:.2f}")
print(f"  - Comida regular: {comida_regular:.2f}")
print(f"  - Comida buena: {comida_buena:.2f}")

print(f"\n💰 Propina recomendada: {propina_porcentaje:.2f}%")
print(f"💵 Monto de la propina: ${monto_propina:.2f}")
print(f"🧾 Total a pagar: ${total_pagar:.2f}")

# 🔟 Visualizar resultados con gráfico
fig, ax = plt.subplots()
ax.plot(propina.universe, fuzz.trimf(propina.universe, [0, 0, 13]), label='Baja')
ax.plot(propina.universe, fuzz.trimf(propina.universe, [0, 13, 25]), label='Media')
ax.plot(propina.universe, fuzz.trimf(propina.universe, [13, 25, 25]), label='Alta')

# Mostrar la propina calculada en el gráfico
ax.axvline(x=propina_porcentaje, color='r', linestyle='--', label=f'Propina Recomendada: {propina_porcentaje:.2f}%')
ax.legend()
plt.title("Funciones de Pertenencia - Propina")
plt.xlabel("Porcentaje de propina")
plt.ylabel("Grado de pertenencia")
plt.show()
