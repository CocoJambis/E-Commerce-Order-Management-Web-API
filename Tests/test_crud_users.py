from App.crud import(
    UserRepository,
)

from App.models import (UserCreate)
import pytest
from fastapi import HTTPException



@pytest.mark.anyio
async def test_create_user(db_session):

    new_user = UserCreate(
        first_name="Mario",
        last_name="Rossi",
        email="mario.rossi@gmail.com",
        password="123"
    )

    user = await UserRepository.create_user(new_user=new_user, db=db_session)

    assert user is not None
    assert user.email == "mario.rossi@gmail.com"


@pytest.mark.anyio
async def test_create_user_existing(db_session):

    new_user = UserCreate(
            first_name="Mario",
            last_name="Rossi",
            email="mario.rossi@gmail.com",
            password="123"
        )
    
    await UserRepository.create_user(new_user=new_user, db=db_session)

    new_user2 = UserCreate(
        first_name="Luigi",
        last_name="Rossi",
        email="mario.rossi@gmail.com",
        password="123"
    )

    with pytest.raises(HTTPException) as exc_info:
        await UserRepository.create_user(new_user=new_user2, db=db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "mario.rossi@gmail.com già esistente"



@pytest.mark.anyio
async def test_list_all_users(db_session):

    new_user = UserCreate(
            first_name="Mario",
            last_name="Rossi",
            email="mario.rossi@gmail.com",
            password="123"
        )
    
    await UserRepository.create_user(new_user=new_user, db=db_session)

    all_users = await UserRepository.user_list(db=db_session)

    assert all_users is not None
    assert isinstance(all_users, list)
    assert len(all_users) == 1
    assert all_users[0].email == "mario.rossi@gmail.com"

@pytest.mark.anyio
async def test_list_all_users_empty(db_session):

    list = await UserRepository.user_list(db=db_session)

    assert list == []


@pytest.mark.anyio
async def test_delete_user(db_session):

    new_user = UserCreate(
                first_name="Mario",
                last_name="Rossi",
                email="mario.rossi@gmail.com",
                password="123"
            )
        
    await UserRepository.create_user(new_user=new_user, db=db_session)

    result = await UserRepository.delete_user(
        user_id = 1,
        db = db_session)

    assert result == "User con id : 1 eliminato dal database!"


@pytest.mark.anyio
async def test_delete_user_not_existing(db_session):


    with pytest.raises(HTTPException) as exc_info:
        await UserRepository.delete_user(user_id = 1, db = db_session)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User con id : 1 non esistente nel database!"


