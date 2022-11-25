from flask import Flask, render_template
# render_templete은 .html 파일을 text형태로 변환

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')
    # templates 폴더를 만들고 그 안에 html파일을 넣어야함. 그러나 css는 적용되지않음.
app.run(debug=True)