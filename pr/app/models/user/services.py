import re
import secrets
import hashlib

from flask import sessions
from flask_login import login_user

from SuppleTime.pr.app.models.user.login_manager import login_manager

from dependency_injector.wiring import inject, Provide
from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.database.unit_of_work import UnitOfWork
from SuppleTime.pr.app.database.repository import Repository
from SuppleTime.pr.app.database.exceptions import NotFoundException

from SuppleTime.pr.app.models.user import User, ConfirmUser

from SuppleTime.pr.app.config import salt
        
        
@inject
def get_all_users(repository: Repository = Provide[Container.users_repository]) -> list:
    return repository.list()


@inject
def get_user(id: int, repository: Repository = Provide[Container.users_repository]) -> None or User:
    try:
        return repository.get(id=id)
    except NotFoundException as exc:
        print("User not found: ", exc)
        return None


@login_manager.user_loader
def load_user(id):
    return get_user(id=id)


@inject
def is_user_in_db(email: str, repository: Repository = Provide[Container.users_repository]):
    return True if repository.get(email=email) else False


def generate_token():
    return secrets.token_urlsafe()


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
 
@inject
def check_password(email: str, password: str, repository: Repository = Provide[Container.users_repository]):
    #email = data.get("email")
    #password = data.get("password")
    user = repository.get(email=email)
    password_hash_db = user.confirm_users.password_hash
    password_hash = get_password_hash(password)
    if password_hash_db == password_hash:
        return True
    return False

@inject
def login(data, repository: Repository = Provide[Container.users_repository]):
    email = data.get("email")
    password = data.get("password")
    user = repository.get(email=email)
    remember = True if data.get("rememberme") else False
    if password is None or password == "" or email is None or email == "": 
        return ("Please enter your email and password","error") #("�� ����� ������������ ������", "error")
    if check_password(email, password):
        login_user(user, remember=remember)
        return ("Success", "message")
    return ("Wrong email or password ", "error")
            
    
@inject
def create_user(name: str, email: str, password: str, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        user_id = len(get_all_users())
        new_user = User(name=name, email=email, id=user_id)
        new_confirm_user = ConfirmUser(id=user_id, token=generate_token(), password_hash=get_password_hash(password))
        uow.repository.save(new_user)
        uow.repository.save(new_confirm_user)
        uow.commit()
        return True


def is_valid_email(email: str) -> bool: 
    return re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email)


def is_valid_password(password: str) -> bool:
    if len(password) < 8:
        return "Make sure that your password is at least 8 characters long"  #"���������, ��� ��� ������ ������ 8 �������� � �����"
    elif re.search('[0-9]',password) is None:
        return "Make sure that your password contains at least one digit" #"���������, ��� � ����� ������ ���� �����"
    elif re.search('[A-Z]',password) is None: 
        return "Make sure that your password contains at least one capital letter" #"���������, ��� � ����� ������ ���� ��������� �����"
    else:
        return True


def register_user(data) -> str:
    email = data.get("email")
    password = data.get("password")
    if password is None or password == "" or email is None or email == "": return ("Please enter your email and password","error") #("�� ����� ������������ ������", "error")
    if email == '' or not is_valid_email(email): return ("Incorrect email","error")#("������������ email","error")
    is_valid = is_valid_password(password)
    if is_valid is not True: return (is_valid, "error")
    if is_user_in_db(email): return ("This email address is already taken please choose a unique one","error")#("������������ � ����� email ��� ����������", "error")
    name = email.split("@")[0]
    return ("Registration successful", "message") if create_user(name, email, password) else ("Unknown error, please try again later", "error")


@inject
def delete_all_users(unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        #users = get_all_users()
        uow.repository.session.query(ConfirmUser).delete()
        uow.repository.session.query(User).delete()
        
        uow.commit()


