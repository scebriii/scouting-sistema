import database as db


def cargar_datos_mock():
    if db.hay_datos():
        return

    r1 = db.insertar_rival(
        "CD Atlético Norte",
        "4-3-3",
        "Posesión posicional, salida en corto, presión alta tras pérdida",
    )
    r2 = db.insertar_rival(
        "UD Levante Sur",
        "5-3-2",
        "Bloque bajo, juego directo al delantero de referencia, transiciones rápidas",
    )

    informes_r1 = [
        (
            "Ataque organizado",
            "Fortaleza",
            "Superioridad interior con mediocentros entre líneas",
            None,
        ),
        ("Ataque organizado", "KPI", "Posesión media", "62%"),
        ("Ataque organizado", "KPI", "xG por partido", "1.8"),
        (
            "Defensa organizada",
            "Debilidad",
            "Espalda de los laterales muy expuesta al proyectarse",
            None,
        ),
        ("Defensa organizada", "KPI", "Goles encajados por partido", "1.4"),
        (
            "Transición ofensiva",
            "Fortaleza",
            "Extremo derecho muy rápido en conducción tras robo",
            None,
        ),
        (
            "Transición defensiva",
            "Debilidad",
            "Lentos en el repliegue por el carril central",
            None,
        ),
        (
            "ABP",
            "Debilidad",
            "Vulnerables al segundo palo en córners defensivos",
            None,
        ),
        ("ABP", "KPI", "Goles encajados de ABP", "35% del total"),
    ]
    for fase, tipo, desc, kpi in informes_r1:
        db.insertar_informe(r1, fase, tipo, desc, kpi)

    informes_r2 = [
        (
            "Ataque organizado",
            "Debilidad",
            "Poca creación en juego posicional, dependen del balón largo",
            None,
        ),
        ("Ataque organizado", "KPI", "Posesión media", "38%"),
        (
            "Defensa organizada",
            "Fortaleza",
            "Bloque bajo muy compacto, difícil jugar por dentro",
            None,
        ),
        ("Defensa organizada", "KPI", "Goles encajados por partido", "0.9"),
        (
            "Transición ofensiva",
            "Fortaleza",
            "Delantero referencia gana duelos aéreos y sostiene la contra",
            None,
        ),
        ("Transición ofensiva", "KPI", "Goles en contraataque", "45% del total"),
        (
            "Transición defensiva",
            "Fortaleza",
            "Repliegue intensivo de los carrileros",
            None,
        ),
        (
            "ABP",
            "Fortaleza",
            "Muy peligrosos en saques de banda largos y córners",
            None,
        ),
        ("ABP", "Debilidad", "Barrera desorganizada en faltas frontales", None),
    ]
    for fase, tipo, desc, kpi in informes_r2:
        db.insertar_informe(r2, fase, tipo, desc, kpi)

    interacciones = [
        (
            r1,
            "Laterales muy ofensivos dejan la espalda libre",
            "Atacar con nuestros extremos al espacio tras recuperación",
            "Oportunidad",
            "Primeros 5 segundos tras robo en campo propio",
        ),
        (
            r1,
            "Presión alta tras pérdida",
            "Riesgo en nuestra salida en corto; alternar con juego directo al pivote",
            "Amenaza",
            "Salida de balón en primer tercio",
        ),
        (
            r1,
            "Vulnerables al segundo palo en córners",
            "Cargar el segundo palo con nuestros dos centrales",
            "Oportunidad",
            "Córners a favor durante todo el partido",
        ),
        (
            r2,
            "Bloque bajo compacto por dentro",
            "Amplitud máxima y cambios de orientación para abrir el bloque",
            "Amenaza",
            "Ataque organizado contra defensa posicionada",
        ),
        (
            r2,
            "Delantero referencia sostiene contras",
            "Vigilancia constante de un central + pivote en cada ataque nuestro",
            "Amenaza",
            "Cada pérdida en campo rival",
        ),
        (
            r2,
            "Barrera desorganizada en faltas frontales",
            "Buscar faltas en zona frontal; ensayar tiro directo y jugada de barrera",
            "Oportunidad",
            "Faltas entre 18-25 metros",
        ),
    ]
    for rid, car, imp, tv, ven in interacciones:
        db.insertar_interaccion(rid, car, imp, tv, ven)

    db.guardar_plan(
        r1,
        "Explotar la espalda de los laterales y proteger la salida de balón ante su presión alta",
        "Tras robo, primer pase al espacio del extremo (máx. 2 toques)",
        "Si presionan la salida, balón directo al pivote y jugar segunda jugada",
        "En córner a favor, doble carga al segundo palo",
        "Martes: rondo posicional 6v4 con salida bajo presión. Jueves: transiciones 4v3 "
        "a campo abierto tras robo. Viernes: circuito de ABP ofensivo (córner al segundo palo).",
    )
