"""empty message

Revision ID: c98cf4406141
Revises: 83ae9bf38b03
Create Date: 2019-09-27 09:30:04.580338

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c98cf4406141'
down_revision = '83ae9bf38b03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'course_sections', 'courses', ['course_id'], ['id'])
    op.create_foreign_key(None, 'enrollments', 'schedules', ['schedule_id'], ['id'])
    op.create_foreign_key(None, 'enrollments', 'students', ['student_id'], ['id'])
    op.create_foreign_key(None, 'schedules', 'teachers', ['teacher'], ['id'])
    op.create_foreign_key(None, 'schedules', 'subjects', ['subject_id'], ['id'])
    op.create_foreign_key(None, 'schedules', 'course_sections', ['section_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.add_column('enrollments', sa.Column('updated_at', mysql.DATETIME(), nullable=False))
    op.add_column('enrollments', sa.Column('created_at', mysql.DATETIME(), nullable=False))
    op.drop_constraint(None, 'enrollments', type_='foreignkey')
    op.drop_constraint(None, 'enrollments', type_='foreignkey')
    op.drop_column('enrollments', 'start_year')
    op.drop_column('enrollments', 'end_year')
    op.drop_constraint(None, 'course_sections', type_='foreignkey')
    # ### end Alembic commands ###
