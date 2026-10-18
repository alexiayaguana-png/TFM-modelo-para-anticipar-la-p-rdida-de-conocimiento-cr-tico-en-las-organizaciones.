import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Modelo Predictivo de Riesgo de Conocimiento | People Analytics",
    page_icon="🧠",
    layout="wide"
)

# Estilo visual y cabecera
st.title("🧠 Modelo de Diagnóstico: Anticipación de Pérdida de Conocimiento Crítico")
st.markdown("""
*Herramienta interactiva basada en el TFM de People Analytics y Gestión del Talento Digital.*  
Este cuadro de mando evalúa de forma integrada la exposición demográfica, la criticidad del conocimiento, los mecanismos de transferencia y el clima organizacional para prevenir riesgos ante el relevo generacional[cite: 1].
""")

st.divider()

# Panel lateral para la entrada de datos del empleado/puesto
st.sidebar.header("⚙️ Parámetros de Evaluación del Puesto")
st.sidebar.markdown("Selecciona o introduce los indicadores del perfil analizado:")

# 1. Dimensión Demográfica
st.sidebar.subheader("1. Dimensión Demográfica")
horizonte_salida = st.sidebar.selectbox(
    "Horizonte temporal de jubilación/salida:",
    ["Más de 5 años (> 5 años) [Bajo]", "Entre 2 y 5 años [Medio]", "Menos de 2 años (< 2 años) [Alto]"],
    index=2
)
antiguedad = st.sidebar.slider("Antigüedad en la empresa (años):", 1, 35, 18)

# 2. Dimensión Conocimiento Crítico
st.sidebar.subheader("2. Conocimiento Crítico")
impacto_operativo = st.sidebar.selectbox(
    "Impacto operativo de la pérdida:",
    ["Bajo (Operativa rutinaria)", "Medio (Afecta parcialmente)", "Alto (Paralización o pérdida crítica)"],
    index=2
)
nivel_tacito = st.sidebar.selectbox(
    "Naturaleza del conocimiento:",
    ["Explícito y documentado", "Parcialmente tácito", "Mayoritariamente tácito y no documentado"],
    index=2
)

# 3. Dimensión Transferencia
st.sidebar.subheader("3. Transferencia de Conocimiento")
canales_transferencia = st.sidebar.selectbox(
    "Mecanismos de transferencia activos:",
    ["Mentoría formal y redes distribuidas [Protector]", "Canales informales cotidianos [Medio]", "Sin canales formales ni mentorías [Agravante]"],
    index=2
)

# 4. Dimensión Clima Organizacional
st.sidebar.subheader("4. Clima Organizacional")
clima_organizacional = st.sidebar.selectbox(
    "Clima y cultura de colaboración:",
    ["Alta confianza y seguridad psicológica [Protector]", "Clima neutro / moderado", "Clima competitivo o hermético [Agravante]"],
    index=2
)

# Lógica de cálculo del Nivel de Riesgo Global (según las reglas de tu TFM)
# Asignamos puntuaciones internas (1: Bajo, 2: Medio, 3: Alto)
p_demo = 3 if "Menos de 2 años" in horizonte_salida else (2 if "Entre 2 y 5 años" in horizonte_salida else 1)
p_crit = 3 if "Mayoritariamente tácito" in nivel_tacito or "Alto" in impacto_operativo else (2 if "Parcialmente" in nivel_tacito else 1)
p_trans = 3 if "Sin canales" in canales_transferencia else (2 if "informales" in canales_transferencia else 1)
p_clima = 3 if "competitivo" in clima_organizacional else (2 if "neutro" in clima_organizacional else 1)

# Regla integradora de decisión
# Si hay salida inminente (p_demo=3) + conocimiento crítico (p_crit=3) + mala transferencia (p_trans=3) => RIESGO ALTO
score_total = (p_demo + p_crit + p_trans + p_clima) / 4

if p_demo == 3 and p_crit == 3 and p_trans >= 2:
    nivel_riesgo = "ALTO (Intervención Preventiva Prioritaria)"
    color_risk = "red"
elif score_total >= 2.5 or p_crit == 3:
    nivel_riesgo = "ALTO (Intervención Preventiva Prioritaria)"
    color_risk = "red"
elif score_total >= 1.75:
    nivel_riesgo = "MEDIO (Intervención Programada)"
    color_risk = "orange"
else:
    nivel_riesgo = "BAJO (Monitoreo Ordinario)"
    color_risk = "green"

# Cuerpo Principal del Dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Puntuación Global del Modelo", value=f"{score_total:.2f} / 3.0")
with col2:
    st.metric(label="Exposición Demográfica", value="Crítica (< 2 años)" if p_demo==3 else "Estable")
with col3:
    st.metric(label="Vulnerabilidad del Saber", value="Alta / Tácito" if p_crit==3 else "Controlada")

st.markdown("### 🎯 Diagnóstico Integrado del Puesto")
st.markdown(f"""
<div style="padding: 20px; border-radius: 10px; background-color: #f8f9fa; border-left: 6px solid {color_risk};">
    <h3 style="margin:0; color: {color_risk};">Nivel de Riesgo Global: {nivel_riesgo}</h3>
    <p style="margin-top: 10px; font-size: 16px;">
    El análisis cruzado de las dimensiones indica que la posición presenta una vulnerabilidad <b>{nivel_riesgo.split()[0]}</b> ante el relevo generacional. 
    Se requiere activar los protocolos de actuación correspondientes a este nivel de alerta.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Pestañas de detalle analítico
tab1, tab2, tab3 = st.tabs(["📊 Desglose por Dimensiones", "🚨 Plan de Acción RRHH", "💡 Insights de People Analytics"])

with tab1:
    st.subheader("Evaluación detallada de factores")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Dimensión Demográfica:** Puntuación {p_demo}/3")
        st.progress(p_demo / 3)
        st.write(f"**Conocimiento Crítico:** Puntuación {p_crit}/3")
        st.progress(p_crit / 3)
    with col_b:
        st.write(f"**Transferencia (Riesgo Insuficiencia):** Puntuación {p_trans}/3")
        st.progress(p_trans / 3)
        st.write(f"**Clima Organizacional (Riesgo Barreras):** Puntuación {p_clima}/3")
        st.progress(p_clima / 3)

with tab2:
    st.subheader("Medidas preventivas recomendadas por la herramienta:")
    if "ALTO" in nivel_riesgo:
        st.error("🚨 **Acciones Prioritarias Requeridas:**")
        st.markdown("""
        1. **Entrevistas de explicitación:** Iniciar sesiones semanales de transferencia con el experto sénior.
        2. **Liberación de horas:** Asignar presupuesto para reducir carga operativa ordinaria y enfocar al mentor.
        3. **Asignación formal de sucesores:** Crear parejas de trabajo y monitorizar el grado de asimilación del conocimiento tácito.
        """)
    elif "MEDIO" in nivel_riesgo:
        st.warning("⚠️ **Acciones de Intervención Programada:**")
        st.markdown("""
        1. Actualizar manuales y repositorios de procesos documentales.
        2. Fomentar talleres transversales y aprendizaje *on-the-job*.
        """)
    else:
        st.success("✅ **Seguimiento Ordinario:**")
        st.markdown("Mantener la actualización rutinaria de procedimientos y la revisión periódica del cuadro de mandos.")

with tab3:
    st.markdown("""
    * **Valor analítico:** Este prototipo demuestra cómo la analítica de personas permite pasar de una gestión reactiva a una estrategia predictiva.
    * **Fuentes integradas:** Datos de sistemas HRIS, evaluación de mandos y análisis de redes informales (ONA).
    """)

st.divider()
st.caption("People Analytics TFM Dashboard | Desarrollado para fines académicos y de simulación profesional.")
