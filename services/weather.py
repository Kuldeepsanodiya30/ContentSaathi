import requests


def get_weather(city="Parbhani"):
    url = "https://wttr.in/{}?format=j1".format(city)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        weather = current["weatherDesc"][0]["value"]

        return {
            "weather": weather,
            "temperature": int(temperature)
        }

    except Exception as e:
        print("Weather error:", e)

        return {
            "weather": "Unknown",
            "temperature": None
        }


# Test
if __name__ == "__main__":
    weather = get_weather("Parbhani")

    print("Weather:", weather["weather"])
    print("Temperature:", weather["temperature"], "°C")