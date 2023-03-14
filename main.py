from pickle import TRUE
import uuid
from flask import Flask, redirect, render_template, request, url_for, session
import hashlib
from flask_sqlalchemy import SQLAlchemy
from models import Booking, User, Listroom, getdb,Reviews
from datetime import timedelta
from flask_login import current_user,login_user,LoginManager,logout_user
import os
import datetime
import json
import random
db = getdb()
DB_NAME = "database.db"


app = Flask(__name__)

app.config['SECRET_KEY'] = 'random string'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['upload_folder']='static/upload/'
app.permanent_session_lifetime = timedelta(minutes=5)
db.init_app(app)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route("/")
def index():
    rooms=Listroom.query.all()
    room=[]
    for _ in range(8):
        z=random.choice(rooms)
        room.append(z)
        rooms.remove(z)
    rev=Reviews.query.all()
    return render_template("index.html",login=0,ra=rev,user=current_user,link=room)

login_manager=LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(id):
    user=User.query.get(int(id))
    return user


@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == hashlib.sha256(password.encode('utf-8')).hexdigest():
                login_user(user,remember=True)
                return redirect(url_for('index'))
        return redirect(url_for('register'))


    return redirect(url_for('index'))

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        user_name = request.form['name']
        password = request.form['password']
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        isowner = request.form['user']

        if isowner == 'host' :
            isowner = True
        else:
            isowner = False

        user =  User(email=email,password=password, user_name=user_name,isowner=isowner)
        db.session.add(user)
        db.session.commit()
        login_user(user,remember=True)
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('register.html')

@app.route("/list_a_room",methods=['GET','POST'])
def list_a_room():
    if request.method == 'GET':   
        if current_user:
            return render_template('list_a_room.html')
        else:
            return render_template("index.html",login=1)
    elif request.method == 'POST':
        if current_user.isowner==True:
            data=dict(request.form)
            pic=request.files['profile_pic']
            pic_name=str(uuid.uuid1())+"."+(pic.filename.split('.'))[-1] 
            pic.save(os.path.join(app.config['upload_folder'],pic_name))       
            {'host_phone_number': '222', 'city': '22222', 'homestay_name': 'asdfSD', 'homestay_address': 'dsvD', 
            'homestay_discription': 'DZCADSDVdsvDSvdv', 'homestay_number': 'dsVZDV', 'homestay_capacity': 'zxVZVZDV', 
            'Open_Seating_areas': 'True',
            'Air_Condition': 'True', 'Television': 'True', 'Pet_Friendly': 'True'}
            l=['Parking','Internet','Running_Hot_water','Open_Seating_areas',"Air_Condition","Pet_Friendly","Toiletries","Smoking_Allowed","Library","Bonfire","Barbecue","Pick_and_dropService"]
            for i in l:
                if i not in data.keys():
                    data[i]=False
                else:
                    data[i]=True
            print(data)
            list=Listroom(phone_no= int(data['host_phone_number']),
            city = data['city'].capitalize(),
            host_name = data['host_name'],
            homestay_name = data['homestay_name'],
            address = data['homestay_address'],
            description= data['homestay_discription'],
            no_of_room = data['homestay_capacity'],
            Parking = data["Parking"],
            Internet = data["Internet"],
            Running_Hot_water = data["Running_Hot_water"],
            Open_Seating_areas = data["Open_Seating_areas"],
            Air_Condition = data["Air_Condition"],
            Pet_Friendly = data["Pet_Friendly"],
            Toiletries = data["Toiletries"],
            Smoking_Allowed = data["Smoking_Allowed"],
            Library = data["Library"],
            Bonfire = data["Bonfire"],
            Barbecue = data["Barbecue"],
            Pick_and_dropService = data["Pick_and_dropService"],
            rent=data['rent'],
            pic='/static/upload/'+pic_name,
            uid = current_user.id,
            email=current_user.email)
            db.session.add(list)
            db.session.commit()
            with open('static\javascript/insname.json','r') as f:
                l=json.load(f)
            l.append(list.city)
            with open('static\javascript/insname.json','w') as f:
                json.dump(l,f)
            return redirect(url_for('index'))
@app.route('/<room_id>/profile')
def host_profile(room_id):
    room=Listroom.query.filter_by(id=int(room_id)).first()
    print(room)
    if room:
        l=[]
        if room.Parking ==True:
            l.append('Parking')

        if room.Internet ==True:
            l.append('Internet')

        if room.Running_Hot_water ==True:
            l.append('Running_Hot_water')

        if room.Open_Seating_areas ==True:
            l.append('Open_Seating_areas')

        if room.Air_Condition ==True:
            l.append('Air_Condition')

        if room.Pet_Friendly ==True:
            l.append('Pet_Friendly')

        if room.Toiletries ==True:
            l.append('Toiletries')

        if room.Smoking_Allowed ==True:
            l.append('Smoking_Allowed')

        if room.Library ==True:
            l.append('Library')

        if room.Bonfire ==True:
            l.append('Bonfire')

        if room.Barbecue ==True:
            l.append('Barbecue ')

        if room.Pick_and_dropService ==True:
            l.append('Pick_and_dropService')
        return render_template('host_profile.html',host=room,face=l,reviews=Reviews.query.filter_by(room_id=room.id).all())
    else:
        return redirect(url_for('index'))
@app.route('/<room_id>/review',methods=['POST'])
def review(room_id):
    data=request.form
    review=Reviews(review=data['review'],room_id=int(room_id),user_id=current_user.id)
    db.session.add(review)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/<name>')
def gujarat(name):
    
    return render_template(f'{name}.html')


@app.route('/Parking')
def Parking():
    fac=Listroom.query.filter_by(Parking=True).all()
    rev=Reviews.query.all()
    print(fac)
    return render_template('face.html',post=fac,re=rev,user=current_user)
@app.route('/Internet')
def Internet():
    fac=Listroom.query.filter_by(Internet=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Running_Hot_water')
def Running_Hot_water():
    fac=Listroom.query.filter_by(Running_Hot_water=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Open_Seating_areas')
def Open_Seating_areas():
    fac=Listroom.query.filter_by(Open_Seating_areas=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Air_Condition')
def Air_Condition():
    fac=Listroom.query.filter_by(Air_Condition=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Pet_Friendly')
def Pet_Friendly():
    fac=Listroom.query.filter_by(Pet_Friendly=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Toiletries')
def Toiletries():
    fac=Listroom.query.filter_by(Toiletries=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Smoking_Allowed')
def Smoking_Allowed():
    fac=Listroom.query.filter_by(Smoking_Allowed=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Library')
def Library():
    fac=Listroom.query.filter_by(Library=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Bonfire')
def Bonfire():
    fac=Listroom.query.filter_by(Bonfire=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Barbecue')
def Barbecue():
    fac=Listroom.query.filter_by(Barbecue=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)
@app.route('/Pick_and_dropService')
def Pick_and_dropService():
    fac=Listroom.query.filter_by(Pick_and_dropService=True).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)

@app.route('/<room_id>/book',methods=['GET','POST'])
def book(room_id):
    if request.method=='POST':
        data=dict(request.form)
        ar_date=data['arrivals'].split('-')
        ar_date=datetime.datetime(int(ar_date[0]),int(ar_date[1]),int(ar_date[2]))
        le_date=data['leaving'].split('-')
        le_date=datetime.datetime(int(le_date[0]),int(le_date[1]),int(le_date[2]))
        print(data)
        booking=Booking( no_of_rooms= int(data['no_of_rooms']),
        no_of_guest= int(data[ 'no_of_guest']),
        contact_no= int(data[ 'contact_number']),
        date_ar=ar_date,
        date_le=le_date,
        room_id =room_id,
        user_id =current_user.id)
        db.session.add(booking)
        db.session.commit()
        stay=Listroom.query.filter_by(id=int(room_id)).first()
        return render_template('details.html',book=booking,user=current_user,host=stay)      
    return render_template('booking.html')
@app.route('/<city>/city')
def city(city):
    fac=Listroom.query.filter_by(city=city).all()
    rev=Reviews.query.all()
    return render_template('face.html',post=fac,login=0,ra=rev,user=current_user)

@app.route('/contact')
def contact():
    return render_template('contact.html')
if __name__ == '__main__':

    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

    





