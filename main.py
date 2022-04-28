import smtplib

import requests
from datetime import datetime
import time

YOUR_EMAIL_HERE = "example@gmail.com"
YOUR_PASSWORD_HERE = "examplePassword"

parameters = {
    "lat": 45.421532,
    "lng": -75.697189,
    "formatted": 0,
}


def iss_position_overhead():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    data = iss_response.json()["iss_position"]
    longitude = float(data["longitude"])
    latitude = float(data["latitude"])
    iss_position = (longitude, latitude)
    if iss_position[0] <= 50 or iss_position[0] >= 40 and -70 >= iss_position[1] >= -80:
        return True
    else:
        return False


def check_sun_status():
    sun_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    sun_response.raise_for_status()
    data = sun_response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    current_time = datetime.now()
    if sunrise >= current_time.hour >= sunset:
        return True
    else:
        return False


while True:
    if iss_position_overhead() and check_sun_status():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=YOUR_EMAIL_HERE, password=YOUR_PASSWORD_HERE)
        connection.sendmail(
            from_addr=YOUR_EMAIL_HERE,
            to_addrs=YOUR_EMAIL_HERE,
            msg="ISS Status\n\nLook up! The ISS is currently above you :)"
        )
    time.sleep(30)
