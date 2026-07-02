"""
Tests — SUBE Prioridad: matriz de información mínima por rol.

Estos tests verifican que:

- cada actor reciba sólo la información mínima necesaria;
- la visibilidad pública sea siempre "Usuario SUBE Prioridad";
- validadoras y molinetes no reciban causa médica;
- choferes no reciban diagnóstico ni nuevas obligaciones;
- personal autorizado de estación pueda recibir indicio sólo con consentimiento;
- pasajeros colaboradores nunca conozcan causa, identidad ni diagnóstico;
- analítica use sólo datos agregados;
- se bloqueen solicitudes de indicios fuera de contexto autorizado;
- se bloqueen campos prohibidos como DNI, diagnóstico o CUD visible.
"""

from __future__ import annotations

import pytest

from minimal_information_roles import (
    DisclosureDecision,
    EcosystemRole,
    InformationItem,
    OperationalContext,
    VisibilityScope if False else None,
)
