import os, time
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
# denosing setup

import torch
from basicsr.models import create_model
from basicsr.utils import img2tensor as _img2tensor, tensor2img, imwrite
from basicsr.utils.options import parse
import numpy as np
import cv2
import matplotlib.pyplot as plt

# render_templete은 .html 파일을 text형태로 변환

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
filename_ = ''
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
# 루트 라우팅
@app.route('/')
def index():
    return render_template('home.html')
     # templates 폴더를 만들고 그 안에 html파일을 넣어야함. 그러나 css는 적용되지않음.

# 이미지 업로드 라우팅
@app.route('/', methods=['GET','POST'])
def upload_image():
    global filename_
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename_ = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_))
        #flash('upload_image filename: ' + filename_)
        print(filename_)
        return redirect(url_for('convert_page_index'))
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
# converted_page first image
@app.route('/display')
def display_image():
    print('display_image filename: ' + filename_)
    return redirect(url_for('static', filename='uploads/' + filename_), code=301)

# converted_page second imgage
@app.route('/display_denoise')
def display_denoise_image():
    
    print('display_denoise_image filename: ' + filename_)
    # Create Model
    opt_path = 'NAFNet/options/test/SIDD/NAFNet-width64.yml'
    opt = parse(opt_path, is_train=False)
    opt['dist'] = False
    NAFNet = create_model(opt) 
    print("step1")
        
    # Inference and Denosing
    input_path = f'static/uploads/{filename_}'
    output_path = f'static/denoised/{filename_}'
    print("step2")

    img_input = imread(input_path)
    print("step3")
    inp = img2tensor(img_input)
    print("step4")
    single_image_inference(NAFNet, inp, output_path)
    print("step5")
    
    # time.sleep(1)
    print('sleep 1sec')
    # denoised image return
    return redirect(url_for('static', filename='denoised/' + filename_), code=301)
    

# converted_page 라우팅
@app.route('/convert_page/',methods=['GET','POST'])
def convert_page_index():
    print('hi')
    print(filename_)
    return render_template('convert_page.html')


def imread(img_path):
  img = cv2.imread(img_path)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img

def img2tensor(img, bgr2rgb=False, float32=True):
    img = img.astype(np.float32) / 255.
    return _img2tensor(img, bgr2rgb=bgr2rgb, float32=float32)

def display(img1, img2):
  fig = plt.figure(figsize=(25, 10))
  ax1 = fig.add_subplot(1, 2, 1) 
  plt.title('Input image', fontsize=16)
  ax1.axis('off')
  ax2 = fig.add_subplot(1, 2, 2)
  plt.title('NAFNet output', fontsize=16)
  ax2.axis('off')
  ax1.imshow(img1)
  ax2.imshow(img2)

def single_image_inference(model, img, save_path):
    print("step4 start")
    model.feed_data(data={'lq': img.unsqueeze(dim=0)})
    print("step4-1 start")

    if model.opt['val'].get('grids', False):
        model.grids()

    model.test()
    print("step4-2 start")

    if model.opt['val'].get('grids', False):
        model.grids_inverse()
    print("step4-3 start")

    visuals = model.get_current_visuals()
    print("step4-4 start")

    sr_img = tensor2img([visuals['result']])
    print("step4-5 start")

    imwrite(sr_img, save_path)
    print("step4 end")
    
from flask import send_from_directory

@app.route('/csv_file_download_with_file', methods=['POST'])
def csv_file_download_with_file(): 
    global filename_
    return send_from_directory('static/denoised/',filename_,
                     as_attachment=True)

# 서버실행
app.run(debug=True, port=5001)

