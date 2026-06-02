import pymysql

# DB CRUD

# conn    = 데이터베이스 연결 객체
# cursor  = SQL 실행 객체

class BoardDAO:
       
    def __init__(self):

        self.host = "localhost"
        self.user = "board_user"
        self.password = "board1234"
        self.database = "board_db"

    def get_connection(self):

        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset="utf8mb4"
        )
       
    def insert_board(self, title, content, writer):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
        INSERT INTO board
        (title, content, writer)
        VALUES
        (%s, %s, %s)
        """
        
        # sql = f"""
        #     INSERT INTO board
        #     (title, content, writer)
        #     VALUES
        #     ('{title}', '{content}', '{writer}')
        #     """

        # f-string → 출력문, 로그용
        # %s 파라미터 바인딩 → SQL용
        
        cursor.execute(
            sql,
            (title, content, writer)
        )

        conn.commit()
        cursor.close()
        conn.close()

        print("등록 완료")

    def select_all(self):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT *
        FROM board
        ORDER BY id DESC
        """

        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        return result

    def select_one(self, board_id):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
        SELECT *
        FROM board
        WHERE id=%s
        """

        cursor.execute(sql, (board_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result

    def delete_board(self, board_id):

        conn = self.get_connection()
        cursor = conn.cursor()

        sql = """
        DELETE
        FROM board
        WHERE id=%s
        """

        cursor.execute(sql, (board_id,))

        conn.commit()

        cursor.close()
        conn.close()

        print("삭제 완료")
