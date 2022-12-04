from flask import Flask



app = Flask(__name__)

topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'} 
]

@app.route('/')
def index():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return f''' <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {liTags}
            </ol>
            <h2>Welcome</h2>
            Hello, Web
        </body>
    </html>'''  
@app.route('/create/')
def create():
    return 'Create'

@app.route('/read/<int:num>/')
def read(num):
    title = ''
    body = ''
    for topic in topics:
        if num == topic['id']:
            title = topic['title']
            body = topic['body']
    return f''' <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1><a href="/">{title}</a></h1>
            <h2>{body}</h2>
            
        </body>
    </html>'''  

# 아래는 파일 다운로드를 위한 예시
@app.route("/file_download")
def hello():
    return '''
    <a href="/csv_file_download_with_file">Click me.</a>
    
    <form method="POST" action="/">
        <input
                type="submit"
                name="down"
                id="down-submit"
                formaction="csv_file_download_with_file"
            />
    </form>
    '''

from flask import send_file
from flask import Flask, flash, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename


@app.route('/csv_file_download_with_file', methods=['GET', 'POST'])
def csv_file_download_with_file():
    file = request.files['file']
    file_name = secure_filename(file.filename)
    
    # Create Model
    opt_path = 'NAFNet/options/test/SIDD/NAFNet-width64.yml'
    opt = parse(opt_path, is_train=False)
    opt['dist'] = False
    NAFNet = create_model(opt) 
    print("step1")
    
    # Inference and Show results
    input_path = file_name
    output_path = 'NAFNet/demo_output/noisy-demo-4.png'
    print("step2")

    img_input = imread(input_path)
    print("step3")
    inp = img2tensor(img_input)
    print("step4")
    single_image_inference(NAFNet, inp, output_path)
    print("step5")

    return send_file(file_name,
                     as_attachment=True)


# denosing 

import torch
from basicsr.models import create_model
from basicsr.utils import img2tensor as _img2tensor, tensor2img, imwrite
from basicsr.utils.options import parse
import numpy as np
import cv2
import matplotlib.pyplot as plt

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


app.run(debug=True)