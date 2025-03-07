import logging
from logging.handlers import TimedRotatingFileHandler
import os
import datetime


def setup_logger(log_name: str = "app_logger", log_file_path='app.log', log_level=logging.INFO):
    """
    Configura un logger con rotación semanal que muestra fecha, nivel, fichero y mensaje.

    Args:
        log_name (str): Nombre del logger (por defecto "app_logger")
        log_file_path (str): Ruta al archivo de log
        log_level (int): Nivel de log (por defecto INFO)

    Returns:
        logging.Logger: Logger configurado
    """
    # Crear el directorio de logs si no existe
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Crear logger
    logger = logging.getLogger("AppLogger")
    logger.setLevel(log_level)

    # Evitar duplicar handlers si la función se llama múltiples veces
    if logger.handlers:
        return logger

    # Crear un handler para la rotación semanal
    # El when='W0' indica que rota cada lunes (inicio de semana)
    handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when='W0',
        interval=1,
        backupCount=4,  # Guarda hasta 4 archivos de backup
        encoding='utf-8'
    )

    # Configurar el formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Opcionalmente, agregar handler para mostrar logs en consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Ejemplo de uso
if __name__ == "__main__":
    # Inicializar el logger
    logger = setup_logger(log_file_path='logs/aplicacion.log')

    # Ejemplos de mensajes de log
    logger.debug("Este es un mensaje de depuración")
    logger.info("Este es un mensaje informativo")
    logger.warning("Este es un mensaje de advertencia")
    logger.error("Este es un mensaje de error")
    logger.critical("Este es un mensaje crítico")