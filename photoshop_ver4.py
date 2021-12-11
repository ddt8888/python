# 미니 포토샵 프로젝트
# 포토샵과 같은 소프트웨어를 '영상처리(Image Processing) 프로그램' 이라 함
# 원칙적으로 영상처리에 대한 이론과 알고리즘을 익힌 후 미니 포토샵 프로그램을 작성하면 좋음
# 현실적으로 이론을 배제하고 화면에 구현되는 것 위주로 진행

# 주의 사항1. 이미지 파일명이나 저장된 경로에 한글이 들어가면 안됨
# 주의 사항2. 이미지 크기는 가로와 세로가 동일해야 함
# 주의 사항3. 처리하는 속도가 다소 오래 걸림

# 사용할 라이브러리 또는 모듈을 임포트


# 윈도우 프로그래밍을 하기 위한 모듈
from tkinter import *

# 파일 입출력을 위한 모듈
from tkinter.filedialog import *

# 숫자나 문자를 입력 받기 위한 모듈
from tkinter.simpledialog import *

# 설치한 이미지 처리 기능을 제공하는 이미지매직의 라이브러리 임포트
# GIF, PNG 뿐 아니라 JPG 같은 이미지를 모두 처리하기 위해 외부 라이브러리 이미지 매직 사용
from wand.image import *


# 모든 함수들이  공통적으로 사용할 전역 변수 선언부
window, canvas, paper = None, None, None
photo, photo2, readFp = None, None, None  # photo는 처음 불러들인 원본 이미지, photo2는 처리 결과를 저장할 변수
oriX, oriY = 0, 0  # 원본 이미지의 폭과 높이를 저장하는 함수

# alkdsjf
# 함수 정의 부분
# 이미지를 화면상에 출력하는 사용자 정의 함수 선언
def displayImage(img, width, height):
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY
    # 이전 캔버스가 존재한다면 이전 캔버스를 삭제하여 기존에 이미지가 출력된 캔버스를 깨끗하게 처리
    if canvas != None:
        canvas.destroy()

    # 새 캔버스 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    canvas = Canvas(window, width=width, height=height)

    # 새 캔버스에 붙일 종이(paper) 생성, 처리된 이미지의 가로 세로 사이즈대로 생성
    # 새 종이는 다양한 이미지 파일 포맷이 아닌 단순히 빈 이미지를 보여줄 것이라 PhotoImage()로 생성
    paper = PhotoImage(width=width, height=height)

    # 새 캔버스에 종이(paper)를 붙임 ( 차후 그 종이 위에 처리된 이미지를 출력)
    # 생성될 위치는 가로 세로의 사이즈의 중간 위치
    canvas.create_image((width/2, height/2), image=paper, state="normal")

    blob = img.make_blob(format='RGB')  # 이미지를 바이너리 코드로 변환해주는 함수, 배열의 형태로 저장
    # print(type(blob)) # blob 자료형 출력 테스트, blob 의 자료형은 bytes 로 리스트형태의 문자열 데이터타입
    # print(blob)
    # print(blob[0],blob[1],blob[2],blob[3],blob[4],blob[5]) # blob 리스트 값 출력 테스트

    # 이미지의 폭과 높이만큼 반복해서 픽셀의 RGB 값을 추출
    for i in range(0, width):
        for k in range(0, height):
            # blob[0],blob[3],blob[6],blob[9]...의 값을 r에 저장
            r = blob[(i*3*width)+(k*3) + 0]
            # blob[1],blob[4],blob[7],blob[10], 의 값을 g에 저장
            g = blob[(i*3*width)+(k*3) + 1]
            # blob[2],blob[5],blob[8],blob[11]의 값을 g에 저장
            b = blob[(i*3*width)+(k*3) + 2]
            # paper에 칼라로 점을 찍어줌, 세로로 높이만큼 찍고 가로를 너비만큼 반복
            # r,g,b값 을 (02x)에 의해 각각 두자리 16진수로 변환하여 rgb 값으로 결합한 후 (k,i)에 찍어줌
            paper.put("#%02x%02x%02x" % (r, g, b), (k, i))
            # print(r,g,b)  # r,g,b값 출력 테스트
            # print("#%02x%02x%02x, (%d, %d)" % (r,g,b, k,i)) # r,g,b값 을 16진수로 변환 결과 출력 테스트
    # 처리된 결과 이미지의 픽셀을 찍어둔 종이paper가 붙여있는 캔버스를 화면에 출력

    # canvas.pack()
    # 파일 열기로 연 이미지를 화면 가운데에맞춰 출력하기
    canvas.place(x=(840-width)/2, y=(645-height)/2+35)


# 파일 열기
def func_open():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY, readFp

    # askopenfilename() 함수로 파일 열기 대화상자를 나타내어 그림 파일 선택
    readFp = askopenfilename(parent=window, filetypes=(
        ("모든 그림 파일", "*.jpg;*.jpeg;*.bmp;*.png;*.tif;*.gif;"), ("모든 파일", "*.*")))

    # 이미지는 GIF, JPG, PNG를 불러와 모두 처리하기 위해 PhotoImage() 가 아닌
    # Wand 라이브러리에서 제공하는 Image()를 사용

    # 이미지를 준비하는 단계
    # photo는 처음 불러들인 원본 이미지
    photo = Image(filename=readFp)
    oriX = photo.width  # 원본 이미지의 가로 사이즈를 oriX에 저장
    oriY = photo.height  # 원본 이미지의 세로 사이즈를 oriX에 저장

    # photo2는 처리 결과를 저장할 변수
    photo2 = photo.clone()  # 원본 이미지의 photo를 복사하여 photo2에 저장
    newX = photo2.width
    newY = photo2.height
    # 복제된 photo2를 캔버스의 페이퍼에 디스플레이하는 사용자 정의 함수 실행
    displayImage(photo2, newX, newY)

    photo_Label = Label(window, text=readFp, fg="white", bg="gray")
    photo_Label.place(x=43, y=37)


# 파일 저장
def func_save():

    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # photo2는 func_open() 함수를 실행하면 생성됨
    # 파일을 열지 않았다면 저장하기를 눌렀을 때 함수를 빠져나감
    if photo2 == None:
        return

    # 대화 상자로부터 넘겨받은 파일의 정보를 saveFp에 저장
    saveFp = asksaveasfile(parent=window, mode="w", defaultextension=".jpg", filetypes=(
        ("JPG 파일", "*.jpg;*.jpeg"), ("모든 파일", "*.*")))
    savePhoto = photo2.convert("jpg")  # 결과 이미지인 photo2를 jpg로 변환
    savePhoto.save(filename=saveFp.name)  # 파일 저장 대화창에서 입력받은 파일 이름으로 저장

# 되돌리기


def func_revert():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    photo2 = photo.clone()  # 원본을 복제해서 photo2 덮어쓰기
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 프로그램 종료
def func_exit():
    window.quit()
    window.destroy()

# 이미지 확대


def func_zoomin():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None:
        return

    # askinteger() 함수를 실행해 대화 상자로 확대할 배수 입력받음
    scale = askinteger("확대배수", "확대할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    # photo2 = photo.clone()  # 원본 이미지 photo를 복제하여 photo2에 저장
    # 원본 이미지의 가로 세로 사이즈에 배수를 곱하여 크기 변경
    photo2.resize(int(newX * scale), int(newY * scale))
    newX = photo2.width  # 변경된 이미지의 가로 사이즈 newX에 저장
    newY = photo2.height  # 변경된 이미지의 세로 사이즈 newY에 저장
    # 처리된 이미지의 이미지, 가로,세로 정보를 displayImage() 함수에 넘겨줌
    displayImage(photo2, newX, newY)


# 이미지 축소
def func_zoomout():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None:
        return

    # askinteger() 함수를 실행해 대화 상자로 축소할 배수 입력받음
    scale = askinteger("축소배수", "축소할 배수를 입력하세요(2~4)", minvalue=2, maxvalue=4)
    # photo2 = photo.clone()  # 원본 이미지 photo를 복제하여 photo2에 저장
    # 원본 이미지의 가로 세로 사이즈에 배수를 나누어 크기 변경
    photo2.resize(int(newX / scale), int(newY / scale))
    newX = photo2.width  # 변경된 이미지의 가로 사이즈 newX에 저장
    newY = photo2.height  # 변경된 이미지의 세로 사이즈 newY에 저장
    # 처리된 이미지의 이미지, 가로,세로 정보를 displayImage() 함수에 넘겨줌
    displayImage(photo2, newX, newY)


# 상하 반전, flip() 함수 사용
def func_mirror1():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None:
        return

    photo2.flip()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 좌우 반전, flop() 함수 사용
def func_mirror2():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None:
        return

    photo2.flop()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리1 > 회전
# 대화창을 통해 정수를 입력받아 그 수만큼 회전
# Wand 라이브러리에서 제공하는 rotate(각도)함수를 사용
def func_rotate():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    if photo2 == None:
        return

    degree = askinteger("회전", "회전할 각도를 입력하세요(0~360)", minvalue=0, maxvalue=360)
    photo2.rotate(degree)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리2 > 밝게/어둡게
# Wand 라이브러리에서 제공하는 modulate(명도값,채도값,색상값)함수를 사용
# 명도는 modulate(명도값, 100, 100) 함수를 사용
# 원본의 명도값이 100이므로 100이상은 '밝게', 100 이하는 '어둡게' 처리
# 밝게, modulate(밝기값, 100, 100) 함수에 100~200 값 입력
def func_bright():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("밝게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(value, 100, 100)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


def func_dark():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("어둡게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=200)
    photo2.modulate(value, 100, 100)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리2 > 선명하게/탁하게
# Wand 라이브러리에서 제공하는 modulate(100,채도값,100)함수를 사용
# 원본의 채도값이 100이므로 100 이상은 '선명하게', 100 이하는 '탁하게' 처리
def func_clear():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("선명하게", "값을 입력하세요(100~200)", minvalue=100, maxvalue=200)
    photo2.modulate(100, value, 100)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


def func_unclear():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("탁하게", "값을 입력하세요(0~100)", minvalue=0, maxvalue=100)
    photo2.modulate(100, value, 100)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리2 > 흑백이미지
# 이미지의 type 값을 "grayscale"로 설정
def func_bw():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    photo2.type = "grayscale"
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)


# 이미지 처리3 > 이미지 색조 변경
def func_hue():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askinteger("색조", "값을 입력하세요(0~200)", minvalue=0, maxvalue=200)
    photo2.modulate(100, 100, value)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_sepia():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askfloat("세피아", "값을 입력하세요(0.0~1.0)", minvalue=0, maxvalue=1)
    photo2.sepia_tone(threshold=value)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_spread():
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY  # 전역 변수 선언

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return

    value = askfloat("흩뿌리기", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    photo2.spread(radius=value)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_kuwahara() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    photo2.transform_colorspace('gray')
    value1 = askfloat("emboss_radius", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    value2 = askfloat("emboss_sigma", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    photo2.kuwahara(radius=value1, sigma=value2)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_emboss() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    value1 = askfloat("kuwahara_radius", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    value2 = askfloat("kuwahara_sigma", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    photo2.emboss(radius=value1, sigma=value2)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_charcoal() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    value1 = askfloat("charcoal_radius", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    value2 = askfloat("charcoal_sigma", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    photo2.charcoal(radius=value1, sigma=value2)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_polaroid() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    photo2.polaroid()
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_vignette() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    value1 = askfloat("vignette_sigma", "값을 입력하세요(0.0~10.0)", minvalue=0, maxvalue=10)
    value2 = askinteger("vignette_x", "값을 입력하세요(0.0~180)", minvalue=0, maxvalue=180)
    value3 = askinteger("vignette_y", "값을 입력하세요(0.0~180)", minvalue=0, maxvalue=180)
    photo2.vignette(sigma=value1, x=value2, y=value3)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_wave() :
    global window, canvas, paper, photo, photo2, oriX, oriY, newX, newY

    # 파일을 열지 않았다면 명령어를 실행했을 때 함수를 빠져나감
    if photo2 == None:
        return
    value1 = askinteger("wave_amplitude", "값을 입력하세요", minvalue=0, maxvalue=100)
    value2 = askinteger("wave_length", "값을 입력하세요", minvalue=0, maxvalue=100)
    photo2.wave(amplitude=photo2.height / value1, wave_length=photo2.width / value2)
    newX = photo2.width
    newY = photo2.height
    displayImage(photo2, newX, newY)

def func_drawing() : 
    canvas_width = 500
    canvas_height = 150

    def paint( event ):
        python_green = "#476042"
        x1, y1 = ( event.x - 1 ), ( event.y - 1 )
        x2, y2 = ( event.x + 1 ), ( event.y + 1 )
        w.create_oval( x1, y1, x2, y2, fill = python_green )

    master = Tk()
    master.title( "낙서장" )
    master.geometry("500x500")
    w = Canvas(master, 
            width=canvas_width, 
            height=canvas_height)
    w.pack(expand = YES, fill = BOTH)
    w.bind( "<B1-Motion>", paint )

    '''menubar=Menu(master)
    master.config(menu=menubar)

    fileMenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="color", menu=fileMenu)
    fileMenu.add_command(label="red", command=red)'''
        
    mainloop()

    
# 메인 코드부
window = Tk()   # 부모 윈도우
window.geometry("1074x679")
window.title("PhotoShop_김상훈(Ver.4)")


# 배경이미지 출력
bgPhoto = PhotoImage(file="0929_김상훈/bg123.png")     # 배경 이미지 준비
bg_Image = Label(window, image=bgPhoto)       # 이미지 생성
bg_Image.place(x=-2, y=-2)                       # 이미지 디스플레이


# 1.메뉴 자체 생성
# 메뉴 자체 = Menu(부모 윈도우)
# 부모 윈도우.config(menu = 메뉴 자체)
mainMenu = Menu(window)     # 메뉴자체
window.config(menu=mainMenu)


# 2. 상위 메뉴 생성
# 상위 메뉴 = Menu(메뉴자체)
# 메뉴자체.add_cascade(label="상위 메뉴 텍스트", menu=상위메뉴)
# add_cascade() 메소드는 상위 메뉴와 하위 메뉴 연결

fileMenu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="file", menu=fileMenu)


# 3. 하위 메뉴 생성
# 상위메뉴.add_command(label="하위 메뉴1", command=함수1)
# add_command() 메소드는 기본 메뉴 항목 생성
fileMenu.add_command(label="open", command=func_open)
fileMenu.add_command(label="save", command=func_save)
fileMenu.add_separator()  # 구분선 삽입
fileMenu.add_command(label="revert", command=func_revert)
fileMenu.add_separator()  # 구분선 삽입
fileMenu.add_command(label="exit", command=func_exit)


# 두번째 상위 메뉴(edit) 생성
image1Menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="edit", menu=image1Menu)
image1Menu.add_command(label="zoomin", command=func_zoomin)
image1Menu.add_command(label="zoomout", command=func_zoomout)
image1Menu.add_separator()  # 구분선 삽입
image1Menu.add_command(label="flip", command=func_mirror1)
image1Menu.add_command(label="flop", command=func_mirror2)
image1Menu.add_separator()  # 구분선 삽입
image1Menu.add_command(label="rotate", command=func_rotate)


# 세번째 상위 메뉴(image) 생성
image2Menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="image", menu=image2Menu)
image2Menu.add_command(label="brightness", command=func_bright)
image2Menu.add_command(label="darkness", command=func_dark)
image2Menu.add_separator()  # 구분선 삽입
image2Menu.add_command(label="clear", command=func_clear)
image2Menu.add_command(label="unclear", command=func_unclear)
image2Menu.add_command(label="spread", command=func_spread)
image2Menu.add_separator()  # 구분선 삽입
image2Menu.add_command(label="grayscale", command=func_bw)
image2Menu.add_command(label="hue", command=func_hue)
image2Menu.add_command(label="sepia", command=func_sepia)

# 네번째 상위 메뉴(filter) 생성
filterMenu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="filter", menu=filterMenu)
filterMenu.add_command(label="emboss", command=func_emboss)
filterMenu.add_command(label="kuwahara", command=func_kuwahara)
filterMenu.add_separator() 
filterMenu.add_command(label="polaroid", command=func_polaroid)
filterMenu.add_command(label="vignette", command=func_vignette)

#다섯번째 상위 메뉴(func) 생성
image3Menu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="func", menu=image3Menu)
image3Menu.add_command(label="charcoal", command=func_charcoal)
image3Menu.add_command(label="wave", command=func_wave)
image3Menu.add_separator() 
image3Menu.add_command(label="drawing", command=func_drawing)

window.mainloop()
