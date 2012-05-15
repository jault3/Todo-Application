from sys import path
import os, functools, pickle
path.append(os.getcwd()+"\\Lib\\site-packages")

import flask, flask.views
from flask import json
from wtforms import Form, BooleanField, TextField, SelectMultipleField, validators
app = flask.Flask(__name__)

app.secret_key = os.urandom(24)

todoList = {}

#This class extending the Form class creates a SelectMultipleField to allow the
#user to choose multiple tasks to mark as complete
class MarkAsCompleteForm(Form):
    Tasks = SelectMultipleField('Tasks',choices=[])

class ListTasks():
    def __init__(self):
        stringList = ''
        with open('todo.json','rb') as fp:
            todoList = dict(json.load(fp))
        for key in todoList.keys():
            stringList=stringList+key
        flask.flash(stringList)
    
class Main(flask.views.MethodView):
    def get(self):
        with open('todo.json','rb') as fp:
            todoList = dict(json.load(fp))
        form = MarkAsCompleteForm(flask.request.form)
        form.Tasks.choices = [(key,key+' - By: '+todoList[key]) for key in todoList.keys()]
        return flask.render_template('index.html',form=form)

    def post(self):
        chosen = flask.request.form['Tasks']
        with open('todo.json','rb') as fp:
            todoList = dict(json.load(fp))
        todoList[chosen] = "COMPLETED"
        with open('todo.json','wb') as fp:
            json.dump(todoList,fp)
        return flask.redirect(flask.url_for('index'))

class AddTask(flask.views.MethodView):
    def get(self):
        return flask.render_template('addTask.html')

    def post(self):
        with open('todo.json','rb') as fp:
            todoList = dict(json.load(fp))
        task = flask.request.form['description']
        dateToFinish = flask.request.form['finishBy']
        todoList[task] = dateToFinish
        with open('todo.json','wb') as fp:
            json.dump(todoList,fp)
        flask.flash("Your task has been successfully added!  Redirecting...")
        return flask.redirect(flask.url_for('addTask'))

class DeleteTask(flask.views.MethodView):
    def get(self):
        with open('todo.json','rb') as fp:
            todoList = dict(json.load(fp))
        count = 1
        for key in todoList.keys():
            flask.flash(count)
            flask.flash(') ')
            flask.flash(key)
            count = count +1
        return flask.render_template('deleteTask.html')

    def post(self):
        with open('todo.json','rb') as fp:
            todoList = dict(json.load(fp))
        taskChoice = int(flask.request.form['taskChoice'])
        taskChoice = taskChoice-1
        keys = todoList.keys()
        try:
            key = keys[taskChoice]
            del todoList[key]
            with open('todo.json','wb') as fp:
                json.dump(todoList,fp)
            flask.flash('Removed.')
        except:
            key = 'Please choose one of the options below.'
        return flask.redirect(flask.url_for('deleteTask'))
  
app.add_url_rule('/',view_func=Main.as_view('index'), methods=['GET','POST'])
app.add_url_rule('/addTask/',view_func=AddTask.as_view('addTask'),methods=['GET','POST'])
app.add_url_rule('/deleteTask/',view_func=DeleteTask.as_view('deleteTask'),methods=['GET','POST'])

app.debug = True
app.run()

