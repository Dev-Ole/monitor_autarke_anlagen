import json
import datetime
import urllib.request

def ConvertSpeed(speed):
	speed = speed * 3.6  # m/s in km/
	speed = round(speed,1)
	#speed = str(speed)
	return speed

def ConvertTime(time):
	"""Zeitstempel formatieren"""
	converted_time = datetime.datetime.fromtimestamp(
		int(time)
	).strftime('%H:%M')
	return converted_time

def url_builder():
	"""URL von Openweathermap erzeugen.
	Es werden Daten der Tagesprognose und Vorhersage benötigt.
	Daten übergeben an data_fetch Funktion"""
	user_api = "YOUR-API-HERE"
	city_id = "Berlin,de"
	unit = "metric"  # Fahrenheit = imperial, Celsius = metric, Kelvin = default.
	# Für Koordinaten api.openweathermap.org/data/2.5/weather?lat=35&lon=139
	api_current = "http://api.openweathermap.org/data/2.5/weather?q="
	api_forecast = "http://api.openweathermap.org/data/2.5/forecast?q="
	# City ID hier: http://bulk.openweathermap.org/sample/city.list.json.gz

	api_url_current = api_current + str(city_id) + "&mode=json&units=" + unit + "&APPID=" + user_api
	api_url_forecast = api_forecast + str(city_id) + "&mode=json&units=" + unit + "&APPID=" + user_api + "&cnt=3"
	full_api_url = (api_url_current, api_url_forecast)
	return full_api_url


def data_fetch(full_api_url):
	"""Daten aus URL abfrufen in UTF-8 dekodieren
	und an data_organizer übergeben"""
	#Current Weather
	current_url = urllib.request.urlopen(full_api_url[0])
	current_output = current_url.read().decode("utf-8")
	current_data = json.loads(current_output)
	current_url.close()

	#forecast Weather
	forecast_url = urllib.request.urlopen(full_api_url[1])
	forecast_output = forecast_url.read().decode("utf-8")
	forecast_data = json.loads(forecast_output)
	forecast_url.close()
	weatherData = (current_data, forecast_data)
	return weatherData


def data_organizer(weatherData):
	"""Wetterdaten aus JSON Liste formatieren
	und an einzelne Variablen übergeben.
	"""
	global daytime
	global temp
	global temp_min
	global temp_max
	global humidity
	global pressure
	global wind
	global condition
	global sunrise
	global sunset
	global city
	temp = []
	temp_min = []
	temp_max = []
	humidity = []
	clouds = []
	condition =[]
	pressure = []
	wind = []

	daytime = ConvertTime(weatherData[0].get("dt"))
	sunrise = ConvertTime(weatherData[0].get("sys").get("sunrise"))
	sunset = ConvertTime(weatherData[0].get("sys").get("sunset"))
	city = weatherData[1].get("city").get("name")

	for forecast in weatherData[1].get("list"):
		temp.append(forecast.get("main").get("temp"))
		temp_min.append(forecast.get("main").get("temp_min"))
		temp_max.append(forecast.get("main").get("temp_max"))
		humidity.append(forecast.get("main").get("humidity"))
		pressure.append(forecast.get("main").get("pressure"))
		condition.append(forecast.get("weather")[0].get("id"))
		wind.append(ConvertSpeed(forecast.get("wind").get("speed")))


	print("---------------------------------------")
	print("Letzter Stand: {}".format(daytime))
	print("Temp: {}".format(temp[0]))
	print("Temp: {}".format(temp[1]))
	print("Temp: {}".format(temp[2]))
	print("Max: {}, Min: {}".format(temp_max[0], temp_min[0]))
	print("Max: {}, Min: {}".format(temp_max[1], temp_min[1]))
	print("Max: {}, Min: {}".format(temp_max[2], temp_min[2]))
	print("Humidity: {}".format(humidity[0]))
	print("ID1: {}".format(condition[0]))
	print("ID2: {}".format(condition[1]))
	print("ID3: {}".format(condition[2]))
	# print("sky: {}".format(sky[0]))
	# print("sky: {}".format(sky[1]))
	# print("sky: {}".format(sky[2]))
	# print("Pressure: {}".format(pressure[0]))
	print("Wind: {} km/h".format(wind[0]))
	print("City: {}".format(city))
	print("---------------------------------------")


if __name__ == "__main__":
	try:
		data_organizer(data_fetch(url_builder()))
	except IOError:
		print("no internet")
