# Deployed: 2026-07-04 11:57:42
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
    """Renderiza la Pizarra Táctica con el dashboard TacticalOS unificado."""
    import json

    # Selector de rival para cargar información táctica
    rival_tactico = st.selectbox(
        "Seleccionar rival para cargar sistema táctico",
        [""] + list(nombres.keys()),
        key="tactico_rival",
    )

    # Obtener info del rival seleccionado
    rival_info = None
    sistema = "4-3-3"
    estilo = ""
    if rival_tactico:
        rival_id = nombres[rival_tactico]
        rival_info = db.obtener_rival(rival_id)
        if rival_info:
            sistema = str(rival_info.get("sistema_tactico", "4-3-3"))
            estilo = str(rival_info.get("estilo_juego", ""))

    # Datos del rival para inyección en el dashboard
    rival_data = json.dumps({
        "rival": rival_tactico,
        "sistema": sistema if rival_tactico else "4-3-3",
        "estilo": estilo,
    })

    # HTML del dashboard TacticalOS unificado
    html_content = _build_tacticalos_html(rival_data)

    st.components.v1.html(
        html_content,
        height=1100,
        scrolling=True,
    )

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


def _build_tacticalos_html(rival_data: str) -> str:
    """Construye el HTML autocontenido del dashboard TacticalOS."""
    return f"""
<!DOCTYPE html>
<html class="dark" lang="es">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>TacticalOS — {rival_data}</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500;600&family=Geist:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script id="tailwind-config">
tailwind.config = {{
    darkMode: "class",
    theme: {{
        extend: {{
            colors: {{
                background: "#131315",
                surface: "#18181b",
                surface-dim: "#131315",
                surface-bright: "#39393b",
                surface-container: "#201f22",
                surface-container-low: "#1c1b1d",
                surface-container-high: "#2a2a2c",
                surface-container-highest: "#353437",
                surface-container-lowest: "#0e0e10",
                surface-variant: "#353437",
                surface-glass: "#111827b8",
                border-technical: "#27272a",
                border-glass: "#ffffff14",
                text-primary: "#fafafa",
                text-secondary: "#94a3b8",
                text-muted: "#64748b",
                on-surface: "#e5e1e4",
                on-primary: "#002e6a",
                primary: "#adc6ff",
                "primary-container": "#4d8eff",
                "primary-fixed": "#d8e2ff",
                "primary-fixed-dim": "#adc6ff",
                "on-primary-fixed": "#001a42",
                "on-primary-fixed-variant": "#004395",
                inverse-primary: "#005ac2",
                secondary: "#c8c5ca",
                "secondary-container": "#47464a",
                "on-secondary": "#303033",
                "on-secondary-fixed": "#1b1b1e",
                "on-secondary-fixed-variant": "#47464a",
                tertiary: "#4edea3",
                "tertiary-container": "#00a572",
                "tertiary-fixed": "#6ffbbe",
                "tertiary-fixed-dim": "#4edea3",
                "on-tertiary": "#003824",
                "on-tertiary-fixed": "#002113",
                "on-tertiary-fixed-variant": "#005236",
                error: "#ffb4ab",
                "error-container": "#93000a",
                "on-error": "#690005",
                "on-error-container": "#ffdad6",
                canvas: "#09090b",
                "outline": "#8c909f",
                "outline-variant": "#424754",
                "inverse-surface": "#e5e1e4",
                "inverse-on-surface": "#313032",
                "accent-blue-glow": "#3b82f666",
                "threat-red": "#ef4444",
                "warning-amber": "#f59e0b",
                "on-background": "#e5e1e4",
            }},
            fontFamily: {{
                "headline-lg": ["Geist", "sans-serif"],
                "headline-md": ["Geist", "sans-serif"],
                "body-lg": ["Inter", "sans-serif"],
                "body-md": ["Inter", "sans-serif"],
                "label-sm": ["Geist", "sans-serif"],
                "stats-lg": ["Geist Mono", "monospace"],
                "stats-md": ["Geist Mono", "monospace"],
            }},
            fontSize: {{
                "headline-lg": ["32px", {{lineHeight:"40px",letterSpacing:"-0.02em",fontWeight:"700"}}],
                "headline-md": ["24px", {{lineHeight:"32px",letterSpacing:"-0.01em",fontWeight:"600"}}],
                "body-lg": ["16px", {{lineHeight:"24px",fontWeight:"400"}}],
                "body-md": ["14px", {{lineHeight:"21px",fontWeight:"400"}}],
                "label-sm": ["12px", {{lineHeight:"16px",fontWeight:"600"}}],
                "stats-lg": ["18px", {{lineHeight:"24px",fontWeight:"600"}}],
                "stats-md": ["14px", {{lineHeight:"20px",fontWeight:"500"}}],
            }},
            spacing: {{
                xs: "4px", sm: "8px", md: "16px", lg: "24px", xl: "32px",
            }},
        }},
    }},
}}
</script>
<style>
body {{ background-color: #09090b; color: #fafafa; overflow: hidden; font-family: 'Inter', sans-serif; }}
.spring-physics {{ transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
.glow-active {{ box-shadow: 0 0 20px 0 rgba(59, 130, 246, 0.4); }}
.pitch-lines {{ stroke: rgba(255, 255, 255, 0.15); stroke-width: 1px; fill: none; filter: drop-shadow(0 0 2px rgba(255,255,255,0.2)); }}
.pitch-grid {{ background-image: linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px); background-size: 40px 40px; }}
input[type="range"] {{ -webkit-appearance: none; width: 100%; background: transparent; }}
input[type="range"]::-webkit-slider-thumb {{ -webkit-appearance: none; height: 16px; width: 16px; border-radius: 50%; background: #adc6ff; cursor: pointer; margin-top: -6px; box-shadow: 0 0 10px rgba(77, 142, 255, 0.5); }}
input[type="range"]::-webkit-slider-runnable-track {{ width: 100%; height: 4px; cursor: pointer; background: #27272a; border-radius: 2px; }}
.tactical-node {{ width: 32px; height: 32px; border-radius: 50%; border: 1.5px solid rgba(255,255,255,0.8); display: flex; align-items: center; justify-content: center; font-family: 'Geist Mono', monospace; font-size: 14px; font-weight: 600; cursor: grab; position: absolute; background: #18181b; box-shadow: 0 4px 12px rgba(0,0,0,0.5); transition: border-color 0.2s, box-shadow 0.2s; }}
.tactical-node:hover {{ border-color: #adc6ff; box-shadow: 0 0 15px rgba(59, 130, 246, 0.4); }}
.node-def {{ border-color: #4edea3; color: #4edea3; }}
.node-att {{ border-color: #ef4444; color: #ef4444; }}
@keyframes dash {{ to {{ stroke-dashoffset: -8; }} }}
</style>
</head>
<body class="flex flex-col h-screen antialiased text-text-primary selection:bg-primary-container selection:text-on-primary-container">
<!-- TopNavBar -->
<header class="fixed top-0 w-full z-50 flex justify-between items-center px-lg h-16 bg-surface-glass backdrop-blur-xl border-b border-border-glass">
<div class="flex items-center gap-sm">
<span class="material-symbols-outlined text-primary text-[28px]" style="font-variation-settings: 'FILL' 1;">speed</span>
<span class="font-headline-lg text-headline-lg font-bold text-primary tracking-tight">TacticalOS</span>
<span class="ml-4 font-stats-md text-stats-md text-tertiary flex items-center gap-2 px-3 py-1 bg-tertiary-container/10 rounded-full border border-tertiary/20">
<span class="w-2 h-2 rounded-full bg-tertiary animate-pulse"></span>
LIVE TELEMETRY v2.4
</span>
</div>
<nav class="hidden md:flex gap-md h-full items-center">
<a class="font-body-md text-body-md h-full flex items-center px-2 text-text-secondary hover:text-primary transition-colors duration-200" href="#">Analysis</a>
<a class="font-body-md text-body-md h-full flex items-center px-2 text-primary font-bold border-b-2 border-primary pb-[2px] transition-colors duration-200" href="#">Simulator</a>
<a class="font-body-md text-body-md h-full flex items-center px-2 text-text-secondary hover:text-primary transition-colors duration-200" href="#">Scouting</a>
<a class="font-body-md text-body-md h-full flex items-center px-2 text-text-secondary hover:text-primary transition-colors duration-200" href="#">Library</a>
</nav>
<div class="flex items-center gap-md">
<button class="text-text-secondary hover:text-primary transition-colors spring-physics hover:scale-110">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="text-text-secondary hover:text-primary transition-colors spring-physics hover:scale-110">
<span class="material-symbols-outlined">settings</span>
</button>
<div class="w-8 h-8 rounded-full bg-surface-variant border border-border-glass overflow-hidden ml-sm cursor-pointer">
<span class="material-symbols-outlined text-[18px]">person</span>
</div>
</div>
</header>
<div class="flex flex-1 pt-16 overflow-hidden">
<!-- SideNavBar -->
<aside class="hidden md:flex flex-col fixed left-0 top-16 bottom-0 z-40 w-64 bg-surface-glass backdrop-blur-2xl border-r border-border-glass shadow-lg shadow-accent-blue-glow/10 overflow-y-auto">
<div class="p-lg border-b border-border-glass">
<h3 class="font-headline-md text-headline-md text-primary mb-1">Sim Engine</h3>
<p class="font-stats-md text-stats-md text-text-secondary">Defensive Phase Analysis</p>
</div>
<div class="p-lg flex flex-col gap-lg">
<div class="flex flex-col gap-md">
<h4 class="font-label-sm text-label-sm text-text-muted uppercase tracking-widest">Defensive AI Block</h4>
<div class="flex bg-surface-container rounded-lg p-1 border border-border-glass">
<button class="flex-1 py-1 px-2 font-label-sm text-label-sm rounded-md text-text-secondary hover:text-primary transition-colors">Low</button>
<button class="flex-1 py-1 px-2 font-label-sm text-label-sm rounded-md bg-primary-container/20 text-primary border border-primary/30 glow-active">Mid</button>
<button class="flex-1 py-1 px-2 font-label-sm text-label-sm rounded-md text-text-secondary hover:text-primary transition-colors">High</button>
</div>
<div class="flex flex-col gap-2 mt-2">
<div class="flex justify-between items-center">
<span class="font-label-sm text-label-sm text-text-secondary">Horizontal Shift</span>
<span class="font-stats-md text-stats-md text-primary">68%</span>
</div>
<input class="w-full" max="100" min="1" type="range" value="68"/>
</div>
<div class="flex flex-col gap-2">
<div class="flex justify-between items-center">
<span class="font-label-sm text-label-sm text-text-secondary">Vertical Compactness</span>
<span class="font-stats-md text-stats-md text-primary">42m</span>
</div>
<input class="w-full" max="100" min="1" type="range" value="42"/>
</div>
</div>
<div class="flex flex-col gap-md mt-4 border-t border-border-glass pt-lg">
<h4 class="font-label-sm text-label-sm text-text-muted uppercase tracking-widest">Visual Overlays</h4>
<label class="flex items-center justify-between cursor-pointer group">
<span class="font-body-md text-body-md text-text-secondary group-hover:text-text-primary transition-colors">Voronoi Tessellation</span>
<div class="relative">
<input checked class="sr-only" type="checkbox"/>
<div class="block bg-surface-container w-10 h-6 rounded-full border border-border-glass"></div>
<div class="dot absolute left-1 top-1 bg-primary w-4 h-4 rounded-full transition transform translate-x-4 shadow-[0_0_8px_rgba(77,142,255,0.6)]"></div>
</div>
</label>
<label class="flex items-center justify-between cursor-pointer group">
<span class="font-body-md text-body-md text-text-secondary group-hover:text-text-primary transition-colors">Vision Cones</span>
<div class="relative">
<input class="sr-only" type="checkbox"/>
<div class="block bg-surface-container w-10 h-6 rounded-full border border-border-glass"></div>
<div class="dot absolute left-1 top-1 bg-surface-variant w-4 h-4 rounded-full transition"></div>
</div>
</label>
<label class="flex items-center justify-between cursor-pointer group">
<span class="font-body-md text-body-md text-text-secondary group-hover:text-text-primary transition-colors">Pressure Heatmap</span>
<div class="relative">
<input class="sr-only" type="checkbox"/>
<div class="block bg-surface-container w-10 h-6 rounded-full border border-border-glass"></div>
<div class="dot absolute left-1 top-1 bg-surface-variant w-4 h-4 rounded-full transition"></div>
</div>
</label>
<label class="flex items-center justify-between cursor-pointer group">
<span class="font-body-md text-body-md text-text-secondary group-hover:text-text-primary transition-colors">Análisis de Espacios</span>
<div class="relative">
<input class="sr-only" type="checkbox"/>
<div class="block bg-surface-container w-10 h-6 rounded-full border border-border-glass"></div>
<div class="dot absolute left-1 top-1 bg-surface-variant w-4 h-4 rounded-full transition"></div>
</div>
</label>
</div>
</div>
<div class="mt-auto p-lg">
<button class="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-lg bg-gradient-to-r from-primary-container to-inverse-primary text-text-primary font-label-sm text-label-sm border border-primary/50 spring-physics hover:scale-[0.98] glow-active">
<span class="material-symbols-outlined text-[18px]">rocket_launch</span>
Launch Simulation
</button>
</div>
</aside>
<!-- Central Area: Tactical Pitch -->
<main class="flex-1 ml-0 md:ml-64 relative bg-canvas pitch-grid flex items-center justify-center mb-20 md:mb-24">
<!-- Floating HUD (Right) -->
<div class="absolute right-lg top-lg flex flex-col gap-md z-20 w-64 pointer-events-none">
<div class="bg-surface-glass backdrop-blur-xl border border-border-glass rounded-xl p-md shadow-lg pointer-events-auto spring-physics hover:border-primary/30">
<h5 class="font-label-sm text-label-sm text-text-muted uppercase mb-1">Line Distance</h5>
<div class="flex items-end gap-2">
<span class="font-headline-lg text-headline-lg text-text-primary leading-none">18.4</span>
<span class="font-stats-md text-stats-md text-text-secondary mb-1">m</span>
</div>
<div class="mt-2 h-1 w-full bg-surface-container rounded-full overflow-hidden">
<div class="h-full bg-tertiary w-3/4 rounded-full shadow-[0_0_8px_rgba(78,222,163,0.6)]"></div>
</div>
</div>
<div class="bg-surface-glass backdrop-blur-xl border border-border-glass rounded-xl p-md shadow-lg pointer-events-auto spring-physics hover:border-primary/30">
<h5 class="font-label-sm text-label-sm text-text-muted uppercase mb-1">Defensive xG</h5>
<div class="flex items-end gap-2">
<span class="font-headline-lg text-headline-lg text-text-primary leading-none">0.12</span>
</div>
<div class="mt-2 flex gap-1">
<div class="h-1 flex-1 bg-tertiary rounded-full shadow-[0_0_8px_rgba(78,222,163,0.6)]"></div>
<div class="h-1 flex-1 bg-surface-container rounded-full"></div>
<div class="h-1 flex-1 bg-surface-container rounded-full"></div>
</div>
</div>
<div class="bg-surface-glass backdrop-blur-xl border border-border-glass rounded-xl p-md shadow-lg pointer-events-auto spring-physics hover:border-primary/30">
<h5 class="font-label-sm text-label-sm text-text-muted uppercase mb-2">Ocupación de Espacios</h5>
<div class="flex items-center justify-between mb-3">
<span class="font-headline-md text-headline-md text-primary">Alta</span>
<span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">stacked_line_chart</span>
</div>
<div class="flex flex-col gap-2 border-t border-border-glass pt-2">
<div class="flex justify-between items-center">
<span class="font-label-sm text-label-sm text-text-secondary">Mapa de Densidad</span>
<div class="flex gap-1">
<div class="w-2 h-2 rounded-full bg-primary"></div>
<div class="w-2 h-2 rounded-full bg-primary/60"></div>
<div class="w-2 h-2 rounded-full bg-primary/30"></div>
</div>
</div>
<div class="flex justify-between items-center">
<span class="font-label-sm text-label-sm text-text-secondary">Canales de Progresión</span>
<span class="font-stats-md text-stats-md text-primary font-bold">74%</span>
</div>
<div class="h-1 w-full bg-surface-container rounded-full overflow-hidden">
<div class="h-full bg-primary w-[74%] rounded-full shadow-[0_0_8px_rgba(77,142,255,0.5)]"></div>
</div>
</div>
</div>
</div>
<!-- Pitch SVG Base -->
<div class="relative w-[800px] h-[500px] max-w-[95%] transform rotate-x-12 scale-95 md:scale-100 transition-transform duration-500">
<svg class="w-full h-full absolute inset-0 pointer-events-none" viewBox="0 0 100 65">
<rect class="pitch-lines" height="65" width="100" x="0" y="0"></rect>
<line class="pitch-lines" x1="50" x2="50" y1="0" y2="65"></line>
<circle class="pitch-lines" cx="50" cy="32.5" r="9.15"></circle>
<circle cx="50" cy="32.5" fill="rgba(255,255,255,0.3)" r="0.5"></circle>
<rect class="pitch-lines" height="37.32" width="16.5" x="0" y="13.84"></rect>
<rect class="pitch-lines" height="37.32" width="16.5" x="83.5" y="13.84"></rect>
<rect class="pitch-lines" height="15.32" width="5.5" x="0" y="24.84"></rect>
<rect class="pitch-lines" height="15.32" width="5.5" x="94.5" y="24.84"></rect>
</svg>
<svg class="w-full h-full absolute inset-0 pointer-events-none z-10" viewBox="0 0 800 500">
<defs>
<linearGradient id="pass-grad" x1="0%" x2="100%" y1="0%" y2="100%">
<stop offset="0%" stop-color="#4edea3" stop-opacity="0.8"></stop>
<stop offset="100%" stop-color="#4edea3" stop-opacity="0.1"></stop>
</linearGradient>
</defs>
<line class="animate-[dash_1s_linear_infinite]" stroke="url(#pass-grad)" stroke-dasharray="4 4" stroke-width="2" x1="240" x2="400" y1="200" y2="350"></line>
<line stroke="#f59e0b" stroke-opacity="0.6" stroke-width="1.5" x1="400" x2="550" y1="350" y2="280"></line>
<line opacity="0.4" stroke="#4edea3" stroke-dasharray="2 2" stroke-width="1" x1="160" x2="240" y1="150" y2="150"></line>
<line opacity="0.4" stroke="#ef4444" stroke-dasharray="2 2" stroke-width="1" x1="240" x2="400" y1="350" y2="200"></line>
<line opacity="0.4" stroke="#f59e0b" stroke-dasharray="2 2" stroke-width="1" x1="520" x2="560" y1="275" y2="150"></line>
</svg>
<div class="absolute inset-0 pointer-events-none opacity-20 z-0 flex">
<div class="w-1/3 h-full bg-threat-red blur-3xl rounded-full translate-x-1/4"></div>
<div class="w-1/3 h-full bg-primary blur-3xl rounded-full translate-x-3/4"></div>
<div class="absolute inset-0 grid grid-cols-6 grid-rows-4 gap-px opacity-30">
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/40 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/60 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/30 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/50 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/40 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/30 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/60 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/40 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/20 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/50 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/10 border border-accent-blue-glow/10"></div>
<div class="bg-accent-blue-glow/30 border border-accent-blue-glow/10"></div>
</div>
</div>
<!-- Defensive Nodes -->
<div class="tactical-node node-def z-20" style="left: 20%; top: 30%;">4</div>
<div class="tactical-node node-def z-20" style="left: 20%; top: 70%;">3</div>
<div class="tactical-node node-def z-20" style="left: 30%; top: 50%;">5</div>
<div class="tactical-node node-def z-20" style="left: 45%; top: 40%;">8</div>
<!-- Attacking Nodes -->
<div class="tactical-node node-att z-20" style="left: 50%; top: 70%;">9</div>
<div class="tactical-node node-att z-20" style="left: 65%; top: 55%;">10</div>
<div class="tactical-node node-att z-20" style="left: 70%; top: 30%;">7</div>
<!-- Ball -->
<div class="absolute w-4 h-4 bg-white rounded-full z-30 shadow-[0_0_10px_rgba(255,255,255,0.8)]" style="left: 68%; top: 56%;"></div>
</div>
</main>
</div>
<!-- BottomNavBar (Timeline & Playback) -->
<footer class="fixed bottom-0 left-0 md:left-64 right-0 z-50 flex flex-col justify-center bg-surface-glass backdrop-blur-xl border-t border-border-glass px-lg py-md rounded-t-xl">
<div class="w-full flex items-center gap-sm mb-4">
<span class="font-stats-md text-stats-md text-text-secondary w-12 text-right">00:14</span>
<div class="flex-1 relative h-6 flex items-center group cursor-pointer">
<div class="absolute w-full h-1 bg-surface-container rounded-full"></div>
<div class="absolute h-1 bg-primary rounded-full shadow-[0_0_8px_rgba(77,142,255,0.5)]" style="width: 45%;"></div>
<div class="absolute w-2 h-4 bg-tertiary rounded-sm left-[20%] -mt-1 group-hover:scale-110 transition-transform"></div>
<div class="absolute w-2 h-4 bg-warning-amber rounded-sm left-[45%] -mt-1 shadow-[0_0_5px_rgba(245,158,11,0.8)] scale-125 z-10"></div>
<div class="absolute w-2 h-4 bg-tertiary rounded-sm left-[75%] -mt-1 group-hover:scale-110 transition-transform"></div>
<div class="absolute w-4 h-4 bg-white rounded-full left-[45%] -ml-2 shadow-lg z-20 transition-transform scale-100 group-hover:scale-125 border-2 border-primary"></div>
</div>
<span class="font-stats-md text-stats-md text-text-secondary w-12">00:30</span>
</div>
<div class="flex justify-between items-center w-full">
<div class="flex gap-4">
<button class="flex flex-col items-center justify-center text-on-surface-variant hover:bg-surface-bright/20 p-2 rounded-xl transition-all spring-physics active:scale-95">
<span class="material-symbols-outlined text-[24px]">settings_backup_restore</span>
<span class="font-label-sm text-label-sm mt-1">Rewind</span>
</button>
<button class="flex flex-col items-center justify-center bg-tertiary-container/20 text-tertiary rounded-xl p-2 px-4 shadow-[0_0_15px_rgba(78,222,163,0.15)] border border-tertiary/30 transition-all spring-physics hover:bg-tertiary-container/30 active:scale-95">
<span class="material-symbols-outlined text-[28px]" style="font-variation-settings: 'FILL' 1;">pause</span>
<span class="font-label-sm text-label-sm mt-1 font-bold">Pause</span>
</button>
<button class="flex flex-col items-center justify-center text-on-surface-variant hover:bg-surface-bright/20 p-2 rounded-xl transition-all spring-physics active:scale-95">
<span class="material-symbols-outlined text-[24px]">play_arrow</span>
<span class="font-label-sm text-label-sm mt-1">Play</span>
</button>
</div>
<button class="flex items-center gap-2 px-4 py-2 bg-surface-variant/50 hover:bg-surface-variant border border-border-glass rounded-lg text-text-primary transition-all spring-physics active:scale-95">
<span class="material-symbols-outlined text-[20px]">save</span>
<span class="font-label-sm text-label-sm">Save Play</span>
</button>
</div>
</footer>
<script>
document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {{
    checkbox.addEventListener('change', function() {{
        const dot = this.parentElement.querySelector('.dot');
        if(this.checked) {{
            dot.classList.remove('translate-x-0', 'bg-surface-variant');
            dot.classList.add('translate-x-4', 'bg-primary', 'shadow-[0_0_8px_rgba(77,142,255,0.6)]');
        }} else {{
            dot.classList.remove('translate-x-4', 'bg-primary', 'shadow-[0_0_8px_rgba(77,142,255,0.6)]');
            dot.classList.add('translate-x-0', 'bg-surface-variant');
        }}
    }});
}});
// Inyectar datos del rival
window.__TACTICAL_RIVAL_DATA = {rival_data};
console.log('TacticalOS initialized with:', window.__TACTICAL_RIVAL_DATA);
</script>
</body>
</html>
"""


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
