from flask import Flask,render_template,request,redirect,url_for,flash,session
import requests
import sqlite3 as sql

app = Flask(__name__)

URL = "https://api.mfapi.in/mf/"

app.secret_key = "selva411"

@app.route('/add',methods= ['POST','GET'])
def home():
         if request.method=='POST':
            fundcode=request.form.get("fundcode")
            api=requests.get(URL+str(fundcode))
            api_js=api.json()
            name=request.form.get('name')
            fund_house=api_js.get('meta').get('fund_house')
            invested_amount=request.form.get('investedamount')
            unitheld=request.form.get('unitsheld')
            nav=api_js.get('data')[0].get('nav')
            currentvalue=float(nav)*float(invested_amount)
            growth=float(currentvalue)-float(unitheld)
            conn = sql.connect('user.db')
            cur = conn.cursor()
            cur.execute("insert into datas_table (NAME,FUNDCODE,INVESTED,UNITSHELD,NAV,CURRENT_VALUE,GROWTH) values (?,?,?,?,?,?,?)",
                        (name,fund_house,invested_amount,unitheld,nav,currentvalue,growth))
            conn.commit()
            return redirect(url_for('login'))
         return render_template('add_user.html')

@app.route('/read')
def read():
    conn = sql.connect('user.db')
    conn.row_factory = sql.Row
    cur = conn.cursor()
    cur.execute('select * from datas_table')
    data = cur.fetchall()
    return render_template('home.html',data=data)



@app.route('/edit_user/<string:id>',methods=['POST','GET'])
def edit_user(id):
            if request.method =='POST':
                fundcode=request.form.get("fundcode")
                api=requests.get(URL+str(fundcode))
                api_js=api.json()
                name=request.form.get('name')
                fund_house=api_js.get('meta').get('fund_house')
                invested_amount=request.form.get('investedamount')
                unitsheld=request.form.get('unitsheld')
                nav=api_js.get('data')[0].get('nav')
                currentvalue=float(nav)*float(invested_amount)
                growth=float(currentvalue)-float(unitsheld)
                conn = sql.connect('user.db')
                cur = conn.cursor()
                cur.execute("update datas_table set NAME=?,FUNDCODE=?,INVESTED=?,UNITSHELD=?,NAV=?,CURRENT_VALUE=?,GROWTH=? where ID=?",
                            (name,fund_house,invested_amount,unitsheld,nav,currentvalue,growth,id))
                conn.commit()
                flash("user Updated","succes")
                return redirect(url_for('read'))
            conn = sql.connect("user.db")
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("select * from datas_table where ID=?",(id,))
            data = cur.fetchone()
            return render_template('edit_user.html',datas=data)




   
@app.route("/delete_user/<string:id>",methods=['GET'])
def delete_user(id):
    conn = sql.connect('user.db')
    cur = conn.cursor()
    cur.execute("delete from datas_table where ID=?",(id,))
    conn.commit()
    flash("User Deleted","warning")
    return redirect(url_for('read'))


@app.route("/si",methods=['POST','GET'])
def signin():
      if request.method =='POST':
            name = request.form['name']
            password = request.form['password']
            conn =sql.connect('user.db')
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute('insert into login (NAME,PASSWORD) values(?,?)',(name,password))
            conn.commit()
            return redirect(url_for('home'))
      return render_template('signup.html')


d_session ={}

@app.route("/",methods=['POST','GET'])
def login():
      if request.method =='POST':
            name = request.form['name']
            password = request.form['password']
            conn =sql.connect('user.db')
            conn.row_factory = sql.Row
            cur = conn.cursor()
            cur.execute("select * from  login  where NAME=?",(name,))
            data = cur.fetchone()
            if data :
                if data['name'] == name  and  data['password'] == password:
                    d_session.update({'name':data['name']})
                    return redirect(url_for('session'))             
            else:
                    return'<h3>user is not exit </h3>'        
      return render_template('login.html')

     

@app.route('/session')
def session():
      conn = sql.connect('user.db')
      conn.row_factory = sql.Row
      cur =conn.cursor()
      cur.execute("select * from datas_table where NAME=?",(d_session["name"],))
      data = cur.fetchall()
      return render_template('home.html',data=data)


if __name__ == "__main__":
    app.run(debug=True)
