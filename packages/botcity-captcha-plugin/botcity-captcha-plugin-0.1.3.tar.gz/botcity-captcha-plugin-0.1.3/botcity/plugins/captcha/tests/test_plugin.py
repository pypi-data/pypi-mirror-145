import os

from botcity.plugins.captcha import BotAntiCaptchaPlugin, BotDeathByCaptchaPlugin


cur_dir = os.path.abspath(os.path.dirname(__file__))


def test_anticaptcha() -> None:
    # AntiCaptcha - Text
    anti_captcha = BotAntiCaptchaPlugin(os.getenv("ANTICAPTCHA_KEY"))
    assert anti_captcha.solve_text(os.path.join(cur_dir, "captcha_ms.jpeg")) == '56nn2'
    anti_captcha.report()

    # AntiCaptcha - Re
    url = 'https://www.google.com/recaptcha/api2/demo'
    site_key = '6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-'
    assert anti_captcha.solve_re(url, site_key)
    anti_captcha.report()

    # AntiCaptcha - Fun
    url = 'https://api.funcaptcha.com/fc/api/nojs/?pkey=69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC'
    site_key = '69A21A01-CC7B-B9C6-0F9A-E7FA06677FFC'
    assert anti_captcha.solve_fun(url, site_key)


def test_deathbycaptcha() -> None:
    # Death By Captcha
    dbc = BotDeathByCaptchaPlugin(os.getenv("DBC_USERNAME"), os.getenv("DBC_PASSWORD"))
    assert dbc.solve(os.path.join(cur_dir, "captcha_ms.jpeg")) == '56nn2'
