import io
from datetime import datetime, timedelta
from localconfig.manager import LocalConfig
from typing import Union
from pymt5adapter import order
from pymt5adapter.const import COPY_TICKS, ORDER_TIME, ORDER_TYPE, POSITION_TYPE, TIMEFRAME_M1, TRADE_ACTION, ORDER_FILLING
from MT5TrdHelper.exchange.exchange_base import Exchaenge
import pymt5adapter as mt5
from pymt5adapter.order import Order
from pymt5adapter.types import TradePosition
from typing import Tuple
import pandas as pd

# connect_path = "D:\\DATA_SET_MACHINE_LEARNING\\trading_engine\\my_trading_system\\connect\\connection.ini"
# add_setting_path = "D:\\DATA_SET_MACHINE_LEARNING\\trading_engine\\my_trading_system\\connect\\additional_settings.ini"


class MT5Exchange(Exchaenge):
    def __init__(self, connect_path, add_setting_path, terminal='real_terminal_connection'):
        """
        exchange class for account re
        """
        # -----------------------------------------------------+
        # * (START)  reading all the configuration and initializing connection class
        # -----------------------------------------------------+
        coneection_config = LocalConfig()
        coneection_config.read(connect_path)
        # config.read('.\\connection.ini')
        keyargs = dict(coneection_config.items(terminal))

        add_sett_config = LocalConfig()
        add_sett_config.read(add_setting_path)
        self.ADDITIONAL_SETTINGS = dict(add_sett_config.items(terminal))

        super(MT5Exchange, self).__init__(**keyargs)
        # -----------------------------------------------------+
        # * (END)  reading all the configuration and initializing connection class
        # -----------------------------------------------------+

    def get_terminal_info(self):
        """
        Get current active account information from mt5
        """
        with self.connected:
            terminal_info = mt5.terminal_info()
            return terminal_info

    def get_account_info(self):
        """
        Get current active account information from mt5
        """
        with self.connected:
            account_info = mt5.account_info()
            return account_info

    def get_current_capital(self, use_balance: bool = False, use_equity: bool = False, use_free_margin: bool = False):
        """
        Get current equity based on parameter
        """
        acc_inf = self.get_account_info()
        if use_balance:
            return acc_inf.balance
        elif use_equity:
            return acc_inf.equity
        elif use_free_margin:
            return acc_inf.margin_free

    def get_position_from_order_send_result(self, result: mt5.OrderSendResult):
        """
        Function to get recently placed order details with ordersendresult object, which is returned by order_send function call
        """
        with self.connected:
            if result.order != 0:
                pos = self.get_position_with_ticket_id(result.order)
            # ! than we take the first item from the order, and take it's position_id(ticket id) and with it we
            elif result.request.position != 0:
                pos = self.get_position_with_ticket_id(result.request.position)
            return pos

    def get_position_with_ticket_id(self, ticket_id: int):
        """
        Get an open position with ticket id
        """
        with self.connected:
            # ! we take the first item from order, and take it's position_id(ticket id) and with it we
            pos = mt5.positions_get(ticket=ticket_id)
            if pos:
                return pos[0]
            else:
                return dict()

    def get_position_with_symbol(self, symbol: str):
        """
        Get an open position with ticket id
        """
        with self.connected:
            # ! we take the first item from order, and take it's position_id(ticket id) and with it we
            pos = mt5.positions_get(symbol=symbol)
            return pos

    def get_position_with_magic(self, magic: int):
        """
        Get all open position with magic number
        """
        positions = self.get_all_open_position()
        pos = filter(lambda p: p.magic == magic, positions)
        pos = list(pos)
        return pos

    def get_all_open_position(self) -> Tuple[TradePosition]:
        """
        Get all open positions
        >>> filter from all positions     
        pos = filter(lambda position: position.ticket == 206080473
                 and position.symbol == 'EURUSD', positions)
        pos = list(pos)
        """
        with self.connected:
            positions = mt5.positions_get()
            return positions

    def get_all_pending_position(self) -> Tuple[TradePosition]:
        """
        Get all open positions
        >>> filter from all positions     
        pos = filter(lambda position: position.ticket == 206080473
                 and position.symbol == 'EURUSD', positions)
        pos = list(pos)
        """
        with self.connected:
            positions = mt5.orders_get()
            positions = filter(lambda pos: pos.type !=
                               ORDER_TYPE.BUY or pos.type != ORDER_TYPE.SELL, positions)
            return tuple(positions)

    def get_total_open_positions(self, all_positions: bool = False, buy_positions: bool = False, sell_positions: bool = False, magic: int = 0, with_magic: bool = False) -> int:
        """
        Get total number of open positions
        >>> If with magic than total position, buy position, sell position will be calculated under this magic number
        >>> Without magic than total position, buy position, sell position will be caluclated for all open position
        """
        with self.connected:
            if with_magic:
                assert magic != 0, 'Please define magic number'
                open_positions = self.get_position_with_magic(magic)
                if all_positions:
                    return len(open_positions)
                elif buy_positions:
                    positions = filter(lambda p: p.type ==
                                       POSITION_TYPE.BUY, open_positions)
                    tot_buy = len(list(positions))
                    return tot_buy
                elif sell_positions:
                    positions = filter(lambda p: p.type ==
                                       POSITION_TYPE.SELL, open_positions)
                    tot_sell = len(list(positions))
                    return tot_sell
            else:
                open_positions = self.get_all_open_position()
                if all_positions:
                    return len(open_positions)
                elif buy_positions:
                    positions = filter(lambda p: p.type ==
                                       POSITION_TYPE.BUY, open_positions)
                    tot_buy = len(list(positions))
                    return tot_buy
                elif sell_positions:
                    positions = filter(lambda p: p.type ==
                                       POSITION_TYPE.SELL, open_positions)
                    tot_sell = len(list(positions))
                    return tot_sell

    def get_history_position(self, order_id: int):
        """
        Get a position from order history with order id, it will return tuple with two position one with entry data and another with exit and profit data
        """
        with self.connected:
            position = mt5.history_deals_get(position=order_id)
            return position

    async def market_order_send(self, symbol: str, price: Union[float, None], volume, order_type, slippage, magic, action=mt5.TRADE_ACTION.DEAL, stop_loss: float = None, take_profit: float = None,  position_ticket=0, comment=None, type_time: ORDER_TIME = None, expiration: datetime = None):
        """
        Function to place a market order(open order, close order)
        """
        with self.connected:
            result = mt5.order_send(action=action, type=order_type,
                                    symbol=symbol, price=price, volume=volume, sl=stop_loss, tp=take_profit, deviation=slippage, type_filling=ORDER_FILLING(
                                        int(self.ADDITIONAL_SETTINGS['execution_type'])), position=position_ticket, magic=magic, comment=comment, type_time=type_time, expiration=expiration)
            if not result.retcode == mt5.TRADE_RETCODE.DONE:
                print(
                    f"Some error occured, while executing order: {result.comment}")
            return result

    def modify_sl(self, stop_loss, position):
        """
        Modify stop loss
        >>> `stop_loss`: stop loss as price
        >>> `position`: position object
        """
        # assert stop_loss, 'Stop loss can\'t be empty'
        with self.connected:

            order = Order.as_modify_sltp(
                position, sl=stop_loss, tp=position.tp, comment=position.comment)
            pos = order.send()
            return pos

    def modify_tp(self, take_profit, position):
        """
        Modify stop loss
        """
        assert take_profit, 'Take profit can\'t be empty'
        with self.connected:

            order = Order.as_modify_sltp(
                position, sl=position.sl, tp=take_profit, comment=position.comment)
            pos = order.send()
            return pos

    def modify_sl_tp(self, take_profit, stop_loss, position):
        """
        Modify stop and take profit together
        >>> `take_profit`: take profit price
        >>> `stop_loss`: stop loss price
        """
        # assert take_profit, 'Take profit can\'t be empty'
        with self.connected:
            order = Order.as_modify_sltp(
                position, sl=stop_loss, tp=take_profit, comment=position.comment)
            pos = order.send()
            return pos

    def calc_order_margin(self, order_type: int, symbol: str, lot: float, price: float):
        """
        Calculate margin required to open a position
        """

        assert lot != 0, "Calculation of lot failed for some reason"
        with self.connected:
            margin = mt5.order_calc_margin(order_type, symbol, lot, price)
            return margin

    def calc_order_profit(self, order_type: int, symbol: str, lot: float, price_open: float, current_price):
        """
        Calculate margin required to open a position
        """
        assert lot != 0, "Calculation of lot failed for some reason"
        with self.connected:
            profit = mt5.order_calc_profit(
                order_type, symbol, lot, price_open, current_price)
            return profit

    def validate_order_margin(self, order_type: int, symbol: str, lot: float, price: float):
        req_margin = self.calc_order_margin(order_type, symbol, lot, price)
        free_margin = self.get_current_capital(use_free_margin=True)
        if free_margin > req_margin:
            return True
        else:
            return False


if __name__ == "__main__":
    exc = MT5Exchange(terminal='XM')
    pos = exc.get_position_with_ticket_id(215066002)
    # ! FOR testing remove async from function
    # result = exc.market_order_send("GBPUSD", action=TRADE_ACTION.PENDING, price=1.4004, volume=0.4, order_type=ORDER_TYPE.BUY_STOP,
    #                                slippage=10, magic=1003, stop_loss=0.0, take_profit=0.0, comment='HI', type_time=ORDER_TIME.GTC, expiration=None)

    # loop = io.get_event_loop()
    # tasks = exc.get_position_with_symbol('GBPUSD'), exc.get_all_open_position()
    # symbol_positions, ret = loop.run_until_complete(io.gather(*tasks))
    # print(symbol_positions)
    # print(ret)

    # ret = exc.get_all_open_position()
    # pos = filter(lambda position: position.ticket == 206080473
    #              and position.symbol == 'EURUSD', ret)

    # ticks = exc.get_ticks_from('EURUSD', datetime.today(), 10)
    # ticks.iloc[-1]
