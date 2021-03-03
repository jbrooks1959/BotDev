# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 21:38:57 2021

@author: Administrator
"""
import time as time
import math
import warnings
import requests

warnings.filterwarnings("ignore")


class Trade:
    def __init__(self, client, strategy, contract_size, tp, sl, pair, use_telegram, bot_token, chat_id,
                 limit_spread, order_type, tracing_spread, tracing_limit, trade_type):

        if order_type == 'TRACK':
            self.tracing = True
        else:
            self.tracing = False

        self.client = client
        self.strategy = strategy
        self.contract_size = contract_size
        self.tp = tp
        self.sl = sl
        self.pair = pair
        self.use_telegram = use_telegram
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.limit_spread = limit_spread
        self.order_type = order_type
        self.tracing_spread = tracing_spread
        self.tracing_limit = tracing_limit
        self.trade_type = trade_type
        self.order_id = ""
        self.sl_order_id = ""
        self.tp_order_id = ""
        self.tl_order_id = ""
        self.limit_filled_status = 0
        self.current_side = 0
        self.order_price = 0
        self.running = True

        while True:
            try:
                self.client.Order.Order_cancelAll(symbol=pair).result()
                self.client.Conditional.Conditional_cancelAll(symbol=pair).result()
                break
            except Exception as ex:
                print(ex)
                time.sleep(2)
                continue
        self.__auxiliary_orders()

    def __get_orders(self, symbol=None):
        if symbol is None:
            symbol = self.pair
        orders = []
        while True:
            try:
                orders = self.client.Order.Order_getOrders(symbol=symbol, limit=50).result()[0]["result"]["data"]
                break
            except Exception as ex:
                print("Order Fetch Error")
                print(ex)
                self.__tg_send("Order Fetch Error")
                self.__tg_send(str(ex))
                time.sleep(2)
                continue
        return orders

    def __get_positions(self):

        while True:
            positions = {}
            try:
                positions = self.client.Positions.Positions_myPositionV2(symbol=self.pair).result()[0]["result"]
                # positions = self.client.Position.Position_get(filter=json.dumps(kwargs)).result()[0]
                break
            except Exception as ex:
                print("Get Position Failed")
                print(ex)
                self.__tg_send("Get Position Failed")
                self.__tg_send(str(ex))
                time.sleep(2)
                continue
        return positions

    def __current_quantity(self):
        position = self.__get_positions()

        if position.get('side') == 'Buy':
            current_quantity = abs(int(position.get('size')))
        else:
            current_quantity = -abs(int(position.get('size')))

        return current_quantity

    def __tg_send(self, bot_message):
        if self.use_telegram:
            try:
                send_text = "https://api.telegram.org/bot" + self.bot_token \
                            + "/sendMessage?chat_id=" + self.chat_id + "&parse_mode=Markdown&text=" + bot_message
                response = requests.get(send_text)
                return response.json()
            except Exception as ex:
                print("tgSend_error")
                print(ex)
                print("Invalid Telegram Bot Token or Chat Id.")
                pass
        else:
            pass
        return None

    def __cancel_sl_order(self):
        while True:
            try:
                if self.sl_order_id != "":
                    self.client.Conditional.Conditional_cancel(
                        symbol=self.pair,
                        stop_order_id=self.sl_order_id
                    ).result()
                break
            except Exception as ex:
                print("Cancellation of Order Failed")
                print(ex)
                time.sleep(2)
                continue
        return None

    def __cancel_orders(self, order_ids):
        while True:
            try:
                if order_ids:
                    if order_ids[0] != "":
                        for i in order_ids:
                            self.client.Order.Order_cancelV2(symbol=self.pair, order_id=i).result()
                break
            except Exception as ex:
                print("Cancellation of Order Failed")
                print(ex)
                time.sleep(2)
                continue
        return None

    def __get_order_book(self):
        ob = []
        while True:
            try:
                res = self.client.Market.Market_orderbook(symbol=self.pair).result()[0]["result"]
                ob = [[i for i in res if i["side"] == "Sell"][0], [i for i in res if i["side"] == "Buy"][0]]
                # ob = [self.client.OrderBook.OrderBook_getL2(symbol=self.pair, depth=1).result()][0][0]
                break
            except Exception as ex:
                print("Order Book Fetch Failed")
                print(ex)
                self.__tg_send("Order Book Fetch Failed")
                self.__tg_send(str(ex))
                time.sleep(2)
                continue
        return ob

    def __new_conditional_order(self, kwargs):
        response = ""
        while True:
            try:
                if kwargs != {}:
                    response = self.client.Conditional.Conditional_new(**kwargs).result()[0]["result"]["stop_order_id"]
                break
            except Exception as ex:
                print("New Order Failed")
                print(ex)
                self.__tg_send("New Order Failed")
                self.__tg_send(str(ex))
                time.sleep(2)
                continue
        return response

    def __new_order(self, kwargs):
        response = {}
        r = 0
        while True:
            try:
                if kwargs != {}:
                    response = self.client.Order.Order_newV2(**kwargs).result()[0]["result"]
                    break
            except Exception as ex:
                print(ex)
                print("New Order Failed")
                self.__tg_send("New Order Failed")
                self.__tg_send(str(ex))
                time.sleep(2)
                continue
        return response

    def __trace_order(self, prediction, order_size):
        order_post = {}
        ob = self.__get_order_book()
        price = float(ob[1 if prediction == 1 else 0]['price']) - prediction * self.tracing_spread
        if order_size < 0:
            side = "Sell"
            order_size = -order_size
        elif order_size > 0:
            side = "Buy"
        else:
            return
        if order_size != 0:
            self.limit_filled_status = 0
            order_post = {
                'symbol': self.pair,
                'side': side,
                'order_type': 'Limit',
                'price': price,
                'qty': order_size,
                'time_in_force': 'GoodTillCancel'
            }
        else:
            pass

        if order_post != {}:
            order_response = self.__new_order(order_post)
            if order_response != {}:
                self.order_id = order_response.get('order_id')
                self.order_price = float(order_response.get('price'))
                if prediction == -1:
                    telegram_string = f"New Tracing Short Order:\nPrice:{price}\nContracts: {order_size}"
                    self.__tg_send(telegram_string)
                else:
                    telegram_string = f"New Tracing Long Order:\nPrice: {price}\nContracts: {order_size}"
                    self.__tg_send(telegram_string)
            else:
                print("New Tracing Order Failed.")

        self.__auxiliary_orders()
        return None

    def __limit_order(self, prediction, order_size):
        order_post = {}
        ob = self.__get_order_book()
        price = float(ob[1 if prediction == 1 else 0]['price']) - prediction * self.limit_spread
        if order_size != 0:
            self.limit_filled_status = 0
            if order_size < 0:
                side = "Sell"
                order_size = -order_size
            else:
                side = "Buy"

            order_post = {
                'symbol': self.pair,
                'side': side,
                'order_type': 'Limit',
                'price': price,
                'qty': order_size,
                'time_in_force': 'GoodTillCancel'
            }

        else:
            pass

        if order_post != {}:
            order_response = self.__new_order(order_post)
            if order_response != {}:
                self.order_id = order_response.get('order_id')
                self.order_price = float(order_response.get('price'))
                if prediction == -1:
                    telegram_string = f"New Limit Short Order:\nPrice: {price}\nContracts: {order_size}"
                    self.__tg_send(telegram_string)
                else:
                    telegram_string = f"New Limit Long Order:\nPrice: {price}\nContracts: {order_size}"
                    self.__tg_send(telegram_string)
            else:
                print("New Limit Order Failed.")

        self.__auxiliary_orders()
        return None

    def __amend_price(self, main_order):
        ob = self.__get_order_book()

        sell_price = float(ob[0]['price']) + self.tracing_spread
        buy_price = float(ob[1]['price']) - self.tracing_spread
        price = 0

        if self.tracing_limit != 0:
            if main_order["side"] == "Sell" and float(main_order['price']) > sell_price > (
                    self.order_price - self.tracing_limit):
                price = sell_price
            elif main_order["side"] == "Buy" and float(main_order['price']) < buy_price < (
                    self.order_price + self.tracing_limit):
                price = buy_price
        else:
            if main_order["side"] == "Sell" and sell_price < float(main_order['price']):
                price = sell_price
            elif main_order["side"] == "Buy" and buy_price > float(main_order['price']):
                price = buy_price

        return price

    def __amend_order(self, orders):
        new = []
        new_index = []
        for i in range(0, len(orders)):
            if orders[i]['order_status'] == 'New':
                new.append(orders[i]['order_id'])
                new_index.append(i)

        if (self.order_id in new) and (self.order_id != ""):
            main_order = orders[new_index[new.index(self.order_id)]]
            # amend_order = {}
            price = self.__amend_price(main_order)
            if price != 0:
                amend_order = {
                    'order_id': self.order_id,
                    'symbol': self.pair,
                    'p_r_price': price
                }
                while True:
                    try:
                        self.client.Order.Order_replace(**amend_order).result()
                        # self.client.Order.Order_amendBulk(orders=json.dumps(amend_order)).result()
                        break
                    except Exception as ex:
                        print(ex)
                        print("Amend Order Error")
                        time.sleep(2)
                        # continue
                        break
        return None

    def __check_filled(self, orders):
        filled = []
        index = []
        for i in range(0, len(orders)):
            if orders[i]['order_status'] == 'Filled':
                filled.append(orders[i]['order_id'])
                index.append(i)

        if self.sl != 0 or self.tp != 0:
            if self.sl_order_id in filled:
                telegram_string = "Your Stop Loss Order has been filled."
                self.sl_order_id = ""
                self.__tg_send(telegram_string)
                self.__cancel_orders(order_ids=[self.tp_order_id])
                self.tp_order_id = ""

            elif self.tp_order_id in filled:
                telegram_string = "Your Take Profit Order has been filled."
                self.tp_order_id = ""
                self.__tg_send(telegram_string)
                self.__cancel_sl_order()
                self.sl_order_id = ""

        if (self.order_id in filled) and (self.limit_filled_status == 0) and self.order_type == "LIMIT":
            i = index[filled.index(self.order_id)]
            q = str(orders[i]['qty'])
            s = str(orders[i]['side'])
            p = str(orders[i]['price'])
            telegram_string = f"Your Limit Order of {q} contracts {s} is now filled at a price of {p}."
            self.order_id = ""
            self.limit_filled_status = 1
            self.__tg_send(telegram_string)
            self.__auxiliary_orders()

        if (self.order_id in filled) and self.order_type == "TRACE":
            i = index[filled.index(self.order_id)]
            q = str(orders[i]['qty'])
            s = str(orders[i]['side'])
            p = str(orders[i]['price'])
            telegram_string = f"Your Tracing Order of {q} contracts {s} is now filled at a price of {p}."
            self.order_id = ""
            self.__tg_send(telegram_string)
            self.__auxiliary_orders()

        return None

    def __redo_order(self):
        orders = self.__get_orders()
        if self.order_type == 'TRACE':
            self.__amend_order(orders)
        self.__check_filled(orders)
        return None

    def __auxiliary_orders(self, avg=0):
        sl_bool = False
        tp_bool = False
        stop_px = 0
        px = 0
        if avg == 0:
            quantity = 0
            price = 0
            position = self.__get_positions()
            # print(position)
            if position != {}:
                price = float(position.get('entry_price'))
                if position.get('side') == 'Buy':
                    quantity = abs(int(position.get('size')))
                else:
                    quantity = -abs(int(position.get('size')))
                # quantity = int(position.get('size'))
                # print(price, quantity)

            if quantity != 0:
                stop_px = price - (quantity / abs(quantity)) * price * self.sl
                stop_px = math.ceil(stop_px * 1) / 1
                px = price + (quantity / abs(quantity)) * price * self.tp
                px = math.ceil(px * 1) / 1

        else:
            price = avg
            stop_px = price - self.current_side * price * self.sl
            stop_px = math.ceil(stop_px * 1) / 1
            px = price + self.current_side * price * self.tp
            px = math.ceil(px * 1) / 1
            quantity = self.current_side * self.contract_size

        # kwargs = {"ordStatus": "New"}
        # active_orders = self.__get_orders(**kwargs)
        active_orders = self.__get_orders()
        # print(active_orders)

        new_id = []
        new_index = []
        for i in range(0, len(active_orders)):
            if active_orders[i]['order_status'] == 'New' or active_orders[i]['order_status'] == 'Untriggered':
                new_id.append(active_orders[i]['order_id'])
                new_index.append(i)

        order_post = {}
        conditional_order = {}

        if -quantity < 0:
            side = "Sell"
        elif -quantity > 0:
            side = "Buy"
        else:
            return

        ob = self.__get_order_book()
        base_price = float(ob[1 if side == "Sell" else 0]['price'])


        if self.sl != 0:
            if self.sl_order_id in new_id:
                sl_order = active_orders[new_index[new_id.index(self.sl_order_id)]]
                if sl_order['side'] == 'Sell':
                    r = -1
                else:
                    r = 1
                if int(sl_order['qty']) * r != -quantity or float(sl_order['ext_fields']['trigger_price']) != stop_px:
                    self.__cancel_sl_order()
                    self.sl_order_id = ""
                    conditional_order = {
                        'symbol': self.pair,
                        'side': side,
                        'order_type': 'Market',
                        'qty': abs(-quantity),
                        'base_price': base_price,
                        'stop_px': stop_px,
                        'time_in_force': 'GoodTillCancel',
                    }

                    sl_bool = True
            else:
                conditional_order = {
                    'symbol': self.pair,
                    'side': side,
                    'order_type': 'Market',
                    'qty': abs(-quantity),
                    'base_price': base_price,
                    'stop_px': stop_px,
                    'time_in_force': 'GoodTillCancel',
                }
                sl_bool = True

        else:
            stop_px = "No Stop Loss!"

        if self.tp != 0:
            if self.tp_order_id in new_id:
                tp_order = active_orders[new_index[new_id.index(self.tp_order_id)]]
                if tp_order['side'] == 'Sell':
                    r = -1
                else:
                    r = 1
                if tp_order['qty'] * r != -quantity or tp_order['price'] != px:
                    self.__cancel_orders(order_ids=[self.tp_order_id])
                    self.tp_order_id = ""
                    order_post = {
                        'side': side,
                        'symbol': self.pair,
                        'order_type': 'Limit',
                        'qty': abs(-quantity),
                        'price': px,
                        'time_in_force': 'GoodTillCancel'
                    }
                    tp_bool = True
            else:
                order_post = {
                    'side': side,
                    'symbol': self.pair,
                    'order_type': 'Limit',
                    'qty': abs(-quantity),
                    'price': px,
                    'time_in_force': 'GoodTillCancel'
                }
                tp_bool = True

        else:
            px = "No Take Profit!"

        if quantity != 0:
            while True:
                try:
                    order_response = {}
                    if sl_bool is False and tp_bool is False:
                        break
                    else:
                        conditional_order_id = ""
                        if sl_bool:
                            conditional_order_id = self.__new_conditional_order(conditional_order)
                        if tp_bool:
                            order_response = self.__new_order(order_post)

                    if sl_bool and tp_bool:
                        self.sl_order_id = conditional_order_id
                        self.tp_order_id = order_response.get('order_id')

                    elif sl_bool is False and tp_bool is True:
                        self.tp_order_id = order_response.get('order_id')

                    elif sl_bool is True and tp_bool is False:
                        self.sl_order_id = conditional_order_id

                    else:
                        pass
                    break

                except Exception as ex:
                    time.sleep(2)
                    print("Auxiliary Order Place")
                    print(ex)
                    continue

            if sl_bool or tp_bool:
                if quantity < 0:
                    telegram_string = f"Auxiliary Orders for Short Open Position:" \
                                      f"\nContracts: {-quantity}\nStop Loss: {stop_px}\nTake Profit: {px}"
                    self.__tg_send(telegram_string)

                elif quantity > 0:
                    telegram_string = f"Auxiliary Orders for Long Open Position:" \
                                      f"\nContracts: {-quantity}\nStop Loss: {stop_px}\nTake Profit: {px}"
                    self.__tg_send(telegram_string)
        return None

    def __market_order(self, prediction, order_size):

        if order_size < 0:
            side = "Sell"
            order_size = -order_size
        elif order_size > 0:
            side = "Buy"
        else:
            return

        order_post = {
            'symbol': self.pair,
            'side': side,
            'order_type': 'Market',
            'qty': order_size,
            'time_in_force': 'GoodTillCancel'
        }
        if order_size != 0:
            order_response = self.__new_order(order_post)
            avg = float(order_response.get('price'))

            if prediction == -1:
                telegram_string = f"New Market Short:\nPrice: {avg}\nContracts: {order_size}"
                self.__tg_send(telegram_string)

            else:
                telegram_string = f"New Market Long:\nPrice: {avg}\nContracts: {order_size}"
                self.__tg_send(telegram_string)

            # self.__auxiliary_orders(avg=avg)
            self.__auxiliary_orders()

        else:
            self.__auxiliary_orders()
        return None

    def execute_trade(self):
        if self.running:
            prediction = self.strategy.predict()
            try:
                if prediction == 2 and self.current_side == 1:
                    self.current_side = 0
                    self.__cancel_orders(order_ids=[self.order_id])
                    self.order_id = ""
                    order_size = -self.__current_quantity()
                    prediction = -1
                    if order_size != 0:
                        if self.order_type == "MARKET":
                            self.__market_order(prediction, order_size)
                        elif self.order_type == "LIMIT":
                            self.__limit_order(prediction, order_size)
                        elif self.order_type == "TRACE":
                            self.__trace_order(prediction, order_size)

                elif prediction == -2 and self.current_side == -1:
                    self.current_side = 0
                    self.__cancel_orders(order_ids=[self.order_id])
                    self.order_id = ""
                    order_size = -self.__current_quantity()
                    prediction = 1
                    if order_size != 0:
                        if self.order_type == "MARKET":
                            self.__market_order(prediction, order_size)
                        elif self.order_type == "LIMIT":
                            self.__limit_order(prediction, order_size)
                        elif self.order_type == "TRACE":
                            self.__trace_order(prediction, order_size)

                elif prediction == -1 and self.current_side != -1:
                    self.current_side = -1
                    self.__cancel_orders(order_ids=[self.order_id])
                    self.order_id = ""
                    current_open_position = self.__current_quantity()

                    if self.trade_type != "LONG":
                        order_size = -(self.contract_size + current_open_position)
                    else:
                        order_size = -current_open_position

                    if self.order_type == "MARKET":
                        self.__market_order(prediction, order_size)
                    elif self.order_type == "LIMIT":
                        self.__limit_order(prediction, order_size)
                    elif self.order_type == "TRACE":
                        self.__trace_order(prediction, order_size)

                elif prediction == 1 and self.current_side != 1:
                    self.current_side = 1
                    self.__cancel_orders(order_ids=[self.order_id])
                    self.order_id = ""
                    current_open_position = self.__current_quantity()

                    if self.trade_type != "SHORT":
                        order_size = self.contract_size - current_open_position
                    else:
                        order_size = -current_open_position

                    if self.order_type == "MARKET":
                        self.__market_order(prediction, order_size)
                    elif self.order_type == "LIMIT":
                        self.__limit_order(prediction, order_size)
                    elif self.order_type == "TRACE":
                        self.__trace_order(prediction, order_size)

            except Exception as ex:
                print(ex)
                print("This is a Fatal Error. Please report it.")
                time.sleep(5)
                self.__auxiliary_orders()
                self.current_side = 0
                self.running = True

            self.__redo_order()
        return None

