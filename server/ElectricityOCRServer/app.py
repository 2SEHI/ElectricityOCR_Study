# flask 웹 서버를 만들기 위해서 필수
from flask import Flask, request
from flask import send_file
from flask import render_template

# 앱 생성
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 요청 과 요청을 받으면 처리할 함수를 생성
# 포트번호까지의 요청이 오면 templates 디렉토리의 index.html을 출력
@app.route('/')
def index():
    return render_template('index.html')

import common.db as db
from flask import jsonify

# 조회
@app.route('/list')
def list():
    dao = db.Dao()
    result, data = dao.select_all()
    # 출력의 형태 : json
    response = {'result' : result, 'data' : data}
    return jsonify(response)

# 파일 다운로드
@app.route('/listimagedownload/<pictureurl>')
def listimagedownload(pictureurl):
    file_name = 'static/img/' + pictureurl
    print(file_name)
    # file_name : 실제 파일의 경로(server쪽)
    # mimetypes : 파일의 종류
    # attachment_filename : 다운로드 되었을 때의 파일 이름(client쪽)
    return send_file(file_name, mimetype='application/octect-stream',
                     attachment_filename=pictureurl,
                     as_attachment =True)

# 전력량 계량기 등록
@app.route('/detail/<serial_id>')
def detail(serial_id):
    dao = db.Dao()
    result, data = dao.select_one(serial_id)
    print(data["supply_type"])
    # 출력의 형태 : json
    response = {'result' : result, 'data' : data}
    return jsonify(response)

# 자신의 IP로 접속할 수 있도록 서버를 구동
# 회사 내에서만 접속가능하게 하고 싶다면 host를 변경
app.run(host='0.0.0.0', debug=True)