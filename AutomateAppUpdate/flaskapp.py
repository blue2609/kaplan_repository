from flask import Flask,render_template,url_for
from application import getApps


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('mainPage.html',mbats_apps_df=getApps.getMBATSApps())

if __name__ == '__main__':
    app.run(debug=True)