import re
import secrets
import hashlib

from flask import sessions, render_template
from flask_login import login_user

from SuppleTime.pr.app.models.user.login_manager import login_manager

from dependency_injector.wiring import inject, Provide
from SuppleTime.pr.app.containers import Container

from SuppleTime.pr.app.database.unit_of_work import UnitOfWork
from SuppleTime.pr.app.database.repository import Repository
from SuppleTime.pr.app.database.exceptions import NotFoundException

from SuppleTime.pr.app.models.user import User, ConfirmUser, NonConfirmedUser
from SuppleTime.pr.app.models.Email import Email
from SuppleTime.pr.app.models.Workspace import *
from SuppleTime.pr.app.models.Workspace.services import *

from SuppleTime.pr.app.config import salt
        
#requests  
@inject
def get_all_users(repository: Repository = Provide[Container.users_repository]) -> list:
    return repository.list()


@inject
def get_all_nonconfirmedusers(repository: Repository = Provide[Container.nonconfirmed_users_repository]) -> list:
    return repository.list()


@inject
def get_user(repository: Repository = Provide[Container.users_repository], **kwargs) -> None or User:
    try:
        return repository.get(**kwargs)
    except NotFoundException as exc:
        print("User not found: ", exc)
        return None


@inject
def get_nonconfirmed_user(repository: Repository = Provide[Container.nonconfirmed_users_repository], **kwargs) -> None or NonConfirmedUser:
    try:
        return repository.get(**kwargs)
    except NotFoundException as exc:
        pass


# @inject
# def get_nonconfirmed_user_by_email(email: str, repository: Repository = Provide[Container.nonconfirmed_users_repository]) -> None or NonConfirmedUser:
#     try:
#         return repository.get(email=email)
#     except NotFoundException as exc:
#         print("User not found: ", exc)
#         return None


# @inject
# def get_nonconfirmed_user_by_token(token: str, repository: Repository = Provide[Container.nonconfirmed_users_repository]) -> None or NonConfirmedUser:
#     try:
#         return repository.get(confirm_token=token)
#     except NotFoundException as exc:
#         print("User not found: ", exc)
#         return None


@inject
def get_confirmed_user(repository: Repository = Provide[Container.confirm_users_repository], **kwargs) -> None or User:
    try:
        return repository.get(**kwargs)
    except NotFoundException as exc:
        pass

# @inject
# def get_confirmed_user_by_token(token: str, repository: Repository = Provide[Container.confirm_users_repository]) -> None or User:
#     try:
#         return repository.get(token=token)
#     except NotFoundException as exc:
#         pass


# @inject
# def is_user_in_db(email: str, repository: Repository = Provide[Container.users_repository]) -> User:
#     return repository.get(email=email)


#loading user
@login_manager.user_loader
def load_user(id):
    return get_user(id=id)


#security
def generate_token():
    return secrets.token_urlsafe()


def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

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
 

def check_password(email: str, password: str):
    user = get_user(email=email)
    if not user: return False
    return user.confirm_users.password_hash == get_password_hash(password)


def login(data):
    email = data.get("email")
    password = data.get("password")
    user = get_user(email=email)
    remember = True if data.get("rememberme") else False
    if password is None or password == "" or email is None or email == "": 
        return ("Please enter your email and password","error") #("�� ����� ������������ ������", "error")
    if check_password(email, password):
        login_user(user, remember=remember)
        return ("Success", "message")
    return ("Wrong email or password ", "error")
            
    
@inject
def create_user(name: str, email: str, password_hash: str, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        new_user = User(name=name, email=email)
        uow.repository.save(new_user)
        uow.commit()
        uow.repository.session.refresh(new_user)
        uow.repository.session.expunge(new_user)
        new_confirm_user = ConfirmUser(id=new_user.id, token=generate_token(), password_hash=password_hash)
        uow.repository.save(new_confirm_user)
        uow.commit()
        return new_user


@inject
def delete_nonconfirmed_user(id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        uow.repository.session.query(NonConfirmedUser).filter_by(id=id).delete()
        uow.commit()


@inject
def delete_all_users(unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        #users = get_all_users()
        uow.repository.session.query(ConfirmUser).delete()
        uow.repository.session.query(Trackers).delete()
        uow.repository.session.query(User).delete()
        # uow.repository.session.query(NonConfirmedUser).delete()
        
        uow.commit()


@inject
def delete_user(id: int, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        uow.repository.session.query(Trackers).filter_by(user_id=id).delete()
        uow.repository.session.query(ConfirmUser).filter_by(id=id).delete()
        uow.repository.session.query(Tracked_tasks).filter_by(tracked_user_id=id).delete()
        uow.repository.session.query(User).filter_by(id=id).delete()
        
        uow.commit()


@inject
def create_nonconfirmed_user(email, password, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    with unit_of_work as uow:
        nonconfirmeduser = NonConfirmedUser(id=len(get_all_nonconfirmedusers()) + 1, email=email, password_hash=get_password_hash(password), confirm_token=generate_token())
        uow.repository.save(nonconfirmeduser)

        uow.commit()
        return nonconfirmeduser.confirm_token


def preregister_user(data) -> str:
    email = data.get("email")
    password = data.get("password")
    if password is None or password == "" or email is None or email == "": return ("Please enter your email and password","error") #("�� ����� ������������ ������", "error")
    if email == '' or not is_valid_email(email): return ("Incorrect email","error")#("������������ email","error")
    is_valid = is_valid_password(password)
    if is_valid is not True: return (is_valid, "error")
    # if get_nonconfirmed_user(email=email): return ("This email address is already taken please choose a unique one","error")#("������������ � ����� email ��� ����������", "error")
    if get_user(email=email): return ("This email address is already taken please choose a unique one","error")
    nonuser = get_nonconfirmed_user(email=email)
    if nonuser:
        delete_nonconfirmed_user(nonuser.id)
    
    confirm_token = create_nonconfirmed_user(email, password)
    if confirm_token:
        Email.send(email, render_template("auth/confirm_email_mail.html", confirm_token=confirm_token), "Email Verify", is_html=True)
        return ("We send email on your email", "message") 
    return ("Unknown error, please try again later", "error")


def final_register_user(user):
    delete_nonconfirmed_user(user.id)
    user = create_user(user.email.split("@")[0], user.email, user.password_hash)
    create_tracker(user.id)
    return user


def send_passwd_mail(email: str):
    if email == '':
        return ("Valid email", "error")
    user = get_user(email=email)
    if user:
        Email.send(email, f"suppletime.ru/auth/passwordchange/{user.confirm_users.token}", "Password change", is_html=True)
        return ("Check your email.", "message")


def send_enter_mail(email: str):
    if email == '':
        return ("Valid email", "error")
    user = get_user(email=email)
    if user:
        Email.send(email, f"suppletime.ru/auth/enterbymail/{user.confirm_users.token}", "Enter by mail")
        return ("Check your email.", "message")


@inject
def change_password(user: ConfirmUser, passwd1: str, passwd2: str, unit_of_work: UnitOfWork = Provide[Container.user_uow]):
    if passwd1 != passwd2: return ("p1 != p2", "error")
    is_valid = is_valid_password(passwd1)
    if not is_valid: return is_valid
    with unit_of_work as uow:
        user = uow.session.query(ConfirmUser).filter_by(id=user.id).first()
        user.password_hash = get_password_hash(passwd1)
        user.token = generate_token()

        uow.commit()
        return ("Success", "message")
    return "ERROR", "error"
