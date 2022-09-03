# import library flask
from flask import Flask,jsonify, request
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL


#Creación objeto flask
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*":{"origin":'*'}})
# Llave secreta
app.secret_key = "apiRest"

# configuración conexión sql
app.config['MYSQL_HOTS'] = 'http://127.0.0.1:3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yetafe53'
app.config['MYSQL_DB'] = 'frozen_tastebd'

# crear objeto MySQL
mysql = MySQL(app)

# Función para obtener información de base de datos
def getData(sQuerry):
    cursor = mysql.connection.cursor()
    cursor.execute(sQuerry)
    data = cursor.fetchall()
    return data

# Función para agregar un dato en la db
def addData(sQuerry):
    data = False
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(sQuerry)
        mysql.connection.commit()
        data = True
    except:
        data = False
    return data

# función para actualizar la db
def updateData(sQuerry):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(sQuerry)
        mysql.connection.commit()
    except:
        mysql.connection.rollback()

# Función para eliminar un dato de la base de datos
def deleteData(sQuerry):
    cursor = mysql.connection.cursor()
    cursor.execute(sQuerry)
    mysql.connection.commit()
    cursor.execute(sQuerry)
    records = cursor.fetchall()
    if len(records) == 0:
        data = "Record Deleted successfully "
    else:
        data = "Record Deleted successfully "
    return data
# Función para obtener los productos
@app.route("/products", methods = ['GET'])
def getProducts():
    dirProducts = {}
    listProducts = []
    data = getData("SELECT * FROM product")
    for product in data:
        dirProducts = {"id":product[0],"producto":product[1]}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Ruta para consultar un producto
@app.route('/products/<string:product>', methods = ['GET'])
def getProduct(product):
    dirProducts = {}
    listProducts = []
    data = getData(f"SELECT * FROM product WHERE product_name = '{product}'")
    if (len(data) > 0):
        for product in data:
            dirProducts = {"id": product[0], "producto": product[1]}
            listProducts.append(dirProducts)
    else:
        dirProducts = {"Error":"La búsqueda no arrojo resultado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Define la ruta para los productos a guardar
@app.route("/products", methods = ['POST'])
def postProduct():
    dirProducts = {}
    listProducts = []
    new_product = request.json['name']
    data = addData(f"INSERT INTO product (product_name) VALUES ( '{new_product}')")
    if (data):
        dirProducts = {"Success": "El producto ingresado agregado correctamente"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto ingresado no ha sido agregado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Define la ruta para los productos a editar
@app.route("/products/<string:product>", methods = ['PUT'])
def updateProduct(product):
    data = getData(f"SELECT * FROM product WHERE product_name = '{product}'")
    higher = idHigher(data)
    new_product = request.json['name']
    dirProducts = {}
    listProducts= []
    if (len(data) > 0):
        querry = (f"UPDATE product SET product_name = '{new_product}' WHERE (idproduct = '{higher}');")
        updateData(querry)
        dirProducts = {"Success": "El producto ha sido modificado"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto no ha sido encontrado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Define la ruta para los productos a guardar
@app.route("/products/<string:product>", methods = ['DELETE'])
def deleteProduct(product):
    data = getData(f"SELECT * FROM product WHERE product_name = '{product}' ")
    dirProducts = {}
    listProducts = []
    if (len(data) > 0):
        data = deleteData(f"DELETE FROM product WHERE product_name = '{product}' ")
        dirProducts = {"Success": "El producto ha sido eliminado"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto ingresado no ha sido encontrado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)


# Define la ruta para los sabores
@app.route("/flavors", methods = ['GET'])
# Consultar los sabores
def getFlavors():
    dirFlavers = {}
    listFlavors = []
    data = getData("SELECT * FROM flavor")
    for flavor in data:
        dirFlavors = {"id":flavor[0],"sabor":flavor[1]}
        listFlavors.append(dirFlavors)
    return jsonify(listFlavors)

# Ruta para consultar un producto
@app.route('/flavors/<string:flavor>', methods = ['GET'])
#función para obtener un sabor
def getFlavor(flavor):
    dirProducts = {}
    listProducts = []
    data = getData(f"SELECT * FROM flavor WHERE flavor_name = '{flavor}'")
    if (len(data) > 0):
    # Conversión a Json
        for flavor in data:
            dirProducts = {"id": flavor[0], "sabor": flavor[1]}
            listProducts.append(dirProducts)
    else:
        dirProducts = {"Error":"La búsqueda no arrojo resultado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Define la función para guardar un nuevo sabor
@app.route("/flavors", methods = ['POST'])
def postFlavors():
    dirProducts = {}
    listProducts = []
    new_flavor = request.json['name']
    data = addData(f"INSERT INTO flavor (flavor_name) VALUES ( '{new_flavor}')")
    if (data):
        dirProducts = {"Success": "El sabor ingresado agregado correctamente"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El sabor ingresado no ha sido agregado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)


# Define la ruta para los sabores a editar
@app.route("/flavors/<string:flavor>", methods = ['PUT'])
def updateFlavor(flavor):
    data = getData(f"SELECT * FROM flavor WHERE flavor_name = '{flavor}'")
    higher = idHigher(data)
    new_flavor = request.json['name']
    dirProducts = {}
    listProducts= []
    if (len(data) > 0):
        querry = (f"UPDATE flavor SET flavor_name = '{new_flavor}' WHERE (idflavor = '{higher}');")
        updateData(querry)
        dirProducts = {"Success": "El sabor ha sido modificado"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El sabor no ha sido encontrado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Define la ruta para los sabores a guardar
@app.route("/flavors/<string:flavor>", methods = ['DELETE'])
def deleteFlavors(flavor):
    data = getData(f"SELECT * FROM flavor WHERE flavor_name = '{flavor}' ")
    dirProducts = {}
    listProducts = []
    if (len(data) > 0):
        data = deleteData(f"DELETE FROM flavor WHERE flavor_name = '{flavor}' ")
        dirProducts = {"Success": "El sabor ha sido eliminado"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El sabor ingresado no ha sido encontrado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Consultar lineas de producto
@app.route("/productsline", methods = ['GET'])
def getProductsLine():
    dirLines = {}

    listLine = []

    data = getData("SELECT * FROM product_line")
    for line in data:
        dirLines = {"id":line[0],"producto":line[1]}
        listLine.append(dirLines)
    return jsonify(listLine)

# Consutlar una linea de producto
@app.route('/productsline/<string:lineproduct>', methods = ['GET'])
def getProductLine(lineproduct):
    dirProducts = {}
    listProducts = []
    data = getData(f"SELECT * FROM product_line WHERE product_line_name = '{lineproduct}'")
    if (len(data) > 0):
        for product in data:
            dirProducts = {"id": product[0], "Linea de produccion": product[1]}
            listProducts.append(dirProducts)
    else:
        dirProducts = {"Error":"La búsqueda no arrojo resultado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

#Ingresar una linea de producto
@app.route("/productsline", methods = ['POST'])
def postProductsLine():
    dirProducts = {}
    listProducts = []
    newLine = request.json['name']
    data = addData(f"INSERT INTO product_line (product_line_name) VALUES ( '{newLine}')")
    if (data):
        dirProducts = {"Success": "El producto ingresado agregado correctamente"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto ingresado no ha sido agregado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Editar una linea de producto
@app.route("/productsline/<string:lineproduct>", methods = ['PUT'])
def updateProductsLine(lineproduct):
    data = getData(f"SELECT * FROM product_line WHERE product_line_name = '{lineproduct}'")
    higher = idHigher(data)
    newLine = request.json['name']
    dirProducts = {}
    listProducts= []
    if (len(data) > 0):
        querry = (f"UPDATE product_line SET product_line_name = '{newLine}' WHERE (idproduct_line = '{higher}');")
        updateData(querry)
        dirProducts = {"Success": "la linea de producto ha sido modificada"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "la linea de producto no ha sido encontrada"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Eliminar una linea de producto
@app.route("/productsline/<string:lineproduct>", methods = ['DELETE'])
def deleteProductsLine(lineproduct):
    data = getData(f"SELECT * FROM product_line WHERE product_line_name = '{lineproduct}' ")
    dirProducts = {}
    listProducts = []

    if (len(data) > 0):
        data = deleteData(f"DELETE FROM product_line WHERE product_line_name = '{lineproduct}' ")
        dirProducts = {"Success":"La linea de producto ha sido eliminada"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "la linea de producto ingresado no ha sido encontrada"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Ingresar un producto con un sabor
@app.route("/products/x/flavor", methods = ['POST'])
def postProductXFlavor():
    dirProducts = {}
    listProducts = []
    newProduct = request.json['product']
    newFlavor = request.json['flavor']
    idProduct = idHigher(getData(f"SELECT * FROM product WHERE product_name = '{newProduct}'"))
    idFlavor = idHigher(getData(f"SELECT * FROM flavor WHERE flavor_name = '{newFlavor}'"))
    data = addData(f"INSERT INTO product_x_flavor (id_product,id_flavor) VALUES ( '{idProduct}','{idFlavor}')")
    if (data):
        dirProducts = {"Success": "El producto ingresado agregado correctamente"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto ingresado no ha sido agregado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# ingresar un linea de producto por producto
@app.route("/products/x/line", methods = ['POST'])
def postProductXLine():
    dirProducts = {}
    listProducts = []
    newProduct = request.json['product']
    newLine = request.json['line']
    idProduct = idHigher(getData(f"SELECT * FROM product WHERE product_name = '{newProduct}'"))
    idLine = idHigher(getData(f"SELECT * FROM product_line WHERE product_line_name = '{newLine}'"))
    data = addData(f"INSERT INTO product_x_productline (id_prod,id_line) VALUES ( '{idProduct}','{idLine}')")
    if (data):
        dirProducts = {"Success": "El producto ingresado agregado correctamente"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto ingresado no ha sido agregado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# Ingresar un producto completo
@app.route("/products/complete", methods = ['POST'])
def postProductComplete():
    dirProducts = {}
    listProducts = []
    newProduct = request.json['product']
    newFlavor = request.json['flavor']
    newLine = request.json['line']
    idProduct = idHigher(getData(f"SELECT * FROM product WHERE product_name = '{newProduct}'"))
    idFlavor = idHigher(getData(f"SELECT * FROM flavor WHERE flavor_name = '{newFlavor}'"))
    idLine = idHigher(getData(f"SELECT * FROM product_line WHERE product_line_name = '{newLine}'"))
    productForFlavor = addData(f"INSERT INTO product_x_flavor (id_product,id_flavor) VALUES ( '{idProduct}','{idFlavor}')")
    productForLine = addData(f"INSERT INTO product_x_productline (id_prod,id_line) VALUES ( '{idProduct}','{idLine}')")
    if ((productForFlavor) and (productForLine)):
        dirProducts = {"Success": "El producto ingresado agregado correctamente"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "El producto ingresado no ha sido agregado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# consultar un producto completo
@app.route('/products/complete')
def joinData():
    data = getData(f"SELECT p.product_name, "+
                   f"fl.flavor_name, "+
                   f"pl.product_line_name "+
                   f"FROM product as p "+
                   f"INNER JOIN product_x_flavor as pf ON p.idproduct = pf.id_product "+
                   f"INNER JOIN flavor as fl ON pf.id_flavor = fl.idflavor "+
                   f"INNER JOIN product_x_productline as pp ON p.idproduct = pp.id_prod "+
                   f"INNER JOIN product_line as pl ON pp.id_line = pl.idproduct_line")

    dirProducts = {}
    listProducts = []
    if (len(data) > 0):
        # Conversión a Json
        for product in data:
            dirProducts = {"producto": product[0], "sabor": product[1], "linea": product[2]}
            listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "La búsqueda no arrojo resultado"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# eliminar un producto completo
@app.route("/products/complete/<string:product>/<string:flavor>/<string:productline>", methods = ['DELETE'])
def deleteProductComplete(product,flavor,productline):

    idProduct = idHigher(getData(f"SELECT * FROM product WHERE product_name = '{product}'"))
    idFlavor = idHigher(getData(f"SELECT * FROM flavor WHERE flavor_name = '{flavor}'"))
    idLine = idHigher(getData(f"SELECT * FROM product_line WHERE product_line_name = '{productline}'"))
    dirProducts = {}
    listProducts = []

    if ((idProduct > 0) and (idFlavor > 0) and (idLine > 0) ):
        productForFlavor = deleteData(f"DELETE FROM product_x_flavor WHERE id_product = '{idProduct}' AND id_flavor = '{idFlavor}' ")
        productForLine = deleteData(f"DELETE FROM product_x_productline WHERE id_prod = '{idProduct}' AND id_line = '{idLine}'")
        dirProducts = {"Success":"La linea de producto ha sido eliminada"}
        listProducts.append(dirProducts)
    else:
        dirProducts = {"Error": "la linea de producto ingresado no ha sido encontrada"}
        listProducts.append(dirProducts)
    return jsonify(listProducts)

# función para obtener el id del componente
def idHigher(data):
    higher = 0
    for product in data:
        if (product[0] > higher):
           higher = product[0]
    return higher

if ( __name__ == '__main__'):
    app.run(debug = True, port=5000)
