import time
import unittest
from validator import SubePrioridadValidator

class TestSubeAntifraudSystem(unittest.TestCase):
    def setUp(self):
        # Inicializa una validadora limpia para cada escenario de prueba de laboratorio
        self.validator = SubePrioridadValidator()

    def test_scen_1_flujo_solidario_legitimo(self):
        """Caso Exitoso: Coexistencia temporal correcta en la misma unidad."""
        # Usuario prioritario apoya la tarjeta en T0
        res_priority = self.validator.process_transaction("SUBE_PRO_881", is_priority_user=True)
        self.assertEqual(res_priority["action"], "TRIGGER_DISCRET_ALERT")
        
        # Pasajero cooperante cede el asiento y paga 4 segundos después (dentro del umbral de 60s)
        res_cooperante = self.validator.process_transaction("SUBE_COM_992", is_priority_user=False)
        
        self.assertTrue(res_cooperante["bono_eligible"])
        self.assertEqual(res_cooperante["action"], "QUEUE_FOR_CLEARING")
        print("\n[TEST 1 PASSED]: Flujo solidario legítimo procesado y encolado para clearing.")

    def test_scen_2_rechazo_por_ventana_temporal_expirada(self):
        """Filtro Antifraude: Denegar el bono si la re-validación ocurre fuera de los 60 segundos."""
        # Usuario prioritario apoya la tarjeta en T0
        self.validator.process_transaction("SUBE_PRO_881", is_priority_user=True)
        
        # Forzar manualmente una marca de tiempo expirada simulando un retraso en la unidad
        self.validator.active_priority_event["timestamp"] -= 61.0
        
        # Pasajero común valida pasaje ordinario después del tiempo límite
        res_tardio = self.validator.process_transaction("SUBE_COM_554", is_priority_user=False)
        
        self.assertFalse(res_tardio["bono_eligible"])
        self.assertEqual(res_tardio["action"], "STANDARD_FLUID_TRANSACTION")
        print("[TEST 2 PASSED]: Filtro temporal duro ejecutado correctamente. Intento tardío bloqueado.")

    def test_scen_3_aislamiento_y_uniciad_del_bono(self):
        """Filtro Antifraude: Un evento de prioridad otorga únicamente un (1) Bono Solidario."""
        self.validator.process_transaction("SUBE_PRO_332", is_priority_user=True)
        
        # Primer pasajero cede el asiento dentro del delta t (Aprobado)
        res_primer_pasajero = self.validator.process_transaction("SUBE_COM_111", is_priority_user=False)
        self.assertTrue(res_primer_pasajero["bono_eligible"])
        
        # Segundo pasajero valida en el segundo 10 (Debe ser rechazado para evitar duplicación de incentivos)
        res_segundo_pasajero = self.validator.process_transaction("SUBE_COM_222", is_priority_user=False)
        self.assertFalse(res_segundo_pasajero["bono_eligible"])
        self.assertEqual(res_segundo_pasajero["action"], "STANDARD_FLUID_TRANSACTION")
        print("[TEST 3 PASSED]: Blindaje transaccional exitoso. Evitada la clonación de incentivos concurrentes.")

if __name__ == "__main__":
    unittest.main()
