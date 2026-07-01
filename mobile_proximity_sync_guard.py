def _metrics(
    signal: ProximitySignal,
    policy: ProximityGuardPolicy,
) -> Dict[str, Any]:
    """
    Calcula métricas internas del guard.

    Regla corregida:
        Tener dispositivos móviles disponibles o vinculados NO significa que
        se haya usado efectivamente un método de proximidad móvil.

    Por eso:
        - QR, NFC, BLE o código manual sí cuentan como señal usada.
        - SAME_DEVICE_SESSION_DEMO cuenta si además hay vínculo demo válido.
        - NONE_AVAILABLE nunca cuenta como señal móvil usada.
        - La existencia de dispositivos vinculados sólo queda como auditoría.
    """
    mobile_filter_available = (
        signal.priority_user_has_mobile_device
        or signal.collaborator_has_mobile_device
        or signal.priority_device_binding is not None
        or signal.collaborator_device_binding is not None
    )

    handshake_signal_present = _handshake_signal_present(signal)
    device_binding_matched = _device_binding_matched(signal)

    mobile_filter_used = mobile_filter_available and (
        handshake_signal_present
        or (
            signal.proximity_method == ProximityMethod.SAME_DEVICE_SESSION_DEMO
            and device_binding_matched
        )
    )

    proximity_reinforced = mobile_filter_used and _proximity_strength(
        signal=signal,
        policy=policy,
        mobile_filter_used=mobile_filter_used,
    ) in {
        ProximityStrength.STRONG,
        ProximityStrength.MODERATE,
    }

    mobile_filter_absent = not mobile_filter_available
    mobile_filter_available_but_not_used = (
        mobile_filter_available and not mobile_filter_used
    )

    return {
        "mobile_filter_available": mobile_filter_available,
        "mobile_filter_used": mobile_filter_used,
        "mobile_filter_absent": mobile_filter_absent,
        "mobile_filter_available_but_not_used": mobile_filter_available_but_not_used,
        "handshake_signal_present": handshake_signal_present,
        "device_binding_matched": device_binding_matched,
        "proximity_reinforced": proximity_reinforced,
    }
