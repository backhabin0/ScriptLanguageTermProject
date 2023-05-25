from tkinter import *
from tkinter import font
import datetime

g_Tk = Tk()
g_Tk.geometry("1000x600")
DataList = []
url = "openapi.nature.go.kr"
query = "/openapi/service/rest/FungiService/fngsSpcmInfo?ServiceKey=fGahpMpOdPXZYI3PiwdkIW%2BXFL6ElAoipUQonJDz7xVIbvq7ZipdgE1jIdrHjVztgXaFZA2AUpuKAqSyS9GtCg%3D%3D&q1=FB2012112400000141"

# 버섯표본 번호를 적어줘야해용
Q1 = "FB2012112400000141"

# gif 관련 변수에용
frameCnt = 4
frames = [PhotoImage(file='MR.gif', format='gif -index %i' % i).subsample(2) for i in range(frameCnt)]

# 시간 관련
date = datetime.date.today()

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="[버섯도리]")
    MainText.pack()
    MainText.place(x=400)

def InitGif(ind):
    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    g_Tk.after(100, InitGif, ind)

def update_clock():
    now = datetime.datetime.now()
    if(int(now.strftime("%H")) >= 13):
        hour = int(now.strftime("%H")) - 12
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

g_Tk.mainloop()
