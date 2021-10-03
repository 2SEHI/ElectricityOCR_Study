use electricityDB;
-- 샘플 데이터 생성
INSERT INTO electricity_meter_tb (`serial_cd`, `supply_type`, `typename`, `electricity_filename`, `region_cd`)
VALUES(	'0047120' , '교류단상2선식', 'g-type', '847207D64AF9_P1134.jpg','01');
INSERT INTO electricity_meter_tb (`serial_cd`, `supply_type`, `typename`, `electricity_filename`, `region_cd`)
VALUES( '0049081' , '교류단상2선식', 'g-type', '847207D64B4F_P1182.jpg','01');


INSERT INTO modem_tb (`modem_cd`, `serial_cd`, `modem_filename`)
VALUES( '847207D64AF9','0047120', '847207D64AF9_P2134.jpg');

INSERT INTO modem_tb (`modem_cd`, `serial_cd`, `modem_filename`)
VALUES( '847207D64B4F','0049081', '847207D64B4F_P2182.jpg');

INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES( '0047120', '847207D64AF9_P1134_test1.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES('0047120', '847207D64AF9_P1134_test2.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES('0047120', '847207D64AF9_P1134_test3.jpg');


INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ('0049081', '847207D64B4F_P1182_test1.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ( '0049081',  '847207D64B4F_P1182_test2.jpg');
INSERT INTO electricity_preprocessing_tb (`serial_cd`, `pre_filename`)
VALUES ( '0049081',  '847207D64B4F_P1182_test3.jpg');

commit;

select * from electricity_meter_tb;
select * from modem_tb;
select * from electricity_preprocessing_tb;


select electricity_meter_tb.serial_cd as serial_cd, 
electricity_meter_tb.typename as typename, 
electricity_meter_tb.electricity_save_date as electricity_save_date, 
modem_tb.modem_cd as modem_cd 
from modem_tb
join electricity_meter_tb 
on modem_tb.serial_cd = electricity_meter_tb.serial_cd;

insert 

-- 데이터 상세페이지 검색
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
and electricity_meter_tb.serial_cd = '0047120'


-- 데이터 상세페이지 내에서 전처리 이미지파일명 검색
select 
elect_pre_tb.pre_id as pre_id,
elect_pre_tb.serial_cd as serial_cd,
elect_pre_tb.pre_filename as pre_filename
from electricity_meter_tb as elect_tb
join electricity_preprocessing_tb as elect_pre_tb
on elect_tb.serial_cd = elect_pre_tb.serial_cd 
where elect_tb.del_flag = 0
and elect_tb.serial_cd = '0047120'



