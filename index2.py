
import folium
import pandas as pd
import time
import requests
import geopandas as gpd
import os
import keyboard



 #Renk Listeli
renklistesi = {
    1: '#ffffff',
    2: '#bfccff',
    3: '#99f',
    4: '#8ff',
    5: '#7df894',
    6: '#ff0',
    7: '#fd0',
    8: '#ff9100',
    9: '#f00'
    }
cur_dir = os.path.dirname(os.path.realpath(__file__))
harita = folium.Map(location=[38.9637, 35.2433], zoom_start=5)
# Şekil Dosyalarını okuyoruz
Mikro_Levhalar_ve_Büyük_Fay_Bölgeleri = gpd.read_file(cur_dir + '/data/mygeodata/plate-boundaries/shp/Micro_Plates_and_Major_Fault_Zones-line.shp')
Plaka_Arayüzü = gpd.read_file(cur_dir + '/data/mygeodata/plate-boundaries/shp/Plate_Interface-line.shp')
Plaka_Hareketi = gpd.read_file(cur_dir + '/data/mygeodata/plate-boundaries/shp/Plate_Motion-point.shp')
# haritaya katmanlar halinde eklenecek özellik grupları oluşturma
fg_mlbfb = folium.FeatureGroup('Mikro Levhalar ve Büyük Fay Bölgeleri')
fg_pa = folium.FeatureGroup('Plaka Arayüzü')
fg_ph = folium.FeatureGroup('Plaka Hareketi')
fg_dv = folium.FeatureGroup('Deprem Verileri')
# özellik grubuna mikro plakalar ve ana fay bölgeleri verilerinin eklenmesi
folium.Choropleth(
    geo_data=Mikro_Levhalar_ve_Büyük_Fay_Bölgeleri,
    line_color='red',
    line_weight=2,
    line_opacity=1,
    highlight=True
).add_to(fg_mlbfb)
# Özellik grubuna plaka arayüzü verilerinin eklenmesi
folium.Choropleth(
    geo_data=Plaka_Arayüzü,
    line_color='red',
    line_weight=2,
    line_opacity=1,
    highlight=True
).add_to(fg_pa)
# Özellik grubuna plaka hareket verilerinin eklenmesi
folium.GeoJson(Plaka_Hareketi).add_to(fg_ph)
# Katmanları eklemek
fg_mlbfb.add_to(harita)
fg_pa.add_to(harita)
fg_ph.add_to(harita)
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
tooltip = 'Daha Vazla Bilgi'
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
        popup = f"""<div><strong>Yer : </strong>{data["features"][i]["properties"]["place"]}</div>
                    <div>
                        <strong>Büyüklük : </strong>
                        <div style="background-color:{renklistesi.get(mag)}">
                            {data["features"][i]["properties"]["mag"]}
                        </div>
                    </div>
                    <div><strong>Tarih : </strong>{event_time}</div>
                    <div><strong>Tip : </strong>{data["features"][i]["properties"]["type"]}</div>
                """
        # json verilerinden boylam ve enlem alın
        lon = data["features"][i]["geometry"]["coordinates"][0]
        lat = data["features"][i]["geometry"]["coordinates"][1]

        # Özellik grubuna bir çevre ekleyin
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            tooltip=tooltip,
            popup=folium.Popup(popup, max_width=1000),
            color=renklistesi.get(mag),
            fill=True,
            fill_color=renklistesi.get(mag)

        ).add_to(harita)
        print(title,event_time,mag)
          
# haritaya özellik grubu ekle
fg_dv.add_to(harita)
# haritaya katman ekle
folium.LayerControl().add_to(harita)
# HTML dosyamıza kayıt ediyoruz
harita.save('Site/harita.html')

#while True: 
#if keyboard.read_key() == "e":
#os.system('index2.py')
print('Çalışıyor')
time.sleep(60.0)
os.system('index2.py')
  