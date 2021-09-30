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

select * from electricity_meter_tb where serial_cd = ?