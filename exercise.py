import streamlit as st
import random

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Generador de Ejercicios de Física",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Generador de Ejercicios: MRU")
st.markdown("Genera una variante individual o un lote completo con versiones distintas para cada alumno.")

# 2. LÓGICA DE GENERACIÓN (Valores físicos coherentes)
def generar_ejercicio_mru():
    tiempo_min = random.choice([12, 15, 20, 30, 45, 60, 90])
    velocidad_kmh = random.choice([40, 50, 60, 80, 90, 100, 120])
    
    tiempo_h = tiempo_min / 60.0
    distancia_km = velocidad_kmh * tiempo_h
    distancia_m = distancia_km * 1000
    
    return {
        'v': velocidad_kmh,
        't_min': tiempo_min,
        't_h': tiempo_h,
        'd_km': distancia_km,
        'd_m': distancia_m
    }

# Genera N versiones garantizando que sean datos únicos en la medida de lo posible
def generar_lote_versiones(num_versiones):
    versiones = []
    combinaciones_usadas = set()
    
    intentos = 0
    max_intentos = 500  # Evitar bucle infinito si se piden más versiones que combinaciones posibles
    
    while len(versiones) < num_versiones and intentos < max_intentos:
        intentos += 1
        ejercicio = generar_ejercicio_mru()
        clave = (ejercicio['v'], ejercicio['t_min'])
        
        # Si queremos versiones únicas por combinación (v, t)
        if clave not in combinaciones_usadas:
            combinaciones_usadas.add(clave)
            versiones.append(ejercicio)
        elif len(combinaciones_usadas) >= 49:  # 7 tiempos x 7 velocidades = 49 combinaciones únicas
            # Si se piden más de 49 versiones, permitimos repetir combinaciones
            versiones.append(ejercicio)
            
    return versiones

# 3. INTERFAZ EN PESTAÑAS
tab1, tab2 = st.tabs(["👤 Generar 1 Versión Individual", "👥 Generar N Versiones (Para Alumnos)"])

# ---------------------------------------------------------
# PESTAÑA 1: UNA SOLA VERSIÓN
# ---------------------------------------------------------
with tab1:
    st.subheader("Modo Individual")
    
    if st.button("🎲 Generar Ejercicio Único", type="primary"):
        st.session_state['ejercicio_unico'] = generar_ejercicio_mru()

    if 'ejercicio_unico' in st.session_state:
        datos = st.session_state['ejercicio_unico']
        
        st.info(
            f"**Enunciado:**\n\n"
            f"Un automóvil se desplaza en línea recta a una velocidad constante de "
            f"**{datos['v']} km/h** durante un intervalo de **{datos['t_min']} minutos**.\n\n"
            f"👉 *Calcula la distancia total recorrida en metros (m).* "
        )
        
        with st.expander("👁️ Ver Solución Paso a Paso"):
            st.write("**Paso 1: Convertir el tiempo a horas (h)**")
            st.latex(rf"t = \frac{{{datos['t_min']} \text{{ min}}}}{{60}} = {datos['t_h']:.2f} \text{{ h}}")
            
            st.write("**Paso 2: Aplicar la fórmula del MRU ($d = v \cdot t$)**")
            st.latex(rf"d = {datos['v']} \text{{ km/h}} \times {datos['t_h']:.2f} \text{{ h}} = {datos['d_km']:.2f} \text{{ km}}")
            
            st.write("**Paso 3: Convertir el resultado a metros (m)**")
            st.latex(rf"d = {datos['d_km']:.2f} \times 1000 = {datos['d_m']:.0f} \text{{ m}}")
            
            st.success(f"**Respuesta final:** {datos['d_m']:.0f} m")
    else:
        st.write("👈 Haz clic en el botón para generar la primera versión.")

# ---------------------------------------------------------
# PESTAÑA 2: TODAS LAS VERSIONES REQUERIDAS (EJ. 30 ALUMNOS)
# ---------------------------------------------------------
with tab2:
    st.subheader("Generación Masiva por Alumno")
    
    cant_alumnos = st.number_input(
        "Número de alumnos / versiones que necesitas:",
        min_value=1,
        max_value=100,
        value=30,
        step=1
    )
    
    if st.button(f"🚀 Generar {cant_alumnos} Versiones Diferentes"):
        lote = generar_lote_versiones(cant_alumnos)
        
        # Guardar en sesión para mantenerlos en pantalla
        st.session_state['lote_ejercicios'] = lote
        st.success(f"¡Se han generado con éxito {len(lote)} versiones distintas!")

    if 'lote_ejercicios' in st.session_state:
        lote = st.session_state['lote_ejercicios']
        
        # Crear texto formateado listo para descargar en .txt
        texto_descarga = f"=========================================\n"
        texto_descarga += f" BANCO DE EXÁMENES / EJERCICIOS (MRU)\n"
        texto_descarga += f" Total de versiones: {len(lote)}\n"
        texto_descarga += f"=========================================\n\n"
        
        for i, d in enumerate(lote, start=1):
            texto_descarga += f"--- ALUMNO / VERSIÓN #{i} ---\n"
            texto_descarga += f"Enunciado: Un automóvil se desplaza en línea recta a una velocidad constante de {d['v']} km/h durante {d['t_min']} minutos.\n"
            texto_descarga += f"Pregunta: Calcula la distancia total recorrida en metros (m).\n"
            texto_descarga += f"SOLUCIÓN -> t = {d['t_h']:.2f} h | d = {d['d_km']:.2f} km | RESULTADO FINAL: {d['d_m']:.0f} m\n\n"
        
        # Botón para descargar todas las versiones en un solo archivo
        st.download_button(
            label=f"📥 Descargar las {len(lote)} versiones (.txt)",
            data=texto_descarga,
            file_name=f"ejercicios_mru_{len(lote)}_alumnos.txt",
            mime="text/plain"
        )
        
        # Visualizador en pantalla dentro de un contenedor desplegable
        with st.expander("🔍 Previsualizar todas las versiones generadas en pantalla"):
            for i, d in enumerate(lote, start=1):
                st.markdown(f"**Alumno / Versión #{i}**")
                st.write(f"- **Velocidad:** {d['v']} km/h | **Tiempo:** {d['t_min']} min")
                st.write(f"- **Solución:** {d['d_m']:.0f} m")
                st.divider()
