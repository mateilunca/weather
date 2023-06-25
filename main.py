import json
import time

import requests
from json.decoder import JSONDecodeError
from plyer import notification


# citim de la tastatura un oras si sa ne dea temp curenta
# starea curenta vantul si directia vantului
# si presiunea atmosferica
# notificare windows
# daca ploua bine inchidem geamurile strangem rufele


def test_func():
    pass

def get_weather(url, city, auth):
    try:
        headers = {"key": auth}
        response = requests.get(url=url+f"?q={city}", headers=headers)

        if response.status_code == 200:
            response_dict = response.json()
            weather_info = response_dict["current"]
            return weather_info


        else:
            return f"Error: {response.text} with code {response.status_code}"

    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return f"Requestion exception: {e}"
    except Exception as e:
        return f"Exception has occured {e}"


def send_alerts(config, weather: dict):
    for city, v in weather.items():
        notification_alert = []
        if v["temp_c"] > config["max_temp"]:
            notification_alert.append(f"Temperatura este f mare: {v['temp_c']} ")
        if v["wind_kph"] > config["max_wind_velocity"]:
            notification_alert.append(f"Viteza vantului este f mare : {v['wind_kph']} ")
        if v["pressure_mb"] > config["max_pressure"]:
            notification_alert.append(f"Presiunea atmosferica este f mare: {v['pressure_mb']} ")

        print(f"City: {city}\n" + "\n".join(notification_alert))

        if notification_alert:
            notification.notify(
                title=city,
                message=" ".join(notification_alert),
                app_icon=None,
                timeout=10,
            )
        time.sleep(4)





def init_config():

    try:
        with open("config.json", "r") as f:
            config = json.loads(f.read())
        return config
    except JSONDecodeError as e:
        print(f"Exception raised because json file is not valid: {e}")
        exit()
    except FileNotFoundError as e:
        print(f"Nu avem fisierul de config {e}")
        exit()
    except PermissionError as e:
        print(f"Nu ai permisiunea sa citesti fisierul de configurea. {e}")
    except Exception as e:
        print(f"Unknown Exception {e}")
        exit()



if __name__ == "__main__":
    print("Started script here")
    config = init_config()
    weather = {}
    while True:
        city = input("Scrie orasul despre care vrei sa afli informatii. Scrie N pt exit: ")
        if city.lower() == "n":
            break
        weather[city] = get_weather(config["base_url"], city, auth=config["api_key"])

    send_alerts(config, weather)