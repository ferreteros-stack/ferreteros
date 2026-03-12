"""initial schema

Revision ID: 80947128071f
Revises: 
Create Date: 2026-03-05 21:54:30.859977

"""
from alembic import op
import sqlalchemy as sa

revision = '80947128071f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 1. tenants — raíz, sin dependencias
    op.create_table('tenants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('slug', sa.String(100), nullable=False),
    sa.Column('plan', sa.String(50), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('tenants', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_tenants_slug'), ['slug'], unique=True)

    # 2. branches — depende de tenants
    op.create_table('branches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('address', sa.String(255), nullable=True),
    sa.Column('is_main', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('branches', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_branches_tenant_id'), ['tenant_id'], unique=False)

    # 3. products — catálogo global, sin tenant
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(64), nullable=False),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('category', sa.String(100), nullable=True),
    sa.Column('brand', sa.String(100), nullable=True),
    sa.Column('image_url', sa.String(500), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_products_sku'), ['sku'], unique=True)

    # 4. roles — depende de tenants
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_roles_tenant_id'), ['tenant_id'], unique=False)

    # 5. users — depende de tenants, branches, roles
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('branch_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(255), nullable=False),
    sa.Column('email', sa.String(255), nullable=False),
    sa.Column('password_hash', sa.String(255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tenant_id', 'email', name='uq_user_tenant_email')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_tenant_id'), ['tenant_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=False)

    # 6. stocks — depende de tenants, branches, products
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('branch_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('min_stock', sa.Integer(), nullable=True),
    sa.Column('max_stock', sa.Integer(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('cost', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_stocks_tenant_id'), ['tenant_id'], unique=False)

    # 7. sales — depende de tenants, branches, users
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('branch_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('discount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('payment_method', sa.String(50), nullable=False),
    sa.Column('status', sa.String(50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['branch_id'], ['branches.id'], ),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sales_tenant_id'), ['tenant_id'], unique=False)

    # 8. sale_items — depende de sales, products
    op.create_table('sale_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sale_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('discount', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['sale_id'], ['sales.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # 9. ai_logs — depende de tenants
    op.create_table('ai_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tenant_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(100), nullable=False),
    sa.Column('input_data', sa.JSON(), nullable=True),
    sa.Column('output_data', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('ai_logs', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_ai_logs_tenant_id'), ['tenant_id'], unique=False)


def downgrade():
    op.drop_table('ai_logs')
    with op.batch_alter_table('sale_items', schema=None) as batch_op:
        pass
    op.drop_table('sale_items')
    with op.batch_alter_table('sales', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sales_tenant_id'))
    op.drop_table('sales')
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_stocks_tenant_id'))
    op.drop_table('stocks')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_index(batch_op.f('ix_users_tenant_id'))
    op.drop_table('users')
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_roles_tenant_id'))
    op.drop_table('roles')
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_products_sku'))
    op.drop_table('products')
    with op.batch_alter_table('branches', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_branches_tenant_id'))
    op.drop_table('branches')
    with op.batch_alter_table('tenants', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_tenants_slug'))
    op.drop_table('tenants')