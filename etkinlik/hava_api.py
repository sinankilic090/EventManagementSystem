import requests
from django.conf import settings

def hava_durumu_kotu_mu(sehir):
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&lang=tr&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()

        hava_durumu = data['weather'][0]['main'].lower()
        print(f"[DEBUG] Hava durumu: {hava_durumu}")

        if 'rain' in hava_durumu or 'storm' in hava_durumu or 'snow' in hava_durumu:
            return True  # Kötü hava
        return False
    except Exception as e:
        print(f"Hata: {e}")
        return False
