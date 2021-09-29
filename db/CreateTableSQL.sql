-- electricity_meter_TB 전력량계량기 테이블
-- serial_cd 제조번호 pk serial_cd_pk
-- supply_type 단상 타입 
-- typename 타입명
-- electricity_filename
-- region_cd 지역코드
-- electricity_save_date 저장날짜
-- del_flag 삭제 플래그

-- modem_tb 모뎀 정보 테이블
-- modem_cd 모뎀 정보 pk
-- serial_cd 제조번호 fk
-- modem_filename 모뎀 원본 파일명
-- modem_save_date 모뎀 저장날짜

-- electricity_preprocessing_tb 전력량 전처리 파일 테이블
-- pre_id 시퀀스 번호 pk
-- serial_cd 제조번호 fk
-- pre_filename


-- 데이터베이스 생성
create database electricityDB;
-- 데이터베이스 확인
show databases;
-- sehiDB 사용
use electricityDB;
-- User sehi 생성
create user 'flaskServer'@'localhost' identified by '20210420';
-- User localhost로 접속한 sehi에게 sehiDB에 대한 권한 부여
grant all privileges on electricityDB.* to 'flaskServer'@'localhost';
-- User sehi의 권한 확인
SHOW GRANTS FOR 'flaskServer'@localhost;


CREATE TABLE `MY_SCHEMA`.`electricity_meter_tb` (
	`serial_cd`             VARCHAR(30)  NOT NULL COMMENT 'serial_cd',
	`supply_type`           VARCHAR(30)  NULL     COMMENT 'supply_type',
	`typename`              VARCHAR(6)   NULL     COMMENT 'typename',
	`electricity_filename`  VARCHAR(100) NOT NULL COMMENT 'electricity_filename',
	`region_cd`             VARCHAR(20)  NULL     COMMENT 'region_cd',
	`electricity_save_date` DATE         NOT NULL COMMENT 'electricity_save_date',
	`del_flag`              VARCHAR(1)   NOT NULL COMMENT 'del_flag'
)
COMMENT 'electricity_meter_tb'

CREATE command denied to user 'flaskServer'@'localhost' for table 'electricity_meter_tb'
ALTER TABLE `MY_SCHEMA`.`electricity_meter_tb`
	ADD CONSTRAINT `PK_electricity_meter_tb`
		PRIMARY KEY (
			`serial_cd`
		)

ALTER command denied to user 'flaskServer'@'localhost' for table 'electricity_meter_tb'
CREATE TABLE `MY_SCHEMA`.`modem_tb` (
	`modem_cd`        VARCHAR(30)  NOT NULL COMMENT 'modem_cd',
	`serial_cd`       VARCHAR(30)  NOT NULL COMMENT 'serial_cd',
	`modem_filename`  VARCHAR(100) NOT NULL COMMENT 'modem_filename',
	`modem_save_date` DATE         NOT NULL COMMENT 'modem_save_date'
)
COMMENT 'modem_tb'

CREATE command denied to user 'flaskServer'@'localhost' for table 'modem_tb'
ALTER TABLE `MY_SCHEMA`.`modem_tb`
	ADD CONSTRAINT `PK_modem_tb`
		PRIMARY KEY (
			`modem_cd`,
			`serial_cd`
		)

ALTER command denied to user 'flaskServer'@'localhost' for table 'modem_tb'
CREATE TABLE `MY_SCHEMA`.`electricity_preprocessing_tb` (
	`pre_id`       NUMERIC      NOT NULL COMMENT 'pre_id',
	`serial_cd`    VARCHAR(30)  NOT NULL COMMENT 'serial_cd',
	`pre_filename` VARCHAR(100) NOT NULL COMMENT 'pre_filename'
)
COMMENT 'electricity_preprocessing_tb'

CREATE command denied to user 'flaskServer'@'localhost' for table 'electricity_preprocessing_tb'
파일 또는 프로젝트가 삭제되어 에디터를 닫았습니다.
CREATE TABLE `electricityDB`.`electricity_meter_tb` (
	`serial_cd`             VARCHAR(30)  NOT NULL COMMENT 'serial_cd',
	`supply_type`           VARCHAR(30)  NULL     COMMENT 'supply_type',
	`typename`              VARCHAR(6)   NULL     COMMENT 'typename',
	`electricity_filename`  VARCHAR(100) NOT NULL COMMENT 'electricity_filename',
	`region_cd`             VARCHAR(20)  NULL     COMMENT 'region_cd',
	`electricity_save_date` DATE         NOT NULL COMMENT 'electricity_save_date',
	`del_flag`              VARCHAR(1)   NOT NULL COMMENT 'del_flag'
)
COMMENT 'electricity_meter_tb'

DDL 구문이 수행되었습니다.


ALTER TABLE `electricityDB`.`electricity_meter_tb`
	ADD CONSTRAINT `PK_electricity_meter_tb`
		PRIMARY KEY (
			`serial_cd`
		)

DDL 구문이 수행되었습니다.


CREATE TABLE `electricityDB`.`modem_tb` (
	`modem_cd`        VARCHAR(30)  NOT NULL COMMENT 'modem_cd',
	`serial_cd`       VARCHAR(30)  NOT NULL COMMENT 'serial_cd',
	`modem_filename`  VARCHAR(100) NOT NULL COMMENT 'modem_filename',
	`modem_save_date` DATE         NOT NULL COMMENT 'modem_save_date'
)
COMMENT 'modem_tb'

DDL 구문이 수행되었습니다.


ALTER TABLE `electricityDB`.`modem_tb`
	ADD CONSTRAINT `PK_modem_tb`
		PRIMARY KEY (
			`modem_cd`,
			`serial_cd`
		)

DDL 구문이 수행되었습니다.


CREATE TABLE `electricityDB`.`electricity_preprocessing_tb` (
	`pre_id`       NUMERIC      NOT NULL COMMENT 'pre_id',
	`serial_cd`    VARCHAR(30)  NOT NULL COMMENT 'serial_cd',
	`modem_cd`     VARCHAR(30)  NOT NULL COMMENT 'modem_cd',
	`pre_filename` VARCHAR(100) NOT NULL COMMENT 'pre_filename'
)
COMMENT 'electricity_preprocessing_tb'

DDL 구문이 수행되었습니다.


ALTER TABLE `electricityDB`.`electricity_preprocessing_tb`
	ADD CONSTRAINT `PK_electricity_preprocessing_tb`
		PRIMARY KEY (
			`pre_id`,
			`serial_cd`
		)

DDL 구문이 수행되었습니다.


ALTER TABLE `electricityDB`.`modem_tb`
	ADD CONSTRAINT `FK_electricity_meter_tb_TO_modem_tb`
		FOREIGN KEY (
			`serial_cd`
		)
		REFERENCES `electricityDB`.`electricity_meter_tb` (
			`serial_cd`
		)
DDL 구문이 수행되었습니다.


ALTER TABLE `electricityDB`.`electricity_preprocessing_tb`
	ADD CONSTRAINT `FK_electricity_meter_tb_TO_electricity_preprocessing_tb`
		FOREIGN KEY (
			`serial_cd`
		)
		REFERENCES `electricityDB`.`electricity_meter_tb` (
			`serial_cd`
		)
DDL 구문이 수행되었습니다.


