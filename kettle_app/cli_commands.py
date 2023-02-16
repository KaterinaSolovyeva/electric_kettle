import click
import logging.config
import time

from kettle_app import app, db
from settings import Config, LOGGING_CONFIG
from .models import Kettle


logging.config.dictConfig(LOGGING_CONFIG)


@app.cli.command('start')
def load_opinions_command():
    """Функция запуска чайника."""
    click.echo('Для остановки чайника нажмите клавиши: CTRL+C')
    try:
        temperature = Config.BASE_TEMPERATURE
        kettle = Kettle()
        answer = 'empty'
        while answer not in ['да', 'нет']:
            answer = input('Налить воды в чайник? Напишите ответ да или нет: ')
            if answer == 'да':
                water_quantity = input(
                    f'Выберите количество воды от 0 до {Config.MAX_WATER_QUANTITY}: '
                )
                while water_quantity:
                    try:
                        water_quantity = float(water_quantity)
                        break
                    except ValueError:
                        water_quantity = input(
                            f'Напишите число от 0 до {Config.MAX_WATER_QUANTITY}: '
                        )
                if 0 < water_quantity <= Config.MAX_WATER_QUANTITY:
                    logging.info(f'В чайнике теперь {water_quantity} литров.')
                    data = {
                        'water_quantity': water_quantity,
                        'state': 'вкл',
                        'temperature': temperature
                    }
                    kettle.boiling(data)
                    db.session.add(kettle)
                    db.session.commit()

                    increase = kettle.calculate_increase_temperature_in_sec()
                    while temperature < Config.SHUTDOWN_TEMPERATURE:
                        temperature += increase
                        logging.info(f'Температура воды в чайнике {temperature}')
                        kettle.temperature = int(temperature)
                        db.session.commit()
                        time.sleep(1)
                    logging.info('Чайник кипит.')
                    kettle.state = 'вскипел'
                    db.session.commit()

                    time.sleep(Config.BOILING_TIME)
                    kettle.state = 'выкл'
                    db.session.commit()
                    logging.info('Чайник выключен')

                elif water_quantity == 0:
                    logging.info('Чайник всё ещё пуст.')
                else:
                    logging.info('В чайнике может быть не больше 1 литра воды.')
            elif answer == 'нет':
                logging.info('Пустой чайник включать не безопасно. Чайник выключен.')

    except KeyboardInterrupt:
        kettle.state = 'остановлен'
        db.session.commit()
        logging.info('Чайник остановлен.')
