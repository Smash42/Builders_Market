from database.connection import get_connection
from datetime import datetime
from sqlite3 import Error


class Order:

    def __init__(self, order_id, user_id, total ):
        self.order_id = order_id
        self.user_id = user_id
        self.total = total

    
    @staticmethod
    def Create(user_id, total_price) :
            db = get_connection()
            try: 
                cursor = db.cursor()

                cursor.execute("""
                    INSERT INTO orders (user_id, total, status, created_at)
                    VALUES (?, ?, ?, ?)
                """, (user_id, total_price, "Pending", datetime.utcnow()
                ))
                
                order_id = cursor.lastrowid
                db.commit()
                return order_id
            finally:
                db.close()


    @staticmethod
    def GetAll():
        db = get_connection()
        try:
            return db.execute("""
                SELECT * FROM orders
                ORDER BY created_at DESC
            """).fetchall()
        finally:
            db.close()


    @staticmethod
    def GetByUser(user_id):
        db = get_connection()
        try:
            return db.execute("""
                SELECT * FROM orders
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,)).fetchall()
        finally:
            db.close()

    @staticmethod
    def GetByID(order_id):
        db = get_connection()
        try:
            return db.execute("""
                SELECT o.*, u.username 
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                WHERE order_id = ?
            """, (order_id,)).fetchone()
        finally:
            db.close()
    
    @staticmethod
    def UpdateStatus(order_id, status):
        db = get_connection()
        try:
            db.execute("""
                       UPDATE orders
                       SET status = ?, updated_at = ?
                       WHERE order_id = ?
                       """, (status, datetime.utcnow(), order_id))
            db.commit()
        finally:
            db.close()

    @staticmethod
    def Delete(order_id):
        db = get_connection()
        try:
            db.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
            db.commit()
        finally:
            db.close()
        
    
class OrderItem:
    @staticmethod
    def Create(db, order_id, product_id, quantity, purchase_price):
        try:
            cursor = db.cursor()

            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, quantity, purchase_price)
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                product_id,
                quantity,
                purchase_price
            ))

            return cursor.lastrowid

        except Error as e:
            print(f"Error creating order item: {e}")
            return None
        
    @staticmethod
    def GetByOrder(order_id):
        db = get_connection()
        rows = db.execute("""
                         SELECT oi.*, p.product_name,             
                        oi.quantity,
                            oi.purchase_price AS price,
                            (oi.quantity * oi.purchase_price) AS item_total
                         FROM order_items oi
                         JOIN products p
                         ON oi.product_id = p.product_id
                         WHERE oi.order_id = ?
                         """, (order_id,)).fetchall()
        db.close()

        return rows
