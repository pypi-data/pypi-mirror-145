#!/usr/bin/env python

import argparse
import configparser
import json
import sys
from datetime import date, datetime, time, timedelta
from itertools import groupby
from json.decoder import JSONDecodeError
from re import findall
from time import sleep

import requests

from .version import __version__
from .utils import *
from .random_ua import ua


class Badminton():
    """珠海校区羽毛球场预订脚本
    """

    def __init__(self, configpath, begin_time='00:01', max_times=10, token='', auto_pay=True):
        self.session = requests.Session()
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            "User-Agent": ua(),
        }
        self.stocks, self.selects, self.unpaid = [], [], []
        self.capt, self.imbyte = None, None
        self.max_times = max_times
        self.token = token
        self.auto_pay = auto_pay

        try:
            conf_par = configparser.ConfigParser()
            conf_par.read(configpath, encoding='utf-8')
            conf = dict(conf_par['badminton'])
            self.first, self.stock_number = conf['first'], conf['stock_number']
            self.netid, self.password = conf['netid'], conf['password']
        except KeyError:
            print_with_time('检查配置文件是否存在且正确填写')
            sys.exit()
        if not (self.netid and self.password):
            print_with_time('填写 netid 和密码')
            sys.exit()

        try:
            self.stock_name = [int(i) for i in conf['stock_name'].split(',')]
            self.stock_time = [int(i) for i in conf['stock_time'].split(',')]
            self.stock_number = int(conf['stock_number'])
            if not conf['stock_date']:
                self.stock_date = date.today() + timedelta(days=2)
            else:
                self.stock_date = datetime.strptime(
                    conf['stock_date'], "%Y-%m-%d").date()
            # 预订日期前一天 00:00 可以预订，当天 22:00 后无法预订
            self.begin_time = datetime.strptime(begin_time, "%H:%M").time()
            self.begin_datetime = datetime.combine(self.stock_date,
                                                   self.begin_time) - timedelta(days=1)
            self.end_datetime = datetime.combine(self.stock_date, time(22, 0))
        except ValueError:
            print_with_time('检查配置文件填写是否正确')
            sys.exit()

        print_with_time(f'预订日期: {self.stock_date}')
        print_with_time(f"预订场次: {conf['stock_name']}")
        print_with_time(f"预订时间: {conf['stock_time']}")
        print_with_time(f'每个时间段最大预订场地数: {self.stock_number}')


    def login(self):
        """登录
        """
        login_url = "https://cas.sysu.edu.cn/cas/login"
        captcha_url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
        login_form = {"username": "",
                      "password": "",
                      "captcha": "",
                      "_eventId": "submit",
                      "geolocation": "",
                      }
        login_times = 0

        while login_times < self.max_times:
            login_times += 1
            r = self.session.get(login_url, headers=self.headers)
            if 'Log In Successful' in r.text:
                print_with_time('登录有效')
                return True
            print_with_time('开始登录')
            self.imbyte = self.session.get(captcha_url).content
            self.capt = recognize(self.imbyte, self.token, self.max_times)
            login_form['captcha'] = self.capt
            login_form['execution'] = findall(
                'name="execution" value="(.*?)"', r.text)[0]
            login_form["username"] = self.netid
            login_form["password"] = self.password

            r = self.session.post(
                login_url, headers=self.headers, data=login_form)
            if 'success' in r.text:
                print_with_time('登录成功')
                return True
            if 'credential' in r.text:
                print_with_time('用户名或密码错误')
                sys.exit()

            print_with_time(f'验证码错误，第 {login_times} 次重试')
            sleep(1)

        print_with_time('登录重试次数太多，终止')
        sys.exit()


    def wait(self):
        """系统正常开启时间为 00:00-22:00，选择合适等待策略
        """
        now_time = datetime.now()

        if now_time > self.end_datetime:
            print_with_time(f'预订日期已经过去，你可以穿越回 {self.end_datetime} 之前，再见')
            sys.exit()

        if now_time > self.begin_datetime:
            if now_time.hour < 22:
                print_with_time(f'当前时间 {datetime.now()}，开始预订')
                return
            self.begin_datetime += timedelta(days=1)
            print_with_time('预订系统关闭，等到明天开始预订')

        print_with_time(f'未到可预订时间，等到 {self.begin_datetime} 开始预订')
        if (self.begin_datetime - datetime.now()).days > 0:
            print_with_time('!!!警告!!!')
            print_with_time('等待时间超过一天，建议等到明天再来预订!!!')
        print_with_time(f'{self.begin_datetime - datetime.now()} 后开始预订')
        sleep((self.begin_datetime - datetime.now()).seconds - 120)
        print_with_time('检查登录状态')
        if self.login():
            print_with_time(f'{self.begin_datetime - datetime.now()} 后开始预订')
            sleep((self.begin_datetime - datetime.now()).seconds - 3)
            return


    def get_stocks(self):
        """获取指定日期可预订的场次列表
        """
        gym_url = 'https://gym.sysu.edu.cn/product/findOkArea.html'
        try_times = 0
        while try_times < self.max_times:
            try_times += 1
            r = requests.post(
                f'{gym_url}?s_date={self.stock_date}&serviceid=161')
            try:
                json_data = json.loads(r.text)
            except JSONDecodeError:
                print_with_time(f'获取场地信息失败，第 {try_times} 次重试')
                if r.status_code != 200:
                    print_with_time(f'状态码: {r.status_code}，服务器可能崩溃了，等待一分钟后重试')
                    sleep(60)
                    continue
                sleep(3)
                continue
            stocks = json_data['object']

            for stock in stocks:
                dic = {}
                if stock['status'] == 1:
                    for keys in ['id', 'stockid']:
                        dic[keys] = str(stock[keys])
                    for keys in ['price', 's_date']:
                        dic[keys] = stock['stock'][keys]
                    dic['sname'] = int(stock['sname'][2:])
                    dic['time_full'] = stock['stock']['time_no']
                    dic['time_no'] = int(dic['time_full'][:2])
                    self.stocks.append(dic)
            if len(self.stocks) == 0:
                print_with_time("凉了，没场地了，告辞")
                sys.exit()
            print_with_time(f'{self.stock_date} 共计 {len(self.stocks)} 个场地可以预订，开始按条件筛选')
            return
        print_with_time('获取场地信息失败，重试次数达到上限')
        sys.exit()


    def _select(self):
        """根据条件筛选场次
        """
        select = []
        for stock in self.stocks:
            if stock['sname'] in self.stock_name and stock['time_no'] in self.stock_time:
                select.append(stock)
        if len(select) == 0:
            print_with_time('没有满足条件的场地了')
            sys.exit()
        select.sort(key=lambda elem: (self.stock_time.index(elem['time_no']),
                                      self.stock_name.index(elem['sname'])))
        reselect = []
        for _, items in groupby(select,
                                key=lambda elem: self.stock_time.index(elem['time_no'])):
            i = 0
            for stock in items:
                reselect.append(stock)
                i += 1
                if i >= self.stock_number:
                    break
        self.selects = reselect
        if self.first == 'name':
            self.selects.sort(key=lambda elem: (self.stock_name.index(elem['sname']),
                                                self.stock_time.index(elem['time_no'])))
        print_with_time(f"共筛选出 {len(self.selects)} 个场地")
        for stock in self.selects:
            print_with_time(f"{stock['id']} 场地{stock['sname']} {stock['time_full']}")


    def book(self):
        """预订场地
        """
        stock_index = 0
        book_times = 0
        personal_url = 'https://gym.sysu.edu.cn/yyuser/personal.html'
        book_url = 'https://gym.sysu.edu.cn/order/book.html'
        print_with_time('开始预订')
        personal_page = self.session.get(personal_url, headers=self.headers)
        unpaid_orders = find_unpaid_orders(personal_page.text)
        while len(self.unpaid) < 2 and book_times < 10:
            book_times += 1
            try:
                stock = self.selects[stock_index]
            except IndexError:
                print_with_time('可以预订的都试过了')
                break
            data = {"param": book_param(stock), "json": "true"}
            try:
                r = self.session.post(book_url, headers=self.headers, data=data)
                return_data = json.loads(r.text)
            except JSONDecodeError:
                print_with_time(f'预订失败，第 {book_times} 次重试')
                print_with_time(r.text)
                sleep(10)
                continue

            if return_data['result'] == '2':
                print_with_time(f'预订成功：场地 {stock["sname"]} {stock["time_full"]} '
                                f'订单号 {return_data["object"]["orderid"]}，待支付')
                stock_index += 1
                self.unpaid.append(return_data['object']['orderid'])

            elif return_data['message'] == 'USERNOTLOGINYET':
                personal_page = self.session.get(personal_url, headers=self.headers)
                unpaid_orders = find_unpaid_orders(personal_page.text)
                continue

            elif '已被预订' in return_data['message']:
                stock_index += 1
                print_with_time('场次已被预订，尝试下一个')
                continue

            else:
                print_with_time(f'预订失败：{return_data["message"]}，第 {book_times} 次重试')
                sleep(10)
                continue

        if unpaid_orders:
            print_with_time(f'发现未支付订单：{unpaid_orders}，之后一起支付')
            self.unpaid = list(set(self.unpaid + unpaid_orders))
        if not self.unpaid:
            print_with_time('预订失败，重试次数过多，退出')
            sys.exit()
        if not self.auto_pay:
            print_with_time(f'预订成功 {len(self.unpaid)} 个场地，请自行支付')
            sys.exit()
        print_with_time(f'预订成功 {len(self.unpaid)} 个场地，10 秒后自动支付订单')
        sleep(10)


    def pay(self):
        """支付订单
        """
        pay_times = 0
        while pay_times < self.max_times and len(self.unpaid) != 0:
            pay_times += 1
            order_pay = self.unpaid[0]
            print_with_time('支付订单 ' + str(order_pay))
            data1 = {"orderid": order_pay, "payid": 2}
            headers = self.headers
            headers['Referer'] = f'https://gym.sysu.edu.cn/pay/show.html?id={order_pay}'
            data2 = {'param': json.dumps(
                {"payid": 2, "orderid": str(order_pay), "ctypeindex": 0})}

            self.session.get("https://gym.sysu.edu.cn/pay/account/showpay.html",
                                 headers=headers, data=data1)
            r = self.session.post("https://gym.sysu.edu.cn/pay/account/topay.html",
                                  headers=headers, data=data2)
            try:
                return_data = json.loads(r.text)
            except JSONDecodeError:
                print_with_time(f'支付失败，第 {pay_times} 次重试')
                sleep(5)
                self.login()
                continue
            if return_data["result"] == "1":
                print_with_time(f'{str(order_pay)} 支付成功')
                self.unpaid.remove(order_pay)
            else:
                print_with_time(f'支付结果: {return_data["message"]}，重试')
                sleep(5)

        if len(self.unpaid) != 0:
            print_with_time('可能有未成功支付的订单，请手动支付')


    @backoff_retry
    def run(self):
        self.login()
        self.wait()
        self.get_stocks()
        self._select()
        self.book()
        self.pay()
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description='预订中山大学珠海校区羽毛球场地')
    parser.add_argument('config', type=str, help='配置文件路径')
    parser.add_argument('-b', '--begin', metavar='BEGIN TIME', type=str,
                        help='预订开始时间，如 00:05，默认 00:01', default='00:01')
    parser.add_argument('-p', '--pay', metavar='AUTO PAY', type=str,
                        help='是否自动支付，默认为开启', default='True')
    parser.add_argument('-m', '--maxtimes', type=int, help='最大重试次数', default=10)
    parser.add_argument('-t', '--token', type=str, help='cascaptcha api token',
                        default='j6NKyDMPRxjHNHukp7WbBLxycL')
    parser.add_argument('-v', action='version', version=f'%(prog)s {__version__}')

    par = parser.parse_args()
    if par.pay in ['true', 'True', 'TRUE', '1']:
        par.pay = True
    else:
        par.pay = False
    badminton = Badminton(par.config, par.begin, par.maxtimes, par.token, par.pay)
    badminton.run()
