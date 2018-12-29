from bottle import run, template, static_file, get, post, delete, request
import json
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='davidzerah28#05',
                             db='shop',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@post("/category")
def add_category():
    category = request.forms.get("name")
    if not category:
        dictionary = {"STATUS": "ERROR", "MSG": "Name parameter is missing", "CAT_ID": "", "CODE": 400}
        return json.dumps(dictionary)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories WHERE category  = '{}'".format(category)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                dictionary = {"STATUS":"ERROR", "MSG":"Category already exists", "CAT_ID":"", "CODE": 200}
                return json.dumps(dictionary)
            else:
                sql = "INSERT INTO categories (category) VALUES ('{}')".format(category)
                cursor.execute(sql)
                connection.commit()
                id = cursor.lastrowid
                dictionary = {"STATUS": "SUCCESS", "MSG":"", "CAT_ID": id, "CODE": 201}
                return json.dumps(dictionary)
    except:
        dictionary = {"STATUS": "ERROR", "MSG": "Internal error", "CAT_ID":"", "CODE": 500}
        return json.dumps(dictionary)


@delete("/category/<cid>")
def delete_category(cid):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories WHERE id = '{}'".format(cid)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                sql = ('DELETE FROM categories WHERE id = {}'.format(cid))
                cursor.execute(sql)
                connection.commit()
                return json.dumps({"STATUS": "SUCCESS", "MSG":"", "CODE": 201})
            else:
                dictionary = {"STATUS": "ERROR", "MSG":"Category not found", "CODE":404}
                return json.dumps(dictionary)
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "Internal error", "CODE": 500})


@get("/categories")
def list_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()
            dictionary = {"STATUS": "SUCCESS", "MSG":"", "CATEGORIES": result, "CODE": 200}
            return json.dumps(dictionary)
    except:
        dictionary = {"STATUS": "ERROR", "MSG": "Internal error", "CATEGORIES":"", "CODE": 500}
        return json.dumps(dictionary)


@post("/product")
def add_product():
    title = request.forms.get("title")
    description = request.forms.get("desc")
    price = request.forms.get("price")
    img_url = request.forms.get("img_url")
    favorite = request.forms.get("favorite")
    cat_id = request.forms.get("category")
    if favorite == 'on':
        favorite = True
    else:
        favorite = False
    if title == "" or description == "" or price == "" or img_url == "":
        dictionary = {"STATUS": "ERROR", "MSG": "Missing parameters", "PROD_ID": "", "CODE": 400}
        return dictionary
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories WHERE id = {}".format(cat_id)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                sql = "INSERT INTO products (title, description, price, img_url, category_id, favorite) VALUES ('{}', '{}', '{}', '{}', {}, {});".format(title, description, price, img_url, cat_id, favorite)
                cursor.execute(sql)
                connection.commit()
                prod_id = cursor.lastrowid
                dictionary = {"STATUS": "SUCCESS", "MSG": "The product was added/updated successfully", "PROD_ID:": prod_id, "CODE":201}
                return json.dumps(dictionary)
            else:
                dictionary = {"STATUS": "ERROR", "MSG": "Category not found", "PROD_ID": "", "CODE":404}
                return json.dumps(dictionary)
    except:
        dictionary = {"STATUS": "ERROR", "MSG": "Internal error", "PROD_ID": "", "CODE":500}
        return json.dumps(dictionary)


@get("/product/<pid>")
def get_product(pid):
    try:
        with connection.cursor() as cursor:
            sql = ("SELECT * FROM products WHERE id = {}".format(pid))
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                dictionary = {"STATUS": "SUCCESS", "MSG": "", "PRODUCT": result, "CODE": 200}
                return json.dumps(dictionary)
            else:
                dictionary = {"STATUS": "ERROR", "MSG": "Product not found", "PRODUCT": "", "CODE": 404}
                return json.dumps(dictionary)
    except:
        dictionary = {"STATUS": "ERROR", "MSG": "Internal error", "PRODUCT": "", "CODE": 500}
        return json.dumps(dictionary)


@delete("/product/<pid>")
def delete_product(pid):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE id = '{}'".format(pid)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                sql = "DELETE FROM products WHERE id = {}".format(pid)
                cursor.execute(sql)
                connection.commit()
                dictionary = {"STATUS": "SUCCESS", "MSG": "", "CODE": 201}
                return json.dumps(dictionary)
            else:
                dictionary = {"STATUS": "ERROR", "MSG": "Product not found", "CODE": 404}
                return json.dumps(dictionary)
    except:
        dictionary = {"STATUS": "ERROR", "MSG": "Internal error", "CODE": 500}
        return json.dumps(dictionary)


@get("/products")
def list_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products"
            cursor.execute(sql)
            result = cursor.fetchall()
            dictionary = {"STATUS": "SUCCESS", "MSG": "", "PRODUCTS": result, "CODE": 200}
            return json.dumps(dictionary)
    except:
        dictionary = { "STATUS": "ERROR", "MSG": "Internal error", "PRODUCTS": "", "CODE": 500}
        return json.dumps(dictionary)


@get('/category/<cid>/products')
def list_products_by_category(cid):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE category_id = {}".format(cid)
            cursor.execute(sql)
            result = cursor.fetchall()
            if result:
                dictionary = {"STATUS": "SUCCESS", "MSG": "", "PRODUCTS": result, "CODE": 200}
                return json.dumps(dictionary)
            else:
                dictionary = {"STATUS": "ERROR", "MSG": "Category not found", "PRODUCTS": "", "CODE": 404}
                return json.dumps(dictionary)
    except:
        dictionary = {"STATUS": "ERROR", "MSG": "Internal error", "PRODUCTS": "", "CODE": 500}
        return json.dumps(dictionary)


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


#run(host='0.0.0.0', port=argv[1])
if __name__ == "__main__":
    run(host='localhost', port=7000, debug=True)
