from database.connection import get_connection

class Category:
    def __init__(self, category_id, category_name, products= None ):
        self.category_id = category_id
        self.category_name = category_name


    # Create New Category
    @staticmethod
    def Create(name):
        db = get_connection()
        sql = """INSERT INTO categories (category_name) VALUES (?)"""
        cursor = db.execute(sql, [name, ])
        category_id = cursor.lastrowid
        db.commit()
        return Category.FromDB(category_id)
    
   # Delete Category
    def Delete(category_id):
        db = get_connection()
        try:
            db.execute("""
                DELETE FROM categories
                WHERE category_id = ?
            """, (category_id,))
            db.commit()
        finally:
            db.close() 
                               

    #Get all categories
    @staticmethod
    def GetAll():
        db= get_connection()
        sql = "SELECT * FROM categories;"
        results = db.execute(sql).fetchall()
        
        out = []
        for r in results:
            dev = Category.FromDB(r['category_id'])
            if dev is None:
                continue
            out.append(dev)
        return out
    

    @staticmethod
    def FromDB(category_id : int):
        db = get_connection()
        try: 
            row = db.execute("""
                             SELECT c.*
                             FROM categories c 
                             WHERE c.category_id = ?
                             """, (category_id,)).fetchone()
            if row is None:
                return None
            

            category = row['category_id']

            #Get Permissions
            products = db.execute("""
                                SELECT p.product_name
                                FROM products p
                                JOIN product_categories pc ON p.product_id = pc.product_id
                                WHERE pc.category_id = ?
                                     """, (category,)).fetchall()
            product_list = [p['product_name'] for p in products]
            return Category(
                category_id= category_id,
                category_name=row['category_name'],
                products=product_list
            )
        finally:
            db.close()