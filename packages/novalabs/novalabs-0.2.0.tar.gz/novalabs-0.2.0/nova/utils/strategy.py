import socket

from decouple import config
import pandas as pd
from datetime import datetime
import re
from nova.api.nova_client import NovaClient
import time
from nova.utils.constant import POSITION_PROD_COLUMNS

import logging
import logging.handlers

import asyncio
import aiohttp


class Strategy:

    def __init__(self,
                 bot_id: str,
                 candle: str,
                 size: float,
                 window: int,
                 holding: float,
                 bankroll: float,
                 max_down: float,
                 is_logging: bool = False
                 ):

        self.candle = candle
        self.size = size
        self.window_period = window
        self.max_holding = holding
        self.position_opened = pd.DataFrame(columns=POSITION_PROD_COLUMNS)
        self.prod_data = {}
        self.nova = NovaClient(config('NovaAPISecret'))

        self.bankroll = bankroll
        self.max_down = max_down

        self.currentPNL = 0
        self.bot_id = bot_id

        # Logging  and
        logging.getLogger().setLevel(logging.NOTSET)
        # ToDo : add creation date
        logging.basicConfig(filename=f'{self.bot_id}.log', filemode='w')
        self.log = logging.getLogger(socket.gethostname())

        self.logger = is_logging

        if self.logger:
            self.HEADER = 64
            self.FORMAT = 'utf-8'
            self.DISCONNECT_MESSAGE = '!DISCONNECT'

            self.PORT = 5080
            self.SERVER = socket.gethostbyname(socket.gethostname())
            self.ADDR = (self.SERVER, self.PORT)

            self.logger_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.logger_client.connect(self.ADDR)

    def setup_leverage(self, pair: str, lvl: int = 1):
        """
        Note: this function execute n API calls with n representing the number of pair in the list
        Args:
            pair: string that represent the pair you want to setup the leverage
            lvl: integer that increase

        Returns: None, This function update the leverage setting
        """
        try:
            self.client.futures_change_leverage(symbol=pair, leverage=lvl)
            print(f'Setup leverage for {pair}')
        except(Exception):
            print('Setting not working')

    def get_unit_multiplier(self) -> tuple:
        """
        Returns: a tuple that contains the unit and the multiplier needed to extract the data
        """
        multi = int(float(re.findall(r'\d+', self.candle)[0]))

        if 'm' in self.candle:
            return 'minutes', multi
        elif 'h' in self.candle:
            return 'hours', multi
        elif 'd' in self.candle:
            return 'days', multi

    def _data_fomating(self, kline: list) -> pd.DataFrame:
        """
        Args:
            kline: is the list returned by get_historical_klines method from binance

        Returns: dataframe with usable format.
        """
        for k in kline:
            k[0] = datetime.fromtimestamp(int(str(k[0])[:10]))
            del k[6:]

        df = pd.DataFrame(kline, columns=['timeUTC', 'open', 'high', 'low', 'close', 'volume'])
        for var in ["volume", "open", "high", "low", "close"]:
            df[var] = pd.to_numeric(df[var], downcast="float")
        df['timeUTC'] = pd.to_datetime(df['timeUTC'])
        return df

    async def get_klines(self, session, pair):

        url = "https://fapi.binance.com/fapi/v1/klines"
        params = dict(symbol=pair, interval=self.candle, limit=(self.window_period + 1))

        async with session.get(url=url, params=params) as response:
            klines = await response.json()

            klines = klines[:-1]

            df = self._data_fomating(klines)

            self.prod_data[pair] = {}
            self.prod_data[pair]['latest_update'] = df['timeUTC'].max()
            self.prod_data[pair]['data'] = df

    async def get_prod_data(self, list_pair: list):
        """
        Note: This function is called once when the bot is instantiated.
        This function execute n API calls with n representing the number of pair in the list
        Args:
            list_pair: list of all the pairs you want to run the bot on.

        Returns: None, but it fills the dictionary self.prod_data that will contain all the data
        needed for the analysis.
        """

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = []

            for pair in list_pair:

                task = asyncio.ensure_future(self.get_klines(session, pair))
                tasks.append(task)

            await asyncio.gather(*tasks)

    def update_prod_data(self,  pair: str):
        """
        Notes: This function execute 1 API call

        Args:
            pair:  pairs you want to run the bot on ex: 'BTCUSDT', 'ETHUSDT'

        Returns: None, but it updates the dictionary self.prod_data that will contain all the data
        needed for the analysis.
        """
        unit, multi = self.get_unit_multiplier()
        klines = self.client.get_historical_klines(pair, self.candle, f'{multi*2} {unit} ago UTC')

        df = self._data_fomating(klines)

        df_new = pd.concat([self.prod_data[pair]['data'], df])
        df_new = df_new.drop_duplicates(subset=['timeUTC']).sort_values(by=['timeUTC'], ascending=True)
        self.prod_data[pair]['latest_update'] = df_new['timeUTC'].max()
        self.prod_data[pair]['data'] = df_new.tail(self.window_period)

    def get_quantity_precision(self, pair: str) -> tuple:
        """
        Note: => This function execute 1 API call to binance

        Args:
            pair: string variable that represent the pair ex: 'BTCUSDT'

        Returns: a tuple containing the quantity precision and the price precision needed for the pair
        """
        info = self.client.futures_exchange_info()
        for x in info['symbols']:
            if x['pair'] == pair:
                return x['quantityPrecision'], x['pricePrecision']

    def get_price_binance(self, pair: str) -> float:
        """
        Args:
            pair: string variable that represent the pair ex: 'BTCUSDT'
        Returns:
            Float of the latest price for the pair.
        """
        prc = self.client.get_recent_trades(symbol=pair)[-1]["price"]
        return float(prc)

    def get_position_size(self) -> float:
        """
        Returns:
            Float that represents the final position size taken by the bot
        """
        futures_balances = self.client.futures_account_balance()
        balances = 0
        for balance in futures_balances:
            if balance['asset'] == 'USDT':
                balances = float(balance['balance'])

        if balances <= self.size:
            return balances
        else:
            return self.size

    def get_actual_position(self, list_pair: list) -> dict:
        """
        Note: => This function execute 1 API call to binance
        Args:
            list_pair: list of pair that we want to run analysis on
        Returns: a dictionary containing all the current positions on binance
        """
        all_pos = self.client.futures_position_information()
        position = {}
        for pos in all_pos:
            if float(pos['positionAmt']) != 0 and pos['symbol'] in list_pair:
                position[pos['symbol']] = pos
        return position

    def enter_position(self,
                       action: int,
                       pair: str,
                       bot_name: str,
                       tp: float,
                       sl: float):
        """
        Args:
            action: this is an integer that can get the value 1 (for long) or -1 (for short)
            pair: is a string the represent the pair we are entering in position.
            bot_name: is the name of the bot that is trading this pair
            tp: take profit %
            sl: stop loss %
        Returns:
            Send transaction to the exchange and update the backend and the class
        """

        # get the price and size of the trade in USDT
        prc = self.get_price_binance(pair)
        size = self.get_position_size()

        # get the quantity and the price precision
        quantity = (size / prc)
        q_precision, p_precision = self.get_quantity_precision(pair)
        quantity = float(round(quantity, q_precision))

        # build the action information needed
        if action == 1:
            side = 'BUY'
            prc_tp = float(round(prc * (1 + tp), p_precision))
            prc_sl = float(round(prc * (1 - sl), p_precision))
            type_pos = 'LONG'
            closing_side = 'SELL'

        elif action == -1:
            side = 'SELL'
            prc_tp = float(round(prc * (1 - tp), p_precision))
            prc_sl = float(round(prc * (1 + sl), p_precision))
            type_pos = 'SHORT'
            closing_side = 'BUY'

        # send the transaction to the exchange
        order = self.client.futures_create_order(symbol=pair, side=side, type='MARKET', quantity=quantity)

        tp_open = self.client.futures_create_order(symbol=pair, side=closing_side, type='TAKE_PROFIT_MARKET',
                                                   stopPrice=prc_tp, closePosition=True)

        sl_open = self.client.futures_create_order(symbol=pair, side=closing_side, type='STOP_MARKET',
                                                   stopPrice=prc_sl, closePosition=True)

        # update the backend data
        nova_data = self.nova.create_new_bot_position(
            bot_name=bot_name,
            post_type=type_pos,
            value=size,
            state='OPENED',
            entry_price=prc,
            take_profit=float(tp_open['stopPrice']),
            stop_loss=float(sl_open['stopPrice']),
            pair=order['symbol'])

        # update the class position
        new_position = pd.DataFrame([{
            'id': order['orderId'],
            'pair': order['symbol'],
            'status': order['status'],
            'quantity': order['origQty'],
            'type': order['type'],
            'side': order['side'],
            'tp_id': tp_open['orderId'],
            'tp_side': tp_open['side'],
            'tp_type': tp_open['type'],
            'tp_stopPrice': tp_open['stopPrice'],
            'sl_id': sl_open['orderId'],
            'sl_side': sl_open['side'],
            'sl_type': sl_open['type'],
            'sl_stopPrice': sl_open['stopPrice'],
            'nova_id': nova_data['newBotPosition']['_id'],
            'time_entry':  str(order['updateTime'])[:-3]
        }])

        self.position_opened = pd.concat([self.position_opened, new_position])

    def update_position(self, current_position: dict):
        """
        Args:
            current_position: this dictionary is the output of the get_actual_position method
        Returns:
            This function updates the open position of the bot, checking if there is any TP or SL
        """


        # loop through all the positions
        for index, row in self.position_opened.iterrows():
            # verify if the pair position is still open on the exchange
            if row.pair not in list(current_position.keys()):
                # if not update the back end  by looking if it's a TP or SL
                print('Position have been through TP or SL')
                actual_tp = self.client.futures_get_order(symbol=row.pair, orderId=row.tp_id)
                actual_sl = self.client.futures_get_order(symbol=row.pair, orderId=row.sl_id)

                entry_tx = self.client.futures_account_trades(orderId=row.id)

                if actual_tp['status'] == 'FILLED':
                    exit_tx = self.client.futures_account_trades(orderId=row.tp_id)
                    exit_type = 'TP'

                elif actual_sl['status'] == 'FILLED':
                    exit_tx = self.client.futures_account_trades(orderId=row.sl_id)
                    exit_type = 'SL'
                else:
                    break

                print('Update Backend and current data')
                self._push_backend(entry_tx, exit_tx, row.nova_id, exit_type)
                self.position_opened.drop(self.position_opened.index[index], inplace=True)

    def _push_backend(self, entry_tx: list, exit_tx: list, nova_id: str, exit_type: str):
        """
        Args:
            entry_tx: the entry tx list coming from the client
            exit_tx: the exit tx list coming from the client
            nova_id: novalabs position id
            exit_type: String that can take the 4 types TP, SL, MAX_HOLDING, EXIT_POINT
        Returns:
            Updates the data in novalabs backend
        """

        # information needed
        commission_entry = 0
        commission_exit = 0
        entry_total = 0
        entry_quantity = 0
        realized_pnl = 0
        exit_total = 0
        exit_quantity = 0
        type_pos = ''
        pair = entry_tx[0]['symbol']

        # go through all the tx needed to get in and out of the position
        for tx_one in entry_tx:
            commission_entry += float(tx_one['commission'])
            entry_quantity += float(tx_one['qty'])
            entry_total += float(tx_one['qty']) * float(tx_one['price'])
            if tx_one['side'] == 'BUY':
                type_pos = 'LONG'
            else:
                type_pos = 'SHORT'

        for tx_two in exit_tx:
            realized_pnl += float(tx_two['realizedPnl'])
            commission_exit += float(tx_two['commission'])
            exit_quantity += float(tx_two['qty'])
            exit_total += float(tx_two['qty']) * float(tx_two['price'])

        # compute the last information needed
        exit_price = exit_total / exit_quantity
        entry_price = entry_total / entry_quantity
        prc_bnb = self.get_price_binance('BNBUSDT')
        total_fee_usd = (commission_exit + commission_entry) * prc_bnb

        # send updates to the backend
        self.nova.update_bot_position(
            pos_id=nova_id,
            pos_type=type_pos,
            state='CLOSED',
            entry_price=entry_price,
            exit_price=exit_price,
            exit_type=exit_type,
            profit=realized_pnl,
            fees=total_fee_usd,
            pair=pair
        )

        self.currentPNL += realized_pnl

    def exit_position(self,
                      pair: str,
                      side: str,
                      quantity: float,
                      entry_order_id: int,
                      nova_id: str,
                      index_opened: int,
                      exit_type: str):
        """
        Args:
            pair : string that represents the current pair analysed
            side : the type of side to execute to exit a position
            quantity : exact quantity of of token to exit completely the position
            entry_order_id : entry tx id needed to complete the backend data
            nova_id : nova position id to update the backend
            index_opened : index at which the position is located in the position_opened dataframe
            exit_type: String that can take the 4 types TP, SL, MAX_HOLDING, EXIT_POINT
        """

        # Exit send on the market
        order = self.client.futures_create_order(symbol=pair, side=side, type='MARKET', quantity=quantity)
        time.sleep(2)

        # Extract the entry and exit transactions
        entry_tx = self.client.futures_account_trades(orderId=entry_order_id)
        exit_tx = self.client.futures_account_trades(orderId=order['orderId'])

        # Update the position tx in backend and int the class
        self._push_backend(entry_tx, exit_tx, nova_id, exit_type)
        self.position_opened.drop(self.position_opened.index[index_opened], inplace=True)

    def is_max_holding(self):
        """
        Returns:
            This method is used to check if the maximum holding time is reached for each open positions.
        """

        # Compute the current time
        s_time = self.client.get_server_time()
        server_time = int(str(s_time['serverTime'])[:-3])
        server = datetime.fromtimestamp(server_time)

        for index, row in self.position_opened.iterrows():

            # get the number of hours since opening
            entry_time_date = datetime.fromtimestamp(int(row.time_entry))
            diff = server - entry_time_date
            diff_in_hours = diff.total_seconds() / 3600

            # create the Exit Side
            if diff_in_hours >= self.max_holding:

                if row.side == 'BUY':
                    exit_side = 'SELL'
                elif row.side == 'SELL':
                    exit_side = 'BUY'

                self.exit_position(pair=row.pair,
                                   side=exit_side,
                                   quantity=row.quantity,
                                   entry_order_id=row.id,
                                   nova_id=row.nova_id,
                                   index_opened=index,
                                   exit_type='MAX_HOLDING')

    def security_close_all(self, exit_type: str):
        """
        Note: this function has to be executed each time an error stops the bot
        """

        for index, row in self.position_opened.iterrows():

            exit_side = 'SELL'

            if row.side == 'SELL':
                exit_side = 'BUY'

            self.exit_position(
                pair=row.pair,
                side=exit_side,
                quantity=row.quantity,
                entry_order_id=row.id,
                nova_id=row.nova_id,
                index_opened=index,
                exit_type=exit_type
            )
        time.sleep(2)

    def print_log_send_msg(self, msg: str, error: bool = False):
        print(msg)
        self.log.info(msg)

        if self.logger:
            message = msg.encode(self.FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            self.logger_client.send(send_length)
            self.logger_client.send(message)

            if error:
                self.log.error(msg, exc_info=True)

    def security_check_max_down(self):
        """

        """
        self.print_log_send_msg(f'Current bot PNL is {self.currentPNL}')
        max_down_amount = -1 * self.max_down * self.bankroll
        if self.currentPNL <= max_down_amount:
            self.security_close_all(exit_type="MAX_LOSS")



self = Strategy(bot_id='test', candle='15m', size=100, window=3, holding=10, bankroll=1000, max_down=0.3)
asyncio.run(self.get_prod_data(list_pair=['BTCUSDT', 'ETHUSDT']))


