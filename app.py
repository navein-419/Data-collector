from flask import Flask , render_template,request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1425@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] ='postgres://zbzyfpfcayhbbi:4680c6a82723be6d33869a0a940f46e827c484ebdf88333790b931d2743bf6af@ec2-54-243-193-59.compute-1.amazonaws.com:5432/d1o7l4gs97600g?sslmode=require'

db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120),unique=True)
    height=db.Column(db.Integer)

    def __init__(self,email,height):
        self.email=email
        self.height=height




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success",methods=["POST"])
def success():
    if request.method=="POST":
        email=request.form["email_name"]
        height=request.form["height_name"]
        print(email,height)

        if db.session.query(Data).filter(Data.email==email).count()==0:
            data=Data(email,height)
            db.session.add(data)
            db.session.commit()
            average_height=db.session.query(func.avg(Data.height)).scalar()
            average_height=(round(average_height,1))
            count=db.session.query(Data.height).count()
            print(average_height)
            send_email(email, height, average_height, count)
            return render_template("success.html")
        return render_template("index.html",
        text="Seems like we've got something from the email address already.")





if __name__=="__main__":
    app.debug=True
    app.run()
