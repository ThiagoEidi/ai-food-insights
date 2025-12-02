from http import HTTPStatus

import pytest

from app.models import UserRole


@pytest.mark.asyncio
async def test_create_user(client, session):
    response = client.post(
        '/conta/',
        json={
            'username': ' Thiago Eidi HAMada',
            'email': 'teste@teste.com',
            'role': UserRole.PARTNER.value,
            'senha': '123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'thiago eidi hamada',
        'email': 'teste@teste.com',
        'id': 1,
    }


@pytest.mark.asyncio
async def test_create_user_with_same_email(user, client):
    response = client.post(
        '/conta/',
        json={
            'username': 'teste',
            'email': user.email,
            'role': UserRole.CLIENT.value,
            'senha': '123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
