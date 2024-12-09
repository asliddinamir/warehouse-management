from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Product, User, Inbound, Outbound

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        user = None  
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
        
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):  
                login_user(user)
                flash('Login successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password', 'danger')
        return render_template('login.html')



    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out', 'info')
        return redirect(url_for('login'))

    @app.route('/')
    @login_required
    def home():
        return render_template('home.html')

    @app.route('/inventory')
    @login_required
    def inventory():
        if current_user.role == 'manager':
            query = request.args.get('q')
            if query:
                products = Product.query.filter(
                (Product.name.like(f'%{query}%')) | 
                (Product.category.like(f'%{query}%')) |
                (Product.sku.like(f'%{query}%')) |
                (Product.tags.like(f'%{query}%'))
            ).all()
            else:
                products = Product.query.all()
            return render_template('inventory.html', products=products)
        elif current_user.role == 'operator':
            query = request.args.get('q')
            if query:
                products = Product.query.filter(
                (Product.name.like(f'%{query}%')) | 
                (Product.category.like(f'%{query}%')) |
                (Product.sku.like(f'%{query}%')) |
                (Product.tags.like(f'%{query}%'))
            ).all()
            else:
                products = Product.query.all()
            return render_template('inventory_view_only.html', products=products)
        else:
            flash("You don't have permission to access this page.", 'danger')
        return redirect(url_for('home'))


    @app.route('/inventory/add', methods=['POST'])
    @login_required
    def add_product():
        if current_user.role != 'manager':
            flash("You don't have permission to access this page.", 'danger')
            return redirect(url_for('home'))

        category = request.form['category']
        sku = request.form['sku']
        name = request.form['name']
        location = request.form['location']
        quantity = request.form['quantity']
        supplier = request.form['supplier']

        if not category or not sku or not name or not location or not quantity or not supplier:
            flash("All fields are required.", 'danger')
            return redirect(url_for('inventory'))

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
        flash('Product added successfully!', 'success')

        return redirect(url_for('inventory'))

    @app.route('/inventory/update/<int:id>', methods=['GET', 'POST'])
    @login_required
    def update_product(id):
        if current_user.role != 'manager':
            flash("You don't have permission to access this page.", 'danger')
            return redirect(url_for('home'))

        product = Product.query.get(id)
        if not product:
            flash('Product not found!', 'danger')
            return redirect(url_for('inventory'))

        if request.method == 'POST':
            product.category = request.form['category']
            product.sku = request.form['sku']
            product.name = request.form['name']
            product.location = request.form['location']
            product.quantity = request.form['quantity']
            product.supplier = request.form['supplier']

            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('inventory'))

        return render_template('update_product.html', product=product)

    @app.route('/inventory/delete/<int:id>')
    @login_required
    def delete_product(id):
        if current_user.role != 'manager':
            flash("You don't have permission to access this page.", 'danger')
            return redirect(url_for('home'))

        product = Product.query.get(id)
        if product:
            db.session.delete(product)
            db.session.commit()
            flash('Product deleted successfully!', 'success')
        else:
            flash('Product not found!', 'danger')

        return redirect(url_for('inventory'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
