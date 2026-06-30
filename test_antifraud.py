from datetime import datetime, timedelta, timezone

from validator import (
    AntifraudValidator,
    EventoValidacion,
    ResultadoAntifraude,
    crear_evento_demo,
    validar_evento_demo,
)


def test_crear_evento_demo():
    evento = crear_evento_demo()

    assert isinstance(evento, EventoValidacion)
    assert evento.tarjeta_id == "token-demo"
    assert evento.linea == "60"
    assert evento.unidad == "1234"
    assert isinstance(evento.timestamp, datetime)
    assert evento.tipo_evento == "validacion"


def test_evento_simple_permitido():
    validador = AntifraudValidator()

    evento = EventoValidacion(
        tarjeta_id="token-demo-1",
        linea="60",
        unidad="1234",
        timestamp=datetime.now(timezone.utc),
    )

    resultado = validador.validar_y_registrar(evento)

    assert isinstance(resultado, ResultadoAntifraude)
    assert resultado.permitido is True
    assert resultado.motivo == "Evento permitido en entorno demostrativo."
    assert resultado.alertas == []
    assert resultado.score_riesgo == 0


def test_evento_invalido_por_campos_basicos():
    validador = AntifraudValidator()

    evento = EventoValidacion(
        tarjeta_id="",
        linea="",
        unidad="",
        timestamp=datetime.now(timezone.utc),
    )

    resultado = validador.validar_evento(evento)

    assert resultado.permitido is False
    assert resultado.motivo == "Evento inválido por campos básicos incompletos."
    assert "tarjeta_id_requerido" in resultado.alertas
    assert "linea_requerida" in resultado.alertas
    assert "unidad_requerida" in resultado.alertas
    assert resultado.score_riesgo == 100


def test_repeticion_misma_linea_y_unidad_genera_alerta():
    validador = AntifraudValidator()

    ahora = datetime.now(timezone.utc)

    evento_1 = EventoValidacion(
        tarjeta_id="token-demo-2",
        linea="60",
        unidad="1234",
        timestamp=ahora,
    )

    evento_2 = EventoValidacion(
        tarjeta_id="token-demo-2",
        linea="60",
        unidad="1234",
        timestamp=ahora + timedelta(minutes=1),
    )

    validador.validar_y_registrar(evento_1)
    resultado = validador.validar_evento(evento_2)

    assert resultado.permitido is True
    assert "repeticion_misma_linea_y_unidad" in resultado.alertas
    assert resultado.score_riesgo >= 25


def test_validaciones_en_unidades_distintas_genera_alerta():
    validador = AntifraudValidator()

    ahora = datetime.now(timezone.utc)

    evento_1 = EventoValidacion(
        tarjeta_id="token-demo-3",
        linea="60",
        unidad="1234",
        timestamp=ahora,
    )

    evento_2 = EventoValidacion(
        tarjeta_id="token-demo-3",
        linea="60",
        unidad="9999",
        timestamp=ahora + timedelta(minutes=1),
    )

    validador.validar_y_registrar(evento_1)
    resultado = validador.validar_evento(evento_2)

    assert resultado.permitido is True
    assert "validaciones_en_unidades_distintas" in resultado.alertas
    assert resultado.score_riesgo >= 30


def test_exceso_de_eventos_en_ventana_temporal():
    validador = AntifraudValidator(max_eventos_por_ventana=2)

    ahora = datetime.now(timezone.utc)

    evento_1 = EventoValidacion(
        tarjeta_id="token-demo-4",
        linea="60",
        unidad="1001",
        timestamp=ahora,
    )

    evento_2 = EventoValidacion(
        tarjeta_id="token-demo-4",
        linea="61",
        unidad="1002",
        timestamp=ahora + timedelta(minutes=1),
    )

    evento_3 = EventoValidacion(
        tarjeta_id="token-demo-4",
        linea="62",
        unidad="1003",
        timestamp=ahora + timedelta(minutes=2),
    )

    validador.validar_y_registrar(evento_1)
    validador.validar_y_registrar(evento_2)

    resultado = validador.validar_evento(evento_3)

    assert "exceso_de_eventos_en_ventana_temporal" in resultado.alertas
    assert resultado.score_riesgo >= 35


def test_timestamp_futuro_genera_alerta():
    validador = AntifraudValidator()

    evento = EventoValidacion(
        tarjeta_id="token-demo-5",
        linea="60",
        unidad="1234",
        timestamp=datetime.now(timezone.utc) + timedelta(minutes=10),
    )

    resultado = validador.validar_evento(evento)

    assert "timestamp_futuro" in resultado.alertas
    assert resultado.score_riesgo >= 40


def test_estado_del_validador():
    validador = AntifraudValidator()

    estado = validador.estado()

    assert estado["componente"] == "AntifraudValidator"
    assert estado["entorno"] == "mvp-conceptual"
    assert estado["procesa_datos_sensibles"] is False
    assert estado["integracion_real_con_organismos"] is False
    assert estado["integracion_real_sube"] is False
    assert estado["modulo"] == "bono_solidario_futuro_experimental"


def test_reset_limpia_eventos():
    validador = AntifraudValidator()

    evento = crear_evento_demo(tarjeta_id="token-demo-reset")

    validador.validar_y_registrar(evento)

    assert validador.estado()["eventos_en_memoria"] == 1

    validador.reset()

    assert validador.estado()["eventos_en_memoria"] == 0


def test_validar_evento_demo_devuelve_diccionario_serializable():
    resultado = validar_evento_demo()

    assert isinstance(resultado, dict)
    assert "permitido" in resultado
    assert "motivo" in resultado
    assert "alertas" in resultado
    assert "score_riesgo" in resultado
    assert "estado" in resultado

    assert resultado["estado"]["procesa_datos_sensibles"] is False
    assert resultado["estado"]["integracion_real_con_organismos"] is False
