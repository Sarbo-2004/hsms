import pymysql
import csv
mydb = pymysql.connect(
host="localhost",
port= 3306,
user= "root",
password= "",
database= "shop"
)
mycursor=mydb.cursor() 
ph=""
add=""
name=""
             
def product_list():
    print("==============================================================")
    print("\tPRODUCT LIST:-")
    print("==============================================================")

    e=[]
    y=[]
    sql = "SELECT * FROM products"
    mycursor.execute(sql)
    mydb.commit()
    st=""
    results = mycursor.fetchall()
    print("Sl.no | name                      | price | quantity")
    print("--------------------------------------------------------------")
    for i in results:
      for j in i:
        e.append(j)
      y.append(e)
      e=[]
    for i1 in y:
      print(i1[0]," "*(4-len(str(i1[0]))),"|",i1[1]," "*(24-len(str(i1[1]))),"|",i1[2]," "*(4-len(str(i1[2]))),"|",i1[3])
      print("-------------------------------------------------------------")
    print()
    
    print("You will get rewards points according to your shopping bill as follows:-")
    print()
    print("For shopping of Rs 50-100:-10")
    print("For shopping of Rs 100-150:-50")
    print("For shopping of Rs 150-200:-60")
    print("For shopping of Rs 200-250:-70")
    print("For shopping of Rs 250-300:-80")
    print("For shopping of Rs 300-350:-90")
    print("For shopping of Rs 350-400:-100")
    print()
    sql2=f"SELECT rewards FROM {name}.details"
    mycursor.execute(sql2)
    mydb.commit()
    results1 = mycursor.fetchall()
    for v in results1:
      for u in v:
        print("YOUR CURRENT REWARDS:-",u)

    order()

def searchp(n,m):
    sql = "SELECT product_name FROM products"

    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    a=(n,)

    if a in myresult:
        q=(m,)
        sql1 = "SELECT quantity FROM products WHERE product_name=%s"
        mycursor.execute(sql1,a)
        myresult=mycursor.fetchall()
        for i in myresult:
            if q<=i:
                #print("product availabe")
                pass
            else:
                print()
                print(f"Product present only {sum(i)} items")
                order()
    else:
      print()
      print("Product unavailabe")
      order()
      
def update(g):
  t=0
  for j in g:
      sql="SELECT quantity from products WHERE product_name=%s"
      val=(j[0])
      mycursor.execute(sql , val)
      r=mycursor.fetchall()
      for l in r:
          t=(sum(l))
      sql1="UPDATE products SET quantity=%s WHERE product_name=%s"
      val1=((t-int(j[1])) , j[0])
      mycursor.execute(sql1 , val1)
      mydb.commit()

def sign():
    global ph
    global name
    name=input("enter name:")
    # try:
    mycursor.execute(f"CREATE DATABASE {name}")
    ph=int(input("enter phone number:-"))
    add=input("enter address:")
    r=0
    table1=f"CREATE TABLE {name}.items (sl INT AUTO_INCREMENT , product_name VARCHAR(20) , quantity INT(10) , total_price INT(10) , PRIMARY KEY(sl))"
    mycursor.execute(table1)
    table=f"CREATE TABLE {name}.details (sl INT AUTO_INCREMENT , phone_number VARCHAR(10) , address VARCHAR(50) , rewards INT(10) , PRIMARY KEY(sl))"
    mycursor.execute(table)
      
    p=f"INSERT INTO {name}.details (phone_number , address , rewards) VALUES (%s , %s , %s)"
    val=(ph , add , r )
    mycursor.execute(p , val)
    mydb.commit()
    print("****ACCOUNT CREATED SUCCESSFULLY****")
    product_list()
    # except:
    #   print("Account has already been created with this name. Please login!")
    #   login()
      
def login():
    global name 
    name=input("enter registered name:")
    ph1=((input("enter registered phone number:-"),))
    conph= f"SELECT phone_number FROM {name}.details"
    mycursor.execute(conph)
    result=mycursor.fetchall()
    mydb.commit()
    for i in result:
        if i==ph1:
            print()
            print("****LOGIN SUCCESSFUL****")
            product_list()
        else:
            print("phone number incorrect!!")
            login()


def order():
  b=[]
  c=[]
  ts=0
  product_nam=()
  quantit=()
  st=""
  try:
    np=int(input("Enter the number of products you want to order:-"))
  except:
    np=(int(input("Please enter the number of products:-")))
  for j in range (np):
    s=0
    prod=input("enter product:-")
    product_nam=(prod,)
    quantit=int(input("quantity:-"))
    searchp(prod,quantit)
    sql2 = "SELECT price FROM products WHERE product_name=%s"
    mycursor.execute(sql2,product_nam)
    r=mycursor.fetchall()
    for i in r:
      s=i*quantit
    tp=(sum(s))
    b.append(prod)
    b.append(quantit)
    b.append(tp)
    c.append(b)
    b=[]
    print()
  print("Please Review Your Order:-")
  print("=============================================")
 
  print("Item  Ordered  | quantity | price")
  print("---------------------------------------------")
  for k in c:
    print(k[0]," "*(13-len(k[0])),"|",k[1]," "*(7-len(str(k[1]))),"|",k[2])
    print("---------------------------------------------")
    print(st)
    st=""
  for z in c:
    ts=ts+z[2]
  print(f"TOTAL BILL:-{ts} Rs")
  print()
  reward=0
  if ts>=50 and ts<100:
      reward=10
  elif ts>=100 and ts<150:
      reward=20
  elif ts>=150 and ts<200:
      reward=30
  elif ts>=200 and ts<250:
      reward=40
  elif ts>=250 and ts<300:
      reward=60
  elif ts>=300 and ts<350:
      reward=70
  elif ts>=350 and ts<400:
      reward=80
  elif ts>=400 and ts<=450:
    reward=90
  elif ts>=450:
    reward=100
  print()
  print("Do you want to reedem your reward points to get an additional discount or want to store it for future use(y/n):-")
  o=input().lower()
  td=0
  if o =='y':
    td=ts-reward
    print()
    print(f"TOTAL BILL TO BE PAID:-{td} Rs")
  else:
    sql2=f"SELECT rewards FROM {name}.details"
    mycursor.execute(sql2)
    mydb.commit()
    results1 = mycursor.fetchall()
    for v in results1:
      for u in v:
        r1=int(u)+reward
    sql1=f"UPDATE {name}.details SET rewards=%s"
    val1=(r1)
    mycursor.execute(sql1 , val1)
    mydb.commit()

    
    
  print("")
  print("Type y to confirm order or c to cancel")
  if input().lower()=='y':
    for k1 in c:
      #for l1 in k:
        p=f"INSERT INTO {name}.items (product_name , quantity, total_price) VALUES (%s , %s, %s)"
        val=(k1[0] , k1[1], k1[2])
        mycursor.execute(p , val)
        mydb.commit() 
    print("ORDER PLACED SUCCESSFULLY!!")
    print()
    print("THANK YOU FOR SHOPPING FROM US!!")
    bill()
    update(c)

  else:
    print("Do you want to order again?")
    a=input().lower()
    if a=="yes" or a=="y":
      print()
      product_list()
    elif a=="no" or a=="n":
      print()
      print("THANK YOU")

def bill():
  sql=f"SELECT * FROM {name}.items"
  mycursor.execute(sql)
  mydb.commit()
  myresult=mycursor.fetchall()
  f=open("bill.csv",'w',newline='')
  header=['Serial number', 'product','quantity','total_price']
  writer=csv.writer(f)
  writer.writerow(header)
  for i in myresult:
          i=list(i)
          writer.writerow(i)

def insert():
        n=int(input("enter number of products to be added:-"))
        for i in range(n):
          product_nam=input("product name:-")
          pric=int(input("price per unit:-"))
          quantit=int(input("quantity:-"))
          p="INSERT INTO products (product_name , price , quantity) VALUES (%s , %s , %s)"
          val=(product_nam , pric , quantit)
          mycursor.execute(p , val)
          mydb.commit()

def create_table():
    try:
        table="CREATE TABLE products (sl INT AUTO_INCREMENT , product_name VARCHAR(20) , price INT(10) , quantity INT(10) , PRIMARY KEY(sl))"
        result=mycursor.execute(table)
        n=int(input("enter number of products to be added:-"))
        for i in range(n):
          product_nam=input("product name:-")
          pric=int(input("price per unit:-"))
          quantit=int(input("quantity:-"))
          p="INSERT INTO products (product_name , price , quantity) VALUES (%s , %s , %s)"
          val=(product_nam , pric , quantit)
          mycursor.execute(p , val)
          mydb.commit()
    except:
        print("Table is already created.Please insert products")
        print()
        insert()


print("\t -------- WELCOME TO E-STORES --------") 
print()
print("press 1 to add products in the store")
print("press 2 to shop from the store")
print("press 3 to create products table of the store")
z=int(input())
if z==2:
    n=input("Have you already created your account(yes/no):-").lower()
    print()
    if n=='yes':
        login()
    else:
        sign()
    input()
    
elif z==3:
  create_table()  
  input()
elif z==1:
  insert()  
