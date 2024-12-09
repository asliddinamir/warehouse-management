from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate  # Import Flask-Migrate
from models import db, Product

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    @app.route('/')
    def home():
        return render_template('home.html')
    
    @app.route('/inventory')
    def inventory():
        products = Product.query.all()
        return render_template('inventory.html', products=products)

    @app.route('/inventory/add', methods=['POST'])
    def add_product():
        category = request.form['category']
        sku = request.form['sku']
        name = request.form['name']
        location = request.form['location']
        quantity = request.form['quantity']
        supplier = request.form['supplier']

        # Add new product to the database
        new_product = Product(
            category=category,
            sku=sku,
            name=name,
            location=location,
            quantity=quantity,
            supplier=supplier
        )
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('inventory'))

    @app.route('/inventory/update/<int:id>', methods=['POST'])
    def update_product(id):
        product = Product.query.get(id)
        if product:
            product.category = request.form['category']
            product.sku = request.form['sku']
            product.name = request.form['name']
            product.location = request.form['location']
            product.quantity = request.form['quantity']
            product.supplier = request.form['supplier']
            db.session.commit()
        return redirect(url_for('inventory'))

    @app.route('/inventory/delete/<int:id>')
    def delete_product(id):
        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
        return redirect(url_for('inventory'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
