"""API de lectura para comprobar la conexión Python → FastAPI → MySQL."""

import logging
from contextlib import closing

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mysql.connector import Error

from conexion import obtener_conexion

app = FastAPI(title="Finanzas al Alcance")
logger = logging.getLogger(__name__)

# Permitir el frontend servido por HTTP en localhost o 127.0.0.1, en cualquier puerto.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


def consultar(sql, parametros=()):
    """Ejecuta una consulta y devuelve las filas como diccionarios para JSON."""
    try:
        # closing cierra el cursor y la conexión incluso si ocurre un error.
        with closing(obtener_conexion()) as conexion:
            with closing(conexion.cursor(dictionary=True)) as cursor:
                cursor.execute(sql, parametros)
                return cursor.fetchall()
    except ConnectionError as error:
        raise HTTPException(status_code=503, detail=str(error)) from None
    except Error as error:
        logger.error("Error al consultar MySQL (código %s).", error.errno)
        if error.errno in (2006, 2013, 2055):
            raise HTTPException(
                status_code=503,
                detail="Se perdió la conexión con MySQL. Intentá nuevamente.",
            ) from None
        raise HTTPException(
            status_code=500,
            detail="No se pudo consultar la base de datos. Revisá las tablas y columnas esperadas.",
        ) from None


@app.get("/")
def inicio():
    return {"mensaje": "API de Finanzas al Alcance funcionando"}


@app.get("/categorias")
def obtener_categorias():
    return consultar("SELECT * FROM categorias;")


@app.get("/contenidos")
def obtener_contenidos():
    return consultar("SELECT id_contenido, titulo, texto, id_categoria FROM contenidos;")


@app.get("/contenidos/categoria/{id_categoria}")
def obtener_contenidos_por_categoria(id_categoria: int):
    # El valor de la URL se pasa separado del SQL para evitar inyección SQL.
    return consultar(
        "SELECT id_contenido, titulo, texto, id_categoria "
        "FROM contenidos WHERE id_categoria = %s;",
        (id_categoria,),
    )
