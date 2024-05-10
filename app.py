from flask import Flask, render_template,redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "santhoshi"
app.config["MYSQL_DB"] = "library"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

    
@app.route("/addBook", methods=["GET","POST"])
def addBook():
    if request.method == "POST":
        book_name = request.form['book_name']
        book_author = request.form['book_author']
        con = mysql.connection.cursor()
        sql = "insert into books (book_name, book_author) values(%s, %s)"
        con.execute(sql, [book_name, book_author])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("addBook.html")


@app.route("/deleteBook/<string:id>", methods=["GET", "POST"])
def deleteBook(id):
    con = mysql.connection.cursor()
    
    print(id)
    sql = "delete from books where id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))

@app.route("/barrowBook/<string:id>", methods=["GET", "POST"])
def barrowBook(id):
    con = mysql.connection.cursor()
    sql = "select * from books where id=%s;"
    print(id)
    con.execute(sql, [id])
    res = con.fetchall()
    print(res)
    sql = "insert into users (id, book_name, book_author) values (%s, %s, %s);"
    con.execute(sql, [res[0]["id"],res[0]["book_name"],res[0]["book_author"]])
    mysql.connection.commit()
    sql = "delete from books where id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    #con.close()
    return redirect(url_for("home"))

@app.route("/returnBook/<string:id>", methods=["GET", "POST"])
def returnBook(id):
    con = mysql.connection.cursor()
    sql = "select * from users where id=%s;"
    print(id)
    con.execute(sql, [id])
    res = con.fetchall()
    print(res)
    sql = "insert into books (id, book_name, book_author) values (%s, %s, %s);"
    con.execute(sql, [res[0]["id"],res[0]["book_name"],res[0]["book_author"]])
    mysql.connection.commit()
    sql = "delete from users where id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    #con.close()
    return redirect(url_for("home"))

@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "select * from books;"
    con.execute(sql)
    res = con.fetchall()
    print(res)
    sql = "select * from users;"
    con.execute(sql)
    users = con.fetchall()
    return render_template("home.html", datas=[res,users])


if(__name__ == '__main__'):
    app.run(debug=True)