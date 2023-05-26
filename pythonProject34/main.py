from tkinter import *
from tkinter import font
import datetime

g_Tk = Tk()
g_Tk.geometry("1000x600")
DataList = []
url = "openapi.nature.go.kr"

# st는 2번(학명) sw는 e -> 학명에 'e'가 들어가는것 출력
SW = "e"

# 인코딩 된 값을 넣은 query를 넣어요
query = "/openapi/service/rest/FungiService/fngsIlstrSearch?ServiceKey=fGahpMpOdPXZYI3PiwdkIW%2BXFL6ElAoipUQonJDz7xVIbvq7ZipdgE1jIdrHjVztgXaFZA2AUpuKAqSyS9GtCg%3D%3D&st=2&sw="+ SW+"&numOfRows=1000&pageNo=1"

# 버섯표본 번호를 적어줘야해용
Q1 = "FB2012112400000141"

# gif 관련 변수에용
frameCnt_1 = 11
frames_1 = [PhotoImage(file='C_D_mr.gif', format='gif -index %i' % i).subsample(4) for i in range(frameCnt_1)]

# 시간 관련
date = datetime.date.today()

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[버섯도리]")
    MainText.pack()
    MainText.place(x=400)

def InitGif(ind):
    frame = frames_1[ind]
    ind += 1
    if ind == frameCnt_1:
        ind = 0
    label.configure(image=frame)
    g_Tk.after(25, InitGif, ind)

def Search():
    import http.client
    conn = http.client.HTTPConnection(url)
    conn.request("GET", query)
    req = conn.getresponse()

    global DataList
    DataList.clear()

    strXml = req.read().decode('utf-8')
    print(strXml)

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)

    # item 엘리먼트를 가져옵니다.
    itemElements = tree.iter("item") #return list type
    # print(itemElements)


    RenderText = Text(g_Tk, width=50, height=27, borderwidth=12, relief='flat')
    RenderText.pack()
    RenderText.place(x=300,y=100)

    for item in itemElements:
        familyKorNm = item.find("familyKorNm")
        fngsGnrlNm = item.find("fngsGnrlNm")
        fngsPilbkNo = item.find("fngsPilbkNo")

        familyKorNm_text = familyKorNm.text if familyKorNm is not None else ""
        fngsGnrlNm_text = fngsGnrlNm.text if fngsGnrlNm is not None else ""
        fngsPilbkNo_text = fngsPilbkNo.text if fngsPilbkNo is not None else ""

        DataList.append((familyKorNm_text,fngsGnrlNm_text,fngsPilbkNo_text))

    print(len(DataList))
    for i in range(len(DataList)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i+1)
        RenderText.insert(INSERT, "]\n")
        RenderText.insert(INSERT, " 과국명: ")
        RenderText.insert(INSERT, DataList[i][0])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, " 국명: ")
        RenderText.insert(INSERT, DataList[i][1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, " 도감번호: ")
        RenderText.insert(INSERT, DataList[i][2])
        RenderText.insert(INSERT, "\n\n")

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

def update_clock():
    now = datetime.datetime.now()
    if(int(now.strftime("%H")) >= 13):
        hour = int(now.strftime("%H")) - 12
        hour=str(hour)
        current_time = now.strftime("오후 "+hour+":%M")
    else:
        current_time = now.strftime("오전 %H:%M")
    current_date = now.strftime("%Y년 %m월 %d일")
    time_label.config(text=current_time)
    date_label.config(text=current_date)
    g_Tk.after(1000, update_clock)
    date_label.place(x=750,y=500)
    time_label.place(x=800,y=550)

InitTopText()

# gif 부분 입니다
label = Label(g_Tk, bg='white')
label.place(x=50, y=50, anchor=CENTER)
g_Tk.after(0, InitGif, 0)

# 시간 관련 부분입니다
date_label = Label(g_Tk, font=("Arial", 20))
date_label.pack()

time_label = Label(g_Tk, font=("Arial", 18))
time_label.pack()

update_clock()
Search()
g_Tk.mainloop()
