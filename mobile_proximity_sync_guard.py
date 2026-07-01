def create_demo_proximity_signal(
    sync_event_demo_id: str = "demo-mobile-proximity-sync-001",
    priority_user_token: str = "demo-priority-user-001",
    collaborator_user_token: str = "demo-collaborator-user-001",
    priority_payment_method_demo_token: str = "demo-priority-payment-001",
    collaborator_payment_method_demo_token: str = "demo-collaborator-payment-001",
    transport_access_context: TransportAccessContext = TransportAccessContext.IN_VEHICLE_AFTER_PAYMENT,
    proximity_method: ProximityMethod = ProximityMethod.QR_TEMPORARY_DEMO,
    proximity_attempt_timestamp_utc: Optional[datetime] = None,
    access_window_started_at_utc: Optional[datetime] = None,
    trip_window_started_at_utc: Optional[datetime] = None,
    priority_user_confirms_sync: bool = True,
    collaborator_claims_unilaterally: bool = False,
    same_transport_context: bool = True,
    same_vehicle_demo_id: bool = True,
    same_trainset_demo_id: bool = False,
    same_station_demo_id: bool = False,
    same_platform_demo_id: bool = False,
    access_window_matched: bool = True,
    trip_window_matched: bool = True,
    priority_user_has_mobile_device: bool = True,
    collaborator_has_mobile_device: bool = True,
    qr_or_code_token_demo: Optional[str] = "demo-qr-token-001",
    nfc_handshake_token_demo: Optional[str] = None,
    ble_ephemeral_token_demo: Optional[str] = None,
    priority_device_binding: Optional[MobileDeviceBindingDemo] = None,
    collaborator_device_binding: Optional[MobileDeviceBindingDemo] = None,
    offline_mode_detected: bool = False,
    offline_deferred_minutes_elapsed: int = 0,
) -> ProximitySignal:
    required_values = {
        "sync_event_demo_id": sync_event_demo_id,
        "priority_user_token": priority_user_token,
        "collaborator_user_token": collaborator_user_token,
        "priority_payment_method_demo_token": priority_payment_method_demo_token,
        "collaborator_payment_method_demo_token": collaborator_payment_method_demo_token,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    now = proximity_attempt_timestamp_utc or datetime.now(timezone.utc)
    started_at = access_window_started_at_utc or now - timedelta(minutes=2)
    trip_started_at = trip_window_started_at_utc or started_at

    if priority_device_binding is None and priority_user_has_mobile_device:
        priority_device_binding = create_demo_mobile_device_binding(
            user_token=priority_user_token,
            device_session_demo_token="demo-priority-device-001",
            payment_method_demo_token=priority_payment_method_demo_token,
        )

    if collaborator_device_binding is None and collaborator_has_mobile_device:
        collaborator_device_binding = create_demo_mobile_device_binding(
            user_token=collaborator_user_token,
            device_session_demo_token="demo-collaborator-device-001",
            payment_method_demo_token=collaborator_payment_method_demo_token,
        )

    return ProximitySignal(
        sync_event_demo_id=sync_event_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        collaborator_user_token=collaborator_user_token.strip(),
        priority_payment_method_demo_token=priority_payment_method_demo_token.strip(),
        collaborator_payment_method_demo_token=collaborator_payment_method_demo_token.strip(),
        transport_access_context=transport_access_context,
        proximity_method=proximity_method,
        proximity_attempt_timestamp_utc=now,
        access_window_started_at_utc=started_at,
        trip_window_started_at_utc=trip_started_at,
        priority_user_confirms_sync=priority_user_confirms_sync,
        collaborator_claims_unilaterally=collaborator_claims_unilaterally,
        same_transport_context=same_transport_context,
        same_vehicle_demo_id=same_vehicle_demo_id,
        same_trainset_demo_id=same_trainset_demo_id,
        same_station_demo_id=same_station_demo_id,
        same_platform_demo_id=same_platform_demo_id,
        access_window_matched=access_window_matched,
        trip_window_matched=trip_window_matched,
        priority_user_has_mobile_device=priority_user_has_mobile_device,
        collaborator_has_mobile_device=collaborator_has_mobile_device,
        qr_or_code_token_demo=qr_or_code_token_demo,
        nfc_handshake_token_demo=nfc_handshake_token_demo,
        ble_ephemeral_token_demo=ble_ephemeral_token_demo,
        priority_device_binding=priority_device_binding,
        collaborator_device_binding=collaborator_device_binding,
        offline_mode_detected=offline_mode_detected,
        offline_deferred_minutes_elapsed=offline_deferred_minutes_elapsed,
    )
