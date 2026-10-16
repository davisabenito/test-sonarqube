#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba simple para verificar que el código Python funciona.
"""

import pandas as pd
import sys

def test_cargar_datos():
    """Prueba básica de carga de datos."""
    try:
        df = pd.read_csv('datos.csv')
        print(f"✓ Datos cargados correctamente: {len(df)} filas")
        return True
    except Exception as e:
        print(f"✗ Error al cargar datos: {e}")
        return False

def test_procesamiento():
    """Prueba básica de procesamiento."""
    try:
        df = pd.read_csv('datos.csv')
        df['edad'] = df['edad'].fillna(0)
        print(f"✓ Procesamiento básico funciona")
        return True
    except Exception as e:
        print(f"✗ Error en procesamiento: {e}")
        return False

if __name__ == "__main__":
    print("Ejecutando pruebas básicas...")
    test1 = test_cargar_datos()
    test2 = test_procesamiento()

    if test1 and test2:
        print("\n✓ Todas las pruebas pasaron")
        sys.exit(0)
    else:
        print("\n✗ Algunas pruebas fallaron")
        sys.exit(1)
