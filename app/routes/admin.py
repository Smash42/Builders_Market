from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for
from auth.auths import login_required, user_role_required
from auth.permissions import permission_required
from database import connection
from models.permissions import Permission
from models.roles import Role
from models.users import User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

#View All Users
@admin_bp.route('/users', methods=['GET'])
@login_required
@user_role_required('Admin')
def view_users():
    users = User.GetAll()
    return render_template('admin/users.html', users=users)


#User Detail
@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required 
@user_role_required('Admin')
def user_detail(user_id):
    user = User.FromID(user_id)
    roles = Role.GetAll()
    if user is None:
        abort(404)
    #different html page for admin?
    return render_template('admin/user_detail.html', user = user, roles = roles)
 

#Assign/update User Roles
@admin_bp.route('/users/<int:user_id>/role', methods=['POST'])
@login_required
@permission_required('user.changerole')
def update_user_role(user_id):
    user = User.FromID(user_id)
    if not user:
        abort(404)


    role_id = request.form.get('role_id', type = int)
    if not role_id:
        flash("Role is required")
        return redirect(url_for('admin.user_detail', user_id=user_id))
    
    role = Role.FromDB(role_id)
    if not role:
        abort(404)

    User.UpdateRole(user_id, role_id)
    flash("User updated successfully")

    return redirect(url_for('admin.user_detail', user_id=user_id))

#Edit User WITHIN PROFILE?
@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('user.edit')
def edit_user(user_id):
    user = User.FromID(user_id)
    

    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip()

        if len(name) ==0:
            hasError = True
            flash('Error: Enter Valid username')   
        if len(email) ==0:
            hasError = True
            flash('Error: Enter Valid Email')
        #Check Email unique
        if User.FromUsername(name) is not None:
            hasError = True
            flash('Error: Username already registered')

    #Check Email unique
        if User.FromEmail(email) is not None:
            hasError = True
            flash('Error: Email already registered')
        if hasError:
            return redirect(url_for('admin.edit_user', user_id = user_id))
        
        user = User.UpdateUser(user_id, name, email)
    #Get updated user info from form, validate info, if valid update user in DB. 
    return render_template('admin/users_edit.html', user_id = user_id, user = user)

   
#Delete User
@admin_bp.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
@permission_required('user.delete')
def delete_user(user_id):
    user = User.FromID(user_id)
    if user is None:
        abort(404)
    
    if request.method == 'POST':
        User.Delete(user_id)
        flash('User deleted successfully')
        return redirect(url_for('admin.view_users'))
    
    return render_template('admin/users_delete.html', user = user)



# View Roles
@admin_bp.route('/roles', methods=['GET'])
@login_required
@permission_required('role.read')
def view_roles():
    # Add Role Model
    roles = Role.GetAll()
    return render_template('admin/roles.html', roles=roles)


#Create a new role
@admin_bp.route('/roles/add', methods=['GET', 'POST'])
@login_required
@permission_required('role.add')
def create_role():
    if request.method == 'POST':
        role_name = request.form.get('name').strip()    
        description = request.form.get('description').strip()  
        if not role_name:
            flash('Role name Required')
            return render_template('admin/roles_add.html')
        if not description:
            flash('Description required')
            return render_template('admin/roles_add.html')
        
        Role.Create(role_name, description)
        return redirect(url_for('admin.view_roles'))
    return render_template('admin/roles_add.html')



#Edit Role
@admin_bp.route('/roles/<int:role_id>', methods=['GET','POST'])
@login_required
@permission_required('role.edit')
def update_role_permissions(role_id):
    role = Role.FromDB(role_id)
    if role is None:
        abort(404)
        
    permissions = Permission.GetAll()

    if request.method == 'POST':

        permission_list = request.form.getlist("permissions")
        Role.UpdatePermissions(role_id, permission_list)

        return redirect(url_for('admin.view_roles'))
    return render_template('admin/roles_edit.html', role = role, permissions = permissions)


#Delete Role
@admin_bp.route('/roles/<int:role_id>/delete', methods=['GET', 'POST'])
@login_required
@permission_required('role.delete')
def delete_role(role_id):
    role = Role.FromDB(role_id)

    if request.method == 'POST':
        Role.Delete(role_id)
        return redirect(url_for('admin.view_roles'))
    return render_template('admin/roles_delete.html', role = role)
# admin/roles_delete.html

# List all Permissions, read
@admin_bp.route('/permissions', methods=['GET'])
@login_required
@user_role_required('Admin')
def view_permissions():
    permissions = Permission.GetAll()
    return render_template('admin/permissions.html', permissions = permissions)
