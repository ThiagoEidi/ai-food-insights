import pytest
from sqlalchemy import select

from app.enums import UserRole
from app.models import User
from app.utils import verify_password


@pytest.mark.asyncio
async def test_create_user_db(session):
    new_user = User(
        username='thiago',
        email='algum@email.com',
        role=UserRole.CLIENT,
        senha='123',
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    user_db = await session.scalar(
        select(User).where(User.email == 'algum@email.com')
    )

    assert user_db.username == 'thiago'
    assert user_db.email == 'algum@email.com'
    assert user_db.id == 1
    assert verify_password('123', user_db.senha)
