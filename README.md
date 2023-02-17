
# itob-test-assignment

Тестовое задание для ITOB
## Как запустить сервер

Склонируйте репозиторий

```bash
  git clone https://github.com/exxentriq/itob-test-assignment
```

Перейдите в папку с репозиторием на диске

```bash
  cd itob-test-assignment
```

Создайте виртуальную среду и установите все необходимые пакеты (для Linux)

```bash
  python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
```

Создайте виртуальную среду и установите все необходимые пакеты (для Windows)

```bash
  py -3 -m venv venv && venv\Scripts\activate && pip install -r requirements.txt
```

Запустите сервер

```bash
  flask --app app run
```

Сервер будет доступен по адресу

```bash
  127.0.0.1:5000
```
## Справка по API

#### Налить воды в чайник

```
  POST /api/fillKettle?water_level={water_level}&water_temperature={water_temperature}
```

| Параметр | Тип     | Описание                |
| :-------- | :------- | :------------------------- |
| `water_level` | `float` | **Необходимый параметр.** Количество воды в литрах |
| `water_temperature` | `float` | **Необходимый параметр.** Температура воды в Цельсиях |

#### Включить чайник

```
  POST /api/turnOnKettle
```

#### Выключить чайник

```
  POST /api/turnOffKettle
```

#### Получить все записи из базы данных

```
  GET /api/getKettleInfo
```

#### Получить последнюю запись из базы данных

```
  GET /api/getLastDatabaseRecord
```

## Пример использования

Запрос

```
  POST 127.0.0.1:5000/api/fillKettle?water_level=0.5&water_temperature=20.0
```

Ответ сервера

```json
{
    "message": "The kettle water level has been set to 0.5 and water temperature to 20.0."
}
```

Запрос

```
  GET 127.0.0.1:5000/api/getLastDatabaseRecord
```

Ответ сервера

```json
{
    "id": 64,
    "kettle_state": "ON",
    "message": "TEMPERATURE: Water temperature is 70.0°C.",
    "time": 1676634660,
    "water_level_liters": 0.5,
    "water_temperature_celsius": 70.0
}
```