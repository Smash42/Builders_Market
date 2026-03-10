from database.connection import get_connection


class Permission:
    def __init__(self, permission_id, permission_name, description):
        self.permission_id = permission_id
        self.permission_name = permission_name
        self.description = description



    #Get all Roles
    @staticmethod
    def GetAll():
        db= get_connection()
        try:
            rows = db.execute("""
                              SELECT p.*
                              FROM permissions p
                              ORDER BY permission_name
                              """).fetchall()

            return rows
        finally:
            db.close()
    
    # DB from row
    @staticmethod   
    def FromDBRow(row):
        if row is None:
            return None
        return Permission(
            permission_id=row['permission_id'],
            permission_name=row['permission_name'],
            description = row['description']
        )

