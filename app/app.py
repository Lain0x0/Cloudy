""" Cloudy Storage Code By: 0xv98 """

from flask import Flask, render_template

app = Flask(__name__, template_folder='/home/yuun/cloudy_app/templates',
            static_folder='/home/yuun/cloudy_app/styles')


@app.route('/')
def hello():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
