import pandas as pd
import streamlit as st

import database as db
import utils

st.set_page_config(
    page_title="Scouting Inteligente",
    page_icon="🎯",
    layout="wide",
)

db.init_db()
utils.cargar_datos_mock()

st.title("🎯 Sistema Inteligente de Scouting y Planificación")

rivales = db.obtener_rivales()
if not rivales:
    st.warning("No hay rivales registrados. Añade uno en la pestaña de Scouting.")

nombres = {r["nombre"]: r["id"] for r in rivales}

tab1, tab2, tab3 = st.tabs(
    ["📊 Panel General", "📝 Ingesta de Datos", "🧩 Matriz y Plan de Partido"]
)

# ── TAB 1: DASHBOARD ─────────────────────────────────────────────
with tab1:
    if rivales:
        rival_sel = st.selectbox("Próximo rival", list(nombres.keys()), key="dash_rival")
        rid = nombres[rival_sel]
        rival = db.obtener_rival(rid)

        c1, c2 = st.columns(2)
        c1.metric("Sistema táctico", rival["sistema_tactico"])
        c2.markdown(f"**Estilo de juego:** {rival['estilo_juego']}")

        st.divider()

        kpis = db.obtener_informes(rid, tipo="KPI")
        if kpis:
            st.subheader("KPIs principales")
            cols = st.columns(min(len(kpis), 4))
            for i, k in enumerate(kpis):
                cols[i % 4].metric(k["descripcion"], k["valor_kpi"], help=k["fase"])

        st.divider()

        col_f, col_d = st.columns(2)
        with col_f:
            st.subheader("💪 Fortalezas")
            fortalezas = db.obtener_informes(rid, tipo="Fortaleza")
            if fortalezas:
                for f in fortalezas:
                    st.success(f"**{f['fase']}** — {f['descripcion']}")
            else:
                st.caption("Sin fortalezas registradas.")
        with col_d:
            st.subheader("🎯 Debilidades")
            debilidades = db.obtener_informes(rid, tipo="Debilidad")
            if debilidades:
                for d in debilidades:
                    st.error(f"**{d['fase']}** — {d['descripcion']}")
            else:
                st.caption("Sin debilidades registradas.")

        st.divider()
        st.subheader("Informe completo por fases")
        informes = db.obtener_informes(rid)
        if informes:
            df = pd.DataFrame(informes)[["fase", "tipo", "descripcion", "valor_kpi", "fecha"]]
            df.columns = ["Fase", "Tipo", "Descripción", "Valor KPI", "Fecha"]
            st.dataframe(df, use_container_width=True, hide_index=True)

# ── TAB 2: INGESTA DE DATOS ──────────────────────────────────────
with tab2:
    st.subheader("Nuevo rival")
    with st.form("form_rival", clear_on_submit=True):
        fc1, fc2, fc3 = st.columns(3)
        nombre = fc1.text_input("Nombre del rival")
        sistema = fc2.selectbox(
            "Sistema táctico base",
            ["4-3-3", "4-4-2", "4-2-3-1", "3-5-2", "5-3-2", "3-4-3", "Otro"],
        )
        estilo = fc3.text_input("Estilo de juego")
        if st.form_submit_button("Guardar rival", type="primary"):
            if nombre.strip():
                try:
                    db.insertar_rival(nombre.strip(), sistema, estilo.strip())
                    st.success(f"Rival '{nombre}' guardado.")
                    st.rerun()
                except Exception:
                    st.error("Ya existe un rival con ese nombre.")
            else:
                st.error("El nombre es obligatorio.")

    st.divider()
    st.subheader("Nuevo registro de scouting")
    if rivales:
        with st.form("form_informe", clear_on_submit=True):
            ic1, ic2, ic3 = st.columns(3)
            rival_inf = ic1.selectbox("Rival", list(nombres.keys()))
            fase = ic2.selectbox("Fase del juego", db.FASES)
            tipo = ic3.selectbox("Tipo de registro", db.TIPOS_REGISTRO)
            descripcion = st.text_area(
                "Descripción / nota cualitativa",
                placeholder="Ej: El lateral izquierdo pierde la referencia en centros al segundo palo",
            )
            valor_kpi = st.text_input(
                "Valor del KPI (solo si el tipo es KPI)",
                placeholder="Ej: 62%, 1.8 xG, 12 recuperaciones",
            )
            if st.form_submit_button("Guardar registro", type="primary"):
                if descripcion.strip():
                    db.insertar_informe(
                        nombres[rival_inf],
                        fase,
                        tipo,
                        descripcion.strip(),
                        valor_kpi.strip() or None,
                    )
                    st.success("Registro guardado.")
                else:
                    st.error("La descripción es obligatoria.")
    else:
        st.info("Primero crea un rival.")

# ── TAB 3: MATRIZ + PLAN DE PARTIDO ──────────────────────────────
with tab3:
    if rivales:
        rival_plan = st.selectbox("Rival", list(nombres.keys()), key="plan_rival")
        rid_p = nombres[rival_plan]

        st.subheader("🧩 Matriz de interacción")
        st.caption(
            "Cruce: característica del rival → nuestro impacto táctico → ventana de oportunidad/amenaza"
        )

        interacciones = db.obtener_interacciones(rid_p)
        if interacciones:
            df_int = pd.DataFrame(interacciones)[
                ["caracteristica_rival", "impacto_tactico", "tipo_ventana", "ventana"]
            ]
            df_int.columns = [
                "Característica del rival",
                "Nuestro impacto táctico",
                "Tipo",
                "Ventana",
            ]
            st.dataframe(
                df_int,
                use_container_width=True,
                hide_index=True,
                column_config={"Tipo": st.column_config.TextColumn(width="small")},
            )
            n_op = sum(1 for i in interacciones if i["tipo_ventana"] == "Oportunidad")
            n_am = len(interacciones) - n_op
            mc1, mc2 = st.columns(2)
            mc1.metric("🟢 Oportunidades detectadas", n_op)
            mc2.metric("🔴 Amenazas detectadas", n_am)
        else:
            st.info("Sin interacciones registradas para este rival.")

        with st.expander("➕ Añadir interacción"):
            with st.form("form_interaccion", clear_on_submit=True):
                caracteristica = st.text_input("Característica del rival")
                impacto = st.text_input("Nuestro impacto táctico")
                xc1, xc2 = st.columns([1, 2])
                tipo_v = xc1.selectbox("Tipo", ["Oportunidad", "Amenaza"])
                ventana = xc2.text_input("Ventana (cuándo/dónde ocurre)")
                if st.form_submit_button("Guardar interacción", type="primary"):
                    if (
                        caracteristica.strip()
                        and impacto.strip()
                        and ventana.strip()
                    ):
                        db.insertar_interaccion(
                            rid_p,
                            caracteristica.strip(),
                            impacto.strip(),
                            tipo_v,
                            ventana.strip(),
                        )
                        st.success("Interacción guardada.")
                        st.rerun()
                    else:
                        st.error("Todos los campos son obligatorios.")

        st.divider()
        st.subheader("📋 Plan de partido semanal")

        plan = db.obtener_plan(rid_p) or {}
        with st.form("form_plan"):
            objetivo = st.text_area(
                "Objetivo semanal", value=plan.get("objetivo_semanal", "")
            )
            st.markdown("**Las 3 consignas clave de la semana**")
            c1 = st.text_input(
                "Consigna 1", value=plan.get("consigna_1", "") or ""
            )
            c2 = st.text_input(
                "Consigna 2", value=plan.get("consigna_2", "") or ""
            )
            c3 = st.text_input(
                "Consigna 3", value=plan.get("consigna_3", "") or ""
            )
            tareas = st.text_area(
                "Tareas de entrenamiento de transferencia",
                value=plan.get("tareas_entrenamiento", "") or "",
                height=140,
                placeholder="Ej: Martes: rondo 6v4 bajo presión. Jueves: transiciones 4v3...",
            )
            if st.form_submit_button("Guardar plan de partido", type="primary"):
                if objetivo.strip():
                    db.guardar_plan(
                        rid_p,
                        objetivo.strip(),
                        c1.strip(),
                        c2.strip(),
                        c3.strip(),
                        tareas.strip(),
                    )
                    st.success("Plan de partido guardado.")
                else:
                    st.error("El objetivo semanal es obligatorio.")

        if plan:
            st.caption(f"Último plan guardado: {plan.get('fecha', '—')}")
    else:
        st.info("Primero crea un rival en la pestaña de Ingesta.")
