from datetime import datetime, timedelta, timezone

import pytest

from red_sube_trip_window_matcher import (
    AccessContext,
    MatchStatus,
    MatchStrength,
    ParticipantRole,
    TransportMode,
    ValidationPointType,
    assert_no_prohibited_fields,
    create_demo_priority_and_collaborator_signals,
    create_demo_station_turnstile_signals,
    create_demo_trip_window_match_policy,
    create_demo_validation_signal,
    evaluate_trip_window_match,
    result_to_dict,
    run_demo,
    run_station_demo,
)


def test_run_demo_matches_in_vehicle_context():
    result = run_demo()

    assert result["project"] == "SUBE Prioridad"
    assert result["module"] == "Matcher Demo de Ventana Temporal Red SUBE"
    assert result["demo_mode"] is True

    assert result["status"] == "matched"
    assert result["matched"] is True
    assert result["access_context"] == "in_vehicle_after_payment"
    assert result["match_strength"] == "same_vehicle_strong"

    assert result["red_sube_window_matched"] is True
    assert result["effective_sync_window_minutes"] == 10
    assert result["effective_sync_window_matched"] is True

    assert result["same_network"] is True
    assert result["same_transport_mode"] is True
    assert result["same_route"] is True
    assert result["same_vehicle"] is True
    assert result["same_trip"] is True
    assert result["risk_flags"] == []

    assert "pago a bordo" in result["security_notice"]
    assert "molinete" in result["security_notice"]
    assert "DNI" in result["privacy_notice"]
    assert "diagnóstico" in result["privacy_notice"]
    assert "CUD" in result["privacy_notice"]
    assert "chofer no verifica" in result["driver_burden"].lower()

    assert "Sin integración real con SUBE." in result["warnings"]
    assert "Sin integración real con Red SUBE." in result["warnings"]
    assert "La ventana a bordo es más corta que la ventana de espera en andén." in result["warnings"]
    assert "La ventana de molinete contempla espera razonable de tren o subte." in result["warnings"]


def test_run_station_demo_matches_platform_wait_context():
    result = run_station_demo()

    assert result["status"] == "matched"
    assert result["matched"] is True
    assert result["access_context"] == "platform_wait_after_turnstile"
    assert result["match_strength"] == "same_platform_wait_moderate"

    assert result["red_sube_window_matched"] is True
    assert result["effective_sync_window_minutes"] == 45
    assert result["effective_sync_window_matched"] is True

    assert result["same_network"] is True
    assert result["same_transport_mode"] is True
    assert result["same_route"] is True
    assert result["same_vehicle"] is False
    assert result["same_station"] is True
    assert result["same_platform"] is True
    assert result["same_trip"] is False
    assert result["risk_flags"] == []


def test_result_to_dict_is_serializable():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    data = result_to_dict(result)

    assert data["project"] == "SUBE Prioridad"
    assert data["module"] == "Matcher Demo de Ventana Temporal Red SUBE"
    assert data["demo_mode"] is True
    assert isinstance(data["context_summary"], dict)
    assert isinstance(data["risk_flags"], list)
    assert isinstance(data["warnings"], list)
    assert isinstance(data["timestamp_utc"], str)


def test_in_vehicle_window_rejects_when_time_delta_exceeds_short_window():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-bus-window-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-bus-window-001",
        payment_method_demo_token="test-priority-payment-bus-window-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-bus-001",
        vehicle_demo_id="test-vehicle-bus-001",
        trip_demo_id="test-trip-bus-001",
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-bus-window-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-bus-window-001",
        payment_method_demo_token="test-collaborator-payment-bus-window-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-bus-001",
        vehicle_demo_id="test-vehicle-bus-001",
        trip_demo_id="test-trip-bus-001",
        validation_timestamp_utc=timestamp + timedelta(minutes=20),
    )

    policy = create_demo_trip_window_match_policy(
        in_vehicle_proximity_minutes_demo=10,
        station_platform_wait_minutes_demo=45,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=policy,
    )

    assert result.status == MatchStatus.REJECTED
    assert result.matched is False
    assert result.access_context == AccessContext.IN_VEHICLE_AFTER_PAYMENT
    assert result.effective_sync_window_minutes == 10
    assert result.effective_sync_window_matched is False
    assert result.red_sube_window_matched is True
    assert "in_vehicle_sync_window_expired" in result.risk_flags


def test_station_turnstile_window_accepts_longer_wait_before_train_or_subway():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-station-wait-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-station-wait-001",
        payment_method_demo_token="test-priority-payment-station-wait-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-subway-line-a",
        vehicle_demo_id=None,
        station_demo_id="test-station-001",
        turnstile_demo_id="test-turnstile-priority-001",
        platform_demo_id="test-platform-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-station-wait-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-station-wait-001",
        payment_method_demo_token="test-collaborator-payment-station-wait-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-subway-line-a",
        vehicle_demo_id=None,
        station_demo_id="test-station-001",
        turnstile_demo_id="test-turnstile-collaborator-001",
        platform_demo_id="test-platform-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=35),
    )

    policy = create_demo_trip_window_match_policy(
        in_vehicle_proximity_minutes_demo=10,
        station_platform_wait_minutes_demo=45,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=policy,
    )

    assert result.status == MatchStatus.MATCHED
    assert result.matched is True
    assert result.access_context == AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE
    assert result.match_strength == MatchStrength.SAME_PLATFORM_WAIT_MODERATE
    assert result.effective_sync_window_minutes == 45
    assert result.effective_sync_window_matched is True
    assert result.red_sube_window_matched is True
    assert result.same_station is True
    assert result.same_platform is True
    assert result.risk_flags == []


def test_station_turnstile_window_rejects_when_wait_exceeds_platform_window():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-station-expired-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-station-expired-001",
        payment_method_demo_token="test-priority-payment-station-expired-001",
        transport_mode=TransportMode.TRAIN,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-train-line-001",
        vehicle_demo_id=None,
        station_demo_id="test-train-station-001",
        turnstile_demo_id="test-train-turnstile-priority-001",
        platform_demo_id="test-train-platform-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-station-expired-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-station-expired-001",
        payment_method_demo_token="test-collaborator-payment-station-expired-001",
        transport_mode=TransportMode.TRAIN,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-train-line-001",
        vehicle_demo_id=None,
        station_demo_id="test-train-station-001",
        turnstile_demo_id="test-train-turnstile-collaborator-001",
        platform_demo_id="test-train-platform-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=60),
    )

    policy = create_demo_trip_window_match_policy(
        in_vehicle_proximity_minutes_demo=10,
        station_platform_wait_minutes_demo=45,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=policy,
    )

    assert result.status == MatchStatus.REJECTED
    assert result.matched is False
    assert result.access_context == AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE
    assert result.effective_sync_window_minutes == 45
    assert result.effective_sync_window_matched is False
    assert result.red_sube_window_matched is True
    assert "station_platform_sync_window_expired" in result.risk_flags


def test_station_turnstile_requires_same_station_when_policy_requires_it():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-different-station-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-different-station-001",
        payment_method_demo_token="test-priority-payment-different-station-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-subway-line-b",
        vehicle_demo_id=None,
        station_demo_id="test-station-origin-001",
        turnstile_demo_id="test-turnstile-origin-001",
        platform_demo_id="test-platform-origin-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-different-station-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-different-station-001",
        payment_method_demo_token="test-collaborator-payment-different-station-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-subway-line-b",
        vehicle_demo_id=None,
        station_demo_id="test-station-other-001",
        turnstile_demo_id="test-turnstile-other-001",
        platform_demo_id="test-platform-other-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=5),
    )

    policy = create_demo_trip_window_match_policy(
        station_platform_requires_same_station=True,
        route_only_requires_review=True,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=policy,
    )

    assert result.status == MatchStatus.REJECTED
    assert result.matched is False
    assert result.access_context == AccessContext.PLATFORM_WAIT_AFTER_TURNSTILE
    assert "station_platform_requires_same_station" in result.risk_flags


def test_route_only_match_requires_review():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-route-only-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-route-only-001",
        payment_method_demo_token="test-priority-payment-route-only-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-only-001",
        vehicle_demo_id="test-vehicle-priority-route-only-001",
        station_demo_id=None,
        turnstile_demo_id=None,
        platform_demo_id=None,
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-route-only-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-route-only-001",
        payment_method_demo_token="test-collaborator-payment-route-only-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-only-001",
        vehicle_demo_id="test-vehicle-collaborator-route-only-001",
        station_demo_id=None,
        turnstile_demo_id=None,
        platform_demo_id=None,
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=3),
    )

    policy = create_demo_trip_window_match_policy(
        route_only_requires_review=True,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=policy,
    )

    assert result.status == MatchStatus.NEEDS_REVIEW
    assert result.matched is False
    assert result.match_strength == MatchStrength.SAME_ROUTE_TIME_WINDOW_WEAK
    assert result.risk_flags == ["route_only_match_requires_review"]


def test_route_only_match_can_be_accepted_when_policy_allows_it():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-route-accepted-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-route-accepted-001",
        payment_method_demo_token="test-priority-payment-route-accepted-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-accepted-001",
        vehicle_demo_id="test-vehicle-priority-route-accepted-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-route-accepted-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-route-accepted-001",
        payment_method_demo_token="test-collaborator-payment-route-accepted-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-accepted-001",
        vehicle_demo_id="test-vehicle-collaborator-route-accepted-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=3),
    )

    policy = create_demo_trip_window_match_policy(
        route_only_requires_review=False,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
        policy=policy,
    )

    assert result.status == MatchStatus.MATCHED
    assert result.matched is True
    assert result.match_strength == MatchStrength.SAME_ROUTE_TIME_WINDOW_WEAK
    assert result.risk_flags == []


def test_rejects_outside_argentina_context():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-outside-argentina-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-outside-argentina-001",
        payment_method_demo_token="test-collaborator-payment-outside-argentina-001",
        country="Uruguay",
        route_demo_id=collaborator_signal.route_demo_id,
        vehicle_demo_id=collaborator_signal.vehicle_demo_id,
        trip_demo_id=collaborator_signal.trip_demo_id,
        validation_timestamp_utc=collaborator_signal.validation_timestamp_utc,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "collaborator_signal_outside_argentina_context" in result.risk_flags


def test_rejects_when_priority_validation_not_paid():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-not-paid-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-not-paid-001",
        payment_method_demo_token="test-priority-payment-not-paid-001",
        validation_paid=False,
        route_demo_id=priority_signal.route_demo_id,
        vehicle_demo_id=priority_signal.vehicle_demo_id,
        trip_demo_id=priority_signal.trip_demo_id,
        validation_timestamp_utc=priority_signal.validation_timestamp_utc,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "priority_validation_payment_not_confirmed" in result.risk_flags


def test_rejects_same_user_token():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-same-user-token-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token=priority_signal.participant_token,
        payment_method_demo_token="test-collaborator-payment-same-user-token-001",
        route_demo_id=priority_signal.route_demo_id,
        vehicle_demo_id=priority_signal.vehicle_demo_id,
        trip_demo_id=priority_signal.trip_demo_id,
        validation_timestamp_utc=priority_signal.validation_timestamp_utc + timedelta(minutes=1),
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "same_user_token_not_allowed" in result.risk_flags


def test_rejects_same_payment_method_token():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-same-payment-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-same-payment-001",
        payment_method_demo_token=priority_signal.payment_method_demo_token,
        route_demo_id=priority_signal.route_demo_id,
        vehicle_demo_id=priority_signal.vehicle_demo_id,
        trip_demo_id=priority_signal.trip_demo_id,
        validation_timestamp_utc=priority_signal.validation_timestamp_utc + timedelta(minutes=1),
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "same_payment_method_token_not_allowed" in result.risk_flags


def test_rejects_different_network_context():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-different-network-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-different-network-001",
        payment_method_demo_token="test-collaborator-payment-different-network-001",
        network_demo_id="test-other-network",
        route_demo_id=collaborator_signal.route_demo_id,
        vehicle_demo_id=collaborator_signal.vehicle_demo_id,
        trip_demo_id=collaborator_signal.trip_demo_id,
        validation_timestamp_utc=collaborator_signal.validation_timestamp_utc,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "different_network_context" in result.risk_flags


def test_rejects_different_transport_mode():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-different-mode-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-different-mode-001",
        payment_method_demo_token="test-collaborator-payment-different-mode-001",
        transport_mode=TransportMode.TRAIN,
        route_demo_id=collaborator_signal.route_demo_id,
        vehicle_demo_id=collaborator_signal.vehicle_demo_id,
        trip_demo_id=collaborator_signal.trip_demo_id,
        validation_timestamp_utc=collaborator_signal.validation_timestamp_utc,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "different_transport_mode" in result.risk_flags


def test_rejects_red_sube_demo_window_expired():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-red-window-expired-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-red-window-expired-001",
        payment_method_demo_token="test-priority-payment-red-window-expired-001",
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-red-window-expired-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-red-window-expired-001",
        payment_method_demo_token="test-collaborator-payment-red-window-expired-001",
        validation_timestamp_utc=timestamp + timedelta(hours=3),
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert result.red_sube_window_matched is False
    assert "red_sube_demo_window_expired" in result.risk_flags


def test_rejects_no_shared_transport_context():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-no-context-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-no-context-001",
        payment_method_demo_token="test-priority-payment-no-context-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-a",
        vehicle_demo_id="test-vehicle-a",
        trip_demo_id="test-trip-a",
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-no-context-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-no-context-001",
        payment_method_demo_token="test-collaborator-payment-no-context-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-b",
        vehicle_demo_id="test-vehicle-b",
        trip_demo_id="test-trip-b",
        validation_timestamp_utc=timestamp + timedelta(minutes=2),
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert result.match_strength == MatchStrength.NO_MATCH
    assert "no_shared_transport_context" in result.risk_flags


def test_rejects_vehicle_context_missing_for_vehicle_validator():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-missing-vehicle-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-missing-vehicle-001",
        payment_method_demo_token="test-priority-payment-missing-vehicle-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-missing-vehicle",
        vehicle_demo_id=None,
        trip_demo_id="test-trip-missing-vehicle",
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-missing-vehicle-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-missing-vehicle-001",
        payment_method_demo_token="test-collaborator-payment-missing-vehicle-001",
        transport_mode=TransportMode.BUS,
        validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
        route_demo_id="test-route-missing-vehicle",
        vehicle_demo_id="test-vehicle-present-001",
        trip_demo_id="test-trip-missing-vehicle",
        validation_timestamp_utc=timestamp + timedelta(minutes=1),
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "priority_vehicle_context_missing" in result.risk_flags


def test_rejects_station_context_missing_for_turnstile():
    timestamp = datetime.now(timezone.utc)

    priority_signal = create_demo_validation_signal(
        validation_event_demo_id="test-priority-missing-station-001",
        participant_role=ParticipantRole.PRIORITY_USER,
        participant_token="test-priority-user-missing-station-001",
        payment_method_demo_token="test-priority-payment-missing-station-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-subway-line-missing-station",
        vehicle_demo_id=None,
        station_demo_id=None,
        turnstile_demo_id="test-turnstile-missing-station-001",
        platform_demo_id="test-platform-missing-station-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp,
    )

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-missing-station-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="test-collaborator-missing-station-001",
        payment_method_demo_token="test-collaborator-payment-missing-station-001",
        transport_mode=TransportMode.SUBWAY,
        validation_point_type=ValidationPointType.STATION_TURNSTILE,
        route_demo_id="test-subway-line-missing-station",
        vehicle_demo_id=None,
        station_demo_id="test-station-present-001",
        turnstile_demo_id="test-turnstile-present-001",
        platform_demo_id="test-platform-present-001",
        trip_demo_id=None,
        validation_timestamp_utc=timestamp + timedelta(minutes=2),
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "priority_station_context_missing" in result.risk_flags


def test_rejects_free_text_tokens():
    priority_signal, collaborator_signal = create_demo_priority_and_collaborator_signals()

    collaborator_signal = create_demo_validation_signal(
        validation_event_demo_id="test-collaborator-free-text-001",
        participant_role=ParticipantRole.COLLABORATOR,
        participant_token="quiero bono solidario gratis",
        payment_method_demo_token="test-collaborator-payment-free-text-001",
        route_demo_id=collaborator_signal.route_demo_id,
        vehicle_demo_id=collaborator_signal.vehicle_demo_id,
        trip_demo_id=collaborator_signal.trip_demo_id,
        validation_timestamp_utc=collaborator_signal.validation_timestamp_utc,
    )

    result = evaluate_trip_window_match(
        priority_signal=priority_signal,
        collaborator_signal=collaborator_signal,
    )

    assert result.status == MatchStatus.REJECTED
    assert "collaborator_token_looks_like_free_text" in result.risk_flags


def test_assert_no_prohibited_fields_rejects_sensitive_fields():
    with pytest.raises(ValueError) as error:
        assert_no_prohibited_fields(
            {
                "dni": "12345678",
                "diagnostico": "dato no permitido",
                "cud": "dato no permitido",
            }
        )

    message = str(error.value).lower()

    assert "dni" in message
    assert "diagnostico" in message
    assert "cud" in message


def test_create_demo_validation_signal_rejects_empty_required_fields():
    with pytest.raises(ValueError):
        create_demo_validation_signal(
            validation_event_demo_id="",
        )

    with pytest.raises(ValueError):
        create_demo_validation_signal(
            participant_token="",
        )

    with pytest.raises(ValueError):
        create_demo_validation_signal(
            payment_method_demo_token="",
        )

    with pytest.raises(ValueError):
        create_demo_validation_signal(
            network_demo_id="",
        )


def test_create_policy_rejects_invalid_windows():
    with pytest.raises(ValueError):
        create_demo_trip_window_match_policy(
            red_sube_window_hours_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_trip_window_match_policy(
            in_vehicle_proximity_minutes_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_trip_window_match_policy(
            station_platform_wait_minutes_demo=0,
        )

    with pytest.raises(ValueError):
        create_demo_trip_window_match_policy(
            in_vehicle_proximity_minutes_demo=20,
            station_platform_wait_minutes_demo=10,
        )
