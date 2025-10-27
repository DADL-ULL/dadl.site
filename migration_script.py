# from app import app, db, Student

# with app.app_context():
#     # Add new columns
#     with db.engine.connect() as conn:
#         try:
#             conn.execute(db.text('ALTER TABLE student ADD COLUMN is_cosupervised BOOLEAN DEFAULT FALSE'))
#             conn.execute(db.text('ALTER TABLE student ADD COLUMN cosupervisor_name VARCHAR(200)'))
#             conn.execute(db.text('ALTER TABLE student ADD COLUMN cosupervisor_affiliation VARCHAR(300)'))
#             conn.commit()
#             print("✓ Migration successful!")
#         except Exception as e:
#             print(f"Migration failed or columns already exist: {e}")

from app import app, db

with app.app_context():
    try:
        with db.engine.begin() as conn:
            conn.execute(db.text('ALTER TABLE student ADD COLUMN "order" INTEGER DEFAULT 999'))
            print("✓ Added 'order' column to student table")
    except Exception as e:
        print(f"Error (column may already exist): {e}")