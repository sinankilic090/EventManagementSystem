import requests

def hava_durumu_kontrol(sehir):
    api_key = "afa03e98558cf6f0ab22f9f4a1f92cda"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"

    response = requests.get(url)
    if response.status_code == 200:
        veri = response.json()
        print(f"Hava durumu: {veri['weather'][0]['description']}")
        return veri['weather'][0]['main'].lower()
    else:
        print("API çağrısı başarısız:", response.status_code)
        return None

if __name__ == "__main__":
    sehir = "Karabük"
    durum = hava_durumu_kontrol(sehir)
    if durum and "rain" in durum:
        print("Etkinlik iptal olabilir.")
    else:
        print("Etkinlik devam ediyor.")
