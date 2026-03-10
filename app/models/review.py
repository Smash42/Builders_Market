from database.connection import get_connection

class Review:
    def __init__(self, review_id, product_id, user_id, rating):
        self.review_id = review_id
        self.product_id = product_id
        self.user_id = user_id
        self.rating = rating

        # Update Review 
    def UpdateDatabase(self):
        db = get_connection()
        try: 
            sql = """
                UPDATE reviews SET rating =? WHERE review_id = ?;"""

            db.execute(sql, [self.rating, self.review_id] )
            db.commit()
        finally:
            db.close()

    # Delete review
    def Delete(self):
        db = get_connection()
        try:
            sql = """DELETE FROM reviews WHERE review_id = ?;"""
            db.execute(sql, [self.review_id])
            db.commit()
        finally:
            db.close()

# Create New Review
    @staticmethod
    def Create(rating, product_id, user_id):
        db = get_connection()
        try: 
            sql = """INSERT INTO reviews (rating, product_id, user_id) VALUES (?, ?, ?);"""
            cursor = db.execute(sql, [rating, product_id, user_id])
            db.commit()
            review_id = cursor.lastrowid
            return Review.FromDB(review_id)
        finally:
            db.close()

    #Get all reviews
    @staticmethod
    def GetAll():
        db= get_connection()
        try: 
            return db.execute("""
                              SELECT r.*, p.product_name as product_name, u.username as username
                              FROM reviews r
                              JOIN products p ON r.product_id = p.product_id
                              JOIN users u ON r.user_id = u.user_id
                              ORDER BY r.created_at DESC
                              """).fetchall()
        finally:
            db.close()

    #get by user    
    @staticmethod
    def GetByUser(user_id):
        db = get_connection()
        try:
            return db.execute("""
                             SELECT r.*, p.product_name as product_name, u.username as username
                             FROM reviews r
                             JOIN products p ON r.product_id = p.product_id
                             JOIN users u ON r.user_id = u.user_id
                             WHERE r.user_id = ?
                             ORDER BY r.created_at DESC
                              """, (user_id,)).fetchall()
        finally: 
            db.close()    

    #get by product for Product Detail
    @staticmethod
    def GetByProduct(product_id):
        db = get_connection()
        try:
            return db.execute("""
                             SELECT r.*, u.username
                             FROM reviews r
                             JOIN users u ON r.user_id = u.user_id
                              WHERE r.product_id = ?
                             ORDER BY r.created_at DESC
                              """, (product_id,)).fetchall()
        finally: 
            db.close()                                    
    
    # DB from row
    @staticmethod   
    def FromDBRow(row):
        if row is None:
            return None
        return Review(
            review_id=row['review_id'],
            product_id=row['product_id'],
            rating=row['rating'],      
            user_id=row['user_id']
        )

    @staticmethod  
    def FromDB(review_id):
        db = get_connection()
        sql = "SELECT * FROM reviews WHERE review_id = ?;"
        result = db.execute(sql, [review_id,]).fetchone()
        return Review.FromDBRow(result)