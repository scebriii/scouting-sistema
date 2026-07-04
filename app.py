import pandas as pd
import streamlit as st

import database as db
import utils
import tactical_server

# Configuración global de la página
st.set_page_config(
    page_title="Scouting Inteligente",
    page_icon="🎯",
    layout="wide",
)


def inyectar_css_premium():
    """Inyecta CSS personalizado para aplicar un diseño de Glassmorphism."""
    st.markdown(
        """
    <style>
        /* 1. Ocultar el branding por defecto de Streamlit para un look limpio */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* 2. Fondo global inmersivo (Dark Theme deportivo) */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }

        /* 3. Efecto Glassmorphism en métricas, formularios y contenedores */
        [data-testid="stForm"], [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 20px !important;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        /* 4. Micro-interacciones (Hover) al pasar el ratón */
        [data-testid="stForm"]:hover, [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        /* 5. Estilización de las Pestañas (Tabs) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px 8px 0 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: none;
            padding: 10px 20px;
            color: #94a3b8;
        }

        /* Pestaña activa */
        .stTabs [aria-selected="true"] {
            background: rgba(255, 255, 255, 0.15);
            color: #ffffff;
            border-bottom: 2px solid #3b82f6; /* Acento azul tecnológico */
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def inicializar_datos():
    """Inicializa la base de datos y carga los datos de prueba si está vacía."""
    db.init_db()
    utils.cargar_datos_mock()

def render_dashboard(rivales, nombres):
    """Renderiza la pestaña del Panel General."""
    if not rivales:
        st.info("No hay datos para mostrar en el dashboard.")
        return

    rival_sel = st.selectbox("Próximo rival", list(nombres.keys()), key="dash_rival")
    rival_id = nombres[rival_sel]
    rival = db.obtener_rival(rival_id)

    # Cabecera táctica
    c1, c2 = st.columns(2)
    c1.metric("Sistema táctico base", rival["sistema_tactico"])
    c2.markdown(f"Estilo de juego predominante: {rival['estilo_juego']}")
    st.divider()

    # Visualización de KPIs
    kpis = db.obtener_informes(rival_id, tipo="KPI")
    if kpis:
        st.subheader("Indicadores Clave de Rendimiento (KPIs)")
        cols = st.columns(min(len(kpis), 4) or 1)
        for i, k in enumerate(kpis):
            cols[i % 4].metric(label=k["descripcion"], value=k["valor_kpi"], help=k["fase"])
        st.divider()

    # Análisis FODA contextualizado
    col_f, col_d = st.columns(2)
    with col_f:
        st.subheader("💪 Fortalezas detectadas")
        fortalezas = db.obtener_informes(rival_id, tipo="Fortaleza")
        if fortalezas:
            for f in fortalezas:
                st.success(f"{f['fase']} — {f['descripcion']}")
        else:
            st.caption("Sin fortalezas registradas en la base de datos.")
            
    with col_d:
        st.subheader("🎯 Vulnerabilidades")
        debilidades = db.obtener_informes(rival_id, tipo="Debilidad")
        if debilidades:
            for d in debilidades:
                st.error(f"{d['fase']} — {d['descripcion']}")
        else:
            st.caption("Sin debilidades registradas en la base de datos.")

    st.divider()
    
    # Registro histórico
    st.subheader("Informe metodológico completo")
    informes = db.obtener_informes(rival_id)
    if informes:
        df = pd.DataFrame(informes)[["fase", "tipo", "descripcion", "valor_kpi", "fecha"]]
        df.columns = ["Fase del Juego", "Clasificación", "Descripción Táctica", "Valor", "Fecha de Registro"]
        st.dataframe(df, use_container_width=True, hide_index=True)

def render_ingesta(rivales, nombres):
    """Renderiza la pestaña de Ingesta de Datos."""
    st.subheader("Alta de nuevo rival")
    with st.form("form_rival", clear_on_submit=True):
        fc1, fc2, fc3 = st.columns(3)
        nombre = fc1.text_input("Nombre del rival")
        sistema = fc2.selectbox(
            "Sistema táctico base",
            ["1-4-3-3", "1-4-4-2", "1-4-2-3-1", "1-3-5-2", "1-5-3-2", "1-3-4-3", "Otro"],
        )
        estilo = fc3.text_input("Estilo de juego (Ej: Juego de posición, Contragolpe)")
        
        if st.form_submit_button("Guardar perfil de rival", type="primary"):
            if nombre.strip():
                try:
                    db.insertar_rival(nombre.strip(), sistema, estilo.strip())
                    st.success(f"Rival '{nombre}' registrado correctamente.")
                    st.rerun() # Obligatorio para actualizar el estado global
                except Exception:
                    st.error("Error: Ya existe un rival con ese nombre en la base de datos.")
            else:
                st.error("El campo 'Nombre del rival' no puede estar vacío.")

    st.divider()
    
    st.subheader("Registro de eventos de Scouting")
    if not rivales:
        st.info("Debe registrar al menos un rival para añadir informes de scouting.")
        return
    with st.form("form_informe", clear_on_submit=True):
        ic1, ic2, ic3 = st.columns(3)
        rival_inf = ic1.selectbox("Seleccionar Rival", list(nombres.keys()))
        fase = ic2.selectbox("Fase del juego", db.FASES)
        tipo = ic3.selectbox("Clasificación del registro", db.TIPOS_REGISTRO)
        
        descripcion = st.text_area(
            "Descripción cualitativa",
            placeholder="Ej: El pivote defensivo sufre a la espalda en transiciones rápidas.",
        )
        valor_kpi = st.text_input(
            "Valor métrico (Obligatorio si es KPI)",
            placeholder="Ej: 62%, 1.8 xG, 12 recuperaciones",
        )
        
        if st.form_submit_button("Guardar evento de scouting", type="primary"):
            if not descripcion.strip():
                st.error("La descripción cualitativa es obligatoria.")
            elif tipo == "KPI" and not valor_kpi.strip():
                st.error("Si el registro es un KPI, debe incluir un valor métrico.")
            else:
                db.insertar_informe(
                    nombres[rival_inf],
                    fase,
                    tipo,
                    descripcion.strip(),
                    valor_kpi.strip() or None,
                )
                st.success("Evento de scouting guardado con éxito.")
                st.rerun() # Actualiza el dashboard inmediatamente

def render_pizarra_tactica(rivales, nombres):
    """Renderiza la Pizarra Táctica con el simulador React integrado."""
    if not rivales:
        st.info("Registra un rival en 'Ingesta de Datos' para usar la Pizarra Táctica con datos del rival.")

    # Selector de rival para cargar información táctica
    rival_tactico = st.selectbox(
        "Seleccionar rival para cargar sistema táctico",
        [""] + list(nombres.keys()),
        key="tactico_rival",
    )

    # Obtener info del rival seleccionado
    rival_info = None
    if rival_tactico:
        rival_id = nombres[rival_tactico]
        rival_info = db.obtener_rival(rival_id)
        sistema = str(rival_info.get("sistema_tactico", "4-3-3")) if rival_info else "4-3-3"
        estilo = str(rival_info.get("estilo_juego", "")) if rival_info else ""

        # Info del rival en cabecera
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            st.markdown(f"### 🏟️ Analizando a: **{rival_tactico}**")
            st.caption(f"Sistema: {sistema} | Estilo: {estilo or 'No definido'}")

    # Título de la pizarra
    st.markdown("### ⚽ Pizarra Táctica Interactiva — TacticalOS")
    st.caption("Arrastra jugadores para diseñar jugadas. Usa los conos de visión, líneas de pase y analítica CAFYD.")

    # Obtener URL del servidor de estáticos
    tactical_url = tactical_server.get_tactical_url()

    # Inyectar datos del rival como variable global antes del iframe
    import json
    rival_init = json.dumps({
        "rival": rival_tactico,
        "sistema": sistema if rival_tactico else "4-3-3",
        "estilo": estilo,
    })

    # Wrapper HTML: inyecta datos + iframe al simulador
    wrapper_html = f"""
    <script>
        window.__TACTICAL_RIVAL_DATA = {rival_init};
    </script>
    <iframe
        src="{tactical_url}/index.html"
        width="100%"
        height="900"
        frameborder="0"
        style="border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);"
        allowfullscreen
    ></iframe>
    """

    st.components.v1.html(
        wrapper_html,
        height=950,
        scrolling=True,
    )

    # Info adicional debajo
    st.divider()
    with st.expander("💡 Guía rápida de la Pizarra Táctica"):
        st.markdown("""
**TacticalOS** es un simulador táctico avanzado para planificación de partidos:

- **🖱️ Arrastrar jugadores**: Coloca jugadores en posiciones específicas
- **Conos de visión**: Visualiza el campo de visión de cada jugador
- **Líneas de pase**: Identifica opciones de pase disponibles
- **Análisis CAFYD**: Métricas de control territorial, compactidad y orientación
- **Situaciones prefijadas**: Saques de banda, córners, libres, contragolpes
- **Exportar/Importar**: Guarda y carga configuraciones JSON
- **Dibujo libre**: Dibuja rutas, flechas y anotaciones sobre el campo
        """)


def render_plan_partido(rivales, nombres):
    """Renderiza la pestaña de la Matriz de Interacción y Plan de Partido."""
    if not rivales:
        st.info("Registra un rival para generar el plan de partido.")
        return

    rival_plan = st.selectbox("Seleccionar Rival para Planificación", list(nombres.keys()), key="plan_rival")
    rival_id = nombres[rival_plan]

    st.subheader("🧩 Matriz de Interacción Sistémica")
    st.caption("Analiza cómo interactúa el comportamiento del rival con nuestro propio modelo de juego.")

    interacciones = db.obtener_interacciones(rival_id)
    if interacciones:
        df_int = pd.DataFrame(interacciones)[
            ["caracteristica_rival", "impacto_tactico", "tipo_ventana", "ventana"]
        ]
        df_int.columns = ["Patrón del Rival", "Impacto en nuestro sistema", "Clasificación", "Ventana de Acción"]
        
        st.dataframe(
            df_int,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Clasificación": st.column_config.TextColumn(width="small")
            },
        )
        
        # Validar la estructura de datos antes de contar
        n_op = sum(1 for i in interacciones if i.get("tipo_ventana") == "Oportunidad")
        n_am = len(interacciones) - n_op
        
        mc1, mc2 = st.columns(2)
        mc1.metric("🟢 Ventanas de Oportunidad", n_op)
        mc2.metric("🔴 Amenazas Estructurales", n_am)
    else:
        st.info("No hay interacciones tácticas registradas para este rival.")
    with st.expander("➕ Añadir nueva interacción sistémica"):
        with st.form("form_interaccion", clear_on_submit=True):
            caracteristica = st.text_input("Patrón del rival (Ej: Presión alta orientada a banda)")
            impacto = st.text_input("Impacto en nuestro sistema (Ej: Dificulta salida limpia por carriles exteriores)")
            
            xc1, xc2 = st.columns([1, 2])
            tipo_v = xc1.selectbox("Clasificación", ["Oportunidad", "Amenaza"])
            ventana = xc2.text_input("Ventana de Acción (Ej: Atraer por fuera para jugar por dentro)")
            
            if st.form_submit_button("Registrar interacción", type="primary"):
                if caracteristica.strip() and impacto.strip() and ventana.strip():
                    db.insertar_interaccion(
                        rival_id,
                        caracteristica.strip(),
                        impacto.strip(),
                        tipo_v,
                        ventana.strip(),
                    )
                    st.success("Interacción registrada correctamente.")
                    st.rerun()
                else:
                    st.error("Todos los campos analíticos son obligatorios.")

    st.divider()
    st.subheader("📋 Diseño del Plan de Partido y Microciclo")

    plan = db.obtener_plan(rival_id) or {}
    with st.form("form_plan"):
        objetivo = st.text_area(
            "Objetivo táctico principal", value=plan.get("objetivo_semanal", "")
        )
        
        st.markdown("### Consignas Operativas (Máximo 3)")
        c1 = st.text_input("Consigna 1", value=plan.get("consigna_1", "") or "")
        c2 = st.text_input("Consigna 2", value=plan.get("consigna_2", "") or "")
        c3 = st.text_input("Consigna 3", value=plan.get("consigna_3", "") or "")
        
        tareas = st.text_area(
            "Diseño de tareas (Transferencia al entrenamiento)",
            value=plan.get("tareas_entrenamiento", "") or "",
            height=140,
            placeholder="Ej: MD+3: Posesión direccional 6v6+3 comodines priorizando pases filtrados por el carril central.",
        )
        
        if st.form_submit_button("Actualizar Plan de Partido", type="primary"):
            if objetivo.strip():
                db.guardar_plan(
                    rival_id,
                    objetivo.strip(),
                    c1.strip(),
                    c2.strip(),
                    c3.strip(),
                    tareas.strip(),
                )
                st.success("Plan de partido actualizado. Listo para transferir al campo.")
                st.rerun()
            else:
                st.error("El objetivo táctico principal es innegociable.")

    if plan:
        st.caption(f"Última modificación del plan: {plan.get('fecha', 'Desconocida')}")

def main():
    """Función principal de orquestación de la aplicación."""
    # 1. Ejecutar la inyección de CSS antes de renderizar nada
    inyectar_css_premium()
    
    # 2. Inicializar los datos
    inicializar_datos()
    
    # El resto de tu código se mantiene intacto
    st.title("🎯 Sistema Inteligente de Scouting y Planificación")

    rivales = db.obtener_rivales()
    if not rivales:
        st.warning("La base de datos está vacía. Comience dando de alta un rival en 'Ingesta de Datos'.")
        
    nombres = {r["nombre"]: r["id"] for r in rivales}

    tab_dash, tab_ingesta, tab_plan, tab_tactico = st.tabs([
        "📊 Panel de Control", 
        "📝 Ingesta de Datos", 
        "🧩 Matriz Sistémica y Microciclo",
        "⚽ Pizarra Táctica"
    ])

    with tab_dash:
        render_dashboard(rivales, nombres)
        
    with tab_ingesta:
        render_ingesta(rivales, nombres)
        
    with tab_plan:
        render_plan_partido(rivales, nombres)
        
    with tab_tactico:
        render_pizarra_tactica(rivales, nombres)

if __name__ == "__main__":
    main()
