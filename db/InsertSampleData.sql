-- 샘플 데이터 생성
insert into electricity_meter_tb values(
	'0047120' , '교류단상2선식', 'g-type', '847207D64AF9_P1134.jpg','01', 20210929, 0);
insert into electricity_meter_tb values(
	'0049081' , '교류단상2선식', 'g-type', '847207D64B4F_P1182.jpg','01', 20210929, 0);

insert into modem_tb values(
 '847207D64AF9','0047120', '847207D64AF9_P2134.jpg', 20210929);
insert into modem_tb values(
'847207D64B4F','0049081', '847207D64B4F_P2182.jpg', 20210929);

INSERT INTO electricity_preprocessing_tb values(
1, '0047120', '847207D64AF9', '847207D64AF9_P1134_test1.jpg');
INSERT INTO electricity_preprocessing_tb values(
2, '0047120', '847207D64AF9', '847207D64AF9_P1134_test2.jpg');
INSERT INTO electricity_preprocessing_tb values(
3, '0047120', '847207D64AF9', '847207D64AF9_P1134_test3.jpg');


INSERT INTO electricity_preprocessing_tb values(
4, '0049081', '847207D64B4F', '847207D64B4F_P1182_test1.jpg');
INSERT INTO electricity_preprocessing_tb values(
5, '0049081', '847207D64B4F', '847207D64B4F_P1182_test2.jpg');
INSERT INTO electricity_preprocessing_tb values(
6, '0049081', '847207D64B4F', '847207D64B4F_P1182_test3.jpg');

commit;

select * from electricity_meter_tb;
select * from modem_tb;
select * from electricity_preprocessing_tb;


select electricity_meter_tb.serial_cd , 
	electricity_meter_tb.typename , 
	electricity_meter_tb.electricity_save_date, 
	modem_tb.modem_cd
from modem_tb
join electricity_meter_tb 
on modem_tb.serial_cd = electricity_meter_tb.serial_cd;
