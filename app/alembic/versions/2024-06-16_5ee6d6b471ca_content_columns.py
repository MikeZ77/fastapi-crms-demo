"""content columns

Revision ID: 5ee6d6b471ca
Revises: ead411cc0362
Create Date: 2024-06-16 15:32:13.597207

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ee6d6b471ca'
down_revision: Union[str, None] = 'ead411cc0362'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('content_id', sa.UUID(), nullable=False))
    op.add_column('content', sa.Column('license_id', sa.UUID(), nullable=True))
    op.add_column('content', sa.Column('offer_name', sa.String(), nullable=True))
    op.create_index('ix_content_content_id', 'content', ['content_id'], unique=False)
    op.create_unique_constraint(None, 'content', ['content_id'])
    op.drop_column('content', 'offer_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content', sa.Column('offer_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'content', type_='unique')
    op.drop_index('ix_content_content_id', table_name='content')
    op.drop_column('content', 'offer_name')
    op.drop_column('content', 'license_id')
    op.drop_column('content', 'content_id')
    # ### end Alembic commands ###
