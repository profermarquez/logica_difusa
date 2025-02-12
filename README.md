# Contexto
Determinar la propina con lógica difusa
Descripción del problema
Queremos calcular qué porcentaje de propina dejar basado en dos factores:

Calidad del servicio (de 0 a 10).
Calidad de la comida (de 0 a 10).
Propina recomendada (de 0% a 25%).
Paso 1: Definir las variables difusas

Servicio: Malo, regular, bueno.
Comida: Mala, regular, buena.
Propina: Baja, media, alta.
Paso 2: Definir reglas difusas Ejemplo de reglas:

Si el servicio es malo o la comida es mala, la propina es baja.
Si el servicio es regular, la propina es media.
Si el servicio es bueno o la comida es buena, la propina es alta.

# Instalar e activar el entorno virtual
/virtualenv env             /env/Scripts/activate.bat

# requerimientos
pip install numpy

pip install scikit-fuzzy

pip install scipy

pip install packaging

pip install networkx

pip install matplotlib

pip install pygame

# ejecución
py ejemplo_logica_dif.py

py control_riego.py

# libreria
https://scikit-fuzzy.readthedocs.io/en/latest/userguide/getting_started.html
