-- =====================================================================
-- PLIEGO TÉCNICO: ARQUITECTURA DE BASE DE DATOS Y GOBERNANZA DE DATOS
-- PROGRAMA SUBE PRIORIDAD - ESTÁNDAR LEY Nº 25.326 (HABEAS DATA)
-- =====================================================================

-- 1. Capa de Abstracción Médica: Almacenamiento Disociado de Beneficios
-- Esta tabla reside en un entorno aislado (Sandbox) y NO almacena DNI ni diagnósticos clínicos.
CREATE TABLE sube_prioridad_tokens (
    token_id_hash VARCHAR(64) PRIMARY KEY,       -- SHA-256 del hardware ID de la tarjeta (PAN tokenizado)
    atributo_prioridad_status INT DEFAULT 0,    -- 0: Inactivo, 1: Activo binario ("Califica")
    perfil_alertas_ux INT DEFAULT 2,             -- 1: Visible, 2: Discreto (Pantalla Chofer), 3: Pasivo
    fecha_emision TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_caducidad TIMESTAMP WITH TIME ZONE NOT NULL, -- Caducidad cronológica automática según auditoría médica
    CONSTRAINT check_status BINARY (atributo_prioridad_status IN (0, 1)),
    CONSTRAINT check_ux BINARY (perfil_alertas_ux IN (1, 2, 3))
);

-- Indexación de alta velocidad para validación transaccional en pasarelas centralizadas (<500ms)
CREATE INDEX idx_tokens_hash_status ON sube_prioridad_tokens (token_id_hash, atributo_prioridad_status);


-- 2. Capa Analítica de Inteligencia de Negocio (Business Intelligence)
-- Registro de eventos a bordo para la mitigación de riesgos viales y optimización de frecuencias.
CREATE TABLE logs_uso_estadistico_macro (
    log_id SERIAL PRIMARY KEY,
    linea_colectivo_id VARCHAR(10) NOT NULL,
    interno_coche_id VARCHAR(10) NOT NULL,
    geolocalización_hash VARCHAR(12),            -- Geohash simplificado para preservar la privacidad de ruta
    timestamp_evento TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    modo_alerta_disparado INT NOT NULL
);


-- 3. Capa del Módulo Cívico Diferido: Cola del Bono Solidario
-- Filtro transaccional duro para la prevención de fraudes y manipulación de saldos.
CREATE TABLE cola_clearing_bono_solidario (
    clearing_id SERIAL PRIMARY KEY,
    tarjeta_prioridad_hash_anon VARCHAR(64) NOT NULL, -- ID pseudoanónimo del pasajero prioritario
    tarjeta_colaborador_hash_anon VARCHAR(64) NOT NULL, -- ID pseudoanónimo del pasajero cooperante
    linea_colectivo_id VARCHAR(10) NOT NULL,
    interno_coche_id VARCHAR(10) NOT NULL,
    timestamp_prioridad TIMESTAMP WITH TIME ZONE NOT NULL,
    timestamp_bono TIMESTAMP WITH TIME ZONE NOT NULL,
    estado_verificacion VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, PROCESADO, ANOMALO_BLOQUEADO
    puntos_civicos_asignados INT DEFAULT 0
);


-- 4. Rutina Automática de Fallo Seguro y Depuración Cronológica
-- Trigger que purga los tokens cuya ventana temporal de salud ha expirado (Garantía de persistencia mutable)
CREATE OR REPLACE FUNCTION purgar_atributos_caducados()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE sube_prioridad_tokens 
    SET atributo_prioridad_status = 0 
    WHERE fecha_caducidad < CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
