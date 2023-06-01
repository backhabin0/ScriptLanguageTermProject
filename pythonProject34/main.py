from tkinter import *
from tkinter import font
import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Toplevel


g_Tk = Tk()
g_Tk.geometry("1000x600")
DataList = []
mrList = []
url = "openapi.nature.go.kr"
S_data=[]
# st는 2번(학명) sw는 e -> 학명에 'e'가 들어가는것 출력
SW = "e"

# 인코딩 된 값을 넣은 query를 넣어요
query = "/openapi/service/rest/FungiService/fngsIlstrSearch?ServiceKey=fGahpMpOdPXZYI3PiwdkIW%2BXFL6ElAoipUQonJDz7xVIbvq7ZipdgE1jIdrHjVztgXaFZA2AUpuKAqSyS9GtCg%3D%3D&st=2&sw="+ SW+"&numOfRows=1000&pageNo=1"

# gif 관련 변수에용
frameCnt_1 = 11
frames_1 = [PhotoImage(file='C_D_mr.gif', format='gif -index %i' % i).subsample(4) for i in range(frameCnt_1)]

frameCnt_2 = 16
frames_2 = [PhotoImage(file='D_mr2.gif', format='gif -index %i' % i).subsample(4) for i in range(frameCnt_2)]

# 시간 관련
date = datetime.date.today()

def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Malgun Gothic')
    MainText = Button(g_Tk, font=TempFont, text="[버섯도리]", command=ShowAllButtonAction)
    MainText.pack()
    MainText.place(x=400)

def InitGif_1(ind):
    frame = frames_1[ind]
    ind += 1
    if ind == frameCnt_1:
        ind = 0
    label_1.configure(image=frame)
    g_Tk.after(100, InitGif_1, ind)

def InitGif_2(ind):
    frame = frames_2[ind]
    ind += 1
    if ind == frameCnt_2:
        ind = 0
    label_2.configure(image=frame)
    g_Tk.after(50, InitGif_2, ind)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=230, y=130)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=20, height=18, borderwidth=1,
                            yscrollcommand=ListBoxScrollbar.set)
    unique_data_list = list(set([item[0] for item in DataList]))
    for item in unique_data_list:
        SearchListBox.insert('end', item)
    SearchListBox.pack()
    SearchListBox.place(x=10, y=130)

    ListBoxScrollbar.config(command=SearchListBox.yview)

def InitSearchButton():
    TempFont= font.Font(g_Tk,size=14,weight='bold',family='Consolas')
    SearchButton=Button(g_Tk,font = TempFont,text="검색",command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=70,y=565)

def SearchButtonAction():
    global S_data
    global SearchListBox

    iSearchIndex = SearchListBox.curselection()
    if not iSearchIndex:  # 선택된 항목이 없을 경우 함수 종료
        return

    iSearchIndex = iSearchIndex[0]
    unique_data_list = list(set([item[0] for item in DataList]))
    M_search = unique_data_list[iSearchIndex][0]

    if S_data:  # 기존에 생성된 Text 위젯이 있을 경우 제거
        S_data.destroy()

    S_data = Text(g_Tk, width=50, height=27, borderwidth=12, relief='flat')
    S_data.pack()
    S_data.place(x=300, y=100)

    for i in range(len(DataList)):
        if DataList[i][0][0] == M_search:
            S_data.insert(INSERT, " 과국명: ")
            S_data.insert(INSERT, DataList[i][0])
            S_data.insert(INSERT, "\n")
            S_data.insert(INSERT, " 국명: ")
            S_data.insert(INSERT, DataList[i][1])
            S_data.insert(INSERT, "\n")
            S_data.insert(INSERT, " 도감번호: ")
            S_data.insert(INSERT, DataList[i][2])
            S_data.insert('end', "\n\n")

def Search():
    import http.client
    conn = http.client.HTTPConnection(url)
    conn.request("GET", query)
    req = conn.getresponse()

    global DataList
    DataList.clear()
    strXml = req.read().decode('utf-8')
    # print(strXml)

    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    global M_search
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

        mrList.append((familyKorNm_text,fngsGnrlNm_text,fngsPilbkNo_text))

    print(len(mrList))
    DataList = mrList
    print(len(DataList))
    print("\n")
    global S_data

    for i in range(len(mrList)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i+1)
        RenderText.insert(INSERT, "]\n")
        RenderText.insert(INSERT, " 과국명: ")
        RenderText.insert(INSERT, mrList[i][0])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, " 국명: ")
        RenderText.insert(INSERT, mrList[i][1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, " 도감번호: ")
        RenderText.insert(INSERT, mrList[i][2])
        RenderText.insert(INSERT, "\n\n")

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=200)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=27, borderwidth=12, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=215)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

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

def search_word():
    word = entry.get()  # 입력된 단어 가져오기
    print(word)

    global S_data

    if S_data:  # 기존에 생성된 Text 위젯이 있을 경우 제거
        S_data.destroy()

    S_data = Text(g_Tk, width=50, height=27, borderwidth=12, relief='flat')
    S_data.pack()
    S_data.place(x=300, y=100)

    for i in range(len(DataList)):
        if word in DataList[i][1]:  # 입력된 단어가 국명 뒤의 내용에 포함되어 있다면
            S_data.insert(INSERT, " 과국명: ")
            S_data.insert(INSERT, DataList[i][0])
            S_data.insert(INSERT, "\n")
            S_data.insert(INSERT, " 국명: ")
            S_data.insert(INSERT, DataList[i][1])
            S_data.insert(INSERT, "\n")
            S_data.insert(INSERT, " 도감번호: ")
            S_data.insert(INSERT, DataList[i][2])
            S_data.insert('end', "\n\n")

def ShowAllButtonAction():
    global g_isSearched

    RenderText = Text(g_Tk, width=50, height=27, borderwidth=12, relief='flat')
    RenderText.pack()
    RenderText.place(x=300, y=100)

    for i in range(len(mrList)):
        RenderText.insert(INSERT, "[")
        RenderText.insert(INSERT, i+1)
        RenderText.insert(INSERT, "]\n")
        RenderText.insert(INSERT, " 과국명: ")
        RenderText.insert(INSERT, mrList[i][0])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, " 국명: ")
        RenderText.insert(INSERT, mrList[i][1])
        RenderText.insert(INSERT, "\n")
        RenderText.insert(INSERT, " 도감번호: ")
        RenderText.insert(INSERT, mrList[i][2])
        RenderText.insert(INSERT, "\n\n")

def toggle_theme():
    if dark_mode_var.get() == 1:
        style = ttk.Style("darkly")
    else:
        style = ttk.Style("minty")

def open_memo_window():
    # 현재 날짜를 문자열로 가져오기
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    def save_memo():
        memo_text = memo_entry.get("1.0", "end-1c")

        file_name = f"Memo_{current_date}.txt"  # 파일 이름 생성

        with open(file_name, "w", encoding="utf-8") as file:
            file.write(memo_text)

        messagebox.showinfo("Memo Saved", "메모가 정상적으로 저장되었습니다.")

    memo_window = Toplevel()
    memo_window.title("Memo")

    memo_label = Label(memo_window, text="Memo_"+current_date)
    memo_label.pack()

    memo_entry = Text(memo_window, width=50, height=10)
    memo_entry.pack()

    save_button = Button(memo_window, text="Save Memo", command=save_memo)
    save_button.pack()

InitTopText()

# gif 부분 입니다
label_1 = Label(g_Tk, bg='white')
label_1.place(x=180, y=61, anchor=CENTER)
g_Tk.after(0, InitGif_1, 0)

label_2 = Label(g_Tk, bg='white')
label_2.place(x=60, y=62, anchor=CENTER)
g_Tk.after(0, InitGif_2, 0)

# 시간 관련 부분입니다
date_label = Label(g_Tk, font=("console", 20))
date_label.pack()

time_label = Label(g_Tk, font=("console", 18))
time_label.pack()

update_clock()
Search()
InitSearchListBox()
InitSearchButton()

# 입력
entry = Entry(g_Tk, width=22, font=('console 20'))
entry.pack()
entry.place(x=300, y=60)

# 검색 버튼
button = Button(g_Tk, text="검색", command=search_word,width=8, height=2)
button.pack()
button.place(x=640, y=60)

# 메모
OpenButton = Button(g_Tk, text="Open Memo",font=('console 20'), command=open_memo_window)
OpenButton.pack()
OpenButton.place(x=770, y=300)

# 다크모드 체크박스 생성
dark_mode_var = IntVar()
dark_mode_checkbox = Checkbutton(g_Tk, text="다크 모드", variable=dark_mode_var, command=toggle_theme)
dark_mode_checkbox.pack()
dark_mode_checkbox.place(x=800,y=400)

toggle_theme()  # 초기 배경 색상 설정



g_Tk.mainloop()