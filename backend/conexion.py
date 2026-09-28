"""Conexión a la base de datos MySQL del proyecto."""

import logging
import os

import mysql.connector

logger = logging.getLogger(__name__)


def obtener_conexion():
    """Devuelve una conexión; quien la utiliza debe cerrarla al terminar."""
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            database="finanzas_al_alcance",
            user="root",
            # Si MySQL tiene contraseña, definir MYSQL_PASSWORD en la terminal.
            password=os.environ.get("MYSQL_PASSWORD", ""),
            connection_timeout=5,
        )
    except mysql.connector.Error as error:
        # Registrar solo el número de error, sin credenciales ni detalles privados.
        logger.error("No se pudo conectar a MySQL (código %s).", error.errno)
        raise ConnectionError(
            "No se pudo conectar a MySQL. Revisá que el servicio esté activo, "
            "que exista la base finanzas_al_alcance y que las credenciales sean correctas."
        ) from None
