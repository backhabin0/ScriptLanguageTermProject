from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import requests
import io
import http.client
from xml.etree import ElementTree

url = "apis.data.go.kr"
query = "/B553662/peakPoiInfoService/getPeakPoiInfoList?serviceKey=fGahpMpOdPXZYI3PiwdkIW%2BXFL6ElAoipUQonJDz7xVIbvq7ZipdgE1jIdrHjVztgXaFZA2AUpuKAqSyS9GtCg%3D%3D&numOfRows=10000&pageNo=1&type=xml"

Google_API_Key = 'AIzaSyCsVH9cdxc_Pm57ucgLNKcDQdFPKnnq0S0'

select_num = 0

g_Tk = Tk()
g_Tk.geometry("800x500")
mapList = []

conn = http.client.HTTPConnection(url)
conn.request("GET", query)
req = conn.getresponse()

mapList.clear()
strXml = req.read().decode('utf-8')

tree = ElementTree.fromstring(strXml)

itemElements = tree.iter("item")  # return list type

for item in itemElements:
    placeNm = item.find("placeNm")
    lat = item.find("lat")  # 위도
    lot = item.find("lot")  # 경도

    placeNm_text = placeNm.text if placeNm is not None else ""
    lat_text = lat.text if lat is not None else ""
    lot_text = lot.text if lot is not None else ""

    mapList.append((placeNm_text, lat_text, lot_text))

print(len(mapList))
print(mapList)
print("\n")
global S_data


def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=230, y=0)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=20, height=18, borderwidth=1,
                            yscrollcommand=ListBoxScrollbar.set)
    unique_data_list = list(set([item[0] for item in mapList]))
    for item in unique_data_list:
        SearchListBox.insert('end', item)
    SearchListBox.pack()
    SearchListBox.place(x=10, y=0)

    ListBoxScrollbar.config(command=SearchListBox.yview)


def InitSearchButton():
    TempFont = font.Font(g_Tk, size=14, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=70, y=450)


def SearchButtonAction():
    global SearchListBox
    global select_num

    iSearchIndex = SearchListBox.curselection()
    if not iSearchIndex:  # 선택된 항목이 없을 경우 함수 종료
        return

    iSearchIndex = iSearchIndex[0]

    select_num = iSearchIndex

    zoom = 13

    seoul_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={mapList[select_num][1]},{mapList[select_num][2]}&zoom={zoom}&size=800x600&maptype=roadmap&key={Google_API_Key}"
    marker_coordinates = [{'lat': mapList[select_num][1], 'lng': mapList[select_num][2]}]
    for coordinates in marker_coordinates:
        marker_url = f"&markers=color:red%7C{coordinates['lat']},{coordinates['lng']}"
        seoul_map_url += marker_url

    response = requests.get(seoul_map_url)
    image = Image.open(io.BytesIO(response.content))
    photo = ImageTk.PhotoImage(image)
    map_label = Label(g_Tk, image=photo)
    map_label.image = photo
    map_label.place(x=200, y=0, width=800, height=600)



InitSearchButton()
InitSearchListBox()
g_Tk.mainloop()
