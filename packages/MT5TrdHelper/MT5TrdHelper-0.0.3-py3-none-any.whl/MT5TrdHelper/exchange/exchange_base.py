

from datetime import datetime
from typing import Union
from MT5TrdHelper.connect.connection import Connection
import pymt5adapter as mt5
from pymt5adapter.order import Order
import pandas as pd
from abc import abstractmethod, ABCMeta


class Exchaenge(Connection, metaclass=ABCMeta):
    def __init__(self,
                 path,
                 portable,
                 server,
                 login,
                 password,
                 timeout,
                 logger,  # default is None
                 ensure_trade_enabled,  # default is False
                 enable_real_trading,  # default is False
                 raise_on_errors,  # default is False
                 return_as_dict,  # default is False
                 return_as_native_python_objects   # default is False)
                 ):
        """
        exchange class for account re
        """
        super(Exchaenge, self).__init__(path,
                                        portable,
                                        server,
                                        login,
                                        password,
                                        timeout,
                                        logger,  # default is None
                                        ensure_trade_enabled,  # default is False
                                        enable_real_trading,  # default is False
                                        raise_on_errors,  # default is False
                                        return_as_dict,  # default is False
                                        return_as_native_python_objects   # default is False)
                                        )

    @abstractmethod
    def get_account_info(self):
        """
        Get current active account information from mt5
        """
        raise NotImplementedError

    @abstractmethod
    def get_position_from_order_send_result(self, result: mt5.OrderSendResult):
        """
        Function to get recently placed order details with ordersendresult object, which is returned by order_send function call
        """
        raise NotImplementedError

    @abstractmethod
    def get_position_with_ticket_id(self, ticket_id: int):
        """
        Get an open position with ticket id
        """
        raise NotImplementedError

    @abstractmethod
    def get_position_with_symbol(self, symbol: str):
        """
        Get an open position with ticket id
        """
        raise NotImplementedError

    @abstractmethod
    def get_position_with_magic(self, magic: int):
        """
        Get all open position with magic number
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_open_position(self):
        """
        Get all open positions
        """
        raise NotImplementedError

    @abstractmethod
    def get_total_open_positions(self):
        """
        Get total number of open positions
        """
        raise NotImplementedError

    @abstractmethod
    def get_history_position(self, order_id: int):
        """
        Get a position from order history with order id
        """
        raise NotImplementedError

    @abstractmethod
    def market_order_send(self, symbol, volume, order_type, stop_loss, take_profit, slippage, magic, position=0):
        """
        Function to place a market order(open order, close order)
        """
        raise NotImplementedError

    @abstractmethod
    def modify_sl(self, stop_loss, position):
        """
        Modify stop loss
        """
        raise NotImplementedError

    @abstractmethod
    def modify_tp(self, take_profit, position):
        """
        Modify stop loss
        """
        raise NotImplementedError


if __name__ == "__main__":
    conn = mt5.connected()
    with conn:
        exc = Exchaenge()
        symbol_positions = exc.get_position_with_symbol('GBPUSD')
        print(symbol_positions)
