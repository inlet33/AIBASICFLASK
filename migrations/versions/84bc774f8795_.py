"""empty message

Revision ID: 84bc774f8795
Revises: c98cf4406141
Create Date: 2019-09-27 09:53:47.246753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84bc774f8795'
down_revision = 'c98cf4406141'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'course_sections', 'courses', ['course_id'], ['id'])
    op.create_foreign_key(None, 'enrollments', 'students', ['student_id'], ['id'])
    op.create_foreign_key(None, 'enrollments', 'schedules', ['schedule_id'], ['id'])
    op.create_foreign_key(None, 'schedules', 'subjects', ['subject_id'], ['id'])
    op.create_foreign_key(None, 'schedules', 'teachers', ['teacher'], ['id'])
    op.create_foreign_key(None, 'schedules', 'course_sections', ['section_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_constraint(None, 'schedules', type_='foreignkey')
    op.drop_constraint(None, 'enrollments', type_='foreignkey')
    op.drop_constraint(None, 'enrollments', type_='foreignkey')
    op.drop_constraint(None, 'course_sections', type_='foreignkey')
    # ### end Alembic commands ###
