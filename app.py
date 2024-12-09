from flask import Flask, render_template, request, redirect, url_for
from models import db, Product

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def home():
        return "Welcome to the Warehouse Management System!"

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

    @app.route('/inventory/update/<int:id>', methods=['POST'])
    def update_product(id):
        product = Product.query.get(id)
        if product:
            product.name = request.form['name']
            product.description = request.form['description']
            product.quantity = request.form['quantity']
            product.tags = request.form['tags']
            db.session.commit()
        return redirect(url_for('inventory'))

    @app.route('/inventory/delete/<int:id>')
    def delete_product(id):
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
        return redirect(url_for('inventory'))

    with app.app_context():
        db.create_all()  # Create tables in the database

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
