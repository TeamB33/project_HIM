import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
# render_templete은 .html 파일을 text형태로 변환

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])

app.secret_key = "secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename): 
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 루트 라우팅
@app.route('/')
def index():
    return render_template('home.html')
     # templates 폴더를 만들고 그 안에 html파일을 넣어야함. 그러나 css는 적용되지않음.

@app.route('/',methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename:' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('home.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
# 파일 업로드 처리 라우팅

# @app.route('/upload/', methods = ['POST'])
# def upload_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         if f and allowed_file(f.filename):
#             # 저장할 경로 + 파일명
#         filename = secure_filename(f.filename)
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return redirect(url_for('uploaded_file', filename=filename))



# 서버실행
app.run(debug=True)

