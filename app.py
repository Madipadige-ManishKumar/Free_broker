from flask import Flask, render_template, request,send_from_directory
import  dbaccess as db
import os
import sqlite3
UPLOAD_FOLDER = 'static'
U=""
class seehouses:
    def myhouse(self):
      conn,cursor=db.get_db_connection()
      self.id=cursor.execute("SELECT houseid FROM houses").fetchall()
      self.name=cursor.execute("SELECT name FROM houses").fetchall()
      self.pincode=cursor.execute("SELECT pincode FROM houses").fetchall()
      self.img=cursor.execute("SELECT img FROM houses").fetchall()
      self.address=cursor.execute("SELECT address FROM houses").fetchall()
      self.rem=cursor.execute("SELECT rem  FROM houses").fetchall()

class houses:
    def myhouse(self,S):
      conn,cursor=db.get_db_connection()
      self.address=cursor.execute("SELECT address FROM houses WHERE sellerid=?", (S,)).fetchall()
      self.id=cursor.execute("SELECT houseid FROM houses WHERE sellerid=?", (S,)).fetchall()
      self.name=cursor.execute("SELECT name FROM houses WHERE sellerid=?", (S,)).fetchall()
      self.pincode=cursor.execute("SELECT pincode FROM houses WHERE sellerid=?", (S,)).fetchall()
      self.img=cursor.execute("SELECT img FROM houses WHERE sellerid=?", (S,)).fetchall()
    def house_details(self, S):
        conn, cursor = db.get_db_connection()
        # cursor.execute("SELECT address, phno, price, email, area, bedrooms, bathrooms, stoires, mainroad, guestroom, basement, waterheater, AC,parkingslot, prearea, furshing_status FROM houses WHERE houseid=?", (S,))
        self.name  =cursor.execute("SELECT name FROM houses WHERE houseid=?", (S,)).fetchone()
        self.pincode=cursor.execute("SELECT pincode FROM houses WHERE houseid=?", (S,)).fetchone()
        self.address=cursor.execute("SELECT address FROM houses WHERE houseid=?", (S,)).fetchone()
        self.phonenumber=cursor.execute("SELECT phno FROM houses WHERE houseid=?", (S,)).fetchone()
        self.price=cursor.execute("SELECT  price FROM houses WHERE houseid=?", (S,)).fetchone()
        self.email=cursor.execute("SELECT email FROM houses WHERE houseid=?", (S,)).fetchone()
        self.area=cursor.execute("SELECT   area FROM houses WHERE houseid=?", (S,)).fetchone()
        self.noofbedrroms=cursor.execute("SELECT bedrooms FROM houses WHERE houseid=?", (S,)).fetchone()
        self.noofbathrooms=cursor.execute("SELECT bathrooms FROM houses WHERE houseid=?", (S,)).fetchone()
        self.stoires=cursor.execute("SELECT stoires FROM houses WHERE houseid=?", (S,)).fetchone()
        self.mainroad=cursor.execute("SELECT mainroad FROM houses WHERE houseid=?", (S,)).fetchone()
        self.GuestRoom=cursor.execute("SELECT guestroom FROM houses WHERE houseid=?", (S,)).fetchone()
        self.basement =cursor.execute("SELECT basement FROM houses WHERE houseid=?", (S,)).fetchone()
        self.heatwater=cursor.execute("SELECT waterheater FROM houses WHERE houseid=?", (S,)).fetchone()
        self.aircondintionar=cursor.execute("SELECT AC FROM houses WHERE houseid=?", (S,)).fetchone()
        self.parkingslot=cursor.execute("SELECT  parkingslot FROM houses WHERE houseid=?", (S,)).fetchone()
        self.prearea=cursor.execute("SELECT prearea FROM houses WHERE houseid=?", (S,)).fetchone()
        self.furshing=cursor.execute("SELECT furshing_status FROM houses WHERE houseid=?", (S,)).fetchone()
        self.img=cursor.execute("SELECT img FROM houses WHERE houseid=?", (S,)).fetchone()
        self.rem=cursor.execute("SELECT rem  FROM houses WHERE houseid=?", (S,)).fetchone()




       
            # Handle the case where no results were found for the given seller and name
            # You can set default values or handle the situation accordingly
app = Flask(__name__)
def exception(e):
    return "<script> alert('{ex}')</script>".format(ex=e)

@app.errorhandler(Exception)
def handle_error(error):
    exception_name = error.__class__.__name__
    # Log the error or perform any other desired actions
    print(f"An error occurred: {str(error)}")
    # You can return a custom error page or response here if needed
    # For example, return a JSON response with an error message
    return "<script>alert('{err}'+'Please Try again')</script>".format(err=exception_name) # 500 is the HTTP status code for Internal Server Error 



@app.route("/")
def main():
    try:
        return render_template("index.html")
    except  Exception as e:
        exception(e)

@app.route("/AboutUs")
def  About_Us():
    try:
        return render_template("AboutUs.html")  
    except Exception as e:
        exception(e)
@app.route("/login")
def login():
    try:
        return render_template("loginpage.html")
    except Exception as e:
        exception(e)
@app.route("/signup")
def signup():
    try:
        return render_template("signuppage.html")
    except Exception as e:
        exception(e)
@app.route("/homepage")
def home_seller():
    return render_template("sellerhome.html")
@app.route("/homepage1")
def home_buyer():
    return render_template("buyerhome.html")
@app.route("/signupdb",methods=['GET','POST'])
def signupdb():
        U=request.form.get('name')
        E=request.form.get('email')
        P=request.form.get('password')
        Phno=request.form.get('phno')
        o=request.form.get('useras')
        db.signup(U,E,P,Phno,o)
     
        return   render_template("loginpage.html")
@app.route("/logindb",methods=['GET','POST'])
def logindb():
    global id 
    
    try:
        global U,P,n
        U=request.form.get('name')
        P=request.form.get('password')
        n=db.login(U,P)
    
        if n=="yess":
            query="select * from seller where name='{u}'and password='{p}'".format(u=U,p=P)
            conn,cursor=db.get_db_connection()
            cursor.execute(query)   
            print("Good Bye")
            m=cursor.fetchone()
            id=int(m[0])
            print(id)
            return render_template("sellerhome.html")
        elif n=="yesb":
            return  render_template("buyerhome.html")
        else :
            return exception("Account is not found")
    except Exception as e:
        exception(e)
@app.route("/seehouse")
def seehouse():
    ob1=seehouses()
    ob1.myhouse()
    for i in range(len(ob1.rem)):
        if  not  ("best seller" in ob1.rem[i]):
            ob1.rem[i]=0
    
    return render_template("seehouse.html",name=ob1.name,pincode=ob1.pincode,id=ob1.id,img=ob1.img,address=ob1.address,rem=ob1.rem)
@app.route("/seehouse1")
def seehouse1():
    ob1=seehouses()
    ob1.myhouse()
    for i in range(len(ob1.rem)):
        if  not  ("best seller" in ob1.rem[i]):
            ob1.rem[i]=0
    return render_template("myhousenuyer.html",name=ob1.name,pincode=ob1.pincode,id=ob1.id,img=ob1.img,address=ob1.address,rem=ob1.rem)
    
@app.route("/preandadd",methods=['POST','GET'])
def preandadd():
    name=request.form.get('name')
    pin=request.form.get('pin')
    ad=request.form.get('ad')
    phno=request.form.get('phno')
    pr=request.form.get('pr')
    em=request.form.get('em')
    ar=request.form.get('area')
    bd=request.form.get('bd')
    bt=request.form.get('Bt')
    st=request.form.get('st')
    mr=request.form.get('mr')
    gr=request.form.get('gr')
    bm=request.form.get('bm')
    hw=request.form.get('hw')
    ac=request.form.get('ac')
    ps=request.form.get('ps')
    pf=request.form.get('pf')
    fr=request.form.get('fr')
    db.predict(ar,bd,bt,st,mr,gr,bm,hw,ac,ps,pf,fr)
    db.isitclose(pr)
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        file.save('static/' + file.filename)
    file.save(file.filename)
    # file = request.form.get('file')
    # print(file)
    # filename = os.path.join(UPLOAD_FOLDER, file.filename)
    # file.save(filename)
    db.add(id,name,pin,ad,phno,pr,em,ar,bd,bt,st,mr,gr,bm,hw,ac,ps,pf,fr,file.filename)
    return "<script>alert('Inserted susscully')</script> <h1>Thank you </h1> <a href='/myhouse'><button>Back</button></a>"
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/myhouse")
def myhouse():
    # return ""+str(id) 
    myhome=houses()
    myhome.myhouse(id)
    
    # myhome.house_details(id,myhome.name)
    
    return render_template("myhouse.html",name=myhome.name,pincode=myhome.pincode,address=myhome.address,img=myhome.img,id=myhome.id)
    
@app.route("/house/<int:id>", methods=['GET'])
def house_details(id):
    obj=houses()
    obj.house_details(id)
    return render_template("housedetails.html",id=id,name=obj.name,pincode=obj.pincode,address=obj.address,phno=obj.phonenumber,price=obj.price,email=obj.email,area=obj.area, bedrooms=obj.noofbedrroms,bathroom=obj.noofbathrooms,stories=obj.stoires,mainroad=obj.mainroad,guestroom=obj.GuestRoom,basement=obj.basement,heatwater=obj.heatwater,aircondition=obj.aircondintionar,parkingslot=obj.parkingslot,prearea=obj.prearea,furshing=obj.furshing,img=obj.img,rem=obj.rem)
@app.route("/house1/<int:id>", methods=['GET'])
def house_details1(id):
    obj=houses()
    obj.house_details(id)
    return render_template("housedetailsbuyer.html",id=id,name=obj.name,pincode=obj.pincode,address=obj.address,phno=obj.phonenumber,price=obj.price,email=obj.email,area=obj.area, bedrooms=obj.noofbedrroms,bathroom=obj.noofbathrooms,stories=obj.stoires,mainroad=obj.mainroad,guestroom=obj.GuestRoom,basement=obj.basement,heatwater=obj.heatwater,aircondition=obj.aircondintionar,parkingslot=obj.parkingslot,prearea=obj.prearea,furshing=obj.furshing,img=obj.img,rem=obj.rem)


@app.route("/delete/<int:id1>", methods=['GET'])
def delete(id1):
    db.delete(id1)
    myhome=houses()
    myhome.myhouse(id)
    return render_template("myhouse.html",name=myhome.name,pincode=myhome.pincode,address=myhome.address,img=myhome.img,id=myhome.id)
@app.route("/add")
def add_house():
    return render_template("add.html")
@app.route("/Account")
def account():
    email,phno=db.account(U,n,id)
    return render_template("account.html",Uname=U,email=email,phno=phno)


if __name__ == '__main__':
    app.run(debug=True, port=2006, host='0.0.0.0')