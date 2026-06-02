from board_dao import *

board_dao = BoardDAO()

while True:

    print("=" * 40)
    print("1.목록  2.등록  3.내용  4.삭제  0.종료")
    print("=" * 40)

    menu = input("선택 > ")

    if menu == "1":

        boards = board_dao.select_all()

        print()
        print("번호 제목 작성자 작성일")
        print("-" * 40)

        for board in boards:

            print(
                board[0],
                board[1],
                board[2],
                board[3]
            )

    elif menu == "2":

        title = input("제목 : ")
        content = input("내용 : ")
        writer = input("작성자 : ")

        board_dao.insert_board(
            title,
            content,
            writer
        )

        print("등록 완료")

    elif menu == "3":

        num = input("번호 : ")

        board = board_dao.select_one(num)

        if board:

            print()
            print("번호 :", board[0])
            print("제목 :", board[1])
            print("내용 :", board[2])
            print("작성자 :", board[3])
            print("작성일 :", board[4])

    elif menu == "4":

        num = input("삭제 번호 : ")

        board_dao.delete_board(num)

        print("삭제 완료")

    elif menu == "0":

        print("프로그램 종료")
        break