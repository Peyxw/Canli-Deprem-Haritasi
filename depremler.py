
import folium
import pandas as pd
import time
import      requests
import geopandas as gpd
import os
import webbrowser


# Son bir saatteki depremi oku
url_1saat = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson'
url_1gün = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson'
url_7gün = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_week.geojson'
url_30gün = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson'
url_tarih = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minlatitude=3&minlongitude=37&maxlatitude=63&maxlongitude=98&starttime=2023-01-01'
r = requests.get(url_tarih)
data = r.json()
# json'daki kayıt sayısını alma
count = data["metadata"]["count"]

# araç ipucu metni

# tüm json kayıtlarını yineleme
for i in range(0, count-1):
    title = data["features"][i]["properties"]["title"]
    if title.find("Turkey") != -1:
        

        # büyüklüğü al, en yakın sayıya yuvarla ve int'e dönüştür
        mag = int(round(data["features"][i]["properties"]["mag"], 0))

        # zamanı okunabilir biçime dönüştürün
        event_time = time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime(round(data["features"][i]["properties"]["time"]/1000, 10))
                    )
        # Açılır pencereler için html formatı
        
        # json verilerinden boylam ve enlem alın
        lon = data["features"][i]["geometry"]["coordinates"][0]
        lat = data["features"][i]["geometry"]["coordinates"][1]

      
       
        

        print(title,event_time,mag)
       
        Func = open("Site/depremler.html","a+")
        
        Func.write(str(title)+str(mag)+str(event_time)+"\n"+ "<br>") 
        Func.close()

print('Çalışıyor')
time.sleep(120.0)
os.remove("Site/depremler.html")
os.system('depremler.py')
  