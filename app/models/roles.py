from database.connection import get_connection


class Role:
    def __init__(self, role_id, role_name, permissions = None ):
        self.role_id = role_id
        self.role_name = role_name
        self.permissions = permissions or []


#Get all Roles
    @staticmethod
    def GetAll():
        db= get_connection()
        sql = "SELECT * FROM roles;"
        results = db.execute(sql).fetchall()
        
        out = []
        for r in results:
            dev = Role.FromDB(r['role_id'])
            if dev is None:
                continue
            out.append(dev)
        return out
    
    # Create New Role
    @staticmethod
    def Create(name, description):
        db = get_connection()
        sql = """INSERT INTO roles (role_name, description) VALUES (?, ?)"""
        cursor = db.execute(sql, [name, description])
        role_id = cursor.lastrowid
        db.commit()
        return Role.FromDB(role_id)
    
    
# Delete Role
    def Delete(role_id):
        db = get_connection()
        try:
            db.execute("""
                DELETE FROM roles
                WHERE role_id = ?
            """, (role_id,))
            db.commit()
        finally:
            db.close()

    @staticmethod
    def FromDB(role_id : int):
        db = get_connection()
        try: 
            row = db.execute("""
                             SELECT r.role_id, r.role_name
                             FROM roles r 
                             WHERE r.role_id = ?
                             """, (role_id,)).fetchone()
            if row is None:
                return None

            #Get Permissions
            permissions = db.execute("""
                                SELECT p.permission_id, p.permission_name
                                FROM permissions p
                                JOIN role_permissions rp ON p.permission_id = rp.permission_id
                                WHERE rp.role_id = ?
                                     """, (role_id,)).fetchall()
            permission_list = [
                {"permission_id": p["permission_id"], 
                "permission_name": p["permission_name"] }
                for p in permissions]
            
            permission_ids = [p["permission_id"] for p in permissions]

            role =  Role(
                role_id=row["role_id"],
                role_name=row['role_name'],
                permissions=permission_list
            )
        
            role.permission_ids = permission_ids

            return role

        finally:
            db.close()

    @staticmethod
    def UpdatePermissions(role_id, permission_id):
        db = get_connection()
        try:
            db.execute("DELETE FROM role_permissions WHERE role_id = ?", (role_id,))

            for p in permission_id:
                db.execute(
                    "INSERT INTO role_permissions(role_id, permission_id) VALUES (?,?)", 
                    (role_id, p)
                )
            db.commit()
        finally:
            db.close()