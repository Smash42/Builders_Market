
from database.connection import get_connection

class ProductItem:
    def __init__(self, product_id, name, description, price, quantity):
        self.product_id = product_id
        self.product_name = name
        self.description = description
        self.price = price
        self.quantity = quantity

# Update product 
    def UpdateDatabase(self):
        db = get_connection()
        sql = """UPDATE products SET product_name = ?, description = ?, price = ?, quantity = ? WHERE product_id = ?;"""
        db.execute(sql, [self.product_name, self.description, self.price, self.quantity, self.product_id] )
        db.commit()

# Delete product
    def Delete(self):
        db = get_connection()
        sql = """DELETE FROM products WHERE product_id = ?;"""
        db.execute(sql, [self.product_id])
        db.commit()

#Get all products
    @staticmethod
    def GetAll():
        db= get_connection()
        sql = "SELECT * FROM products;"
        results = db.execute(sql).fetchall()
        
        out = []
        for r in results:
            dev = ProductItem.FromDBRow(r)
            if dev is None:
                continue
            out.append(dev)
        return out

# Create New Product
    @staticmethod
    def Create(name, description, price, quantity):
        db = get_connection()
        sql = """INSERT INTO products (product_name, description, price, quantity) VALUES (?, ?, ?, ?);"""
        cursor = db.execute(sql, [name, description, price, quantity])
        product_id = cursor.lastrowid
        db.commit()
        return ProductItem.FromDB(id)
    
# DB from row
    @staticmethod   
    def FromDBRow(row):
        if row is None:
            return None
        return ProductItem(
            product_id=row['product_id'],
            name=row['product_name'],
            description=row['description'],       
            price=row['price'],
            quantity= row['quantity']
    )

    @staticmethod  
    def FromDB(id : int):
        db = get_connection()
        sql = "SELECT * FROM products WHERE product_id = ?;"
        result = db.execute(sql, [id]).fetchone()
        return ProductItem.FromDBRow(result)

        