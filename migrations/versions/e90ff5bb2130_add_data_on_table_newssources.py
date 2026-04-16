"""Add data on table NewsSources

Revision ID: e90ff5bb2130
Revises: 70ac4ac33d0c
Create Date: 2026-04-16 12:09:35.831806

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'e90ff5bb2130'
down_revision: Union[str, Sequence[str], None] = '70ac4ac33d0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


sources = {'bloomberg':
               {'domain': 'bloomberg.com',
                'language': 'us'},
           'the-wall-street-journal':
               {'domain': 'wsj.com',
                'language': 'us'},
           'business-insider':
               {'domain': 'businessinsider.com',
                'language': 'us'},
           'lenta':
               {'domain': 'lenta.ru',
                'language': 'ru'},
           'null':
               {'domain': 'kommersant.ru',
                'language': 'ru'},
           }

def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()

    for api_id, info in sources.items():
        api_id = api_id
        domain = info['domain']
        language = info['language']

        try:
            connection.execute(
                text("""
                        INSERT INTO news_sources (api_id, domain, language, created, updated) 
                        VALUES (:api_id, :domain, :language, NOW(), NOW())
                    """),
            {"api_id": api_id, "domain": domain, 'language': language}
                    )
        except Exception as e:
            print(f'Ошибка: {e}')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    connection = op.get_bind()

    api_ids = [key for key in sources.keys()]

    connection.execute(
        text("""
                DELETE FROM news_sources 
                WHERE api_id IN :api_ids
            """),
        {"api_ids": tuple(api_ids)}
    )
