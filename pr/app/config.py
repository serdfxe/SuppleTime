DATABASE_URL = "postgresql+psycopg2://test:314159@127.0.0.1:5432/suppletime_db"

# EMAIL_PASS = "31415926535asd"
# EMAIL_ADDRES = "noreply@sheeesh.ru"

EMAIL_PASS = "314159asdffdsa"
EMAIL_ADDRES = "noreply@suppletime.ru"

salt = "" 

color_list = [[16, 23, 39], [41, 52, 78], [88, 89, 107], [143, 143, 144], [197, 197, 197], [68, 79, 234], [93, 101, 214], [119, 128, 255], [159, 166, 255], [208, 211, 255], [26, 73, 127], [61, 109, 164], [105, 149, 200], [115, 171, 235], [80, 161, 255], [25, 86, 94], [77, 134, 141], [135, 177, 183], [124, 199, 209], [107, 227, 243], [23, 99, 62], [39, 142, 91], [54, 184, 121], [104, 220, 164], [148, 253, 202], [181, 158, 15], [246, 214, 9], [255, 235, 107], [255, 241, 152], [255, 250, 217], [206, 64, 71], [242, 56, 66], [255, 74, 83], [254, 111, 80], [253, 149, 76], [255, 55, 159], [255, 105, 183], [255, 148, 204], [255, 186, 222], [255, 217, 237]]

sidebar_components = {
    "Главная":"main",
    "Трекер": "tracker",
    "Работа":"work",
    "Планы":"schedule",
    "Команды":"teams",
    "Настройки":"settings",
    "Личный кабинет":"account",
}

url_for_sidebar_components = {
    "main": "main.svg",
    "work": "work.svg",
    "schedule": "statistics.svg",
    "teams": "teams.svg",
    "settings": "settings.svg",
    "account": "account.svg",
    "tracker": "timer.svg"
}

content = {
    "main": "https://c.tenor.com/qwR44XG-f5kAAAAd/%D1%81%D0%BA%D0%B0%D0%BB%D0%B0.gif",
    "work": "https://memepedia.ru/wp-content/uploads/2019/06/stonks-template.png",
    "schedule": "https://s10.stc.yc.kpcdn.net/share/i/12/11065821/wr-960.webp", 
    "teams": "http://risovach.ru/upload/2016/03/mem/nelzya-prosto-tak-vzyat-i-boromir-mem_109594771_orig_.jpg", 
    "settings": "https://www.meme-arsenal.com/memes/b294fe2e35afa11184389f572480661e.jpg", 
    "account": "https://www.meme-arsenal.com/memes/997b08a8d833988619ef9e6cea4233d0.jpg",
    "tracker": ""
}

authforms = {
    "passwordchange": {"title": "Смена пароля", "subtitle": "Введите новый пароль.", "ref": None, "form": [
        ("first_label", "Новый пароль"),
        ("pass_input", "password1", "Введите новый пароль..."),
        ("label", "Подтверждение пароля"),
        ("pass_input", "password2", "Повторно введите новый пароль..."),
        ("submit", "Сменить пароль")]},

    "enterbymail": {"title": "Вход по ссылке", 'subtitle': "Введите Вашу почту. На неё прийдёт ссылка для входа.", "ref": None, "form": [
        ("text_input", "email", "Введите почту..."), 
        ("submit", "Отослать ссылку")]},

    "signup": {"title": "Регистрация", "subtitle": "Введите данные для регистрации.", "ref": ["Уже есть аккаунт?", "/signin"], "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("submit", "Зарегистрироваться")]},

    "signin": {"title": "Авторизация", "subtitle": "Введите данные для входа.", "ref": ["Ещё нет аккаунта?", "/signup"], "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("label", "Пароль"),
        ("pass_input", "password", "Введите пароль..."),
        ("check_box", "rememberme", "Запомнить при следующем входе?"),
        ("ref", "forgotpassword", "Забыли пароль?"),
        ("two_btn", (("submit_btn", "Войти"), ("redirect_btn", "Войти по почте", "enterbymail")))]},
    
    "forgotpassword": {"title": "Забыли пароль?", "subtitle": "Введите Вашу почту. На неё прийдёт ссылка для смены пароля.", "ref": None, "form": [
        ("first_label", "Почта"),
        ("text_input", "email", "Введите почту..."),
        ("submit", "Отправить письмо")]},
}
