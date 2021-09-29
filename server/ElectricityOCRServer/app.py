# flask 웹 서버를 만들기 위해서 필수
from flask import Flask, request
from flask import render_template

# 앱 생성
app = Flask(__name__)

# 요청 과 요청을 받으면 처리할 함수를 생성
# 포트번호까지의 요청이 오면 templates 디렉토리의 index.html을 출력
@app.route('/')
def index():
    return render_template('index.html')

import common.db as db
from flask import jsonify

@app.route('/list')
def list():
    dao = db.Dao()
    data = dao.selectall()
    # 출력의 형태 : json
    response = {'result' : True, 'data' : data}
    return jsonify(response)



# 자신의 IP로 접속할 수 있도록 서버를 구동
# 회사 내에서만 접속가능하게 하고 싶다면 host를 변경
app.run(host='0.0.0.0', debug=True)