DATABASE_URL = "postgresql+psycopg2://test:314159@127.0.0.1:5432/suppletime_db"

EMAIL_PASS = "31415926535asd"
EMAIL_ADDRES = "noreply@sheeesh.ru"

salt = ""

sidebar_components = {
    "Главная":"main",
    "Работа":"work",
    "Планы":"schedule",
    "Команды":"teams",
    "Настройки":"settings",
    "Личный кабинет":"account"
}

url_for_sidebar_components = {
    "main": "main.svg",
    "work": "work.svg",
    "schedule": "statistics.svg",
    "teams": "teams.svg",
    "settings": "settings.svg",
    "account": "account.svg"
}

content = {
    "main": "https://c.tenor.com/qwR44XG-f5kAAAAd/%D1%81%D0%BA%D0%B0%D0%BB%D0%B0.gif",
    "work": "https://memepedia.ru/wp-content/uploads/2019/06/stonks-template.png",
    "schedule": "https://s10.stc.yc.kpcdn.net/share/i/12/11065821/wr-960.webp", 
    "teams": "http://risovach.ru/upload/2016/03/mem/nelzya-prosto-tak-vzyat-i-boromir-mem_109594771_orig_.jpg", 
    "settings": "https://www.meme-arsenal.com/memes/b294fe2e35afa11184389f572480661e.jpg", 
    "account": "https://www.meme-arsenal.com/memes/997b08a8d833988619ef9e6cea4233d0.jpg"
}

authforms = {
    "passwordchange": {"title": "Смена пароля", "subtitle": "Введите новый пароль.", "form": [
        ("first_label", "Новый пароль"),
        ("pass_input", "password1", "Введите новый пароль..."),
        ("label", "Подтверждение пароля"),
        ("pass_input", "password2", "Повторно введите новый пароль..."),
        ("submit", "Сменить пароль")]},

    "enterbymail": {"title": "Вход по ссылке", 'subtitle': "Введите Вашу почту. На неё прийдёт ссылка для входа.", "form": [
        ("text_input", "email", "Введите почту..."), 
        ("submit", "Отослать ссылку")]},

    "signup": {"title": "Регистрация", "subtitle": "Введите данные для регистрации.", "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("submit", "Зарегистрироваться")]},

    "signin": {"title": "Авторизация", "subtitle": "Введите данные для входа.", "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("check_box", "rememberme", "Запомнить при следующем входе?"),
        ("ref", "forgotpassword", "Забыли пароль?"),
        ("two_btn", (("submit_btn", "Войти"), ("redirect_btn", "Войти по почте", "enterbymail")))]},
    
    "forgotpassword": {"title": "Забыли пароль?", "subtitle": "Введите Вашу почту. На неё прийдёт ссылка для смены пароля.", "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("submit", "Отправить письмо")]},
}
