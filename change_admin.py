from app import app, db, AdminUser
from werkzeug.security import generate_password_hash

NEW_USERNAME = 'dadl_admin'  
NEW_PASSWORD = 'dadlull71' 

with app.app_context():
    # Get the first admin user
    admin = AdminUser.query.first()
    
    if admin:
        admin.username = NEW_USERNAME
        admin.password_hash = generate_password_hash(NEW_PASSWORD)
        db.session.commit()
        print(f"✓ Admin credentials updated!")
        print(f"  Username: {NEW_USERNAME}")
        print(f"  Password: {NEW_PASSWORD}")
    else:
        # Create new admin if none exists
        new_admin = AdminUser(
            username=NEW_USERNAME,
            password_hash=generate_password_hash(NEW_PASSWORD),
            name='Administrator'
        )
        db.session.add(new_admin)
        db.session.commit()
        print(f"✓ New admin created!")
        print(f"  Username: {NEW_USERNAME}")
        print(f"  Password: {NEW_PASSWORD}")