from tkinter import *
from tkinter import font
from tkinter import ttk
import tkinter.messagebox
import urllib.request
from xml.etree import ElementTree

window = Tk()
window.geometry("550x500+500+100")
window.title("BoxOfficeAPP")
class BoxOffice:

    def __init__(self):
        # 디폴트
        self.key = 'cc9ca60cb93325b462af073b160ff2dd'
        self.url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key='
        self.area_list_dict = {'전체': '', '서울': '0105001', '경기도': '0105002', '강원도': '0105003',
                               '충청북도': '0105004', '충청남도': '0105005', '경상북도': '0105006', '경상남도': '0105007',
                               '전라북도': '0105008', '전라남도': '0105009', '제주도': '0105010', '부산': '0105011',
                               '대구': '0105012', '대전': '0105013', '울산': '0105014', '인천': '0105015', '광주': '0105016'}
        self.country_list_dict = {'전체': '', '한국':'K','외국':'F'}
        # 메인
        self.MainFont = font.Font(window, size=20, weight='bold', family='Consolas')
        self.MainText = Label(window, font=self.MainFont, text="[일별 박스오피스 검색]")
        self.MainText.pack()
        self.MainText.place(x=133)
        # 공통
        self._font = font.Font(window, size=15, weight='bold', family='Consolas')
        self.root = None
        self.data = None
        self.openDt = None
        self.scrnCnt = None
        self.rank = None
        self.audiAcc = None
        self.movieNm = None
        # 날짜
        self.date_label = None
        self.date = None
        self.date_button = None
        self.targetDt = ''
        # 지역
        self.area_list = None
        self.area_button = None
        self.area = None
        self.area_button = None
        self.area_code = None
        self.item_elements = None
        # 국가
        self.country = None
        self.country_button = None
        self.country_code = None
        self.country_list = None
        # 텍스트박스
        self.frame = None
        self.scrollbar = None
        self.text_box = None

    def date_input_label(self):
        self.date = Label(window, text='날짜입력(YYYYMMDD)', font=self._font)
        self.date_label = Entry(window, font=self._font, width=15, borderwidth=12, relief='ridge')
        self.date_label.pack()
        self.date.place(x=40, y=50)
        self.date_label.place(x=240, y=40)
        self.date_button = Button(window, text="검색", font=self._font, command=self.date_result)
        self.date_button.pack()
        self.date_button.place(x=440, y=45)

    def area_input_label(self):
        self.area_list = ttk.Combobox(window, width=15, height=50, state='readonly')
        self.area_list['values'] = ('전체', '서울', '경기도', '강원도', '충청북도', '충청남도', '경상북도', '경상남도', '전라북도',
                                '전라남도', '제주도', '부산', '대구', '대전', '울산', '인천', '광주')
        self.area_list.pack()
        self.area_list.place(x=130, y=105)
        self.area_list.current(0)       # 디폴트로 보이게 하는 위치.(인덱스번호로) 0->전체
        # 지역선택 text 생성
        self.area = Label(window, text="지역선택", font=self._font)
        self.area.pack()
        self.area.place(x=40, y=100.5)
        # 버튼생성
        self.area_button = Button(window, text="검색", command=self.area_result)
        self.area_button.pack()
        self.area_button.place(x=260, y=100.5)

    def country_input_label(self):
        self.country_list = ttk.Combobox(window, width=15, height=50, state='readonly')
        self.country_list['values'] = ('전체', '한국', '외국')
        self.country_list.pack()
        self.country_list.place(x=130, y=130)
        self.country_list.current(0)
        # 지역선택 text 생성
        self.country = Label(window, text="국가선택", font=self._font)
        self.country.pack()
        self.country.place(x=40, y=126)
        # 버튼생성
        self.country_button = Button(window, text="검색", command=self.country_result)
        self.country_button.pack()
        self.country_button.place(x=260, y=126)


    def render_text_box(self):
        self.frame = Frame(window)
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side='right', fill='y')
        self.text_box = Text(self.frame, width=40, height=20, borderwidth=12, relief='ridge',
                             yscrollcommand=self.scrollbar.set)
        self.text_box.pack()
        self.scrollbar.config(command=self.text_box.yview)
        self.frame.pack()
        self.frame.place(x=220, y=200)
        self.text_box.configure(state='disabled')
        pass

    def date_result(self):
        self.targetDt = self.date_label.get()
        if self.targetDt >= "20040103":
            self.area_input_label()
            self.country_input_label()
        else:
            tkinter.messagebox.showerror("warning", "날짜를 다시 입력하세요")


    def area_result(self):
        self.area_code = self.area_list_dict[self.area_list.get()]
        self.url = self.url + self.key + '&targetDt=' + self.targetDt + '&wideAreaCd=' + self.area_code
        self.text_box.configure(state='normal')
        self.text_box.delete(0.0, END)
        print(self.url)
        self.data = urllib.request.urlopen(self.url).read()
        self.root = ElementTree.fromstring(self.data)
        self.item_elements = self.root.getiterator("dailyBoxOffice")
        self.display_result()
        self.text_box.configure(state='disabled')
        self.country_list.current(0)        # 지역검색 결과보여줄때는 국가검색 디폴트로 전체 가리키게
        self.url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key='

    def country_result(self):
        self.area_code = self.area_list_dict[self.area_list.get()]
        self.country_code = self.country_list_dict[self.country_list.get()]
        self.url = self.url + self.key + '&targetDt=' + self.targetDt + '&wideAreaCd=' + self.area_code+'&repNationCd='+self.country_code
        self.text_box.configure(state='normal')
        self.text_box.delete(0.0, END)
        print(self.url)
        self.data = urllib.request.urlopen(self.url).read()
        self.root = ElementTree.fromstring(self.data)
        self.item_elements = self.root.getiterator("dailyBoxOffice")
        self.display_result()
        self.text_box.configure(state='disabled')

        self.url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key='

    def display_result(self):
        for child in self.item_elements:
            self.rank = child.find('rank').text
            self.openDt = child.find('openDt').text
            self.movieNm = child.find('movieNm').text
            self.audiAcc = child.find('audiAcc').text

            self.text_box.insert(INSERT, '순위 = ' + self.rank + '\n개봉날짜 = ' + self.openDt + '\n영화이름 = '
                                 + self.movieNm + '\n총 관객수 = ' + self.audiAcc)
            self.text_box.insert(INSERT, '\n')
            self.text_box.insert(INSERT, '========================================')
            self.text_box.insert(INSERT, '\n')

    def __del__(self):
        pass

box = BoxOffice()
box.date_input_label()
box.render_text_box()
window.mainloop()