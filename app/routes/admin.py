from flask import Blueprint, request, jsonify, session
from auth.auths import login_required, user_role_required
from auth.permissions import permission_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

#View All Users
@admin_bp.route('/users', methods=['GET'])
@login_required
@user_role_required('admin')
def view_users():
    #stub for now to ensure that all routes are working properly.
    return jsonify({'success': True, 'message': 'GET /api/admin/users Route. User list retrieved successfully' }), 200


#User Detail
@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required 
@user_role_required('admin')

def user_detail(user_id):
    #Stub for now to ensure that all routes are working properly.
    return jsonify({'success': True, 'message': f'GET /api/admin/users/{user_id} Route. User detail retrieved successfully' }), 200

#Assign/update User Roles
@admin_bp.route('/users/<int:user_id>/role', methods=['PATCH'])
@login_required
@user_role_required('admin')
@permission_required('user.changrole')
def update_user_role(user_id):
    #Stub for now to ensure that all routes are working properly.
    #Get new role from form, validate role, if valid update user role in DB. 
    return jsonify({'success': True, 'message': f'PUT /api/admin/users/{user_id}/role Route. User role updated successfully' }), 200

#Delete User
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@permission_required('user.delete')
def delete_user(user_id):
    #Stub for now to ensure that all routes are working properly.
    #Delete user from DB. 
    return jsonify({'success': True, 'message': f'DELETE /api/admin/users/{user_id} Route. User deleted successfully' }), 204

#Edit User
@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
@permission_required('user.edit')
def edit_user(user_id):
    #Stub for now to ensure that all routes are working properly.
    #Get updated user info from form, validate info, if valid update user in DB. 
    return jsonify({'success': True, 'message': f'PUT /api/admin/users/{user_id} Route. User updated successfully' }), 200

# View Roles
@admin_bp.route('/roles', methods=['GET'])
@login_required
@permission_required('role.read')
def view_roles():
    #Stub for now to ensure that all routes are working properly.
    return jsonify({'success': True, 'message': 'GET /api/admin/roles Route. Role list retrieved successfully' }), 200

#Create a new role
@admin_bp.route('/roles', methods=['POST'])
@login_required
@permission_required('role.add')
def create_role():
    #Stub for now to ensure that all routes are working properly.
    #Get role name and permissions from form, validate info, if valid create new role in DB. 
    return jsonify({'success': True, 'message': 'POST /api/admin/roles Route. Role created successfully' }), 201

#Edit Role
@admin_bp.route('/roles/<int:role_id>', methods=['PUT'])
@login_required
@permission_required('role.edit')
def edit_role(role_id):
    #Stub for now to ensure that all routes are working properly.
    #Get updated role name and permissions from form, validate info, if valid update role in DB. 
    return jsonify({'success': True, 'message': f'PUT /api/admin/roles/{role_id} Route. Role updated successfully' }), 200

#Delete Role
@admin_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@login_required
@permission_required('role.delete')
def delete_role(role_id):
    #Stub for now to ensure that all routes are working properly.
    #Delete role from DB. 
    return jsonify({'success': True, 'message': f'DELETE /api/admin/roles/{role_id} Route. Role deleted successfully' }), 204

# List all Permissions, read
@admin_bp.route('/permissions', methods=['GET'])
@login_required
@user_role_required('admin')
def view_permissions():
    #Stub for now to ensure that all routes are working properly.
    return jsonify({'success': True, 'message': 'GET /api/admin/permissions Route. Permission list retrieved successfully' }), 200