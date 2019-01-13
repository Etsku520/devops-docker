from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy.sql import text

from application import app, db, login_required
from application.messages.models import Message
from application.messages.forms import MessageForm
from application.auth.models import Role, User
from application.groups.forms import GroupForm, GroupcategoryFrom
from application.groups.models import Groups, GroupCategory, Category

@app.route("/new/<group_id>/message")
@login_required()
def message_form(group_id):
    return render_template("messages/newMessage.html", form = MessageForm(), group_id=group_id)

@app.route("/messages/<message_id>/")
@login_required()
def modify_message_form( message_id):
    m = Message.query.get(message_id).text
    form = MessageForm()
    form.name.default = m
    form.process()
    
    return render_template("messages/modifyMessage.html", oldMessage = m, form = form)

@app.route("/messages/<message_id>/", methods=["POST"])
@login_required()
def modify_message(message_id):
    form = MessageForm(request.form)

    if not form.validate():
        return render_template("messages/modifyMessage.html", form = form)
    
    m = Message.query.get(message_id)
    if m.account_id == current_user.id or current_user.get_role().role == "ADMIN":
        m.text = form.name.data
        db.session.commit()

    return redirect(url_for("group_messages", group_id = m.group_id))

@app.route("/new/<group_id>/message", methods=["POST"])
@login_required()
def message_new(group_id):
    form = MessageForm(request.form)
    if not form.validate():
        return render_template("messages/newMessage.html", form = form)
        
    m = Message(form.name.data)
    m.text = m.text
    m.account_id = current_user.id
    m.group_id = group_id

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("group_messages", group_id=group_id))

@app.route("/messages/<message_id>/delete", methods=["POST"])
@login_required()
def delete_message(message_id):
    m = Message.query.get(message_id)
    if m.account_id == current_user.id or current_user.get_role().role == "ADMIN":
        db.session.delete(m)
        db.session.commit()

    return redirect(url_for("group_messages", group_id = m.group_id))