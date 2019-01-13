from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy.sql import text

from application import app, db, login_required
from application.messages.models import Message
from application.messages.forms import MessageForm
from application.auth.models import Role, User
from application.groups.forms import GroupForm, GroupcategoryFrom
from application.groups.models import Groups, GroupCategory, Category

@app.route("/new/group")
@login_required()
def group_form():
    return render_template("groups/newGroup.html", form = GroupForm())

@app.route("/new/group", methods=["POST"])
@login_required()
def group_new():
    form = GroupForm(request.form)
    if not form.validate():
        return render_template("groups/newGroup.html", form = form)
    
    g = Groups(form.heading.data)
    g.account_id = current_user.id
    db.session().add(g)
    db.session().commit()

    return redirect(url_for("all_groups"))

@app.route("/groups")
def all_groups():
    return render_template("groups/groups.html", groups = Groups.query.all())

@app.route("/groups/<group_id>/modify", methods=["POST"])
@login_required()
def modify_group(group_id):
    form = GroupForm(request.form)

    if not form.validate():
        return render_template("groups/modifyGroup.html", form = form)
    
    g = Groups.query.get(group_id)
    if g.account_id == current_user.id or current_user.get_role().role == "ADMIN":
        g.heading = form.heading.data
        db.session.commit()

    return redirect(url_for("all_groups"))

@app.route("/groups/<group_id>/modify")
@login_required()
def modify_group_form(group_id):
    g = Groups.query.get(group_id).heading
    form = GroupForm()
    form.heading.default = g
    form.process()

    categories = Groups.categories(group_id)

    return render_template("groups/modifyGroup.html", form = form, group_id = group_id, categories = categories)

@app.route("/groups/<group_id>/")
def group_messages(group_id):
    categories = Groups.categories(group_id)
    messages = Groups.findMessagesByGroup(group_id)
    ug = user_getter()
    g = Groups.query.get(group_id)
    return render_template("messages/messages.html", messages = messages, 
        group_id=group_id, g = g, ug = ug, categories = categories, form = MessageForm())

@app.route("/groups/<group_id>/delete", methods=["POST"])
@login_required()
def delete_group(group_id):
    g = Groups.query.get(group_id)
    if g.account_id == current_user.id or current_user.get_role().role == "ADMIN":
        messages  = g.messages
        gcs = GroupCategory.query.filter_by(group_id = group_id)
        for message in messages:
            db.session.delete(message)
        for gc in gcs:
            db.session.delete(gc)
        db.session.delete(g)
        db.session.commit()

    return redirect(url_for("all_groups"))

@app.route("/groups/<group_id>/add_category", methods=["GET", "POST"])
@login_required()
def add_groupcategory(group_id):
    stmt = text("SELECT * FROM Category WHERE category.id NOT IN (SELECT category.id FROM Category, group_category WHERE category.id = Group_category.category_id AND Group_category.group_id = :id)").params(id = group_id)
    res = db.engine.execute(stmt)
    g = Groups.query.get(group_id)

    response = []
    for row in res:
        response.append({"id":row[0], "category":row[3]})

    if request.method == "GET" and (g.account_id == current_user.id or current_user.get_role().role == "ADMIN"):
        return render_template("groups/addGroupcategory.html", response = response, group_id = group_id)

    if g.account_id == current_user.id or current_user.get_role().role == "ADMIN":
        gc = GroupCategory()
        gc.group_id = g.id
        gc.category_id = request.form.get("category")
        db.session().add(gc)
        db.session().commit()

    return redirect(url_for("add_groupcategory", group_id = group_id))

@app.route("/groups/search", methods=["GET", "POST"])
def group_search():
    categories = Category.query.all()
    if request.method == "GET":
        return render_template("groups/groupSearchFrom.html", categories = categories)
    
    return redirect(url_for("group_search_result", category_id = request.form.get("category")))

@app.route("/groups/<group_id>/remove/<category_id>", methods=["POST"])
@login_required()
def remove_groupcategory(group_id, category_id):
    if g.account_id == current_user.id or current_user.get_role().role == "ADMIN":
        gcs = GroupCategory.query.filter_by(group_id = group_id, category_id = category_id)

        for gc in gcs:
            db.session().delete(gc)
        db.session().commit()
    
    return redirect(url_for("modify_group_form", group_id = group_id))

@app.route("/groups/search/<category_id>")
def group_search_result(category_id):
    stmt = text("SELECT DISTINCT Groups.* FROM Groups, Group_category WHERE Groups.id = group_category.group_id AND group_category.category_id = :id ORDER BY groups.date_modified DESC").params(id=category_id)
    res = db.engine.execute(stmt)

    response = []
    for row in res:
        response.append({"id":row[0], "date_created":row[1], "date_modified":row[2], "heading":row[3], "account_id":row[4], "book_id":row[5]})
    
    return render_template("groups/groupSearch.html", groups = response)

class user_getter():
    
    def get_account(self, account_id):
        return User.query.get(account_id)
