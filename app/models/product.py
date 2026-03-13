
from database.connection import get_connection
from models.categories import Category

class ProductItem:
    def __init__(self, product_id, name, description, price, quantity, image_file):
        self.product_id = product_id
        self.product_name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.image_file = image_file

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
    def Create(name, description, price, quantity, image_file):
        db = get_connection()
        try:
            cursor = db.execute("""
                INSERT INTO products (product_name, description, price, quantity, image_file)
                VALUES (?, ?, ?, ?, ?)
                """, (name, description, price, quantity, image_file))

            product_id = cursor.lastrowid
            db.commit()

            return ProductItem.FromDB(product_id)

        finally:
            db.close()

    @staticmethod
    def GetByID(product_id):
        db = get_connection()
        try:
            row = db.execute(
                "SELECT * FROM products WHERE product_id = ?",
            (product_id,)
            ).fetchone()

            return ProductItem.FromDBRow(row)

        finally:
            db.close()
    
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
            quantity= row['quantity'],
            image_file = row['image_file']
        )

    @staticmethod  
    def FromDB(product_id : int):
        db = get_connection()
        sql = db.execute( """SELECT * FROM products WHERE product_id = ?""", (product_id,)).fetchone()
        db.close()

        return ProductItem.FromDBRow(sql)
    
    #Search Query
    @staticmethod
    def Search(category_id = None, search = None):
        db = get_connection()
        sql = """
            SELECT DISTINCT p.*
            FROM products p
            LEFT JOIN product_categories pc ON p.product_id = pc.product_id
            LEFT JOIN categories c ON pc.category_id = c.category_id
            WHERE 1=1 
            """
        
        param = []

        if category_id:
            sql += " AND pc.category_id = ?"
            param.append(category_id)

        if search:
            sql+= "AND p.product_name LIKE ? OR p.description LIKE ?"
            param.append(f"%{search}%")
            param.append(f"%{search}%")

        
        rows = db.execute(sql, param).fetchall()

        return [ProductItem.FromDBRow(row) for row in rows]

        