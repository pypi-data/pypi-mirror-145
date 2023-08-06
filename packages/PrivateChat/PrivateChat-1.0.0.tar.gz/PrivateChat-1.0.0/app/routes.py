from reprlib import recursive_repr
from flask import render_template, flash, redirect, url_for, request
from flask_login import ID_ATTRIBUTE, current_user, login_required, login_user, logout_user
from app import app, db
from app.models import User, Post, Group
from app.forms import LoginForm, SignupForm, MessageForm, GroupCreateForm
from werkzeug.urls import url_parse
from sqlalchemy import or_, and_

#route of the index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == 'POST':
        members = request.form.getlist('createGroup')
        name = request.form.get('groupName')
        newGroup=Group()
        newGroup.name=name
        newGroup.participants.append(User.query.filter_by(id=current_user.get_id()).first())
        for member in members:
            newGroup.participants.append(User.query.filter_by(id=member).first())
        if(len(newGroup.participants) <3):
            return redirect(url_for('index'))
        db.session.add(newGroup)
        db.session.commit()
        return redirect(url_for('index'))


    choices=[(user.id, user.username) for user in getOnline()]
    form = GroupCreateForm()
    form.member.choices = choices
    form.member.name = "createGroup"
    form.name.label="Groepsnaam"

    return render_template('index.html',users=getOnline(), groups=getGroups(current_user.get_id()), forms=form)

#route of the loging page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        print(form.remember_me.data)
        user.set_online(True)
        db.session.add(user)
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#route of logging out
@app.route('/logout')
def logout():
    current = User.query.filter_by(id=current_user.get_id()).first()
    current.set_online(False)
    db.session.add(current)
    db.session.commit()
    logout_user()

    return redirect(url_for('index'))

#route of the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Geregistreerd!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

#route of the 1-1 chatting page
@app.route('/user/<int:person>', methods=['GET', 'POST'])
@login_required
def user(person):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    #retrieves and prints only messages authored by other person, or current_user is only recipient
    messages=[]
    user = User.query.filter_by(id=current_user.get_id()).first()
    for post in Post.query.join(User, Post.recipients).all():
        if post.author_id==int(current_user.get_id()) or (user in post.recipients and len(post.recipients)==1):
            messages.append(post)
    
    #send message
    form = MessageForm()
    if form.validate_on_submit():
        message = Post(body=form.message.data)
        message.author=user
        message.recipients.append(User.query.filter_by(id=person).first())
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('user', person=person))
        
    return render_template('user.html',users=getOnline(), messages=messages, form=form)


#route of the group-chatting page
@app.route('/group/<int:groupid>', methods=['GET', 'POST'])
@login_required
def group(groupid):
    if (not current_user.is_authenticated):
        return redirect(url_for('login'))

    #makes sure user is part of the group
    groupInfo = Group.query.filter_by(id=groupid).first()
    user = User.query.filter_by(id=current_user.get_id()).first()
    if(user not in groupInfo.participants):
        return redirect(url_for('index'))

    #retrieves and prints messages
    messages=[]
    for post in groupInfo.messages:
        messages.append(post)
    
    #send message
    form = MessageForm()
    if form.validate_on_submit():
        message = Post(body=form.message.data)
        message.author=user
        for groupUser in groupInfo.participants:
            message.recipients.append(groupUser)
        groupInfo.messages.append(message)
        db.session.add(message)
        db.session.add(groupInfo)
        db.session.commit()
        return redirect(url_for('group', groupid=groupid))
        
    return render_template('user.html',users=getOnline(), messages=messages, form=form)

#returns a list of all online users, excluding the current user
def getOnline():
    users = User.query.all()
    onlineUsers = []
    for user in users:
        if(user.is_online() and (user.id != int(current_user.get_id()))):
            onlineUsers.append(user)
    return onlineUsers

#returns a list of groups the user is in
#userid = the user ID of the requested user.
def getGroups(userid):
    groups=[]
    user = User.query.filter_by(id=userid).first()
    for group in Group.query.all():
        if(user in group.participants):
            groups.append(group)
    return groups