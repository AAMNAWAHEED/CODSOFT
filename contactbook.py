from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
app = Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/codsoft'
db = SQLAlchemy(app)
def viewcontacts():
    query = text("select * from contact_book")
    res=db.session.execute(query)
    rows=res.fetchall()
    return rows
@app.route('/')
def main():
    return render_template('contactbook.html',contact_list=viewcontacts())
@app.route('/add')
def addpage():
    return render_template('addcontact.html')
@app.route('/edit',methods=['Get','Post'])
def editecontact():
    if request.method == 'POST':
        id = request.form['contact_id']
        query = text("select * from contact_book where id = :id")
        res = db.session.execute(query,{'id':id})
        row = res.fetchone()
        print(row)

        return render_template('editcontact.html',contact = row)
@app.route("/editcontact",methods=['Get','Post'])
def edit():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        number = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        query = text("update contact_book set contact_name=:name,phone_number=:number,address=:address,email=:email where id = :id ")
        db.session.execute(query,{"id":id,"name":name,"number":number,"address":address,"email":email})
        db.session.commit()
        return render_template('contactbook.html',contact_list=viewcontacts())
    return "error"


@app.route('/delete',methods=['Get','Post'])
def delete():
    if request.method=='POST':
        id = request.form['contact_id']
        query = text("delete from contact_book where id=:id")
        db.session.execute(query,{'id':id})
        db.session.commit()
        return render_template('contactbook.html',contact_list=viewcontacts())
    return render_template('contactbook.html',contact_list=viewcontacts())

@app.route('/addcontact' ,methods=['Get','Post'])
def addcontact():
    if request.method=='POST':
        name = request.form['name']
        number = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        query = text("insert into contact_book(contact_name,phone_number,address,email) values(:name,:number,:address,:email)")
        db.session.execute(query,{"name":name,"number":number,"address":address,"email":email})
        db.session.commit()
        return render_template('contactbook.html',contact_list=viewcontacts())
    return "failed"

@app.route('/search',methods=['Get','Post'])
def search():
    if request.method == 'POST':
        option = request.form['option']
        query = text("select * from contact_book where phone_number = :option or contact_name = :option")
        res = db.session.execute(query,{'option':option})
        rows = res.fetchall()
        if len(rows) == 0 :
            return "no contact exists with this name or number"
        else:
            return render_template("searchcontact.html",contact_list = rows)
    return "error"
if __name__ == '__main__':
    app.run(debug=True)