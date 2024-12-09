import csv
from models import db, Product

def import_csv_to_db(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = Product(
                name=row['name'],
                description=row['description'],
                quantity=int(row['quantity']),
                tags=row['tags']
            )
            db.session.add(product)
        db.session.commit()
