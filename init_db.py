import os
import psycopg2
from config import SubePrioridadConfig

class SubePrioridadDBInitializer:
    """Aprovisionador automático del motor relacional PostgreSQL para SUBE Prioridad."""
    
    def __init__(self):
        # Parámetros de conexión recuperados del estándar de configuración centralizado
        self.db_name = os.getenv("SUBE_DB_NAME", "sube_prioridad_db")
        self.db_user = os.getenv("SUBE_DB_USER", "nacion_servicios_admin")
        self.db_pass = os.getenv("SUBE_DB_PASSWORD", "SecretCriptoPassword123")
        self.db_host = os.getenv("SUBE_DB_HOST", "sube-secure-db")

    def execute_schema_provisioning(self) -> bool:
        """Lee el archivo schema.sql y lo ejecuta en el servidor destino."""
        if not os.path.exists("schema.sql"):
            print("❌ Error Crítico: No se encuentra el archivo 'schema.sql' en la raíz.")
            return False
            
        try:
            # Establece la conexión física con el clúster de la base de datos
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                host=self.db_host,
                port="5432"
            )
            cursor = conn.cursor()
            
            print(f"🔌 Conexión establecida con {self.db_host}. Leyendo schema.sql...")
            with open("schema.sql", "r", encoding="utf-8") as schema_file:
                schema_queries = schema_file.read()
                
            # Ejecución del bloque completo deDDL y triggers del Habeas Data
            cursor.execute(schema_queries)
            conn.commit()
            
            cursor.close()
            conn.close()
            print("✅ [BASE DE DATOS LISTA]: Esquemas de tokens y clearing aprovisionados con éxito.")
            return True
            
        except Exception as error:
            print(f"⚠️ Falla de conectividad o sintaxis en el motor relacional: {error}")
            print("ℹ️ Nota de Laboratorio: Si estás ejecutando fuera del contenedor Docker, esto es esperado.")
            return False

if __name__ == "__main__":
    initializer = SubePrioridadDBInitializer()
    initializer.execute_schema_provisioning()
