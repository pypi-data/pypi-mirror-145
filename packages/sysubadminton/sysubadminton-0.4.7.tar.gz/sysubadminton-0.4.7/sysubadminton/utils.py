import backoff
import json
import requests
from time import sleep
from datetime import datetime
from pathlib import Path
from requests.exceptions import RequestException
from re import findall


def _hdlr(details):
    print_with_time("网络错误，重试 {tries} 次，用时 {wait:0.1f} s".format(**details))

backoff_retry = backoff.on_exception(backoff.expo, RequestException, max_tries=10, on_backoff=_hdlr)


def get_cookies(session):
    cookies_path = Path.home().joinpath('badminton_cookies')
    if cookies_path.exists():
        with open(cookies_path, 'r', encoding='utf-8') as f:
            session.cookies = requests.utils.cookiejar_from_dict(json.load(f))
    else:
        with open(cookies_path, 'w', encoding='utf-8') as f:
            f.wirite(json.dumps(requests.utils.dict_from_cookiejar(session.cookies)))


def print_with_time(string):
    """print with time
    """
    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} {string}')


def find_unpaid_orders(html):
    """find orders
    """
    order_id = findall('myorder_view.*id=(\\d+)', html)
    order_status = findall('(?<=\t)(预订\S+)', html)
    unpaid_orders = []
    for id, status in zip(order_id, order_status):
        if status == '预订中':
            unpaid_orders.append(id)
    return unpaid_orders


def book_param(stock):
    """generate book order paramgrams
    """
    param = json.dumps({
        'activityPrice': 0,
        'activityStr': None,
        'address': None,
        'dates': None,
        'extend': None,
        'flag': '0',
        'isbookall': '0',
        'isfreeman': '0',
        'istimes': '1',
        'merccode': None,
        'order': None,
        'orderfrom': None,
        'remark': None,
        'serviceid': None,
        'shoppingcart': '0',
        'sno': None,
        'stock': {
            stock['stockid']: '1'
        },
        'stockdetail': {
            stock['stockid']: stock['id']
        },
        'stockdetailids': stock['id'],
        'subscriber': '0',
        'time_detailnames': None,
        'userBean': None
    })

    return param


def recognize(imbyte, token, retry):
    """调用 cascaptcha 在线识别验证码
    """
    headers = {'Connection': 'Keep-Alive',
               'Authorization': token,
               'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'}
    files = {'imgfile': ('captcha.jpg', imbyte)}
    recg_times = 0
    while recg_times < retry:
        r = requests.post('https://cascaptcha.vercel.app/api',
                          files=files, headers=headers)
        arrstr = json.loads(r.text)
        if arrstr["success"]:
            print_with_time(f'验证码识别成功: {arrstr["captcha"]}')
            return arrstr["captcha"]
        recg_times += 1
        print_with_time(f'识别失败，第 {recg_times} 次重试')
        sleep(1)

    with open('capt.jpg', 'wb') as f:
        f.write(imbyte)
    return input('验证码识别失败，请手动打开 capt.jpg 识别后输入\n')
