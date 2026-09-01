import streamlit as st
import random

# 1. CONFIGURACIÓN DE LA PÁGINA (Título, ícono y layout)
st.set_page_config(
    page_title="Generador de Ejercicios de Física",
    page_icon="🚗",
    layout="centered"
)

# Estilo visual básico (Título e instrucciones)
st.title("🚗 Generador de Ejercicios: MRU")
st.markdown("Presiona el botón para obtener una variante con datos aleatorios pero coherentes.")

# 2. LÓGICA DE GENERACIÓN (Valores físicos reales)
def generar_ejercicio():
    # Tiempo en minutos (enteros convenientes para evitar decimales infinitos)
    tiempo_min = random.choice([12, 15, 20, 30, 45, 60, 90])
    
    # Velocidad en km/h (valores típicos de tráfico)
    velocidad_kmh = random.choice([40, 50, 60, 80, 90, 100, 120])
    
    # Cálculos físicos
    tiempo_h = tiempo_min / 60.0
    distancia_km = velocidad_kmh * tiempo_h
    distancia_m = distancia_km * 1000
    
    return velocidad_kmh, tiempo_min, tiempo_h, distancia_km, distancia_m

# 3. INTERFAZ INTERACTIVA CON STREAMLIT

# Botón principal para generar nuevo ejercicio
if st.button("🎲 Generar Nuevo Ejercicio", type="primary"):
    v, t_min, t_h, d_km, d_m = generar_ejercicio()
    
    # Guardar en el estado de la sesión para evitar que cambie al interactuar con la pantalla
    st.session_state['ejercicio'] = {
        'v': v, 't_min': t_min, 't_h': t_h, 'd_km': d_km, 'd_m': d_m
    }

# Renderizado del ejercicio (si existe en sesión)
if 'ejercicio' in st.session_state:
    datos = st.session_state['ejercicio']
    
    # Caja destacada con el Enunciado
    st.info(
        f"**Enunciado:**\n\n"
        f"Un automóvil se desplaza en línea recta a una velocidad constante de "
        f"**{datos['v']} km/h** durante un intervalo de **{datos['t_min']} minutos**.\n\n"
        f"👉 *Calcula la distancia total recorrida en metros (m).* "
    )
    
    # Sección oculta con la Solución
    with st.expander("👁️ Ver Solución Paso a Paso"):
        st.write(f"**Paso 1: Convertir el tiempo a horas (h)**")
        st.latex(rf"t = \frac{{{datos['t_min']} \text{{ min}}}}{{60}} = {datos['t_h']:.2f} \text{{ h}}")
        
        st.write(f"**Paso 2: Aplicar la fórmula del MRU ($d = v \cdot t$)**")
        st.latex(rf"d = {datos['v']} \text{{ km/h}} \times {datos['t_h']:.2f} \text{{ h}} = {datos['d_km']:.2f} \text{{ km}}")
        
        st.write(f"**Paso 3: Convertir el resultado a metros (m)**")
        st.latex(rf"d = {datos['d_km']:.2f} \times 1000 = {datos['d_m']:.0f} \text{{ m}}")
        
        st.success(f"**Respuesta final:** {datos['d_m']:.0f} m")

else:
    st.write("👈 Haz clic en el botón de arriba para crear la primera variante.")
