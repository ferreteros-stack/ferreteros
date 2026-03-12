from wsgi import app
from app.core.extensions import db

app_ctx = app.app_context()
app_ctx.push()

# Borrar todas las tablas existentes en orden correcto (respetando FKs)
with db.engine.connect() as conn:
    conn.execute(db.text("DROP TABLE IF EXISTS ai_logs CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS sale_items CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS sales CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS stocks CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS users CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS roles CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS products CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS branches CASCADE"))
    conn.execute(db.text("DROP TABLE IF EXISTS tenants CASCADE"))
    conn.execute(db.text("DELETE FROM alembic_version"))
    conn.commit()

print("Tablas eliminadas y alembic_version limpiada")