import logging
import coloredlogs

def setup_logging():
    logger = logging.getLogger('AnimeBot :')

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Configuration de coloredlogs
    coloredlogs.install(
        level='INFO',  # Niveau de log
        logger=logger,  # Logger à utiliser
        fmt='%(asctime)s %(levelname)s     %(name)s %(message)s',  # Format du message
        datefmt='%Y-%m-%d %H:%M:%S',  # Format de la date
        field_styles={
            'asctime': {'color': 'black', 'bold': True},
            'levelname': {'color': 'black', 'bold': True},
            'name': {'color': 'blue'}
        },
        level_styles={
            'debug': {'color': 'cyan'},
            'info': {'color': 'white'},
            'warning': {'color': 'yellow'},
            'error': {'color': 'red'},
            'critical': {'color': 'red', 'bold': True}
        }
    )

def get_logger(name='AnimeBot :'):
    return logging.getLogger(name)