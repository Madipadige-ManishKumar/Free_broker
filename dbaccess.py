import sqlite3
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
import joblib

curdir = os.path.dirname(os.path.abspath(__file__))

    



def isitclose(p):
    p=int(p)
    global rem
    pre=int(prediction)
    
    print("The Predicted Price is ",pre,"The Given Price",p)
    print("True or false",pre>p)
    if pre<p:
        print("This is If block")

        if (p-pre)<70000:
            
            rem ="You Can Buy This The Price is resonable"
        else:
            rem="The Price is not Reasonable But The House Looks Good"
        print(rem)
    else:
        if (pre-p) > 100000:
            rem="best seller"
        else:
            rem="Price is reasonable"

    



def predict(ar,bd,bt,st,mr,gr,bm,hw,ac,ps,pf,fr):
    
    mr= 1 if mr=="yes"  else (0)
    gr= 1 if gr=="yes"  else (0)
    bm= 1 if bm=="yes"  else (0)
    hw= 1 if hw=="yes"  else (0)
    ac= 1 if ac=="yes"  else (0)
    pf= 1 if pf=="yes"  else (0)
    fr= 1 if fr=="furnished"  else (0)
    print(mr,gr,bm,hw,ac,pf,fr)

    data = pd.read_csv('Housing.csv')
# Split the dataset into features (X) and target (y)
    X = data.drop('price', axis=1)
    y = data['price']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train a Random Forest regressor model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    
    # Save the trained model
    joblib.dump(model, 'housing_model.pkl')

    # Load the model
    loaded_model = joblib.load('housing_model.pkl')

    # Input data for prediction (adjust these values accordingly)
    input_data = [[ar, bd, bt, st, mr, gr, bm, hw, ac, ps, pf, fr]]

    # Make a price prediction
    global prediction
    prediction = loaded_model.predict(input_data)
    print(f'Predicted price: {prediction[0]:.2f}')

def get_db_connection():
    curdir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(curdir, "freebroker.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return connection, cursor




      

def close_db_connection(connection):
    connection.close()

def signup(U,E,P,phno,O):
    connection,cursor=get_db_connection()
    
    if O == "seller":
        query="select seller  from count"
        n=cursor.execute(query).fetchone()
        n=int(n[0])
        
        query="insert into seller values('{id}','{u}','{e}','{p}','{ph}')".format(id=n,u=U,e=P,p=E,ph=phno)
        cursor.execute(query)
        n=n+1
        query="update count set seller='{c}'".format(c=n)
        cursor.execute(query)
        connection.commit()
    elif O=="buyer":
        query="select buyer  from count"
        n=cursor.execute(query).fetchone()
        n=int(n[0])
        n=n+1
        query="insert into buyer values('{id}','{u}','{e}','{p}','{ph}')".format(id=n,u=U,e=P,p=E,ph=phno)
        cursor.execute(query)
        
        query="update count set buyer='{c}'".format(c=n)
        cursor.execute(query)
        connection.commit()
    close_db_connection(connection)
def login(U,P):
    connection,cursor=get_db_connection()
    query="select * from seller where name='{u}'and password='{p}'".format(u=U,p=P)
    cursor.execute(query)
    n=cursor.fetchall()
    query="select * from buyer where name='{u}'and password='{p}'".format(u=U,p=P)
    cursor.execute(query)
    m=cursor.fetchall()
    close_db_connection(connection)
    if n:
        return "yess"
    elif m:
        return "yesb"
    
def add(id,n,pin,ad,phno,pr,em,ar,bd,bt,st,mr,gr,bm,hw,ac,ps,pf,fr,img):
    conn,cursor=get_db_connection()
    m=cursor.execute("select house from count").fetchone()
    print(m)
    m=int(m[0])
    m=m+1
    query="insert into houses values('{j}','{i}','{n}','{p}','{ad}','{ph}','{pr}','{em}','{ar}','{bd}','{bt}','{st}','{mr}','{gr}','{bm}','{hw}','{ac}','{ps}','{pf}','{fr}','{img}','{prp}','{rcm}')".format(i=id,p=pin,ad=ad,ph=phno,pr=pr,em=em,ar=ar,bd=bd,bt=bt,st=st,mr=mr,gr=gr,bm=bm,hw=hw,ac=ac,ps=ps,pf=pf,fr=fr,n=n,j=m,img=img,prp=prediction,rcm=rem)

    cursor.execute(query)
    
    print("This is m",m)
    cursor.execute("update count set house='{c}'".format(c=m))
    conn.commit()
    close_db_connection(conn)
def delete(id):
    conn,cursor=get_db_connection()
    query="delete from houses where houseid={id}".format(id=id)
    cursor.execute(query)
    conn.commit()
    close_db_connection(conn)
def account(u,n,id):
    conn,cursor=get_db_connection()
    if n=="yess":
            email=cursor.execute("select email from seller where id={id}".format(id=id)).fetchone()
            phno=cursor.execute("select phno from seller where id={id}".format(id=id)).fetchone()
        
    elif n=="yesb":
        email=cursor.execute("select email from seller where id={id}".format(id=id)).fetchone()
        phno=cursor.execute("select phno from seller where id={id}".format(id=id)).fetchone()

    close_db_connection(conn)
    return email,phno