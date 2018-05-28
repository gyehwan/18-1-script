import urllib.request
from xml.etree import ElementTree


key = "cc9ca60cb93325b462af073b160ff2dd"
loopFlag = 1

def printMenu():
    print("*************************************************")
    print("                일별 박스오피스 검색               ")
    print("*************************************************")


def areaChoice():

    rcode = int(input("서울(1), 경기도(2), 강원도(3), 충청북도(4)\n충청남도(5), 경상북도(6), 경상남도(7), 전라북도(8)\n전라남도(9)"
                  "제주도(10), 부산(11), 대구(12)\n대전(13), 울산(14), 인천(15), 광주(16)\n 지역을 선택하세요:"))
    area = int('0105000')
    area += rcode
    return '0' + str(area)

def printInformation(url):

    data = urllib.request.urlopen(url).read()
    root = ElementTree.fromstring(data)
    for child in root.iter("dailyBoxOffice"):
        rank = child.find('rank').text
        openDt = child.find('openDt').text
        movieNm = child.find('movieNm').text
        audiAcc = child.find('audiAcc').text
        scrnCnt = child.find('scrnCnt').text

        print('순위 = ' + rank +
              '\n개봉일 = ' + openDt + '\n영화이름 = ' + movieNm + '\n총 관객수 = ' + audiAcc +
              "\n상영한 스크린 수 = " + scrnCnt)
        print('=================================================')

def koreaAndWorld(menu, area, num):
    global key
    if num == 1:
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key='\
              + key + '&targetDt=' + menu + '&wideAreaCd=' + area + '&repNationCd=K'
        printInformation(url)
    if num == 2:
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key='\
              + key + '&targetDt=' + menu + '&wideAreaCd=' + area + '&repNationCd=F'
        printInformation(url)
    if num == 3:
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key='\
              + key + '&targetDt=' + menu + '&wideAreaCd=' + area
        printInformation(url)

def Search(menu):
    global key, loopFlag

    print("지역별 검색 : a")
    print("전체지역 검색 : d")
    choice = str(input("Menu choice:"))
    if choice == 'a':
        areaCode = areaChoice()
        select = str(input("한국영화 검색 : k\n외국영화검색 : w\n전체영화검색 : d\nMenu choice:"))
        if select == 'k':
            koreaAndWorld(menu, areaCode, 1)  # menu = 날짜.
        elif select == 'w':
            koreaAndWorld(menu, areaCode, 2)
        elif select == 'd':
            koreaAndWorld(menu, areaCode, 3)

    elif choice == 'd':
        areaCode= '0105000000'
        select = str(input("한국영화 검색 : k\n외국영화검색 : w\n전체영화검색 : d\nMenu choice:"))
        if select == 'k':
            koreaAndWorld(menu, areaCode, 1)
        elif select == 'w':
            koreaAndWorld(menu, areaCode, 2)
        elif select == 'd':
            koreaAndWorld(menu, areaCode, 3)

    else:
        print("없는 메뉴입니다 다시 고르세요")
        Search(menu)

##### run #####
while (loopFlag > 0):
    printMenu()
    menuKey = input('검색하고자 하는 날짜를 입력하세요(종료를 원하면 q,YYYYMMDD) : ')
    if menuKey != 'q':
        Search(menuKey)
    else:
        loopFlag = 0
else:
    print("Thank you! Good Bye")

