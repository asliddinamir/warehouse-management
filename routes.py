from flask import Flask, render_template, request, redirect, url_for
from models import db, Product

app = Flask(__name__)

@app.route('/inventory')
def inventory():
    products = Product.query.all()
    return render_template('inventory.html', products=products)

@app.route('/inventory/add', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    quantity = request.form['quantity']
    tags = request.form['tags']

    new_product = Product(name=name, description=description, quantity=quantity, tags=tags)
    db.session.add(new_product)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/inventory/delete/<int:id>')
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('inventory'))
