import pymysql
import sqlite3
from flask import g

class Dao:

    def __init__(self):
        self.__SELECT_ALL = '''
        # select * from electricity_meter_tb
        '''
        # self.__SELECT_ALL = '''
        #     select electricity_meter_tb.serial_cd as serial_cd,
        # 	electricity_meter_tb.typename as typename,
        # 	electricity_meter_tb.electricity_save_date as electricity_save_date,
        # 	modem_tb.modem_cd as modem_cd
        #     from modem_tb
        #     join electricity_meter_tb
        #     on modem_tb.serial_cd = electricity_meter_tb.serial_cd;
        #     '''
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
            self.cursor.execute(self.__SELECT_ALL)
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

# dict형태로 데이터를 받아서 삽입하는 메소드
def insertitem(self, item):
    self.connect()
    # 가장 큰 itemid를 가져와서 1을 더해서 itemid를 생성
    self.cursor.execute('select max(itemid) from item')
    data = self.cursor.fetchone()
    # 데이터가 없어서 예외가 발생할 경우를 대비하여 try except문으로 예외처리를 해줍니다.
    try:
        itemid = int(data[0] + 1)

    except:
        itemid = 1

    # 데이터를 삽입하는 sql을 실행
    self.cursor.execute('insert into item values(%s, %s, %s, %s, %s)',
                        (itemid, item['itemname'], item['price'],
                         item['description'], item['pictureurl']))
    # 삽입한 데이터를 데이터베이스에 반영
    self.con.commit()
    # 데이터베이스 접속 해제
    self.close()