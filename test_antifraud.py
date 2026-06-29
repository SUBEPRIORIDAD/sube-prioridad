from datetime import timedelta

import pytest

from validator import AntiFraudEngine, ValidationEvent, now_utc


def make_event(
    card_hash: str,
    bus_id: str = "BUS-001",
    line_id: str = "LINEA-12",
    seconds_after: int = 0,
) -> ValidationEvent:
    base_time = now_utc()

    return ValidationEvent(
        card_hash=card_hash,
        bus_id=bus_id,
        line_id=line_id,
        timestamp=base_time + timedelta(seconds=seconds_after),
    )


def test_bonus_aprobado_en_misma_linea_mismo_colectivo_y_dentro_de_60_segundos():
    engine = AntiFraudEngine()

    priority_event = make_event(card_hash="prioritaria-001", seconds_after=0)
    collaborator_event = make_event(card_hash="colaboradora-001", seconds_after=30)

    result = engine.evaluate_bonus(priority_event, collaborator_event)

    assert result.approved is True
    assert result.bonus_eligible is True
    assert "aprobado" in result.reason.lower()


def test_rechaza_si_la_colaboradora_valida_fuera_de_la_ventana_temporal():
    engine = AntiFraudEngine(time_window_seconds=60)

    priority_event = make_event(card_hash="prioritaria-001", seconds_after=0)
    collaborator_event = make_event(card_hash="colaboradora-001", seconds_after=61)

    result = engine.evaluate_bonus(priority_event, collaborator_event)

    assert result.approved is False
    assert result.bonus_eligible is False
    assert "ventana temporal" in result.reason.lower()


def test_rechaza_si_no_es_el_mismo_colectivo():
    engine = AntiFraudEngine()

    priority_event = make_event(card_hash="prioritaria-001", bus_id="BUS-001")
    collaborator_event = make_event(card_hash="colaboradora-001", bus_id="BUS-999")

    result = engine.evaluate_bonus(priority_event, collaborator_event)

    assert result.approved is False
    assert "mismo colectivo" in result.reason.lower()


def test_rechaza_si_no_es_la_misma_linea():
    engine = AntiFraudEngine()

    priority_event = make_event(card_hash="prioritaria-001", line_id="LINEA-12")
    collaborator_event = make_event(card_hash="colaboradora-001", line_id="LINEA-99")

    result = engine.evaluate_bonus(priority_event, collaborator_event)

    assert result.approved is False
    assert "misma línea" in result.reason.lower()


def test_rechaza_si_es_la_misma_tarjeta():
    engine = AntiFraudEngine()

    priority_event = make_event(card_hash="tarjeta-001")
    collaborator_event = make_event(card_hash="tarjeta-001", seconds_after=10)

    result = engine.evaluate_bonus(priority_event, collaborator_event)

    assert result.approved is False
    assert "misma" in result.reason.lower()


def test_rechaza_repeticion_excesiva_del_mismo_par_de_tarjetas():
    engine = AntiFraudEngine(max_pair_repetitions=3)

    for _ in range(3):
        priority_event = make_event(card_hash="prioritaria-001", seconds_after=0)
        collaborator_event = make_event(card_hash="colaboradora-001", seconds_after=10)
        result = engine.evaluate_bonus(priority_event, collaborator_event)
        assert result.approved is True

    priority_event = make_event(card_hash="prioritaria-001", seconds_after=0)
    collaborator_event = make_event(card_hash="colaboradora-001", seconds_after=10)

    result = engine.evaluate_bonus(priority_event, collaborator_event)

    assert result.approved is False
    assert "repetición excesiva" in result.reason.lower()


def test_rechaza_timestamp_sin_zona_horaria():
    engine = AntiFraudEngine()

    priority_event = make_event(card_hash="prioritaria-001")
    collaborator_event = make_event(card_hash="colaboradora-001")

    collaborator_event = ValidationEvent(
        card_hash=collaborator_event.card_hash,
        bus_id=collaborator_event.bus_id,
        line_id=collaborator_event.line_id,
        timestamp=collaborator_event.timestamp.replace(tzinfo=None),
    )

    with pytest.raises(ValueError):
        engine.evaluate_bonus(priority_event, collaborator_event)
