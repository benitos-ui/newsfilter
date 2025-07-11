from flask import Flask,render_template,request
from models import Utilisateur
from data import session

app=Flask(__name__)
@app.route("/")
def afficher_register():
    return render_template('register.html')

@app.route("/traiter_register",methods=['POST'])
def traiter_register():
    result=request.form
    utilisateur=Utilisateur(
        email=result.get('email'),
        username=result.get('username')
    )
    session.add(utilisateur)
    session.commit()
    return render_template('index.html')


app.run()