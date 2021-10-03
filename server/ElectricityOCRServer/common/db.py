import pymysql
from flask import g

class Dao:

    def __init__(self):
        self.__SELECT_ALL = '''
        select electricity_meter_tb.serial_cd as serial_cd,
        modem_tb.modem_cd as modem_cd ,
        electricity_meter_tb.electricity_filename as electricity_filename, 
        date_format(electricity_meter_tb.electricity_save_date, '%Y-%m-%d %H:%i:%s') as electricity_save_date 
        from electricity_meter_tb 
        join modem_tb 
        on modem_tb.serial_cd = electricity_meter_tb.serial_cd 
        where electricity_meter_tb.del_flag = 0
        '''

        self.__SELECT_ONE = '''
        select  
        electricity_meter_tb.serial_cd as serial_cd,  
        electricity_meter_tb.supply_type as supply_type, 
        electricity_meter_tb.typename as typename, 
        electricity_meter_tb.electricity_filename as electricity_filename, 
        date_format(electricity_meter_tb.electricity_save_date, '%%Y-%%m-%%d %%H:%%i:%%s') as electricity_save_date,  
        modem_tb.modem_cd as modem_cd, 
        modem_tb.modem_filename as modem_filename 
        from electricity_meter_tb 
        join modem_tb 
        on modem_tb.serial_cd = electricity_meter_tb.serial_cd  
        where electricity_meter_tb.del_flag = 0 
        and electricity_meter_tb.serial_cd = %s 
        '''

        self.__SELECT_PRE_FILENAME = '''
        select 
        elect_pre_tb.pre_filename as pre_filename
        from electricity_meter_tb as elect_tb
        join electricity_preprocessing_tb as elect_pre_tb
        on elect_tb.serial_cd = elect_pre_tb.serial_cd 
        where elect_tb.del_flag = 0
        and elect_tb.serial_cd = %s
        '''
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
    def select_all(self):
        # 데이터베이스 연결
        result = True
        li = []
        try:
            self.connect()
            # sql 문 실행
            self.cursor.execute(self.__SELECT_ALL)
            data = self.cursor.fetchall()
            # 데이터를 저장할 list

            for temp in data:
                item = {}
                item['serial_cd'] = temp[0]
                item['modem_cd'] = temp[1]
                item['electricity_filename'] = temp[2]
                item['electricity_save_date'] = temp[3]
                li.append(item)

        except Exception as e:
            # insert 실패시 False 반환
            result = False
        self.close()
        return result, li

    # dict형태로 데이터를 받아서 삽입하는 메소드
    def select_one(self, serial_cd):
        result = True
        item = {}
        try:
            self.connect()
            
            # 제조코드에 해당하는 전력량계량기와 모뎀코드 가져오기
            self.cursor.execute(self.__SELECT_ONE, str(serial_cd))
            data = self.cursor.fetchone()
            # 데이터가 존재하는 경우, 데이터를 json형식으로 설정
            if len(data) > 0:

                item['serial_cd'] = data[0]
                item['supply_type'] = data[1]
                print(data[1])
                item['typename'] = data[2]

                item['electricity_filename'] = data[3]
                item['electricity_save_date'] = data[4]
                item['modem_cd'] = data[5]
                item['modem_filename'] = data[6]
                
                # 제조코드에 해당하는 전처리 이미지파일명 검색
                self.cursor.execute(self.__SELECT_PRE_FILENAME, str(serial_cd))
                filenames = self.cursor.fetchall()
                print(filenames)
                temp = []
                for filename in filenames:
                    temp.append(filename[0])
                item['pre_filenames'] = temp
        except self.cursor.Error as e:
            # insert 실패시 False 반환
            result = False
            print(e)
        self.close()
        return result, item