-- 샘플 데이터 생성
INSERT INTO electricity_meter_tb (`serial_cd`, `supply_type`, `typename`, `electricity_filename`, `region_cd`)
VALUES(	'242500471201603' , '교류단상2선식', 'g-type', '847207D64AF9_P1134.jpg','01');
INSERT INTO electricity_meter_tb (`serial_cd`, `supply_type`, `typename`, `electricity_filename`, `region_cd`)
VALUES( '242500490811603' , '교류단상2선식', 'g-type', '847207D64B4F_P1182.jpg','01');


INSERT INTO modem_tb (`modem_cd`, `serial_cd`, `modem_filename`)
VALUES( '847207D64AF9','242500471201603', '847207D64AF9_P2134.jpg');

INSERT INTO modem_tb (`modem_cd`, `serial_cd`, `modem_filename`)
VALUES( '847207D64B4F','242500490811603', '847207D64B4F_P2182.jpg');

INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES( '242500471201603', '847207D64AF9_P1134_test1.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES('242500471201603', '847207D64AF9_P1134_test2.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES('242500471201603', '847207D64AF9_P1134_test3.jpg');


INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ('242500490811603', '847207D64B4F_P1182_test1.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ( '242500490811603',  '847207D64B4F_P1182_test2.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ( '242500490811603',  '847207D64B4F_P1182_test3.jpg');

INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ('242500471201603', '847207D64B4F_P1182_test1.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ( '242500471201603',  '847207D64B4F_P1182_test2.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ( '242500471201603',  '847207D64B4F_P1182_test3.jpg');

commit;

select * from electricity_meter_tb;
select * from modem_tb;
select * from electricity_preprocessing_tb;



-- 조회화면 : 전력량계량기, 모뎀바코드 정보 조회 Select SQL
select electricity_meter_tb.serial_cd as serial_cd,
modem_tb.modem_cd as modem_cd ,
electricity_meter_tb.electricity_filename as electricity_filename, 
date_format(electricity_meter_tb.electricity_save_date, '%Y-%m-%d %H:%i:%s') as electricity_save_date 
from electricity_meter_tb 
left join modem_tb 
on modem_tb.serial_cd = electricity_meter_tb.serial_cd 
where electricity_meter_tb.del_flag = 0
ORDER BY electricity_save_date DESC;

-- 상세화면 : 전력량계량기, 모뎀 정보 조회 Select SQL
select  
electricity_meter_tb.serial_cd as serial_cd,  
electricity_meter_tb.supply_type as supply_type, 
electricity_meter_tb.typename as typename, 
electricity_meter_tb.electricity_filename as electricity_filename, 
date_format(electricity_meter_tb.electricity_save_date, '%Y-%m-%d %H:%i:%s') as electricity_save_date,  
modem_tb.modem_cd as modem_cd, 
modem_tb.modem_filename as modem_filename,
date_format(modem_tb.modem_save_date,  '%Y-%m-%d %H:%i:%s') as modem_save_date  
from electricity_meter_tb 
left join modem_tb 
on modem_tb.serial_cd = electricity_meter_tb.serial_cd  
where electricity_meter_tb.del_flag = 0 
and electricity_meter_tb.serial_cd =  %s;

-- 상세화면 : 이미지 전처리 파일 조회
select 
electricity_preprocessing_tb.pre_filename as pre_filename
from electricity_meter_tb 
join electricity_preprocessing_tb 
on electricity_preprocessing_tb.serial_cd = electricity_meter_tb.serial_cd
where electricity_meter_tb.del_flag = 0
and electricity_meter_tb.serial_cd = %s
