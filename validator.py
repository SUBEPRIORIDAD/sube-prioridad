from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Tuple

@dataclass(frozen=True)
class ValidationEvent:
"""
Evento técnico pseudoanonimizado de validación.

```
No contiene DNI, nombre, diagnóstico, domicilio ni historia clínica.
"""

card_hash: str
bus_id: str
line_id: str
timestamp: datetime
```

@dataclass
class AntiFraudResult:
approved: bool
reason: str
bonus_eligible: bool = False

class AntiFraudEngine:
"""
Motor antifraude para el Bono Solidario SUBE Prioridad.

```
Regla MVP:
- La tarjeta colaboradora debe validar dentro de los 60 segundos posteriores
  a una validación prioritaria.
- Ambas validaciones deben ocurrir en el mismo colectivo.
- Ambas validaciones deben ocurrir en la misma línea.
- Se controla repetición excesiva entre el mismo par de tarjetas.
"""

def __init__(
    self,
    time_window_seconds: int = 60,
    max_pair_repetitions: int = 3,
) -> None:
    self.time_window_seconds = time_window_seconds
    self.max_pair_repetitions = max_pair_repetitions
    self._pair_counter: Dict[Tuple[str, str], int] = {}

def evaluate_bonus(
    self,
    priority_event: ValidationEvent,
    collaborator_event: ValidationEvent,
) -> AntiFraudResult:
    self._validate_event(priority_event)
    self._validate_event(collaborator_event)

    if priority_event.card_hash == collaborator_event.card_hash:
        return AntiFraudResult(
            approved=False,
            reason="La tarjeta prioritaria y la colaboradora no pueden ser la misma.",
        )

    if collaborator_event.timestamp < priority_event.timestamp:
        return AntiFraudResult(
            approved=False,
            reason="La validación colaboradora no puede ser anterior a la prioritaria.",
        )

    elapsed_seconds = (
        collaborator_event.timestamp - priority_event.timestamp
    ).total_seconds()

    if elapsed_seconds > self.time_window_seconds:
        return AntiFraudResult(
            approved=False,
            reason="La validación colaboradora ocurrió fuera de la ventana temporal.",
        )

    if priority_event.bus_id != collaborator_event.bus_id:
        return AntiFraudResult(
            approved=False,
            reason="Las validaciones no corresponden al mismo colectivo.",
        )

    if priority_event.line_id != collaborator_event.line_id:
        return AntiFraudResult(
            approved=False,
            reason="Las validaciones no corresponden a la misma línea.",
        )

    pair = (priority_event.card_hash, collaborator_event.card_hash)
    current_count = self._pair_counter.get(pair, 0) + 1
    self._pair_counter[pair] = current_count

    if current_count > self.max_pair_repetitions:
        return AntiFraudResult(
            approved=False,
            reason="Se detectó repetición excesiva entre el mismo par de tarjetas.",
        )

    return AntiFraudResult(
        approved=True,
        reason="Bono Solidario aprobado para entorno MVP.",
        bonus_eligible=True,
    )

@staticmethod
def _validate_event(event: ValidationEvent) -> None:
    if not event.card_hash:
        raise ValueError("card_hash es obligatorio.")

    if not event.bus_id:
        raise ValueError("bus_id es obligatorio.")

    if not event.line_id:
        raise ValueError("line_id es obligatorio.")

    if event.timestamp.tzinfo is None:
        raise ValueError("timestamp debe incluir zona horaria.")

def reset_counters(self) -> None:
    self._pair_counter.clear()
```

def now_utc() -> datetime:
return datetime.now(timezone.utc)
