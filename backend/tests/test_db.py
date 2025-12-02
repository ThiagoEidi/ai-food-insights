import pytest
from sqlalchemy import select

from app.models import Store, StoreFoodTypes, User, UserRole
from app.utils import verify_password


@pytest.mark.asyncio
async def test_create_user_db(session):
    new_user = User(
        username='thiago',
        email='algum@email.com',
        role=UserRole.PARTNER,
        senha='123',
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    user_db = await session.scalar(select(User).where(User.email == 'algum@email.com'))

    assert user_db.username == 'thiago'
    assert user_db.email == 'algum@email.com'
    assert user_db.id == 1
    assert verify_password('123', user_db.senha)


@pytest.mark.asyncio
async def test_create_store_db(session, user):
    new_store = Store(
        name='ifood',
        address='rua não sei das quantas',
        partner_id=user.id,
        food_type_associations=[
            StoreFoodTypes(food_type_id=1),
            StoreFoodTypes(food_type_id=3),
            StoreFoodTypes(food_type_id=5),
        ],
    )

    session.add(new_store)
    await session.commit()
    await session.refresh(new_store)

    __import__('ipdb').set_trace()

    store_db = await session.scalar(select(Store).where(Store.name == 'ifood'))

    assert store_db.name == 'ifood'
    assert store_db.address == 'rua não sei das quantas'
    assert store_db.partner_id == user.id
    assert store_db.id == 1
