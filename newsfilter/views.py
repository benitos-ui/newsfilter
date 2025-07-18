from flask import Flask,render_template,request,abort,redirect,url_for,session
from models import Utilisateur,User,UserPreferences
from data import session as db_session
from flask_mail import Message,Mail
from random import *
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField,SelectMultipleField,widgets
from wtforms.validators import DataRequired,Length,Email,NumberRange,EqualTo
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.exc import IntegrityError
import os
from sqlalchemy.orm import relationship
from wtforms.widgets import ListWidget, CheckboxInput
from dotenv import load_dotenv

load_dotenv()


#email="benitoatigossou@gmail.com"
app=Flask(__name__)
app.secret_key="secret"

class Config:
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_DEBUG=app.debug
    MAIL_USERNAME=os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_MAX_EMAILS=None
    MAIL_SUPPRESS_SEND=app.testing
    MAIL_ASCII_ATTACHEMENTS=False

app.config.from_object(Config)

mail=Mail(app)


@app.route("/a_oublie")
def afficher_register():
    return render_template('register.html')

class RegisterForm(FlaskForm):
    nom=StringField("Nom",validators=[DataRequired()])
    prenom=StringField("Prenom",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired(),Email()])
    age=IntegerField("age",validators=[DataRequired(),NumberRange(min=1,max=200,message="l'age doit etre positif")])
    pays=StringField("Pays",validators=[DataRequired()])
    ville=StringField("Ville",validators=[DataRequired()])
    submit=SubmitField("S'inscrire")

class Code(FlaskForm):
    code=IntegerField("code",validators=[DataRequired(),NumberRange(min=10000,max=99999,message="code invalide")]) 
    submit=SubmitField("Envoyer")   

class userform(FlaskForm) :
    username=StringField("Nom d'utilisateur",validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[
        DataRequired(), Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères.")
    ])
    confirm_password = PasswordField("Confirmer le mot de passe", validators=[
        DataRequired(), EqualTo("password", message="Les mots de passe ne correspondent pas.")
    ])
    submit=SubmitField("Envoyer")

class loginform(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")    



THEMES=[     (1,'Politique'),
             (2,'Sport'),
             (3,'Culture'),
             (4,'Santé'),
             (5,'Technologie'),
             (6,'International'),
             (7,'Economie'),
             (8,'Environnement'),
             (9,'Education'),
             (10,'Autre')
        ]  

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class Choiceform(FlaskForm):
    theme=MultiCheckboxField("Choisir vos thèmes préférés",coerce=int)
    submit=SubmitField("Enregistrer vos préférences")

    
   
    
    
    



@app.route("/traiter_register",methods=['POST','GET'])
def traiter_register():
    form=RegisterForm()
    if form.validate_on_submit():
      utilisateur=Utilisateur(
             email=form.email.data,
             nom=form.nom.data,
             prenom=form.prenom.data,
             pays=form.pays.data,
             age=form.age.data,
             ville=form.ville.data
    )
      db_session.add(utilisateur)
      db_session.commit()
      return redirect(url_for('send_email',email=utilisateur.email))
    return render_template('register.html',form=form)


emailsend=True

@app.route("/send_email",methods=['POST','GET'])
def send_email():
   
    validcode=Code()  


    if request.method=='GET':
         email = request.args.get('email') 
         global emailsend
         emailsend=False 
         code=randint(10000,99999)
         session['code'] = str(code)
         session['email'] = email

         msg=Message(
        subject="Confirmation de l'email",
        recipients=[email],
        sender='sodjine558@gmail.com',
        body=f"Nous vous avoyons ce code afin de vérifier votre adresse email.Veuiller copier le code de confirmation ci-dessous.\nVotre code de confirmation est {code}"
    )   
         if emailsend==False:
            mail.send(msg)
            emailsend=True
         return render_template('index.html', validcode=validcode)

    elif request.method=='POST' and  validcode.validate_on_submit():
        code_saisi=str(validcode.code.data)
        code_attendu=session.get('code')
        if code_attendu==code_saisi:
           return redirect (url_for('register_suite'))
        
        else:
              return render_template('register_suite.html', validcode=validcode, erreur="Code incorrect")
        

   
    
    
    return render_template('index.html',validcode=validcode)

 

@app.route("/register_suite",methods=['POST','GET'])
def register_suite():
    form=userform()
    if form.validate_on_submit():
        usr=User(
            username=form.username.data
        )
        usr.set_password(form.password.data)
        db_session.add(usr)
        db_session.commit()
        return redirect(url_for('login'))
    return render_template("register_suite.html",form=form)


    return render_template("register_suite.html")        

@app.route("/",methods=['POST','GET'])
def login():
    form=loginform()
    erreur = None

    if form.validate_on_submit():
        
        
        user=db_session.query(User).filter_by(username=form.username.data).first()

        
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id

            if db_session.query(UserPreferences).filter_by(user_id=user.id).first() is None:
                return redirect(url_for("choices"))
            
            return redirect(url_for("dashboard"))  
        else:
            erreur = "Username ou mot de passe incorrect."

    return render_template("login.html", form=form, errors=erreur)

@app.route("/choices",methods=['POST','GET'])
def choices():
   form=Choiceform()
   form.theme.choices=THEMES
   
   if form.validate_on_submit():
       selected_themes=form.theme.data
       userpreference=UserPreferences(
            theme=selected_themes,
            user_id=session.get("user_id")
       )
       db_session.add(userpreference)
       db_session.commit()
       return redirect(url_for("dashboard"))
   return render_template("choices.html",form=form)


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route('/logout')
def logout():
    session.pop('utilisateur_id', None)
    return redirect(url_for('login'))






if __name__=='__main__':
    app.run(debug=True)

