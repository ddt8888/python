from tkinter import *
from time import *

# 변수 선언 부분
fnameList = ["japan1.png"]
for i in range(2, 10):
    fnameList.append("japan" + str(i) + ".png")

desList = ["오사카 성", "도쿄 디즈니 랜드", "후지산", "온천",
           "오키나와", "후쿠오카 명물 모츠나베", "도쿄 타워", "유니버셜 스튜디오 재팬"]

bgList = ["bg1.png"]
for i in range(2, 10):
    bgList.append("bg" + str(i) + ".png")

num = 0

# 함수 선언 부분
# 다음 버튼을 눌렀을때 실행 되는 clickNext() 함수


def clickNext():
    # global num은 num 전역변수를 함수 안에서 사용하겠다는 의미.
    global num
    # 다음 사진이 나와야하니까 num을 1씩 증가시킨다
    num += 1
    # 사진 번호(index)가 최대 8이므로 8이넘으면 다시 0번으로 돌아간다.
    if num > 7:
        num = 0
    # 변경된 사진 번호에 해당하는 이미지 파일을 pLabel로 변경
    photo = PhotoImage(file="album/gif/" + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.image = photo
    pLabelText.configure(text=desList[num])  # 파일이름 출력하기
    photo2 = PhotoImage(file="album/gif/" + bgList[num])
    winimage.configure(image=photo2)
    winimage.image = photo2

# 이전 버튼을 눌렀을때 실행 되는 clickPrev() 함수


def clickPrev():
    global num
    num -= 1
    if num < 0:
        num = 7
    photo = PhotoImage(file="album/gif/" + fnameList[num])
    pLabel.configure(image=photo)
    pLabel.image = photo
    pLabelText.configure(text=desList[num])  # 파일이름 출력하기
    bgpic = PhotoImage(file="album/gif/" + bgList[num])
    winimage.configure(image=bgpic)
    winimage.image = bgpic

# pageUp 키를 누르면 실행되는 함수
# [다음] 버튼을 누르는 것과 동일한 기능이라서 clickNext() 함수 호출


def pageUp(event):
    clickNext()

# pageDown 키를 누르면 실행되는 함수
# [이전] 버튼을 누르는 것과 동일한 기능이라서 clickPrev() 함수 호출


def pageDown(event):
    clickPrev()


# 메인 코드 부분
window = Tk()
window.geometry("1000x1000")
window.title("사진 앨범 보기")
window.configure(background="#FFD8FB")  # 창 배경색 지정
# 0에 가까울 수록 검정 f에 가까울수록 하얘짐.

# 배경 이미지
winphoto = PhotoImage(file="album/gif/" + bgList[0])  # 이미지 준비
winimage = Label(window, image=winphoto)  # 이미지 생성
winimage.place(x=-2, y=-2)  # 이미지 디스플레이


# window 창에서 키보드 이벤트를 처리하도록 설정한다.
# <Prior>은 pageUp 키를 누르는 이벤트
window.bind("<Prior>", pageUp)
# <Next>는 pageDown 키를 누르는 이벤트
window.bind("<Next>", pageDown)

# 프로그램을 실행 시키면 초기화면에 첫번째 그림을 나오게 한다.
photo = PhotoImage(file="album/gif/" + fnameList[0])
pLabel = Label(window, image=photo)
pLabelText = Label(
    window, text=desList[0], bg="#E7CF5A", fg="black")  # 파일이름 출력하기

# 각 버튼을 눌렀을때 command를 이용해 함수랑 연결시킨다.
btpre = PhotoImage(file="album/gif/album_butprev.png")
btnPrev = Button(window, image=btpre, command=clickPrev,
                 bd=0, highlightthickness=0)
btnex = PhotoImage(file="album/gif/album_butnext.png")
btnNext = Button(window, image=btnex, command=clickNext,
                 bd=0, highlightthickness=0)

# 버튼과 이미지를 place()로 절대위치에 지정해준다.
btnPrev.place(x=50, y=500)
btnNext.place(x=930, y=500)
pLabel.place(x=103, y=103)
pLabelText.place(x=480, y=40)

window.mainloop()
