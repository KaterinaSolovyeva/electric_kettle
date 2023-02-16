from kettle_app import db
from settings import Config


class Kettle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    water_quantity = db.Column(db.Float, default=0, nullable=True)
    state = db.Column(db.String(60), default='выкл')
    temperature = db.Column(db.Integer, default=Config.BASE_TEMPERATURE)

    def boiling(self, data):
        "Изменение параметров модели чайника при его включении."
        for field in ['water_quantity', 'state', 'temperature']:
            if field in data:
                setattr(self, field, data[field])

    def calculate_increase_temperature_in_sec(self):
        """Рассчет времени закипания воды в чайнике.
        Мощность чайника, потраченная для нагрева воды = потребляемая мощность * 0,84
        Количество тепла, требующегося для нагревания воды до температуры кипения =
        масса воды * 4200 * (100 - начальная температура)
        Время нагрева =
        Количество тепла, требующегося для нагревания воды до температуры кипения /
        Мощность чайника, потраченная для нагрева воды
        return: на сколько градусов увеличивается температура воды за секунду
        """
        heat_quantity = (self.water_quantity * 4200 * (100 - self.temperature))/1000
        spent_kettle_power = Config.KETTLE_POWER * 0.84
        boiling_time = int(heat_quantity / spent_kettle_power)
        increase_temperature_in_sec = (100 - self.temperature) / boiling_time
        return increase_temperature_in_sec
