import asyncio
from helpers.entries import Entry
import time
from typing import Tuple
import pandas as pd
from datetime import datetime
from localconfig import config
from connect.connection import Connection
from MetaTrader5 import TIMEFRAME_H1, TIMEFRAME_H4, TIMEFRAME_M1
from pymt5adapter import const
from pymt5adapter.context import _ContextAwareBase
from pymt5adapter.core import copy_rates_from_pos, copy_ticks_from, copy_rates
from pymt5adapter.core import symbol_info as sym_info
from pymt5adapter.core import symbol_info_tick
from pymt5adapter.core import symbol_select
from pymt5adapter.types import SymbolInfo
from pymt5adapter.types import Union

# connect_path = "D:\\DATA_SET_MACHINE_LEARNING\\trading_engine\\my_trading_system\\connect\\connection.ini"


def make_ohlcv(array_of_price):
    """
    With array of price from MT5 it creates ohlcv data
    """
    # create DataFrame out of the obtained data
    ohlcv = pd.DataFrame(array_of_price)
    # convert time in seconds into the datetime format
    ohlcv['time'] = pd.to_datetime(ohlcv['time'], unit='s')
    ohlcv.set_index('time', drop=False, inplace=True)
    ohlcv.columns = ['time', 'Open', 'High', 'Low',
                             'Close', 'Volume', 'Spread', 'Real_Volume']

    return ohlcv


class Symbol(_ContextAwareBase, Connection):
    calc_timeframe = 0
    current_bar = 0
    last_bar = 0
    first_time = True

    current_tick = 0
    first_tick = True
    last_tick = 0

    def __init__(self, symbol: Union[str, SymbolInfo], timeframe, max_bars: int = None, terminal='xm_terminal_connection'):
        # -----------------------------------------------------+
        # * (START)  reading all the configuration and initializing connection class
        # -----------------------------------------------------+
        # config.read('exchange\\connection.ini')
        # ! for interactive python shell
        # config.read(connect_path)
        # if terminal == 'GLOBAL':
        #     keyargs = dict(list(config.real_terminal_connection))
        # elif terminal == 'XM':
        #     keyargs = dict(list(config.xm_terminal_connection))
        # super(Symbol, self).__init__(**keyargs)
        # -----------------------------------------------------+
        # * (END)  reading all the configuration and initializing connection class
        # -----------------------------------------------------+
        self.terminal = terminal
        self.name = symbol
        self._timeframe = timeframe
        self.max_bars = max_bars

    @property
    def terminal(self):
        return self._terminal

    @terminal.setter
    def terminal(self, terminal: str):
        self._terminal = terminal
        keyargs = dict(config.items(terminal))
        super(Symbol, self).__init__(**keyargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, symbol):
        try:
            self._name = symbol.name
            self._info = symbol
        except AttributeError:
            self._name = symbol
            self._info = None
        self._refresh()

    @property
    def df(self) -> pd.DataFrame:
        return self.get_rates_bar(ohlcv=True)

    @property
    def p_value(self) -> int:
        """
        P value for pip calculation 4 digit and 5 digit broker
        """
        digits = self.digits
        if digits == 5 or digits == 3 or digits == 1:
            return 10  # ! to account for 5 digit broker to make the pips for 4 digit
        else:
            return 1

    @property
    def symbol_info(self):
        """
        Get all the information of this symbol, each key is a property of this symbol
        """
        with self.connected:
            symbol_info = sym_info(self.name)
            return symbol_info

    @property
    def timeframe(self):
        return self._timeframe

    @timeframe.setter
    def timeframe(self, timeframe):
        self._timeframe = timeframe

    @property
    def select(self):
        return self._select

    @select.setter
    def select(self, enable: bool):
        with self.connected:
            x = symbol_select(self._name, enable)
            self._select = enable if x else not enable

    @property
    def tick(self) -> Tuple:
        with self.connected:
            self._tick = symbol_info_tick(self.name)
            return self._tick

    @property
    def spread(self) -> float:
        return int(round(self.spread_float / self.trade_tick_size))

    @property
    def bid(self) -> float:
        return self.tick.bid

    @property
    def ask(self) -> float:
        return self.tick.ask

    def _data(self, key):
        rate = self.get_rates_position()
        try:
            return rate[:][key]
        except:
            return 0

    @property
    def tick_volume(self) -> float:
        return self.tick.volume

    @property
    def time(self) -> datetime:
        """
        last bar time for defined timeframe, by default daily
        """
        return pd.to_datetime(self._data('time')[-1], unit='s')

    @property
    def time_bars(self) -> pd.Series:
        """
        last bar time for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        time = pd.Series(df['time'], index=df.index)
        return time

    @property
    def close(self) -> float:
        """
        last close price for defined timeframe, by default daily
        """
        return self._data('close')[-1]

    @property
    def close_bars(self) -> pd.Series:
        """
        all close price for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        Close = pd.Series(df['Close'], index=df.index)
        return Close

    @property
    def low(self) -> float:
        """
        last low price for defined timeframe, by default daily
        """
        return self._data('low')[-1]

    @property
    def low_bars(self) -> pd.Series:
        """
        all low price for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        lows = pd.Series(df['Low'], index=df.index)
        return lows

    @property
    def high(self) -> float:
        """
        last low price for defined timeframe, by default daily
        """
        return self._data('high')[-1]

    @property
    def high_bars(self) -> pd.Series:
        """
        all low price for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        highs = pd.Series(df['High'], index=df.index)
        return highs

    @property
    def open(self) -> float:
        """
        last open price for defined timeframe, by default daily
        """
        return self._data('open')[-1]

    @property
    def open_bars(self) -> pd.Series:
        """
        all open price for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        Open = pd.Series(df['Open'], index=df.index)
        return Open

    @property
    def real_volume(self) -> float:
        """
        last real_volume for defined timeframe, by default daily
        """
        return self._data('real_volume')[-1]

    @property
    def real_volume_bars(self) -> pd.Series:
        """
        all real_volume for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        Real_Volume = pd.Series(df['Real_Volume'], index=df.index)
        return Real_Volume

    @property
    def volume(self) -> float:
        """
        last volume price for defined timeframe, by default daily
        """
        return self._data('volume')[-1]

    @property
    def volume_bars(self) -> pd.Series:
        """
        all volume price for defined timeframe, by default daily
        """
        df = self.get_rates_bar(ohlcv=True)
        Volume = pd.Series(df['Volume'], index=df.index)
        return Volume

    # @property
    # def volume_real(self):
    #     return self.tick.volume_real

    @property
    def is_new_bar(self) -> bool:
        """
        If a new bar occured for defined timeframe
        """
        if self.calc_timeframe != self.timeframe:
            self.calc_timeframe = self.timeframe
            self.first_bar = True

        self.current_bar = self.time

        if self.first_bar == True:
            self.last_bar = self.time
            self.calc_timeframe = self.timeframe
            self.first_bar = False
            return True

        if self.current_bar != self.last_bar:
            self.last_bar = self.current_bar
            self.calc_timeframe = self.timeframe
            return True
        else:
            return False

    @property
    def is_new_tick(self) -> bool:
        """
        check if a new tick has occured
        """
        self.current_tick = pd.to_datetime(self.tick.time, unit='s')

        if self.first_tick == True:
            self.last_tick = pd.to_datetime(self.tick.time, unit='s')
            self.first_tick = False
            return True

        if self.current_tick != self.last_tick:
            self.last_tick = self.current_tick
            return True
        else:
            return False

    @property
    def yen_adjust_factor(self):
        """
        This function returns a constant factor, which is used for position sizing for Yen pairs
        """
        output = 1
        if self.digits == 2 or self.digits == 3:
            output = 100
        return output

    def get_ticks_from(self,
                       datetime_from: Union[datetime, int],
                       count: int,) -> pd.DataFrame:
        """
        get tick data as dataframe
        >>> datetime_from: starting date datetime
        >>> count: how many ticks you want
        """
        with self.connected:
            ticks = copy_ticks_from(
                self.name, datetime_from, count, const.COPY_TICKS.ALL)
            ticks_frame = pd.DataFrame(ticks)
            # convert time in seconds into the datetime format
            ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='s')
            return ticks_frame

    def get_rates_position(self):
        """
        This will get array of bar data, if you want dataframe use make_ohlcv function
        >>> `nth_bar`: how many bar data we want
        """
        with self.connected:
            if self.max_bars:
                # ! 1 for last candle, which is closed
                bars = copy_rates_from_pos(
                    self.name, self.timeframe, 1, self.max_bars)
            else:
                # ! 1 for last candle, which is closed
                bars = copy_rates_from_pos(
                    self.name, self.timeframe, 1, 99999)
            return bars

    def get_rates_bar(self, ohlcv: bool = True):
        """
        This will get array of bar data, if you want dataframe use make_ohlcv function

        """
        with self.connected:
            if self.max_bars:
                # ! 1 for last candle, which is closed
                bars = copy_rates(self.name, self.timeframe,
                                  start_pos=1, count=self.max_bars)
            else:
                bars = copy_rates(self.name, self.timeframe)

            if ohlcv:
                df = make_ohlcv(bars)
                return df
            else:
                return bars

    def normalize_price(self, price: float):
        """
        Normalizes prices as per digits of the pair
        """
        ts = self.trade_tick_size
        if ts != 0.0:
            return round(round(price / ts) * ts, self.digits)

    def lot_size(self, capital, risk_percent: float, stop_point: int, MAX_RISK_PERCENT: float, NEED_CONFIRMATION_FOR_BUY: bool, entry: Entry):
        """
        Find out lot size with stoploss and risk percentage
        """
        # assert stop_point != 0 or stop_point is not None, "You must define stop loss, whoever or what ever your strategy is, I won't allow it"

        # ! checking here if we have define stop_point and risk_percent
        if risk_percent > 0 and stop_point > 0:
            # ! if for some foolish reason we have defined the stop loss to be more than our max risk percent than our risk percent will be max
            trade_size = 0
            while trade_size == 0:
                if risk_percent > MAX_RISK_PERCENT:
                    risk_percent = MAX_RISK_PERCENT

                p = self.p_value

                # ! finding out account margin (MARGIN IS THE AMOUNT WILL TAKE AS LOSS WHEN OUR INITIAL STOP IS HIt)
                margin = capital * (risk_percent / 100)
                tick_size = self.trade_tick_value
                # ! stop_point * p to make a normal pip for both 4 digit and 5 digit broker
                # also with (risk_percent*0.01*account_balance)/(self.trade_contract_size *
                #                self.trade_tick_value*stop_point*self.point * p)
                trade_size = (margin/(stop_point * p)) / tick_size
                # ! to take the lowest value, as round and floor makes it higher but to stay with my risk I will reduce it to lowest ex: 0.0356 to 0.03 not 0.04
                trade_size = float(str(trade_size)[:4])
                if trade_size == 0:
                    if not NEED_CONFIRMATION_FOR_BUY:
                        # ! if autotrade than we will not open a position
                        return 0, 0, 0, 0
                    # ! we will find a new stop loss
                    old_stop_point = stop_point
                    stop_point = (margin / tick_size) * p
                    print(
                        f"With the current stop point of {old_stop_point}, the risk percent of {risk_percent} will have {trade_size} trade size, the stop point must be max at {stop_point}, new stop point is changed at {int(stop_point)}")
                    try:
                        if entry == Entry.Buy:
                            new_price = self.add_subtract_pips_to_price(
                                self.bid, stop_point, add=False)
                            stop_point_agree = int(input(
                                f"do you agree to place stop loss at: {self.normalize_price(new_price)}, enter 1 for yes: "))

                            if stop_point_agree != 1:
                                stop_price = float(
                                    input("define the stop point where you want your stop loss: "))
                                stop_point = self.price_diff_to_pips(
                                    self.bid, stop_price, convert=True)

                                risk_percent = float(input(
                                    "Define a new increased risk percent, cause previous risk percent won't work for this trade: "))
                        elif entry == Entry.Sell:
                            new_price = self.add_subtract_pips_to_price(
                                self.ask, stop_point, add=True)
                            stop_point_agree = int(input(
                                f"do you agree to place stop loss at: {self.normalize_price(new_price)}, enter 1 for yes: "))

                            if stop_point_agree != 1:
                                stop_price = float(
                                    input("define the stop point where you want your stop loss: "))
                                stop_point = self.price_diff_to_pips(
                                    self.ask, stop_price, convert=True)

                                risk_percent = float(input(
                                    "Define a new increased risk percent, cause previous risk percent won't work for this trade: "))
                    except Exception as ve:
                        print(ve.args[0])
                        print(
                            "Typed wrong, try again")
                        stop_point = old_stop_point

            trade_size = self.verify_volume(trade_size)

        else:
            print("No stop point and risk percent is defined")
            trade_size = 0

        return entry, int(stop_point), trade_size, risk_percent

    def lot_size_bt(self, capital, risk_percent: float, stop_point: int, MAX_RISK_PERCENT: float):
        """
        Find out lot size with stoploss and risk percentage, this one is for backtesting purposes
        """
        # assert stop_point != 0 or stop_point is not None, "You must define stop loss, whoever or what ever your strategy is, I won't allow it"

        # ! checking here if we have define stop_point and risk_percent
        if risk_percent > 0 and stop_point > 0:
            # ! if for some foolish reason we have defined the stop loss to be more than our max risk percent than our risk percent will be max
            if risk_percent > MAX_RISK_PERCENT:
                risk_percent = MAX_RISK_PERCENT

            p = self.p_value

            # ! finding out account margin (MARGIN IS THE AMOUNT WILL TAKE AS LOSS WHEN OUR INITIAL STOP IS HIt)
            margin = capital * (risk_percent / 100)
            tick_size = self.trade_tick_value
            # ! stop_point * p to make a normal pip for both 4 digit and 5 digit broker
            # also with (risk_percent*0.01*account_balance)/(self.trade_contract_size *
            #                self.trade_tick_value*stop_point*self.point * p)
            trade_size = (margin/(stop_point * p)) / tick_size
            # ! to take the lowest value, as round and floor makes it higher but to stay with my risk I will reduce it to lowest ex: 0.0356 to 0.03 not 0.04
            trade_size = float(str(trade_size)[:4])
            if trade_size == 0:
                old_stop_point = stop_point
                stop_point = (margin / tick_size) * p
                print(
                    f"With the current stop point of {old_stop_point}, the risk percent of {risk_percent} will have {trade_size} trade size, the stop point must be max at {stop_point}, new stop point is changed at {int(stop_point)}")
            trade_size = self.verify_volume(trade_size)

        else:
            print("No stop point and risk percent is defined")
            trade_size = 0

        return int(stop_point), trade_size

    def verify_volume(self, lot) -> float:
        """
        verify volume with the lowest and highest volume,  size and step value and returns the newely calculated volume
        >>> lot: our calculated lot size
        """
        min_volume = self.volume_min
        max_volume = self.volume_max
        step_volume = self.volume_step

        if lot < min_volume:
            lot = min_volume
        elif lot > max_volume:
            lot = max_volume
        # ! making trade size with step volume
        else:
            lot = round(lot/step_volume) * step_volume

        if step_volume >= 0.1:
            lot = round(lot, 1)
        else:
            lot = round(lot, 2)

        return lot

    def add_subtract_pips_to_price(self, price, pips, add):
        """
        adds or subtracts pips to the price
        >>> `price`: the price with which we want to add or subt
        >>> `pips`: with how many pips we want to add or subtract
        >>> `add`: 'True' for add 'False' for subtract
        """
        P = self.p_value
        pips = (pips*self.point*P)
        if add:
            ret_price = price + pips
        else:
            ret_price = price - pips
        return ret_price

    def price_diff_to_pips(self, first_price: float, second_price: float, convert=False):
        """
        Calculate distance between two price points and convert the differece in pips
        symbol_info: symbol dictionary
        order_price: executed order price
        stop_price: our defined stop price
        convert: if true 20pip, otherwise 200pip(pip for 5 digit broker)
        """
        stop_diff = abs(first_price-second_price)
        get_point = self.point
        if convert:
            P = self.p_value
            price_to_point = int((stop_diff / get_point)/P)
            # ! exact pip like 20 pip
        else:
            price_to_point = int(stop_diff / get_point)
            # ! pip for 5 digit broker like 200

        return price_to_point

    def tick_calc(self, price: float, num_ticks: int):
        """Calculate a new price by number of ticks from the price param. The result is normalized to the
        tick-size of the instrument.

        :param price: The price to add or subtract ticks from.
        :param num_ticks: number of ticks. If subtracting ticks then this should be a negative number.
        :return: A new price adjusted by the number of ticks and normalized to tick-size.
        """
        return self.normalize_price(price + num_ticks * self.trade_tick_size)

    def refresh_rates(self):
        # with self.connected:
        self.tick
        return self

    def _refresh(self):
        info = self._info or self.symbol_info
        # ! if symbol is not selected in market watch select the symbol
        self.select = info.select if info.select else True
        self.refresh_rates()
        # self.spread = info.spread
        # self.volume_real = info.volume_real
        self.custom = info.custom
        self.chart_mode = info.chart_mode
        self.visible = info.visible
        self.session_deals = info.session_deals
        self.session_buy_orders = info.session_buy_orders
        self.session_sell_orders = info.session_sell_orders
        # self.volume = info.volume
        self.volumehigh = info.volumehigh
        self.volumelow = info.volumelow
        self.digits = info.digits
        self.spread_float = info.spread_float
        self.ticks_bookdepth = info.ticks_bookdepth
        self.trade_calc_mode = info.trade_calc_mode
        self.trade_mode = info.trade_mode
        self.start_time = info.start_time
        self.expiration_time = info.expiration_time
        self.trade_stops_level = info.trade_stops_level
        self.trade_freeze_level = info.trade_freeze_level
        self.trade_exemode = info.trade_exemode
        self.swap_mode = info.swap_mode
        self.swap_rollover3days = info.swap_rollover3days
        self.margin_hedged_use_leg = info.margin_hedged_use_leg
        self.expiration_mode = info.expiration_mode
        self.filling_mode = info.filling_mode
        self.order_mode = info.order_mode
        self.order_gtc_mode = info.order_gtc_mode
        self.option_mode = info.option_mode
        self.option_right = info.option_right
        self.bidhigh = info.bidhigh
        self.bidlow = info.bidlow
        self.askhigh = info.askhigh
        self.asklow = info.asklow
        self.lasthigh = info.lasthigh
        self.lastlow = info.lastlow
        self.volumehigh_real = info.volumehigh_real
        self.volumelow_real = info.volumelow_real
        self.option_strike = info.option_strike
        self.point = info.point
        self.trade_tick_value = info.trade_tick_value
        self.trade_tick_value_profit = info.trade_tick_value_profit
        self.trade_tick_value_loss = info.trade_tick_value_loss
        self.trade_tick_size = info.trade_tick_size
        self.trade_contract_size = info.trade_contract_size
        self.trade_accrued_interest = info.trade_accrued_interest
        self.trade_face_value = info.trade_face_value
        self.trade_liquidity_rate = info.trade_liquidity_rate
        self.volume_min = info.volume_min
        self.volume_max = info.volume_max
        self.volume_step = info.volume_step
        self.volume_limit = info.volume_limit
        self.swap_long = info.swap_long
        self.swap_short = info.swap_short
        self.margin_initial = info.margin_initial
        self.margin_maintenance = info.margin_maintenance
        self.session_volume = info.session_volume
        self.session_turnover = info.session_turnover
        self.session_interest = info.session_interest
        self.session_buy_orders_volume = info.session_buy_orders_volume
        self.session_sell_orders_volume = info.session_sell_orders_volume
        self.session_open = info.session_open
        self.session_close = info.session_close
        self.session_aw = info.session_aw
        self.session_price_settlement = info.session_price_settlement
        self.session_price_limit_min = info.session_price_limit_min
        self.session_price_limit_max = info.session_price_limit_max
        self.margin_hedged = info.margin_hedged
        self.price_change = info.price_change
        self.price_volatility = info.price_volatility
        self.price_theoretical = info.price_theoretical
        self.price_greeks_delta = info.price_greeks_delta
        self.price_greeks_theta = info.price_greeks_theta
        self.price_greeks_gamma = info.price_greeks_gamma
        self.price_greeks_vega = info.price_greeks_vega
        self.price_greeks_rho = info.price_greeks_rho
        self.price_greeks_omega = info.price_greeks_omega
        self.price_sensitivity = info.price_sensitivity
        self.basis = info.basis
        self.category = info.category
        self.currency_base = info.currency_base
        self.currency_profit = info.currency_profit
        self.currency_margin = info.currency_margin
        self.bank = info.bank
        self.description = info.description
        self.exchange = info.exchange
        self.formula = info.formula
        self.isin = info.isin
        self.page = info.page
        self.path = info.path
        return self


if __name__ == "__main__":

    # tasks = set()

    # class Strategy():
    #     """
    #     Strategy class example
    #     """

    #     def __init__(self, symbol: str):
    #         self.symbol = Symbol(symbol, TIMEFRAME_M1)

    #     async def next(self):
    #         """
    #         will perform next check
    #         """
    #         symbol = self.symbol
    #         # print("Called for symbol: ", symbol.name)

    #         # print("2nd Call for symbol: ", symbol.name)
    #         if symbol.is_new_tick:
    #             print(f"{symbol.name} New Tick: ",
    #                   pd.to_datetime(symbol.tick.time, unit='s'))
    #             print("Bid: ", symbol.normalize_price(symbol.tick.bid),
    #                   " Ask: ", symbol.normalize_price(symbol.tick.ask))

    #         new_bar = symbol.is_new_bar
    #         if new_bar:
    #             print(f"{symbol.name} New Bar: ", symbol.time)
    #         # print(tasks)
    #         task = asyncio.create_task(self.next(), name=symbol)
    #         tasks.add(task)

    # symbols = ['EURUSD', 'GBPUSD', 'AUDUSD', 'USDJPY', 'USDCHF']

    # # -----------------------------------------------------+
    # # * (START)  One way of doing it
    # # -----------------------------------------------------+

    # async def run_live():
    #     for symbol in symbols:
    #         strtg = Strategy(symbol)
    #         task = asyncio.create_task(strtg.next(), name=symbol)
    #         tasks.add(task)
    #     while True:
    #         done, _pending = await asyncio.wait(tasks, timeout=0.01)
    #         tasks.difference_update(done)
    #         print('--'*10)

    # async def async_main() -> None:
    #     try:
    #         await run_live()
    #     except asyncio.CancelledError:
    #         print('Process got cancelled')
    #         # ! if for some reason we cancel the progress, we will cancel all the remaining process
    #         for task in tasks:
    #             task.cancel()
    #         # ! for being grasious we will give one last chanche to any task might be pending
    #         done, pending = await asyncio.wait(tasks, timeout=1.0)
    #         # ! remvoing the done and any pending task in the list
    #         tasks.difference_update(done)
    #         tasks.difference_update(pending)
    #         # ! still checking if there is any pending task
    #         if tasks:
    #             print("warning: more tasks added while we were cancelling")

    # loop = asyncio.get_event_loop()
    # task = loop.create_task(async_main())
    # # ! after 10 seconds we will cancel the task
    # loop.call_later(600, task.cancel)
    # loop.run_until_complete(task)
    # -----------------------------------------------------+
    # * (END)  One way of doing it
    # -----------------------------------------------------+

    sym = Symbol('EURJPY', const.TIMEFRAME_H1, 3000)
    # ! WE CAN ALSO CHANGE THE TIMEFRAME, LAST BAR VALUE WILL BE CHANGED TOO
    # sym.timeframe = const.TIMEFRAME_M1
    # rates_df = sym.get_rates_bar()
    # df = make_ohlcv(rates_df)
    print(sym.high_bars)
    time = sym.time
    print(time)
    close = sym.normalize_price(sym.close)
    print(close)
    close_array = sym.close_bars.to_numpy()
    print(close_array[-2])
    low = sym.normalize_price(sym.low)
    print(low)
    sym.timeframe = TIMEFRAME_H4
    close_array = sym.close_bars.to_numpy()
    print(close_array[-2])
    new_bar = sym.is_new_bar
    tries = 0
    while tries < 6000:
        new_tick = sym.is_new_tick
        if new_tick:
            print("New Tick: ", pd.to_datetime(sym.tick.time, unit='s'))
            print("Bid: ", sym.normalize_price(sym.tick.bid),
                  " Ask: ", sym.normalize_price(sym.tick.ask))
        # else:
        #     print('Not a new tick, Old Tick: ',
        #           pd.to_datetime(sym.tick.time, unit='s'))

        new_bar = sym.is_new_bar
        if new_bar:
            print("New Bar: ", sym.time)
        # else:
        #     print("Old Bar: ", sym.time)

        tries += 1
    print(Symbol('CHFJPY', TIMEFRAME_H1))
