-- electricity_meter_TB 전력량계량기 테이블
-- 	serial_cd 전력량계 제조번호 
-- 	supply_type 저압배전방식
-- 	typename 전력량계 종류
-- 	electricity_filename 전력량계량기 원본이미지파일명
-- 	region_cd 지역코드
-- 	electricity_save_date 전력량계 저장날짜
-- 	del_flag 삭제 플래그

-- modem_tb 모뎀 정보 테이블
-- 	modem_cd 모뎀 정보 pk
-- 	serial_cd 제조번호 fk
-- 	modem_filename 모뎀 원본이미지파일명
-- 	modem_save_date 모뎀 저장날짜

-- electricity_preprocessing_tb 전력량 전처리 이미지파일 테이블
-- 	pre_id 시퀀스 번호 pk
-- 	serial_cd 전력량계 제조번호 fk
-- 	pre_filename 전처리과정 이미지파일명


-- 데이터베이스 생성
create database electricityDB;
-- 데이터베이스 확인
show databases;
-- electricityDB 사용
use electricityDB;
-- User 생성
create user 'flaskServer'@'localhost' identified by '20210420';
-- User localhost로 접속한 flaskServer에게 electricityDB에 대한 권한 부여
grant all privileges on electricityDB.* to 'flaskServer'@'localhost';
-- User 권한 확인
SHOW GRANTS FOR 'flaskServer'@localhost;

-- electricity_meter_tb
CREATE TABLE `electricityDB`.`electricity_meter_tb` (
	`serial_cd`             VARCHAR(30)  NOT NULL COMMENT 'serial_cd', -- serial_cd
	`supply_type`           VARCHAR(30)  NULL     COMMENT 'supply_type', -- supply_type
	`typename`              VARCHAR(6)   NULL     COMMENT 'typename', -- typename
	`electricity_filename`  VARCHAR(100) NOT NULL COMMENT 'electricity_filename', -- electricity_filename
	`region_cd`             VARCHAR(20)  NULL     COMMENT 'region_cd', -- region_cd
	`electricity_save_date` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'electricity_save_date', -- electricity_save_date
	`del_flag`              VARCHAR(1)   NOT NULL DEFAULT 0 COMMENT 'del_flag' -- del_flag
)
COMMENT 'electricity_meter_tb';

-- electricity_meter_tb
ALTER TABLE `electricityDB`.`electricity_meter_tb`
	ADD CONSTRAINT `PK_electricity_meter_tb` -- electricity_meter_tb 기본키
		PRIMARY KEY (
			`serial_cd` -- serial_cd
		);

-- modem_tb
CREATE TABLE `electricityDB`.`modem_tb` (
	`modem_cd`        VARCHAR(30)  NOT NULL COMMENT 'modem_cd', -- modem_cd
	`serial_cd`       VARCHAR(30)  NOT NULL COMMENT 'serial_cd', -- serial_cd
	`modem_filename`  VARCHAR(100) NOT NULL COMMENT 'modem_filename', -- modem_filename
	`modem_save_date` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'modem_save_date' -- modem_save_date
)
COMMENT 'modem_tb';

-- modem_tb
ALTER TABLE `electricityDB`.`modem_tb`
	ADD CONSTRAINT `PK_modem_tb` -- modem_tb 기본키
		PRIMARY KEY (
			`modem_cd` -- modem_cd
		);

-- electricity_preprocessing_tb
CREATE TABLE `electricityDB`.`electricity_preprocessing_tb` (
	`pre_id`       INT          NOT NULL COMMENT 'pre_id', -- pre_id
	`serial_cd`    VARCHAR(30)  NOT NULL COMMENT 'serial_cd', -- serial_cd
	`pre_filename` VARCHAR(100) NOT NULL COMMENT 'pre_filename' -- pre_filename
)
COMMENT 'electricity_preprocessing_tb';

-- electricity_preprocessing_tb
ALTER TABLE `electricityDB`.`electricity_preprocessing_tb`
	ADD CONSTRAINT `PK_electricity_preprocessing_tb` -- electricity_preprocessing_tb 기본키
		PRIMARY KEY (
			`pre_id` -- pre_id
		);

ALTER TABLE `electricityDB`.`electricity_preprocessing_tb`
	MODIFY COLUMN `pre_id` INT NOT NULL AUTO_INCREMENT COMMENT 'pre_id';

ALTER TABLE `electricityDB`.`electricity_preprocessing_tb`
	AUTO_INCREMENT = 1;

-- modem_tb
ALTER TABLE `electricityDB`.`modem_tb`
	ADD CONSTRAINT `FK_electricity_meter_tb_TO_modem_tb` -- electricity_meter_tb -> modem_tb
		FOREIGN KEY (
			`serial_cd` -- serial_cd
		)
		REFERENCES `electricityDB`.`electricity_meter_tb` ( -- electricity_meter_tb
			`serial_cd` -- serial_cd
		);

-- electricity_preprocessing_tb
ALTER TABLE `electricityDB`.`electricity_preprocessing_tb`
	ADD CONSTRAINT `FK_electricity_meter_tb_TO_electricity_preprocessing_tb` -- electricity_meter_tb -> electricity_preprocessing_tb
		FOREIGN KEY (
			`serial_cd` -- serial_cd
		)
		REFERENCES `electricityDB`.`electricity_meter_tb` ( -- electricity_meter_tb
			`serial_cd` -- serial_cd
		);