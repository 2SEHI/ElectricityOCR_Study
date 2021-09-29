import pymysql
import sqlite3
from flask import g

class Dao:

    def __init__(self):
        self.__DATABASE = '/path/to/database.db'

    #  데이터베이스 연결 메소드
    def connect(self):
        # 연결
        self.con = pymysql.connect(host='localhost',
                                   port=3306,
                                   user='flaskServer',
                                   passwd='20210420',
                                   db='electricitydb',
                                   charset='utf8')
        # 데이터베이스 사용 객체 생성
        self.cursor = self.con.cursor()

    # 데이터베이스 연결 해제 메소드
    def close(self):
        self.con.close()

    # 전체 데이터 가져오기
    def selectall(self):
        # 데이터베이스 연결
        self.connect()
        li = []
        try:
            # sql 문 실행
            self.cursor.execute("select * from electricity_meter_tb")
            data = self.cursor.fetchall()
            # 데이터를 저장할 list

            for temp in data:
                dic = {}
                dic['serial_cd'] = temp[0]
                dic['supply_type'] = temp[1]
                dic['typename'] = temp[2]
                dic['electricity_filename'] = temp[3]
                dic['region_cd'] = temp[4]
                dic['electricity_save_date'] = temp[5]
                dic['del_flag'] = temp[6]
                li.append(dic)

        except Exception as e:
            # insert 실패시 False 반환
            result = False
        self.close()
        return li
