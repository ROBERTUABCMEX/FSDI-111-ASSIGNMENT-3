from flask import request, render_template
from app import app
from app.databases import create, read, update, delete, scan
from datetime import datetime
from app.forms.product import ProductForm



@app.route("/")
def index():
    #serv_time = datetime.now().strftime("%F %H:%M:%S")
    """return{
        "ok": True,
        "version": "1.0.0",
        "server_time": serv_time
    }"""
    return render_template("base.html")


@app.route("/product_form", methods=["GET", "POST"])
def product_form():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        category = request.form.get("category")
        price = request.form.get("price")

        create(name, price, category, description)

    form = ProductForm()
    return render_template("form_example.html", form=form)


@app.route("/products")
def get_all_products():
    out = scan()
    #out["ok"] = True
    #out["message"] = "Success"
    #return out
    return render_template("products.html", products=out["body"])


@app.route("/products/<pid>")
def get_one_product(pid):
    out = read(int(pid))
    out["ok"] = True
    out["message"] = ["Success"]
    # return out
    return render_template("products.html", products=out["body"])


@app.route("/products", methods=["POST"])
def create_product():
    product_data = request.json
    new_id = create(
        product_data.get("name"),
        product_data.get("price"),
        product_data.get("category"),
        product_data.get("description"),
    )

    return {"ok": True, "message": "Success", "new_id": new_id}


@app.route("/products/<pid>", methods=["PUT"])
def update_product(pid):
    product_data = request.json

    out = update(int(pid), product_data)

    return {"ok": out, "message": "Updated"}


@app.route("/aboutme/<name>")
def aboutme(name):
    lastname="Camarena"
    hobbies = "Baseball"
    return render_template("aboutme.html", first_name=name, last_name=lastname, hobbies=hobbies)

@app.route('/square/<int:number>')
def square(number):
    return ("<h1>Squared of %s  is %s</h1>" % (number, number**2))

@app.route('/agent')
def agent():
    user_agent = request.headers.get("User-Agent")
    return "<p>Agent: %s</p>" % user_agent

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
