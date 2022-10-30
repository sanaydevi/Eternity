from application import app, db
from flask import render_template, request, json, Response, redirect, flash, url_for, session
from application.models import User, Relationships
from application.forms import LoginForm,Registration,AddRelations
from flask_login import login_required, current_user
import sounddevice as sd
from scipy.io.wavfile import write
import uuid
import os


# fs = 44100  # Sample rate
# seconds = 3  # Duration of recording
#
# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
# sd.wait()  # Wait until recording is finished
# write('output.wav', fs, myrecording)  # Save as WAV file

@app.route('/recorder', methods=['GET','POST'])
def recorder():
    if session.get('username'):
        user_id = (session.get('user_id'))
        if request.method == "GET":
            classes = list(User.objects.aggregate(*[[
                {
                    '$lookup': {
                        'from': 'relationships',
                        'localField': 'user_id',
                        'foreignField': 'user_id',
                        'as': 'r1'
                    }
                }, {
                    '$unwind': {
                        'path': '$r1',
                        'includeArrayIndex': 'r1_id',
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'user_id': user_id
                    }
                }
            ]]))
        return render_template("recorder.html", login=True,classes=classes, messageRecorded=False)
    else:
        return render_template("recorder.html", login=False, messageRecorded=False)

@app.route('/save-record', methods=['GET','POST'])
def save_record():
    print("SAVE/Record")
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".mp3"
    print(file_name)
    full_file_name = os.path.join(r"/Users/sanaydevi/PycharmProjects/Eternity/application/uploads/", file_name)
    file.save(full_file_name)
    if session.get('username'):
        print("siiiiiiiiii")
        return render_template("recorder.html", login=True, messageRecorded=True)
    else:
        return render_template("recorder.html", login=False, messageRecorded=False)

@app.route('/relations',methods=['GET','POST'])
def relation():
        add_relations = AddRelations()
        if request.method == "GET":
            if session.get('username'):
                user_id = (session.get('user_id'))


                if request.method == "GET":
                    classes = list(User.objects.aggregate(*[[
                        {
                            '$lookup': {
                                'from': 'relationships',
                                'localField': 'user_id',
                                'foreignField': 'user_id',
                                'as': 'r1'
                            }
                        }, {
                            '$unwind': {
                                'path': '$r1',
                                'includeArrayIndex': 'r1_id',
                                'preserveNullAndEmptyArrays': False
                            }
                        }, {
                            '$match': {
                                'user_id': user_id
                            }
                        }
                    ]]))

                return render_template("relationships.html",login=True,relation=add_relations,classes=classes)
            else:
                return render_template("relationships.html",login=False,relation=add_relations)

        if request.method == "POST":
            # session.pop('username',None)
            if add_relations.validate_on_submit():
                try:
                    user_id = session.get('user_id')
                    name = request.form.get("name")
                    email = request.form.get("email")
                    number = request.form.get("number")
                    famMem = Relationships(user_id=user_id, email=email, name=name, phone_number=number)
                    famMem.save()
                    flash("Added relationship!", "success")
                    classes = list(User.objects.aggregate(*[[
                        {
                            '$lookup': {
                                'from': 'relationships',
                                'localField': 'user_id',
                                'foreignField': 'user_id',
                                'as': 'r1'
                            }
                        }, {
                            '$unwind': {
                                'path': '$r1',
                                'includeArrayIndex': 'r1_id',
                                'preserveNullAndEmptyArrays': False
                            }
                        }, {
                            '$match': {
                                'user_id': user_id
                            }
                        }
                    ]]))

                except:
                    flash("Sorry, something went wrong.", "danger")
                finally:
                    return render_template("relationships.html",login=True,relation=add_relations,classes=classes)
        return render_template("relationships.html", login=True, relation=add_relations)


@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    if session.get('username'):
        return render_template("index2.html", login=True, index=True)
    else:
        return render_template("index2.html", login=False, index=True)



@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    registration = Registration()
    if request.method == "POST":
        session.pop('username',None)
        if registration.validate_on_submit():
            try:
                user_id = User.objects.count()
                user_id += 1
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                email = request.form.get("email")
                password = request.form.get("password")
                user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
                user.set_password(password)
                user.save()
                flash("Registration successfull!", "success")
            except:
                flash("Sorry, something went wrong.", "danger")
            finally:
                return render_template("login.html", title="Login", form=form, registration=registration, loginFlag=True,
                                       login=False)
        elif form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.objects(email=email).first()
            if user and user.get_password(password):
                flash(f"{user.first_name}, you are successfully logged in!", "success")
                #session.permanent = False
                session['user_id'] = user.user_id
                session['username'] = user.first_name
                return redirect(url_for('index', login=True))
            else:
                flash("Sorry, something went wrong.", "danger")
        if request.method == "GET":
            if session.get('username'):
                return redirect(url_for('index', login=True))
    return render_template("login.html", title="Login",form=form,registration=registration,loginFlag=False, login=False)

@app.route("/logout")
def logout():
    session['user_id']=False
    session.pop('username',None)
    return redirect(url_for('index'))

# @app.route('/register')
# def register():
#     return render_template("register.html", register=True, login=False)
#

# @app.route("/user")
# def user():
#     User(user_id=6,first_name="Sanay",last_name="Devi",email="sanaydevi@gmail.com",password="M@nu1212").save()
#     User(user_id=7, first_name="Jainetri", last_name="Merchant", email="jainetrimerhcant@gmail.com", password="M@nu1212").save()
#     users = User.objects.all()
#     return render_template("user.html",users=users)