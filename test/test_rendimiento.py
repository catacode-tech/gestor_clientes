import time
import os
from cliente import ClienteRegular
from base_datos import GestorBaseDatos

def evaluar_rendimiento(cantidad_registros=1000):
    db_perf = "perf_temp.db"
    json_perf = "perf_temp.json"
    csv_perf = "perf_temp.csv"
    
    gestor = GestorBaseDatos(db_path=db_perf, json_path=json_perf, csv_path=csv_perf)
    
    print(f"=== PRUEBA DE RENDIMIENTO ({cantidad_registros} REGISTROS) ===")
    
    # 1. Medir tiempo de inserción masiva
    inicio_insert = time.time()
    for i in range(cantidad_registros):
        cliente = ClienteRegular(f"ID_{i}", f"Usuario {i}", f"user{i}@test.com", "12345678", "Direccion")
        gestor.guardar_cliente(cliente)
    fin_insert = time.time()
    tiempo_insert = fin_insert - inicio_insert
    print(f"-> Insercion de {cantidad_registros} registros: {tiempo_insert:.4f} segundos")
    
    # 2. Medir tiempo de lectura/consulta completa
    inicio_lectura = time.time()
    registros = gestor.obtener_todos()
    fin_lectura = time.time()
    tiempo_lectura = fin_lectura - inicio_lectura
    print(f"-> Lectura de {len(registros)} registros: {tiempo_lectura:.4f} segundos")
    
    # Limpieza
    for archivo in [db_perf, json_perf, csv_perf]:
        if os.path.exists(archivo):
            os.remove(archivo)
            
    print("==================================================")

if __name__ == "__main__":
    evaluar_rendimiento()