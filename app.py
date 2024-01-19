from flask import Flask,render_template,url_for,request,redirect,flash
from pymongo import MongoClient
import datetime
from bson import ObjectId

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#creating client for mongo
client= MongoClient('localhost',27017)

#creating database
db = client.flask_database
#creating a collection
todos = db.todos
all_todos = todos.find()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method== 'POST':
        content = request.form['content']
        status = request.form['status']
        current_date = datetime.datetime.today()
        formatted_date = current_date.strftime("%Y-%m-%d")
        todos.insert_one({'content':content,'status': status,'date_created':formatted_date})
        return redirect(url_for('index'))
    
    return render_template('index.html')

@app.route("/view")
def view():
    all_todos = todos.find()
    return render_template('view.html',todos=all_todos)

#same as app.route('delete',methods =[post])
@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id":ObjectId(id)})
    return redirect(url_for('view'))

@app.route('/<id>/update/', methods=['POST'])
def update(id):
    task = todos.find_one({"_id":ObjectId(id)})
    return render_template('update_task.html',task=task)

@app.post('/<id>/update_task/')
def update_task(id):
    if request.method== 'POST':
        content = request.form['edit_name']
        status = request.form['status_edit']
        todos.find_one_and_update({"_id":ObjectId(id)},{"$set":{
            'content':content,
            'status':status
        }})
        flash("Updated Successfully",'success')
        return redirect(url_for('view'))

if __name__ == "__main__":
    app.run(debug=True)