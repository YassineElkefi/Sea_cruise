from typing import Optional
from fastapi import FastAPI , Request
import mysql.connector
import json
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
"http://localhost:4200",
"https://sea-cruise-6a3f5.web.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add")
async def add(request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"INSERT INTO `croisiere`(`Trajet`, `map`, `port`, `duree`, `depart`, `enfant`, `internet`, `club`, `pension`, `image`) VALUES('{body['trajet']}', '{body['map']}', '{body['port']}','{body['duree']}','{body['depart']}','{body['enfant']}','{body['internet']}','{body['club']}','{body['pension']}', '{body['image']}');")
    mydb.commit()
    return {"OK"}
    
@app.get("/select")
def gets():
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM croisiere")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data


@app.delete("/supp")
async def supp(request:Request):
    mydb = mysql.connector.connect(host = "localhost", user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"delete from `croisiere` where `Trajet`='{body['trajet']}';")
    mydb.commit()
    return {"OK"}

@app.put("/modif")
async def modif(request:Request):
    mydb = mysql.connector.connect(host = "localhost", user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    try:
       mycursor.execute(f"update `croisiere` set `Trajet`='{body['trajet']}',`port`='{body['port']}' , `duree`='{body['duree']}' , `depart`='{body['depart']}' , `enfant`='{body['enfant']}' , `internet`='{body['internet']}' , `club`='{body['club']}' , `pension`='{body['pension']}' , `map`='{body['map']}' , `image`='{body['image']}' where `id`={body['tr']};")
       mydb.commit()
       return {"OK"}
    except: 
       mydb.rollback()
       return{"NON"}

@app.post("/register")
async def reg(request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"SELECT * FROM client WHERE email = '{body['mail']}'")
    rv = mycursor.fetchone()
    mycursor.execute(f"SELECT max(id) FROM client")
    rs = mycursor.fetchone()[0]
    print (rs)
    if (rv):
        return '{"Email already exists!"}'
    else:
        mycursor.execute(f"INSERT INTO `client` VALUES ('', '{body['last']}', '{body['first']}', '{body['mail']}', '{body['pwd']}', '{body['ville']}', '{body['dn']}', '{body['phone']}');")
        mydb.commit()
        mycursor.execute(f"SELECT id FROM client WHERE email = '{body['mail']}'")
        row_headers=[x[0] for x in mycursor.description] 
        rv = mycursor.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        return json_data

@app.post("/login")
async def db_test(request : Request):

    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    print (body)
    mycursor.execute(f"select * from client CL where (CL.email = '{body['user']}') and (CL.password = '{body['pwd']}')")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

@app.get("/client")
def gets(id:str):
    mydb = mysql.connector.connect(host = "localhost", user = "root" , password = "" , database = "seacruise")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM client where id={id}")
    row_headers=[x[0] for x in mycursor.description]  
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data