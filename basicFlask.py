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
    
    <form method="get" action="csv_file_download_with_file">
        <button type="submit">Download!</button>
    </form>
    '''

from flask import send_file

@app.route('/csv_file_download_with_file')
def csv_file_download_with_file():
    file_name = f"static/uploads/Background.png"
    return send_file(file_name,
                     as_attachment=True)

app.run(debug=True)