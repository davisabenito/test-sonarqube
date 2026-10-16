#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de limpieza de datos con malas prácticas intencionales para SonarQube.
Este código contiene problemas de calidad que SonarQube debe detectar.
"""

import pandas as pd
import numpy as np
import os
import sys
import csv
import json
from datetime import datetime
import time
import hashlib

# Variables globales (mala práctica)
global_var_1 = None
global_var_2 = None
global_var_3 = None
global_var_4 = None
global_var_5 = None

# Constantes con nombres malos (mala práctica)
A = 1
B = 2
C = 3

def cargar_datos_sin_verificar(ruta):
    """Carga datos sin verificar si el archivo existe (mala práctica)."""
    df = pd.read_csv(ruta)
    return df

def procesar_datos_duplicado(df):
    """Función con código duplicado (mala práctica)."""
    # Primera parte duplicada
    df['columna1'] = df['columna1'].fillna(0)
    df['columna2'] = df['columna2'].fillna(0)
    df['columna3'] = df['columna3'].fillna(0)
    df['columna4'] = df['columna4'].fillna(0)
    df['columna5'] = df['columna5'].fillna(0)

    # Segunda parte duplicada (código repetido)
    df['columna1'] = df['columna1'].fillna(0)
    df['columna2'] = df['columna2'].fillna(0)
    df['columna3'] = df['columna3'].fillna(0)
    df['columna4'] = df['columna4'].fillna(0)
    df['columna5'] = df['columna5'].fillna(0)

    return df

def funcion_demasiado_larga(df):
    """Función con más de 50 líneas (mala práctica)."""
    # Línea 1
    df['col1'] = df['col1'].fillna(0)
    # Línea 2
    df['col2'] = df['col2'].fillna(0)
    # Línea 3
    df['col3'] = df['col3'].fillna(0)
    # Línea 4
    df['col4'] = df['col4'].fillna(0)
    # Línea 5
    df['col5'] = df['col5'].fillna(0)
    # Línea 6
    df['col6'] = df['col6'].fillna(0)
    # Línea 7
    df['col7'] = df['col7'].fillna(0)
    # Línea 8
    df['col8'] = df['col8'].fillna(0)
    # Línea 9
    df['col9'] = df['col9'].fillna(0)
    # Línea 10
    df['col10'] = df['col10'].fillna(0)
    # Línea 11
    df['col11'] = df['col11'].fillna(0)
    # Línea 12
    df['col12'] = df['col12'].fillna(0)
    # Línea 13
    df['col13'] = df['col13'].fillna(0)
    # Línea 14
    df['col14'] = df['col14'].fillna(0)
    # Línea 15
    df['col15'] = df['col15'].fillna(0)
    # Línea 16
    df['col16'] = df['col16'].fillna(0)
    # Línea 17
    df['col17'] = df['col17'].fillna(0)
    # Línea 18
    df['col18'] = df['col18'].fillna(0)
    # Línea 19
    df['col19'] = df['col19'].fillna(0)
    # Línea 20
    df['col20'] = df['col20'].fillna(0)
    # Línea 21
    df['col21'] = df['col21'].fillna(0)
    # Línea 22
    df['col22'] = df['col22'].fillna(0)
    # Línea 23
    df['col23'] = df['col23'].fillna(0)
    # Línea 24
    df['col24'] = df['col24'].fillna(0)
    # Línea 25
    df['col25'] = df['col25'].fillna(0)
    # Línea 26
    df['col26'] = df['col26'].fillna(0)
    # Línea 27
    df['col27'] = df['col27'].fillna(0)
    # Línea 28
    df['col28'] = df['col28'].fillna(0)
    # Línea 29
    df['col29'] = df['col29'].fillna(0)
    # Línea 30
    df['col30'] = df['col30'].fillna(0)
    # Línea 31
    df['col31'] = df['col31'].fillna(0)
    # Línea 32
    df['col32'] = df['col32'].fillna(0)
    # Línea 33
    df['col33'] = df['col33'].fillna(0)
    # Línea 34
    df['col34'] = df['col34'].fillna(0)
    # Línea 35
    df['col35'] = df['col35'].fillna(0)
    # Línea 36
    df['col36'] = df['col36'].fillna(0)
    # Línea 37
    df['col37'] = df['col37'].fillna(0)
    # Línea 38
    df['col38'] = df['col38'].fillna(0)
    # Línea 39
    df['col39'] = df['col39'].fillna(0)
    # Línea 40
    df['col40'] = df['col40'].fillna(0)
    # Línea 41
    df['col41'] = df['col41'].fillna(0)
    # Línea 42
    df['col42'] = df['col42'].fillna(0)
    # Línea 43
    df['col43'] = df['col43'].fillna(0)
    # Línea 44
    df['col44'] = df['col44'].fillna(0)
    # Línea 45
    df['col45'] = df['col45'].fillna(0)
    # Línea 46
    df['col46'] = df['col46'].fillna(0)
    # Línea 47
    df['col47'] = df['col47'].fillna(0)
    # Línea 48
    df['col48'] = df['col48'].fillna(0)
    # Línea 49
    df['col49'] = df['col49'].fillna(0)
    # Línea 50
    df['col50'] = df['col50'].fillna(0)
    return df

def funcion_sin_documentacion():
    """Función sin documentación (mala práctica)."""
    pass

def usar_print_en_lugar_de_logging():
    """Usar print en lugar de logging (mala práctica)."""
    print("Iniciando proceso")
    print("Procesando datos")
    print("Finalizando proceso")

def excepcion_generica():
    """Capturar excepción genérica (mala práctica)."""
    try:
        resultado = 1 / 0
    except Exception:
        pass

def anidamiento_excesivo(df):
    """Anidamiento excesivo de if/else (mala práctica)."""
    if df is not None:
        if len(df) > 0:
            if 'columna' in df.columns:
                if df['columna'].notna().any():
                    if df['columna'].sum() > 100:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def complejidad_ciclomatica_alta(x):
    """Función con alta complejidad ciclomática (mala práctica)."""
    if x > 100:
        return "mayor_100"
    elif x > 90:
        return "mayor_90"
    elif x > 80:
        return "mayor_80"
    elif x > 70:
        return "mayor_70"
    elif x > 60:
        return "mayor_60"
    elif x > 50:
        return "mayor_50"
    elif x > 40:
        return "mayor_40"
    elif x > 30:
        return "mayor_30"
    elif x > 20:
        return "mayor_20"
    elif x > 10:
        return "mayor_10"
    else:
        return "menor_10"

def parametro_demasiados(param1, param2, param3, param4, param5, param6, param7, param8):
    """Función con demasiados parámetros (mala práctica)."""
    return param1 + param2 + param3 + param4 + param5 + param6 + param7 + param8

def variable_no_usada():
    """Variable definida pero no usada (mala práctica)."""
    no_usada = "esta variable no se usa"
    return "hola"

def import_no_usado():
    """Import no utilizado (mala práctica)."""
    from typing import List
    return "hola"

def comentario_inutil():
    """Comentario que no aporta valor (mala práctica)."""
    # Este es un comentario que no dice nada útil
    x = 5  # asignar 5 a x
    return x

def hardcoding():
    """Valores hardcodeados (mala práctica)."""
    url = "http://localhost:9000"
    puerto = 9000
    usuario = "admin"
    password = "admin123"
    return url, puerto, usuario, password

def parametro_por_defecto_mutuable(lista=[]):
    """Parámetro por defecto mutable (mala práctica grave)."""
    lista.append("nuevo_elemento")
    return lista

def codigo_muerto():
    """Código muerto (mala práctica)."""
    x = 5
    return 10
    x = 100  # Este código nunca se ejecuta
    print("esto nunca se imprime")

def comparacion_redundante(x):
    """Comparación redundante (mala práctica)."""
    if x == x:
        return True
    else:
        return False

def asignacion_no_usada():
    """Asignación que no se usa (mala práctica)."""
    x = 5
    y = 10
    z = 15
    return y

def concatenacion_string_ineficiente(s):
    """Concatenación de strings ineficiente (mala práctica)."""
    resultado = ""
    for i in range(100):
        resultado = resultado + str(i)  # Ineficiente
    return resultado

def funcion_magic_number():
    """Números mágicos sin constante (mala práctica)."""
    if x > 42:
        return "mayor"
    elif x < 17:
        return "menor"
    else:
        return "igual"

def sql_injection_simulada(usuario):
    """Simulación de SQL injection (mala práctica de seguridad)."""
    query = "SELECT * FROM users WHERE name = '" + usuario + "'"
    return query

def empty_except():
    """Except vacío (mala práctica)."""
    try:
        resultado = 1 / 0
    except:
        pass

def funcion_no_retornada():
    """Función que debería retornar algo pero no lo hace (mala práctica)."""
    if True:
        return True
    # No hay return en else

def comentario_muy_largo():
    """Comentario muy largo que no aporta valor (mala práctica)."""
    # Este es un comentario extremadamente largo que no aporta ningún valor
    # al código y solo sirve para ocupar espacio y hacer que el archivo sea
    # más difícil de leer y mantener, lo cual es una mala práctica según
    # las reglas de calidad de código de SonarQube y otros linters.
    x = 5
    return x

def demasiadas_lineas_vacias():
    """Demasiadas líneas vacías (mala práctica)."""


    x = 5


    y = 10


    return x + y

def variable_shadowing(x):
    """Variable shadowing (mala práctica)."""
    x = x + 1
    return x

def uso_de_tipo():
    """Uso de type() en lugar de isinstance (mala práctica)."""
    if type(x) == int:
        return "es int"
    else:
        return "no es int"

def literal_comentario_inutil():
    """Literal string no usado (mala práctica)."""
    "este string no se usa"
    return True

def clonar_con_slice(lista):
    """Clonar con slice en lugar de copy() (mala práctica)."""
    nueva_lista = lista[:]
    return nueva_lista

def check_none_comparision(obj):
    """Comparación con None usando == en lugar de is (mala práctica)."""
    if obj == None:
        return True
    return False

def try_except_finally():
    """Try-except-finally con excepción genérica (mala práctica)."""
    try:
        resultado = risky_operation()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()

def risky_operation():
    """Operación riesgosa simulada."""
    return 1 / 0

def cleanup():
    """Limpieza simulada."""
    pass

def deprecated_function():
    """Función marcada como deprecated pero sin docstring."""
    pass

def not_implemented():
    """Función con NotImplementedError sin mensaje."""
    raise NotImplementedError

def infinite_loop_possibility():
    """Posible loop infinito (mala práctica)."""
    x = 0
    while x < 10:
        x = x + 0  # Esto nunca incrementa realmente x

def function_with_too_many_returns(x):
    """Función con demasiados returns (mala práctica)."""
    if x < 0:
        return "negativo"
    elif x == 0:
        return "cero"
    elif x == 1:
        return "uno"
    elif x == 2:
        return "dos"
    elif x == 3:
        return "tres"
    elif x == 4:
        return "cuatro"
    elif x == 5:
        return "cinco"
    else:
        return "otro"

def string_comparison_case_sensitive(s1, s2):
    """Comparación de strings case-sensitive cuando debería ser case-insensitive."""
    return s1 == s2

def unused_import_function():
    """Función que usa imports pero de forma incorrecta."""
    from collections import defaultdict
    return True

def hardcoded_password():
    """Password hardcodeado (mala práctica de seguridad)."""
    password = "admin123"
    return password

def insecure_hash(password):
    """Hash inseguro (mala práctica de seguridad)."""
    return hashlib.md5(password.encode()).hexdigest()

def temporizador():
    """Uso de time.sleep en producción (mala práctica)."""
    time.sleep(5)
    return "listo"

def eval_usage():
    """Uso de eval() (mala práctica de seguridad)."""
    x = eval("1 + 1")
    return x

def exec_usage():
    """Uso de exec() (mala práctica de seguridad)."""
    exec("x = 5")
    return x

# ============================================
# CÓDIGO DUPLICADO INTENCIONAL PARA SONARQUBE
# ============================================

def duplicado_1():
    """Función duplicada 1 - primera versión."""
    x = 5
    y = 10
    z = x + y
    return z

def duplicado_2():
    """Función duplicada 2 - misma lógica que duplicado_1."""
    x = 5
    y = 10
    z = x + y
    return z

def duplicado_3():
    """Función duplicada 3 - misma lógica que duplicado_1."""
    x = 5
    y = 10
    z = x + y
    return z

def procesar_datos_v1(df):
    """Procesar datos versión 1 - código duplicado."""
    df['col1'] = df['col1'].fillna(0)
    df['col2'] = df['col2'].fillna(0)
    df['col3'] = df['col3'].fillna(0)
    df['col4'] = df['col4'].fillna(0)
    df['col5'] = df['col5'].fillna(0)
    return df

def procesar_datos_v2(df):
    """Procesar datos versión 2 - código duplicado de v1."""
    df['col1'] = df['col1'].fillna(0)
    df['col2'] = df['col2'].fillna(0)
    df['col3'] = df['col3'].fillna(0)
    df['col4'] = df['col4'].fillna(0)
    df['col5'] = df['col5'].fillna(0)
    return df

def procesar_datos_v3(df):
    """Procesar datos versión 3 - código duplicado de v1."""
    df['col1'] = df['col1'].fillna(0)
    df['col2'] = df['col2'].fillna(0)
    df['col3'] = df['col3'].fillna(0)
    df['col4'] = df['col4'].fillna(0)
    df['col5'] = df['col5'].fillna(0)
    return df

def validar_datos_v1(data):
    """Validar datos versión 1 - código duplicado."""
    if data is None:
        return False
    if len(data) == 0:
        return False
    if 'id' not in data:
        return False
    if 'nombre' not in data:
        return False
    return True

def validar_datos_v2(data):
    """Validar datos versión 2 - código duplicado de v1."""
    if data is None:
        return False
    if len(data) == 0:
        return False
    if 'id' not in data:
        return False
    if 'nombre' not in data:
        return False
    return True

def validar_datos_v3(data):
    """Validar datos versión 3 - código duplicado de v1."""
    if data is None:
        return False
    if len(data) == 0:
        return False
    if 'id' not in data:
        return False
    if 'nombre' not in data:
        return False
    return True

def limpiar_texto_v1(texto):
    """Limpiar texto versión 1 - código duplicado."""
    texto = texto.strip()
    texto = texto.lower()
    texto = texto.replace('  ', ' ')
    texto = texto.replace('\n', ' ')
    texto = texto.replace('\t', ' ')
    return texto

def limpiar_texto_v2(texto):
    """Limpiar texto versión 2 - código duplicado de v1."""
    texto = texto.strip()
    texto = texto.lower()
    texto = texto.replace('  ', ' ')
    texto = texto.replace('\n', ' ')
    texto = texto.replace('\t', ' ')
    return texto

def limpiar_texto_v3(texto):
    """Limpiar texto versión 3 - código duplicado de v1."""
    texto = texto.strip()
    texto = texto.lower()
    texto = texto.replace('  ', ' ')
    texto = texto.replace('\n', ' ')
    texto = texto.replace('\t', ' ')
    return texto

def calcular_estadisticas_v1(numeros):
    """Calcular estadísticas versión 1 - código duplicado."""
    if not numeros:
        return 0, 0, 0
    promedio = sum(numeros) / len(numeros)
    maximo = max(numeros)
    minimo = min(numeros)
    return promedio, maximo, minimo

def calcular_estadisticas_v2(numeros):
    """Calcular estadísticas versión 2 - código duplicado de v1."""
    if not numeros:
        return 0, 0, 0
    promedio = sum(numeros) / len(numeros)
    maximo = max(numeros)
    minimo = min(numeros)
    return promedio, maximo, minimo

def calcular_estadisticas_v3(numeros):
    """Calcular estadísticas versión 3 - código duplicado de v1."""
    if not numeros:
        return 0, 0, 0
    promedio = sum(numeros) / len(numeros)
    maximo = max(numeros)
    minimo = min(numeros)
    return promedio, maximo, minimo

def main():
    """Función principal con múltiples malas prácticas."""
    # Usar variable global
    global global_var_1
    global_var_1 = "valor"

    # Cargar datos sin verificar
    df = cargar_datos_sin_verificar("datos.csv")

    # Procesar con código duplicado
    df = procesar_datos_duplicado(df)

    # Función demasiado larga
    df = funcion_demasiado_larga(df)

    # Usar print en lugar de logging
    usar_print_en_lugar_de_logging()

    # Excepción genérica
    excepcion_generica()

    # Anidamiento excesivo
    resultado = anidamiento_excesivo(df)

    # Complejidad ciclomática alta
    categoria = complejidad_ciclomatica_alta(50)

    # Demasiados parámetros
    suma = parametro_demasiados(1, 2, 3, 4, 5, 6, 7, 8)

    # Variable no usada
    variable_no_usada()

    # Import no usado
    import_no_usado()

    # Comentario inútil
    comentario_inutil()

    # Hardcoding
    url, puerto, usuario, password = hardcoding()

    # Parámetro mutable por defecto
    parametro_por_defecto_mutuable()

    # Código muerto
    codigo_muerto()

    # Comparación redundante
    comparacion_redundante(5)

    # Asignación no usada
    asignacion_no_usada()

    # Concatenación ineficiente
    concatenacion_string_ineficiente("test")

    # SQL injection simulada
    sql_injection_simulada("admin")

    # Except vacío
    empty_except()

    # Función no retornada
    funcion_no_retornada()

    # Comentario muy largo
    comentario_muy_largo()

    # Demasiadas líneas vacías
    demasiadas_lineas_vacias()

    # Variable shadowing
    variable_shadowing(5)

    # Uso de type()
    uso_de_tipo(5)

    # Literal comentario inútil
    literal_comentario_inutil()

    # Clonar con slice
    clonar_con_slice([1, 2, 3])

    # Comparación con None
    check_none_comparision(None)

    # Try except finally
    try_except_finally()

    # Deprecated function
    deprecated_function()

    # Not implemented
    # not_implemented()

    # Loop infinito
    infinite_loop_possibility()

    # Demasiados returns
    function_with_too_many_returns(3)

    # String comparison
    string_comparison_case_sensitive("hola", "HOLA")

    # Unused import
    unused_import_function()

    # Hardcoded password
    hardcoded_password()

    # Insecure hash
    insecure_hash("password")

    # Temporizador
    temporizador()

    # Eval usage
    eval_usage()

    # Exec usage
    exec_usage()

    print(f"Proceso completado. URL: {url}, Puerto: {puerto}")

if __name__ == "__main__":
    main()
