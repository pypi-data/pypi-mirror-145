from MT5TrdHelper.helpers.entries import Entry
from pymt5adapter.types import OrderSendResult, TradePosition
import pytz
import pandas as pd
import time
from typing import Callable, Union
from datetime import datetime, timedelta
from MT5TrdHelper.exchange.symbol_base import Symbol
from MT5TrdHelper.exchange.mt5_exchange import MT5Exchange
# from helpers.database_helpers import get_hidden_be_db, get_hidden_sl_db, get_hidden_tp_db, get_hidden_trl_sl_db, insert_hidden_be_sl_db, insert_hidden_sl_db, insert_hidden_tp_db, insert_update_symbol_wave_info, insert_updt_hidden_trl_sl_db
import pymt5adapter as mt5
from pymt5adapter.const import ORDER_TIME, ORDER_TYPE, TIMEFRAME_M1, TRADE_ACTION, TRADE_RETCODE
from pymt5adapter.const import POSITION_TYPE

MARKET_CLOSED = 'Market closed'


class Trade:

    def __init__(self, exchange: MT5Exchange, symbol: str, magic_number=123456, slipaage=10, terminal='real_terminal_connection'):
        """
        initialize trade class
        exchange: an exchange base class object
        magic number = for identifying bot
        slippage: as deviation in the order functions
        """
        self.magic_number = magic_number
        self.slipaage = slipaage
        self.exchange = exchange
        self.TERMINAL = terminal
        self.symbol_name = symbol
        # ! Global variables
        self.FirstTick = True
        self.InitialCapital = 0
        self.profitAndLoss = 0
        self.output = False
        self.HiddenSLList = []
        self.HiddenTPList = []
        self.HiddenBEList = []
        self.HiddenTrailingList = []
        self.VolTrailingList = []
        self.HiddenVolTrailingList = []

    async def close_position(self, position: TradePosition) -> OrderSendResult:
        """
        Function to close an open position with TradePosition object
        """
        exc = self.exchange
        order_type = mt5.ORDER_TYPE.BUY if position.type == mt5.ORDER_TYPE.SELL else mt5.ORDER_TYPE.SELL
        position = exc.get_position_with_ticket_id(position.ticket)
        try:
            result = await exc.market_order_send(order_type=order_type, symbol=position.symbol,
                                                 volume=position.volume, position_ticket=position.ticket, slippage=self.slipaage, magic=self.magic_number, price=None)
            if result.retcode == mt5.TRADE_RETCODE.DONE:
                print("Successfully Closed Position: ", result.request.position)
            return result
        except Exception as ex:
            print(ex.args)

    async def close_position_volume(self, position: mt5.TradePosition, volume: float) -> mt5.OrderSendResult:
        """
        Function to close an open position with TradePosition object
        """
        exc = self.exchange
        order_type = mt5.ORDER_TYPE.BUY if position.type == mt5.ORDER_TYPE.SELL else mt5.ORDER_TYPE.SELL
        try:
            result = await exc.market_order_send(order_type=order_type, symbol=position.symbol,
                                                 volume=volume, position_ticket=position.ticket, slippage=self.slipaage, magic=self.magic_number, price=None)
            if result.retcode == mt5.TRADE_RETCODE.DONE:
                print("Successfully Closed Position: ", result.request.position)
            return result
        except Exception as ex:
            print(ex.args)

    async def close_all_position(self) -> None:
        """
        Function to close an open position with TradePosition object
        """
        exc = self.exchange
        magic = self.magic_number
        positions = exc.get_position_with_magic(magic)
        for pos in positions:
            order_type = ORDER_TYPE.BUY if pos.type == ORDER_TYPE.SELL else ORDER_TYPE.SELL
            try:
                result = await exc.market_order_send(order_type=order_type, symbol=pos.symbol,
                                                     volume=pos.volume, position=pos.ticket, slippage=self.slipaage, magic=self.magic_number)

            except Exception as ex:
                print(ex.args)

    async def close_all_buy_position(self) -> None:
        """
        Function to close an open position with TradePosition object
        """
        exc = self.exchange
        magic = self.magic_number
        positions = exc.get_position_with_magic(magic)
        buy_pos = filter(lambda p: p.type == POSITION_TYPE.BUY, positions)
        for pos in buy_pos:
            order_type = ORDER_TYPE.SELL
            try:
                result = await exc.market_order_send(order_type=order_type, symbol=pos.symbol,
                                                     volume=pos.volume, position=pos.ticket, slippage=self.slipaage, magic=self.magic_number)

            except Exception as ex:
                print(ex.args)

    async def close_all_sell_position(self) -> None:
        """
        Function to close an open position with TradePosition object
        """
        exc = self.exchange
        magic = self.magic_number
        positions = exc.get_position_with_magic(magic)
        buy_pos = filter(lambda p: p.type == POSITION_TYPE.SELL, positions)
        for pos in buy_pos:
            order_type = ORDER_TYPE.BUY
            try:
                result = await exc.market_order_send(order_type=order_type, symbol=pos.symbol,
                                                     volume=pos.volume, position=pos.ticket, slippage=self.slipaage, magic=self.magic_number)

            except Exception as ex:
                print(ex.args)

    async def close_all_pending_position(self, parameter_list):
        """
        Closes all pending position
        """
        exc = self.exchange
        for pos in exc .get_all_pending_position():
            await self.close_position(pos)

        assert len(exc .get_all_pending_position(
        )) == 0, 'Some pending Position may not have closed, take manual action'

    # ! place order via open market order (BUY SELL FUNCTION BELOW NOT NEEDED ANY MORE)
    # def buy(self, symbol: str, volume: float, sl_ticks: Union[int, float, None], tp_ticks: Union[int, float, None],) -> mt5.TradePosition:
    #     # TODO Implement P in sl & tp
    #     exc = self.exchange
    #     slippage = self.slipaage
    #     magic = self.magic_number

    #     tick = exc.get_symbol_info_tick(symbol)
    #     tick_size = exc.get_symbol_info(symbol).trade_tick_size
    #     sl = tick.ask - sl_ticks * tick_size if sl_ticks else None
    #     tp = tick.ask + tp_ticks * tick_size if tp_ticks else None
    #     result = exc.market_order_send(symbol=symbol, volume=volume, stop_loss=sl, take_profit=tp,
    #                                    order_type=mt5.ORDER_TYPE.BUY, slippage=slippage, magic=magic)
    #     assert result.comment != MARKET_CLOSED, 'Market is closed trade at a later time'
    #     pos = exc.get_position_from_order_send_result(result)
    #     return pos

    # def sell(self, symbol: str, volume: float, sl_ticks: int = None, tp_ticks: int = None) -> mt5.TradePosition:
    #     # TODO Implement P in sl & tp
    #     exc = self.exchange
    #     slippage = self.slipaage
    #     magic = self.magic_number

    #     tick = exc.get_symbol_info_tick(symbol)
    #     tick_size = exc.get_symbol_info(symbol).trade_tick_size

    #     sl = tick.bid + sl_ticks * tick_size if sl_ticks else None
    #     tp = tick.ask - tp_ticks * tick_size if tp_ticks else None
    #     result = exc.market_order_send(symbol=symbol, volume=volume, stop_loss=sl, take_profit=tp,
    #                                    order_type=mt5.ORDER_TYPE.SELL, slippage=slippage, magic=magic)

    #     pos = exc.get_position_from_order_send_result(result)
    #     assert pos.comment != MARKET_CLOSED, 'Market is closed trade at a later time'

    #     return pos

    def is_vol_limit_breached(self, symbol: str, VolLimitActivated: bool, VolMulti: float, ATR_val: float, debug: bool, entry_variable: Union[int, Entry]):
        """
        This function determines if our maximum volatility threshold is breached
        #  2 steps to this function:
        # --------
        #  1) It checks the price movement between current time and the closing price of the last completed 1min bar(shift 1 of 1min timeframe).
        #  2) Return True if this price movement > VolLimitMulti * VolATR
        """
        exc = self.exchange
        output = False
        one_min_sym = Symbol(symbol, TIMEFRAME_M1, terminal=self.TERMINAL)

        close = one_min_sym.close

        if(VolLimitActivated == False):
            return(output)

        priceMovement = abs(one_min_sym.bid-close)

        if(priceMovement > VolMulti*ATR_val):
            output = True
            if debug:
                if entry_variable in Entry:
                    print("Max volatility limit reached, Order won't be executed now")

        return(output)

    def is_max_pos_reached(self, max_positions_total: int, max_position_per_symbol: int, symbol_name: str, debug: bool, entry_variable: Union[int, Entry]):
        """
        This function checks the number of positions we are holding against the maximum allowed
        """
        result = False
        exc = self.exchange
        magic = self.magic_number
        positions = exc.get_position_with_magic(magic)
        pos = list(filter(lambda p: p.type == POSITION_TYPE.BUY or p.type ==
                          POSITION_TYPE.SELL, positions))
        symbol_pos = list(filter(lambda p: p.symbol == symbol_name, pos))

        if(len(pos) >= max_positions_total):
            result = True
            if(debug):
                if entry_variable in Entry:
                    print(
                        f"Max Orders Reached for this portoflio, no new order will be executed")

        elif len(symbol_pos) >= max_position_per_symbol:
            result = True
            if(debug):
                if entry_variable in Entry:
                    print(
                        f"Max Symbol Order Reached for symbol {symbol_name}, no new order will be executed")

        return(result)

    def modify_sl(self, ticket_id: int, SL: Union[int, float] = None) -> TradePosition:
        """
        modify sl for an already executed order
        """
        exc = self.exchange

        position = exc.get_position_with_ticket_id(ticket_id)
        symbol = Symbol(position.symbol, TIMEFRAME_M1, terminal=self.TERMINAL)

        if position.type == ORDER_TYPE.SELL:
            if isinstance(SL, int):
                stoploss = symbol.normalize_price(max(position.price_open, symbol.ask)+(SL *
                                                                                        symbol.p_value*symbol.point))
                stoploss = self.adjust_above_stop_level(
                    symbol, stoploss)
        if position.type == ORDER_TYPE.BUY:
            if isinstance(SL, int):
                SL = symbol.normalize_price(min(position.price_open, symbol.bid)-(SL *
                                                                                  symbol.p_value*symbol.point))
                SL = self.adjust_below_stop_level(symbol, SL)

        result = exc.modify_sl(stop_loss=SL, position=position)
        # ! checking if the retcode is done
        print(
            "Modify SL Result, ", result.comment)
        pos = exc.get_position_from_order_send_result(result)
        return pos

    def modify_tp(self, ticket_id: int, TP: Union[int, float] = None) -> TradePosition:
        """
        modify tp for an already executed order
        """
        exc = self.exchange

        position = exc.get_position_with_ticket_id(ticket_id)
        symbol = Symbol(position.symbol, TIMEFRAME_M1, terminal=self.TERMINAL)
        if position.type == mt5.ORDER_TYPE.SELL:
            if isinstance(TP, int):
                TP = symbol.bid - (TP * symbol.trade_tick_size)
            TP = self.adjust_below_stop_level(symbol, TP)
        if position.type == mt5.ORDER_TYPE.BUY:
            if isinstance(TP, int):
                TP = symbol.ask + (TP * symbol.trade_tick_size)
            TP = self.adjust_above_stop_level(symbol, TP)

        result = exc.modify_tp(take_profit=TP, position=position)
        # ! checking if the retcode is done
        print(
            "Modify TP Result, ", result.comment)
        pos = exc.get_position_from_order_send_result(result)
        return pos

    def adjust_below_stop_level(self, symbol: Symbol, stop_price: float, points=0):
        """
        adjust price below stop level
        """
        current_price = symbol.bid
        point = symbol.point
        # ! minimum stop loss required by the broker, don't have to apply p_value here
        stop_level = symbol.trade_stops_level * point
        calc_stop_price = current_price - stop_level
        add_points = points * point
        if stop_price < calc_stop_price - add_points:
            return stop_price
        else:
            new_price = calc_stop_price - add_points
            # print('Price adjusted below stop level to ', new_price)
            return new_price

    def adjust_above_stop_level(self, symbol: Symbol, stop_price, points=0):
        """
        adjust price above stop level
        """
        current_price = symbol.bid
        point = symbol.point
        # ! minimum stop loss required by the broker, don't have to apply p_value here
        stop_level = symbol.trade_stops_level * point
        calc_stop_price = current_price + stop_level
        add_points = points * point
        if stop_price > calc_stop_price + add_points:
            return stop_price
        else:
            new_price = calc_stop_price + add_points
            # print('Price adjusted above stop level to ', new_price)
            return new_price

    async def set_break_even_stop(self, ticket_id, min_profit_pip=0, lock_profit=0, break_even_close_half: bool = False):
        """
        Set break even stop for an order
        """
        exc = self.exchange

        assert min_profit_pip != 0, "minimum profit should be more than 0"

        result = exc.get_position_with_ticket_id(ticket_id)
        set_break_even_stop = False
        break_even_stop = 0

        # ! order and symbol information
        order_type = result.type
        order_symbol = result.symbol
        symbol = Symbol(order_symbol, TIMEFRAME_M1, terminal=self.TERMINAL)
        order_stop_loss = result.sl
        order_take_profit = result.tp
        order_open_price = result.price_open

        # ! only taking the p value

        # ! convert pips to prices
        min_profit = min_profit_pip * symbol.point * symbol.p_value

        lock_profit_val = 0
        if lock_profit > 0:
            lock_profit_val = lock_profit * symbol.point * symbol.p_value

        if order_type == ORDER_TYPE.BUY:
            break_even_stop = order_open_price + lock_profit_val
            break_even_stop = symbol.normalize_price(break_even_stop)
            # current_profit = exc.calc_order_profit(
            #     order_type, symbol.name, result.volume, order_open_price, symbol.bid)
            current_profit_pip = symbol.bid - order_open_price
            current_profit_pip = symbol.normalize_price(current_profit_pip)

            order_stop_loss = symbol.normalize_price(order_stop_loss)

            if break_even_stop > order_stop_loss and current_profit_pip >= min_profit:
                set_break_even_stop = True

        elif order_type == ORDER_TYPE.SELL:
            break_even_stop = order_open_price - lock_profit_val
            break_even_stop = symbol.normalize_price(break_even_stop)
            # current_profit = exc.calc_order_profit(
            #     order_type, symbol.name, result.volume, order_open_price, symbol.ask)
            current_profit_pip = order_open_price - symbol.ask
            current_profit_pip = symbol.normalize_price(current_profit_pip)

            order_stop_loss = symbol.normalize_price(order_stop_loss)
            if (break_even_stop < order_stop_loss or order_stop_loss == 0) and current_profit_pip >= min_profit:
                set_break_even_stop = True
        # ! set trailing step
        if set_break_even_stop:
            assert break_even_stop != 0, 'For some reason trail stop price haven\'t changed'
            result = exc.modify_sl(stop_loss=break_even_stop, position=result)

            # ! checking if the retcode is done
            assert result.retcode == mt5.TRADE_RETCODE.DONE
            pos = exc.get_position_from_order_send_result(result)
            # ! closing half of the trade on breakeven
            if break_even_close_half:
                half_vol = pos.volume * .5
                corrected_volume = symbol.verify_volume(
                    half_vol)
                if corrected_volume != pos.volume:
                    # ! we are not in the lowest volume closing half volume is possible
                    await self.close_position_volume(pos, corrected_volume)
                    self.CLOSE_HALF_PORTION = True
                else:
                    print(
                        f"We are in a lowest possible volume closing half volume is not possible for {symbol.name}")

    def set_break_even_stop_all(self, symbol: Symbol, min_profit, lock_profit=0):
        exc = self.exchange
        # magic = self.magic_number

        positions = exc.get_position_with_magic(self.magic_number)
        symbol_pos = list(filter(lambda p: p.symbol == symbol.name, positions))
        for position in symbol_pos:
            order_type = position.type
            if(order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL):
                self.set_break_even_stop(
                    position.ticket, min_profit, lock_profit)

    def is_loss_limit_breached(self, loss_limit_activated: bool, loss_limit_percentage: float, debug: bool, entry_signal_trigger: Union[int, Entry]):
        """
        This function determines if our maximum loss threshold is breached
        """
        initial_capital = self.exchange.get_current_capital(use_balance=True)
        if(loss_limit_activated == False):
            return(self.output)

        if(self.FirstTick == True):
            self.InitialCapital = initial_capital
            self.FirstTick = False

        profitAndLoss = (initial_capital/self.InitialCapital)-1

        if(profitAndLoss < -loss_limit_percentage/100):
            self.output = True
            profitAndLossPrint = round(profitAndLoss, 4)*100
            if(debug):
                if(entry_signal_trigger in Entry):
                    print("Entry trade triggered but not executed. Loss threshold breached. Current Loss: " +
                          str(profitAndLossPrint) + "%")

        return(self.output)

    def set_trailing_stop_all_price(self, symbol: Symbol, price, min_profit=0, step=10):
        """
        set trailing stop for all open order with price
        """
        exc = self.exchange
        magic = self.magic_number

        total_positions = exc.get_position_with_magic(self.magic_number)
        symbol_pos = list(filter(lambda p: p.symbol ==
                                 symbol.name, total_positions))
        for position in symbol_pos:
            order_type = position.type
            magic_number = position.magic
            if(magic_number == magic and (order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL)):
                self.set_trailing_stop_by_price(
                    position.ticket, price, min_profit, step)

    def set_vol_trailing_stop_all_price(self, symbol: Symbol, vol_value: float, min_profit: int = 0, step=10):
        """
        set trailing stop for all open order with price
        """
        exc = self.exchange
        magic = self.magic_number

        total_positions = exc.get_position_with_magic(self.magic_number)
        symbol_pos = list(filter(lambda p: p.symbol ==
                                 symbol.name, total_positions))
        for position in symbol_pos:
            order_type = position.type
            magic_number = position.magic
            if(magic_number == magic and (order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL)):
                if order_type == ORDER_TYPE.BUY:
                    price = symbol.bid - vol_value
                    self.set_trailing_stop_by_price(
                        position.ticket, price, min_profit, step)
                elif order_type == ORDER_TYPE.SELL:
                    price = symbol.ask + vol_value
                    self.set_trailing_stop_by_price(
                        position.ticket, price, min_profit, step)

    def set_trailing_stop_by_price(self, ticket_id, trail_price, min_profit, step=10):
        """
        Trailing stop price
        """
        exc = self.exchange
        magic = self.magic_number

        assert trail_price != 0 or trail_price != None, 'You must define trail price'
        set_trailing_stop = False

        result = exc.get_position_with_ticket_id(ticket_id)
        order_type = result.type
        order_symbol = result.symbol
        symbol = Symbol(order_symbol, TIMEFRAME_M1, terminal=self.TERMINAL)
        order_stop_loss = result.sl
        if order_stop_loss == 0:
            hidden_sl_list = self.HiddenSLList
            x = 0
            while x < len(hidden_sl_list):
                #  Looping through all order number in list
                orderTicketNumber = hidden_sl_list[x][0]
                orderSL = hidden_sl_list[x][1]
                if orderTicketNumber == ticket_id:
                    print(
                        'YOU SHOULDN\'T USE HIDDEN SL WITH TRAIL STOP POINT, EITHER USE BOTH HIDDEN OR BOTH REVEALED')
                    if order_type == ORDER_TYPE.BUY:
                        order_stop_loss = result.price_open - \
                            (orderSL * symbol.p_value * symbol.point)
                        break
                    elif order_type == ORDER_TYPE.SELL:
                        order_stop_loss = result.price_open + \
                            (orderSL * symbol.p_value * symbol.point)
                        break
                x = +1

        order_take_profit = result.tp
        order_open_price = result.price_open

        min_profit = min_profit * symbol.point*symbol.p_value
        step_value = step * symbol.point * symbol.p_value
        # if step < 10:
        #     step_value = 10 * symbol.point * symbol.p_value
        if order_type == ORDER_TYPE.BUY:
            trail_price = self.adjust_below_stop_level(symbol,
                                                       trail_price)

            # current_profit = exc.calc_order_profit(
            #     order_type, symbol.name, result.volume, order_open_price, symbol.bid)
            current_profit_pip = symbol.bid - order_open_price
            current_profit_pip = symbol.normalize_price(current_profit_pip)
            if trail_price > (order_stop_loss+step_value) and current_profit_pip >= min_profit:
                set_trailing_stop = True

        elif order_type == ORDER_TYPE.SELL:
            trail_price = self.adjust_above_stop_level(symbol,
                                                       trail_price)
            # current_profit = exc.calc_order_profit(
            #     order_type, symbol.name, result.volume, order_open_price, symbol.ask)
            current_profit_pip = order_open_price - symbol.ask
            current_profit_pip = symbol.normalize_price(current_profit_pip)
            if trail_price < (order_stop_loss-step_value or order_stop_loss == 0) and current_profit_pip >= min_profit:
                set_trailing_stop = True

        # ! set trailing step
        if set_trailing_stop:
            assert trail_price != 0, 'For some reason trail stop price haven\'t changed'
            pos = exc.modify_sl(stop_loss=trail_price, position=result)

            # ! checking if the retcode is done
            assert pos.retcode == mt5.TRADE_RETCODE.DONE, 'Trail Stop Setting In MT5 Caused some problem.'
            print(
                f"Trail Stop Updated for {pos.request.symbol}, to {trail_price}")

    def set_trailing_stop_all_point(self, symbol: Symbol, trail_points: int, min_profit: int, step=10):
        """
        set trailing stop for all open order with points
        """
        exc = self.exchange
        magic = self.magic_number
        total_positions = exc.get_position_with_magic(self.magic_number)
        symbol_pos = list(filter(lambda p: p.symbol ==
                                 symbol.name, total_positions))

        for position in symbol_pos:
            order_type = position.type
            magic_number = position.magic
            if(order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL):
                self.set_trailing_stop_by_point(
                    position.ticket, trail_points, min_profit, step)

    def set_trailing_stop_by_point(self, ticket_id, trail_points, min_profit, step=10):
        """
        set trailing stop with points
        """
        exc = self.exchange
        magic = self.magic_number

        assert trail_points != 0, 'vai set jokhon korbi to 0 disos kela'
        # ! initially kept set_trailing_stop to be false, and trail stop price to 0
        set_trailing_stop = False
        trail_stop_price = 0
        result = exc.get_position_with_ticket_id(ticket_id)
        order_type = result.type
        order_symbol = result.symbol
        symbol = Symbol(order_symbol, TIMEFRAME_M1, terminal=self.TERMINAL)
        order_stop_loss = result.sl
        if order_stop_loss == 0:
            hidden_sl_list = self.HiddenSLList
            x = 0
            while x < len(hidden_sl_list):
                #  Looping through all order number in list
                print(
                    'YOU SHOULDN\'T USE HIDDEN SL WITH TRAIL STOP POINT, EITHER USE BOTH HIDDEN OR BOTH REVEALED')
                doesOrderExist = False
                orderTicketNumber = hidden_sl_list[x][0]
                orderSL = hidden_sl_list[x][1]
                if orderTicketNumber == ticket_id:
                    if order_type == ORDER_TYPE.BUY:
                        order_stop_loss = result.price_open - \
                            (orderSL * symbol.p_value * symbol.point)
                        break
                    elif order_type == ORDER_TYPE.SELL:
                        order_stop_loss = result.price_open + \
                            (orderSL * symbol.p_value * symbol.point)
                        break
                x += 1
        order_take_profit = result.tp
        order_open_price = result.price_open

        # ! convert inputs to prices
        trail_points = trail_points * symbol.point * symbol.p_value
        min_profit = min_profit * symbol.point * symbol.p_value

        step_value = step * symbol.point * symbol.p_value

        # if step < 10:
        #     step_value = 10 * symbol.point * symbol.p_value

        if order_type == ORDER_TYPE.BUY:
            trail_stop_price = symbol.bid - trail_points
            trail_stop_price = symbol.normalize_price(trail_stop_price)

            # current_profit_pip = exc.calc_order_profit(
            #     order_type, symbol.name, result.volume, order_open_price, symbol.bid)
            current_profit_pip = symbol.bid - order_open_price
            current_profit_pip = symbol.normalize_price(current_profit_pip)
            if trail_stop_price > order_stop_loss+step_value and current_profit_pip >= min_profit:
                set_trailing_stop = True

        elif order_type == ORDER_TYPE.SELL:
            trail_stop_price = symbol.ask + trail_points
            trail_stop_price = symbol.normalize_price(trail_stop_price)
            # current_profit_pip = exc.calc_order_profit(
            #     order_type, symbol.name, result.volume, order_open_price, symbol.ask)
            current_profit_pip = order_open_price - symbol.ask
            current_profit_pip = symbol.normalize_price(current_profit_pip)
            if (trail_stop_price < order_stop_loss-step_value or order_stop_loss == 0) and current_profit_pip >= min_profit:
                set_trailing_stop = True

        if set_trailing_stop:
            assert trail_stop_price != 0, 'For some reason trail stop price haven\'t changed'
            pos = exc.modify_sl(stop_loss=trail_stop_price, position=result)

            # ! checking if the retcode is done
            assert pos.retcode == mt5.TRADE_RETCODE.DONE, 'Trail Stop Setting In MT5 Caused some problem.'
            print(
                f"Trail Stop Updated for {pos.request.symbol}, to {trail_stop_price}")

    # +------------------------------------------------------------------+
    # * (START) Set Hidden Stop Loss
    # +------------------------------------------------------------------+

    def set_stop_loss_hidden(self, debug: bool, SL: float, OrderNum: int, insert_hidden_sl_db: Callable):
        """
            insert_hidden_sl_db # this function should called db to insert the df
            This function calculates hidden stop loss amount and tags it to the appropriate order using an array
        """
        insert_hidden_sl_db(OrderNum, SL)
        if (debug):
            print(
                f"EA Debug: Order {str(OrderNum)} assigned with a hidden SL at {str(SL)}")

    # +------------------------------------------------------------------+
    #  * (END) Set Hidden Stop Loss
    #  +------------------------------------------------------------------+

    # +------------------------------------------------------------------+
    #  * (START) Set Hidden Take Profit
    # +------------------------------------------------------------------+
    def set_take_profit_hidden(self, debug: bool, TP: float, OrderNum: int, insert_hidden_tp_db: Callable):
        """
        insert_hidden_tp_db # this function should called db to insert the df
        This function calculates hidden take profit amount and tags it to the appropriate order using an array
        """
        insert_hidden_tp_db(OrderNum, TP)
        if (debug):
            print(
                f"EA Debug: Order {str(OrderNum)} assigned with a hidden tp at {str(TP)}")
    # +------------------------------------------------------------------+
    #  * (END) End of Set Hidden Take Profit
    # +------------------------------------------------------------------+

    # +------------------------------------------------------------------+
    #  * (START) Trigger Hidden Stop Loss
    # +------------------------------------------------------------------+
    async def trigger_stop_loss_hidden(self, debug: bool, symbol: Symbol, ticket: int, hidden_sl_df: pd.DataFrame):
        """
            hidden_sl_df = get_hidden_sl_db() # this function should called db to collect the df
            # This funciton is for Live Trading Only
            # This function does two 2 things:
            >>> 1) Clears appropriate elements of your HiddenSLList if positions has been closed
            >>> 2) Closes positions based on its hidden stop loss levels

        """
        exc = self.exchange
        pos = exc.get_position_with_ticket_id(ticket)
        # length = len(hidden_sl_list)
        hidden_sl_df = hidden_sl_df[hidden_sl_df['order_id'] == ticket]
        if pos and len(hidden_sl_df.index) != 0:
            hidden_sl = hidden_sl_df['stop_loss'].iloc[0]
            if pos.type == POSITION_TYPE.BUY and hidden_sl >= symbol.bid:
                close = True
            elif pos.type == POSITION_TYPE.SELL and hidden_sl <= symbol.ask:
                close = True
            else:
                close = False

            if close:
                if(debug):
                    print("EA Debug: Stop Loss hidden hit Trying to close position " +
                          str(ticket)+" ...")
                # HandleTradingEnvironment(debug, Retry_Interval);
                closing = await self.close_position(pos)
                # closing = OrderClose(
                #     OrderTicket(), OrderLots(), Bid, Slip*K, Blue);
                if(debug and not closing):
                    print(
                        "EA Debug: Unexpected Error has happened. While closing the order")
                elif(debug and closing):
                    print("EA Debug: Position successfully closed.")
    #  +------------------------------------------------------------------+
    #  * End of Trigger Hidden Stop Loss
    #  +------------------------------------------------------------------+

    # +------------------------------------------------------------------+
    #  * Trigger Hidden Take Profit
    # +------------------------------------------------------------------+

    async def trigger_take_profit_hidden(self, debug: bool, symbol: Symbol, ticket: int, hidden_tp_df: pd.DataFrame):
        """
        hidden_tp_df = get_hidden_tp_db() # this function should called db to collect the df
        # This function does two 2 things:
        >>> 1) Clears appropriate elements of your HiddenTPList if positions has been closed
        >>> 2) Closes positions based on its hidden take profit levels
        """
        exc = self.exchange
        pos = exc.get_position_with_ticket_id(ticket)

        hidden_tp_df = hidden_tp_df[hidden_tp_df['order_id'] == ticket]
        if pos and len(hidden_tp_df.index) != 0:
            take_profit = hidden_tp_df['take_prft'].iloc[0]
            if pos.type == POSITION_TYPE.BUY and take_profit <= symbol.bid:
                close = True
            elif pos.type == POSITION_TYPE.SELL and take_profit >= symbol.ask:
                close = True
            else:
                close = False

            if close:
                if(debug):
                    print("EA Debug: Take profit hidden hit, Trying to close position " +
                          str(ticket)+" ...")
                # HandleTradingEnvironment(debug, Retry_Interval);
                closing = await self.close_position(pos)
                # closing = OrderClose(
                #     OrderTicket(), OrderLots(), Bid, Slip*K, Blue);
                if(debug and not closing):
                    print(
                        "EA Debug: Unexpected Error has happened. While closing the order")
                elif(debug and closing):
                    print("EA Debug: Position successfully closed.")
    #  +------------------------------------------------------------------+
    #  * End of Trigger Hidden Take Profit
    #  +------------------------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Volatility-Based Stop Loss
    # -----------------------------------------------------+
    def vol_based_stop_loss(self, isVolatilitySwitchOn: bool, fixedStop: int, volATR: float, volMultiplier: float) -> float:
        """
        Volatility-Based Stop Loss
        """
        if not isVolatilitySwitchOn:
            # ! If Volatility Stop Loss not activated. Stop Loss = Fixed Pips Stop Loss
            StopL = fixedStop
        else:
            # ! Stop Loss in Pips (better to send as decicmal points like I did, DON'T CHANGE)
            # StopL = volMultiplier*volATR/(digits*symobol_point)
            StopL = volMultiplier*volATR
        return (StopL)
    # -----------------------------------------------------+
    # * (END) Volatility-Based Stop Loss
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Volatility-Based Take Profit
    # -----------------------------------------------------+

    def vol_based_take_profit(self, isVolatilitySwitchOn: bool, fixedTP: int, volATR: float, volMultiplier: float):
        """
        Volatility-Based Take Profit
        """
        if not isVolatilitySwitchOn:
            TakeP = fixedTP
            # ! If Volatility Take Profit not activated. Take Profit = Fixed Pips Take Profit
        else:
            # ! Take Profit in Pips (better to send as decicmal points like I did, DON'T CHANGE)
            # TakeP = volMultiplier*volATR/(digits*symobol_point)
            TakeP = volMultiplier*volATR
            # ! Take Profit in Pips

        return(TakeP)

    # -----------------------------------------------------+
    # * (END)  Volatility-Based Take Profit
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Update Hidden Trailing List
    # -----------------------------------------------------+
    def update_hidden_trailing_list(self):
        """
        This function clears the elements of your HiddenTrailingList if the corresponding positions has been closed
        """
        hidden_trail_list = self.HiddenTrailingList
        exc = self.exchange

        # ! THIS CODE BLOCK HERE NEED'S TO BE TESTED
        x = 0
        while x < len(hidden_trail_list):
            doesPosExist = False
            orderTicketNumber = hidden_trail_list[x][0]

            if orderTicketNumber != 0:
                pos = exc.get_position_with_ticket_id(orderTicketNumber)

                if pos:
                    doesPosExist = True
                    # break
            if not doesPosExist:
                # ! Deletes elements if the order number does not match any current positions
                del hidden_trail_list[x]
                x = 0 if x == 0 else x - 1
                continue
            x += 1

    # -----------------------------------------------------+
    # * (END)  Update Hidden Trailing List
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Set and Trigger Hidden Trailing
    # -----------------------------------------------------+

    async def set_and_trigger_hidden_trailing(self, debug: bool, symbol: Symbol, ticket_id, trail_in_point: bool, trail_point_price: Union[int, float], min_profit: int, hidden_sl_df: pd.DataFrame, hidden_trl_sl_df: pd.DataFrame, insert_updt_hidden_trl_sl_db: Callable, step=10):
        """
        hidden_sl_df = get_hidden_sl_db() # this function should called db to collect the df
        hidden_trl_sl_df = get_hidden_trl_sl_db() # this function should called db to collect the df
        insert_updt_hidden_trl_sl_db  # this function should called db to insert the df
        # This function does 2 things.
        >>> 1) It sets hidden trailing stops for all positions
        >>> 2) It closes the positions if hidden trailing stops levels are breached
        """
        exc = self.exchange
        pos = exc.get_position_with_ticket_id(ticket_id)

        min_profit = min_profit * symbol.point * symbol.p_value
        step_value = step * symbol.point * symbol.p_value
        hidden_trl_sl_exist = hidden_trl_sl_df[hidden_trl_sl_df['order_id']
                                               == pos.ticket]

        if pos:
            if len(hidden_trl_sl_exist.index) > 0:

                # if hidden_trail_list[x][0] == pos.ticket:
                tl_sl = hidden_trl_sl_exist['hidden_traili_sl'].iloc[0]
                # trail_points = tl_sl * symbol.point * symbol.p_value
                close = False
                if pos.type == POSITION_TYPE.BUY and tl_sl >= symbol.bid:
                    close = True
                elif pos.type == POSITION_TYPE.SELL and tl_sl <= symbol.ask:
                    close = True

                if close:
                    if(debug):
                        print("EA Debug: Trailing Stop hit, Trying to close position " +
                              str(pos.ticket)+" ...")
                    # HandleTradingEnvironment(debug, Retry_Interval);
                    closing = await self.close_position(pos)
                    # closing = OrderClose(
                    #     OrderTicket(), OrderLots(), Bid, Slip*K, Blue);
                    if(debug and not closing):
                        print(
                            "EA Debug: Unexpected Error has happened. While closing the order")
                    elif(debug and closing):
                        print("EA Debug: Position successfully closed.")

                    # break
                else:
                    # ! Step 2: If there are hidden trailing stop records and the position was not closed in Step 1. We update the hidden trailing stop record.
                    if pos.type == ORDER_TYPE.BUY:
                        if trail_in_point:
                            trail_stop_price = symbol.bid - trail_point_price
                            trail_stop_price = symbol.normalize_price(
                                trail_stop_price)
                        else:
                            trail_stop_price = symbol.normalize_price(
                                trail_point_price)

                        # current_profit_pip = exc.calc_order_profit(
                        #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.bid)
                        current_profit_pip = symbol.bid - pos.price_open
                        current_profit_pip = symbol.normalize_price(
                            current_profit_pip)
                        if trail_stop_price > tl_sl+step_value and current_profit_pip >= min_profit:
                            if debug:
                                print(
                                    f"Trailing stop updated for position {str(pos.ticket)} in  {str(trail_stop_price)}:")
                            insert_updt_hidden_trl_sl_db(
                                pos.ticket, trail_stop_price)
                    elif pos.type == ORDER_TYPE.SELL:
                        if trail_in_point:
                            trail_stop_price = symbol.ask + trail_point_price
                            trail_stop_price = symbol.normalize_price(
                                trail_stop_price)
                        else:
                            trail_stop_price = symbol.normalize_price(
                                trail_point_price)
                        # current_profit_pip = exc.calc_order_profit(
                        #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.ask)
                        current_profit_pip = pos.price_open - symbol.ask
                        current_profit_pip = symbol.normalize_price(
                            current_profit_pip)
                        if trail_stop_price < tl_sl-step_value and current_profit_pip >= min_profit:
                            print(
                                f"Trailing stop updated for position {str(pos.ticket)} in  {str(trail_stop_price)}:")
                            insert_updt_hidden_trl_sl_db(
                                pos.ticket, trail_stop_price)

            # ! Step 3: If there are no hidden trailing stop records, add new record.
            else:
                # Slot is empty
                order_stop_loss = pos.sl
                if order_stop_loss == 0:
                    pos_sl_db = hidden_sl_df[hidden_sl_df['order_id']
                                             == pos.ticket]
                    if pos_sl_db.index > 0:
                        order_stop_loss = pos_sl_db['stop_loss'].iloc[0]

                if pos.type == ORDER_TYPE.BUY:
                    if trail_in_point:
                        # ! if the trail is in point
                        trail_stop_price = symbol.bid - trail_point_price
                        trail_stop_price = symbol.normalize_price(
                            trail_point_price)
                    else:
                        # ! if the trail is in price
                        trail_stop_price = symbol.normalize_price(
                            trail_point_price)
                    # current_profit_pip = exc.calc_order_profit(
                    #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.bid)
                    current_profit_pip = symbol.bid - pos.price_open
                    current_profit_pip = symbol.normalize_price(
                        current_profit_pip)
                    # ! as we don't have any prior sl if our min_profit is achived we will set trail_stop_price as our trail stop
                    if trail_stop_price > (order_stop_loss+step_value) and current_profit_pip >= min_profit:
                        # ! inserting the trail stop loss to db
                        print(
                            f"Trailing stop activated for position {str(pos.ticket)} in  {str(trail_stop_price)}:")
                        insert_updt_hidden_trl_sl_db(
                            pos.ticket, trail_stop_price)

                elif pos.type == ORDER_TYPE.SELL:
                    if trail_in_point:
                        trail_stop_price = symbol.ask + trail_point_price
                        trail_stop_price = symbol.normalize_price(
                            trail_point_price)
                    else:
                        trail_stop_price = symbol.normalize_price(
                            trail_point_price)
                    # current_profit_pip = exc.calc_order_profit(
                    #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.ask)
                    current_profit_pip = pos.price_open - symbol.ask
                    current_profit_pip = symbol.normalize_price(
                        current_profit_pip)
                    # ! as we don't have any prior sl if our min_profit is achived we will set trail_stop_price as our trail stop
                    if trail_stop_price < (order_stop_loss-step_value or order_stop_loss == 0) and current_profit_pip >= min_profit:
                        print(
                            f"Trailing stop activated for position {str(pos.ticket)} in  {str(trail_stop_price)}:")
                        insert_updt_hidden_trl_sl_db(
                            pos.ticket, trail_stop_price)

        else:
            print(f"Position already closed for ticket: {ticket_id}")
    # -----------------------------------------------------+
    # * (END)  Set and Trigger Hidden Trailing
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START) Update And Review Vol Trailing List (NO NEED FOR THIS SECTION AS IT'S HANDLED IN trailing stop point)
    # -----------------------------------------------------+

    # def update_vol_trailing_list(self, vol_trail_multp: int, min_profit: int, step: int = 10):
    #     """
    #     Updates The List of vol trailing list, with a volatility
    #     """
    #     magic = self.magic_number
    #     vol_trail_list = self.VolTrailingList
    #     exc = self.exchange

    #     # ! THIS CODE BLOCK HERE NEED'S TO BE TESTED
    #     x = 0
    #     while x < len(vol_trail_list):
    #         doesPosExist = False
    #         orderTicketNumber = vol_trail_list[x][ 0]

    #         if orderTicketNumber != 0:
    #             pos = exc.get_position_with_ticket_id(orderTicketNumber)

    #             if pos:
    #                 symbol = Symbol(pos.symbol, TIMEFRAME_M1,terminal=self.TERMINAL)
    #                 doesPosExist = True
    #                 vol_trail_point = vol_trail_multp*vol_trail_list[x][ 1] / \
    #                     (symbol.p_value *
    #                      symbol.point)  # Volatility trailing stop amount in Pips
    #                 order_type = pos.type
    #                 magic_number = pos.magic
    #                 if(magic_number == magic and (order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL)):
    #                     self.set_trailing_stop_by_point(
    #                         pos.ticket, vol_trail_point, min_profit, step)

    #                 # break
    #         if not doesPosExist:
    #             # ! Deletes elements if the order number does not match any current positions
    #             vol_trail_list[x][ 0] = 0
    #             vol_trail_list[x][ 1] = 0

    # -----------------------------------------------------+
    # * (END) Update Vol Trailing List
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Set Volatility Trailing Stop
    # -----------------------------------------------------+

    # def set_vol_trailing_stop(self, volATR: float, vol_trail_multp,  min_profit: int, step: int = 10):
    #     """
    #     set trailing stop for all open order with points
    #     """
    #     vol_trail_list = self.VolTrailingList
    #     exc = self.exchange
    #     magic = self.magic_number

    #     IsVolTrailingStopAdded = False
    #     total_positions = exc.get_position_with_magic(magic)
    #     for position in total_positions:
    #         symbol = Symbol(position.symbol, TIMEFRAME_M1,terminal=self.TERMINAL)
    #         vol_trail_point = vol_trail_multp*volATR / \
    #             (symbol.p_value*symbol.point)  # Volatility trailing stop amount in Pips
    #         order_type = position.type
    #         magic_number = position.magic
    #         if(magic_number == magic and (order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL)):
    #             self.set_trailing_stop_by_point(
    #                 position.ticket, vol_trail_point, min_profit, step)
    #             IsVolTrailingStopAdded = True

    #         if IsVolTrailingStopAdded:
    #             for z in range(len(vol_trail_list)+1):
    #                 if vol_trail_list[z][ 0] == 0:
    #                     #  Checks if the element is empty
    #                     vol_trail_list[z][ 0] == position.ticket
    #                     # ! we are only keeping the volATR which was at the time of opening the trdae
    #                     vol_trail_list[z][ 1] == volATR / \
    #                         (symbol.p_value *
    #                          symbol.point)  # Volatility trailing stop amount in Pips
    #                     # ! break from this loop only
    #                     break

    # -----------------------------------------------------+
    # * (END)  Set Volatility Trailing Stop
    # -----------------------------------------------------+

    # +------------------------------------------------------------------+
    #  * (START) Update Hidden Breakeven Stops List
    # +------------------------------------------------------------------+
    def update_hidden_BE_list(self):
        """
        This function clears the elements of your HiddenBEList if the corresponding positions has been closed
        """
        hidden_be_list = self.HiddenBEList
        exc = self.exc
        x = 0
        while x < len(hidden_be_list):
            doesPosExist = False
            orderTicketNumber = hidden_be_list[x]
            if(orderTicketNumber != 0):
                #  Order exists
                pos = exc.get_position_with_ticket_id(
                    orderTicketNumber)

                if pos:
                    doesPosExist = True
                    break
            if(doesPosExist == False):
                # ! Deletes elements if the order number does not match any current positions
                del hidden_be_list[x]
                x = 0 if x == 0 else x - 1
                continue

            x += 1

    #  +------------------------------------------------------------------+
    #  * (End) Update Hidden Breakeven Stops List
    #  +------------------------------------------------------------------+

    # +------------------------------------------------------------------+
    #  * (START) Set and Trigger Hidden Breakeven Stops
    # +------------------------------------------------------------------+
    async def set_and_trigger_BE_hidden(self, debug: bool, symbol: Symbol, ticket: int, min_profit_pip: int, lock_profit: int, be_hdn_df: pd.DataFrame, hidden_sl_df: pd.DataFrame, insert_hidden_be_sl_db: Callable):
        """
        hidden_sl_df = get_hidden_sl_db() # this function should called db to collect the df
        be_hdn_df = get_hidden_be_db() # this function should called db to collect the df
        insert_hidden_be_sl_db  # this function should called db to insert the df
        This function scans through the current positions and does 2 things:
        1) If the position is in the hidden breakeven list, it closes it if the appropriate conditions are met
        2) If the positon != the hidden breakeven list, it adds it to the list if the appropriate conditions are met
        """
        exc = self.exchange
        pos = exc.get_position_with_ticket_id(ticket)
        be_hdn_df = be_hdn_df[be_hdn_df['order_id'] == ticket]
        if pos:
            if len(be_hdn_df.index) != 0:
                be_hidden = be_hdn_df['break_even_stop'].iloc[0]
                if pos.type == POSITION_TYPE.BUY and be_hidden <= symbol.bid:
                    # ! price came down and bid is equal to price open so close the position
                    close = True
                elif pos.type == POSITION_TYPE.SELL and be_hidden >= symbol.ask:
                    # ! price gone up and ask is equal to price open so close the position
                    close = True

                if close:
                    if(debug):
                        print("EA Debug:Break Even Stop hit, Trying to close position " +
                              str(pos.ticket)+" ...")
                    # HandleTradingEnvironment(debug, Retry_Interval);
                    closing = await self.close_position(pos)
                    # closing = OrderClose(
                    #     OrderTicket(), OrderLots(), Bid, Slip*K, Blue);
                    if(debug and not closing):
                        print(
                            "EA Debug: Unexpected Error has happened. While closing the order")
                    elif(debug and closing):
                        print("EA Debug: Position successfully closed.")
            else:
                min_profit = min_profit_pip * symbol.point * symbol.p_value

                lock_profit_val = 0
                if lock_profit > 0:
                    lock_profit_val = lock_profit * symbol.point * symbol.p_value

                order_stop_loss = pos.sl
                if order_stop_loss == 0:
                    pos_sl_db = hidden_sl_df[hidden_sl_df['order_id']
                                             == pos.ticket]
                    order_stop_loss = pos_sl_db['stop_loss']

                if pos.type == POSITION_TYPE.BUY:
                    break_even_stop = pos.price_open + lock_profit_val
                    if break_even_stop > order_stop_loss and (symbol.bid - pos.price_open) > min_profit:
                        add_be = True
                elif pos.type == POSITION_TYPE.SELL:
                    break_even_stop = pos.price_open - lock_profit_val
                    if break_even_stop > order_stop_loss and (pos.price_open - symbol.ask) > min_profit:
                        add_be = True
                else:
                    add_be = False

                if add_be:
                    insert_hidden_be_sl_db(pos.ticket, break_even_stop)
                    if(debug):
                        print("EA debug: Order "+str(pos.ticket) +
                              " assigned with a hidden breakeven stop.")
        else:
            print(f"Position already closed for ticket: ", ticket)
    #  +------------------------------------------------------------------+
    #  * (END) Set and Trigger Hidden Breakeven Stops
    #  +------------------------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Update Hidden Volatility Trailing List
    # -----------------------------------------------------+

    def update_hidden_vol_trailing_list(self):
        """
        This function clears the elements of your HiddenVolTrailingList if the corresponding positions has been closed
        """
        hidden_vol_trail_list = self.HiddenVolTrailingList
        exc = self.exchange

        # ! THIS CODE BLOCK HERE NEED'S TO BE TESTED
        x = 0
        while x < len(hidden_vol_trail_list):
            doesPosExist = False
            orderTicketNumber = hidden_vol_trail_list[x][0]

            if orderTicketNumber != 0:
                pos = exc.get_position_with_ticket_id(orderTicketNumber)

                if pos:
                    doesPosExist = True
                    # break
            if not doesPosExist:
                # ! Deletes elements if the order number does not match any current positions
                del hidden_vol_trail_list[x]
                x = 0 if x == 0 else x - 1
                continue
            x += 1

    # -----------------------------------------------------+
    # * (END) Update Hidden Volatility Trailing List
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  Set Trigger Review Hidden Vol Trailing
    # -----------------------------------------------------+

    async def set_trigger_review_hidden_vol_trailing(self, debug: bool, symbol: Symbol, volATR: float, vol_trail_multp: int,  min_profit: int, step: int = 10):
        """
        # This function does 2 things.
        >>> 1) It sets hidden trailing stops for all positions
        >>> 2) It closes the positions if hidden trailing stops levels are breached
        """
        magic = self.magic_number
        doesHiddenVolTrailingRecordExist = False
        hidden_Vol_trail_list = self.HiddenVolTrailingList
        exc = self.exchange
        positions = exc.get_position_with_magic(magic)
        symbol_pos = list(filter(lambda p: p.symbol == symbol.name, positions))

        for pos in symbol_pos:
            x = 0
            while x < len(hidden_Vol_trail_list):
                vol_trailing_stop_level = 0
                # Volatility trailing stop amount in Pips
                vol_trail_point = vol_trail_multp * volATR
                min_profit = min_profit * symbol.point * symbol.p_value
                step_value = step * symbol.point * symbol.p_value
                if hidden_Vol_trail_list[x][0] == pos.ticket:
                    doesHiddenTrailingRecordExist = True
                    vol_trailing_stop_level = hidden_Vol_trail_list[x][1]
                    close = False

                    # ! TRIGGER
                    if doesHiddenTrailingRecordExist:
                        if pos.type == POSITION_TYPE.BUY and vol_trailing_stop_level >= symbol.bid:
                            close = True
                        elif pos.type == POSITION_TYPE.SELL and vol_trailing_stop_level <= symbol.ask:
                            close = True

                        if close:
                            if(debug):
                                print("EA Debug:Hidden vol trail hit, Trying to close position " +
                                      str(pos.ticket)+" ...")
                            # HandleTradingEnvironment(debug, Retry_Interval);
                            closing = await self.close_position(pos)
                            # closing = OrderClose(
                            #     OrderTicket(), OrderLots(), Bid, Slip*K, Blue);
                            if(debug and not closing):
                                print(
                                    "EA Debug: Unexpected Error has happened. While closing the order")
                            elif(debug and closing):
                                print("EA Debug: Position successfully closed.")

                            # break
                        # ! REVIEW
                        else:
                            # ! Step 2: If there are hidden trailing stop records and the position was not closed in Step 1. We update the hidden trailing stop record.
                            if pos.type == ORDER_TYPE.BUY:
                                trail_stop_price = symbol.bid - vol_trail_point
                                trail_stop_price = symbol.normalize_price(
                                    trail_stop_price)
                                # current_profit_pip = exc.calc_order_profit(
                                #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.bid)
                                current_profit_pip = symbol.bid - pos.price_open
                                current_profit_pip = symbol.normalize_price(
                                    current_profit_pip)
                                if trail_stop_price > vol_trailing_stop_level+step_value and current_profit_pip >= min_profit:
                                    hidden_Vol_trail_list[x][1] = trail_stop_price
                            elif pos.type == ORDER_TYPE.SELL:
                                trail_stop_price = symbol.ask + vol_trail_point
                                trail_stop_price = symbol.normalize_price(
                                    trail_stop_price)
                                # current_profit_pip = exc.calc_order_profit(
                                #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.ask)
                                current_profit_pip = pos.price_open - symbol.ask
                                current_profit_pip = symbol.normalize_price(
                                    current_profit_pip)
                                if trail_stop_price < vol_trailing_stop_level-step_value and current_profit_pip >= min_profit:
                                    hidden_Vol_trail_list[x][1] = trail_stop_price
                # ! (SET) If there are no hidden trailing stop records, add new record.
            if not doesHiddenVolTrailingRecordExist:
                order_stop_loss = pos.sl
                if order_stop_loss == 0:
                    hidden_sl_list = self.HiddenSLList
                    x = 0
                    while x < len(hidden_sl_list):
                        #  Looping through all order number in list
                        # doesOrderExist = False
                        orderTicketNumber = hidden_sl_list[x][0]
                        orderSL = hidden_sl_list[x][1]
                        if orderTicketNumber == pos.ticket:
                            if pos.type == ORDER_TYPE.BUY:
                                order_stop_loss = pos.price_open - \
                                    (orderSL * symbol.p_value * symbol.point)
                                break
                            elif pos.type == ORDER_TYPE.SELL:
                                order_stop_loss = pos.price_open + \
                                    (orderSL * symbol.p_value * symbol.point)
                                break

                        x += 1

                if pos.type == ORDER_TYPE.BUY:
                    vol_trail_point = vol_trail_multp*volATR
                    trail_stop_price = symbol.bid - vol_trail_point
                    trail_stop_price = symbol.normalize_price(
                        trail_stop_price)
                    # current_profit_pip = exc.calc_order_profit(
                    #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.bid)
                    current_profit_pip = symbol.bid - pos.price_open
                    current_profit_pip = symbol.normalize_price(
                        current_profit_pip)

                    # ! as we don't have any prior sl if our min_profit is achived we will set trail_stop_price as our trail stop
                    if trail_stop_price > (order_stop_loss+step) and current_profit_pip >= min_profit:
                        hidden_Vol_trail_list.append(
                            [pos.ticket, trail_stop_price])

                elif pos.type == ORDER_TYPE.SELL:
                    vol_trail_point = vol_trail_multp*volATR
                    trail_stop_price = symbol.ask + vol_trail_point
                    trail_stop_price = symbol.normalize_price(
                        trail_stop_price)
                    # current_profit_pip = exc.calc_order_profit(
                    #     pos.type, symbol.name, pos.volume, pos.price_open, symbol.ask)
                    current_profit_pip = pos.price_open - symbol.ask
                    current_profit_pip = symbol.normalize_price(
                        current_profit_pip)
                    # ! as we don't have any prior sl if our min_profit is achived we will set trail_stop_price as our trail stop
                    if trail_stop_price < (order_stop_loss-step or order_stop_loss == 0) and current_profit_pip >= min_profit:
                        hidden_Vol_trail_list.append(
                            [pos.ticket, trail_stop_price])

    # -----------------------------------------------------+
    # * (END)  Set Trigger Review Hidden Vol Trailing
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START) OPEN FROM MARKET
    # -----------------------------------------------------+

    async def OpenPositionMarket(self, symbol: Symbol, lot, order_type: int, SL: Union[int, None], TP: Union[int, None], Journaling: bool, Max_Retries_Per_Tick: int, ECN: bool = False, sl_in_pip: bool = True, tp_in_pip: bool = True):
        """
        This function submits new orders
        >>> `oreder_type`: POSITION_TYPE.BUY,POSITION_TYPE.SELL
        >>> `lot`: lot is volume for order
        >>> `SL`: stop loss in point
        >>> `TP`: take profit in point
        >>> `Journaling`: To print information
        >>> `P`: P value for pair
        >>> `Max_Retries_Per_Tick`: max tries on error
        >>> `ECN`: If broker is a ECN broker, order will be placed first, than we will modify with SL & TP
        """
        exc = self.exchange
        magic = self.magic_number
        Slip = self.slipaage
        P = symbol.p_value

        # ! this is a temporary code remove it in the next run
        # lot = lot if lot > 0 else 0.01
        # -----------------------------------------------------+
        # * (START)  check margin available
        # -----------------------------------------------------+
        is_margin_available = exc.validate_order_margin(
            order_type, symbol.name, lot, symbol.ask)

        if not is_margin_available:
            print("Can not open a trade. Not enough free margin to open " +
                  str(lot)+" on "+symbol.name)
            return dict()

        # -----------------------------------------------------+
        # * (END) check margin available
        # -----------------------------------------------------+
        if order_type == ORDER_TYPE.BUY or order_type == ORDER_TYPE.SELL:
            # ! execute only if we have buy or sell order type

            # ! Slippage is in points. 1 point = 0.0001 on 4 digit broker and 0.00001 on a 5 digit broker
            slippage = Slip*P
            buy_sell = 'BUY ' if order_type == ORDER_TYPE.BUY else 'SELL '
            comment = " "+buy_sell+"(#"+str(magic)+")"
            # ! if this order doesn't get executed under 5 seconds it will be expired(FOR MARKET ORDER EXPIRATION NOT NEEDED)
            # expiration = datetime.today() + timedelta(minutes=5)
            tries = 0
            stoploss = SL
            takeprofit = TP
            price = 0
            # if not ECN:
            #     # ! Edits stops and take profits before the market order is placed
            #     while(tries < Max_Retries_Per_Tick):
            #         # -----------------------------------------------------+
            #         # * (START)  Retriving Bid Ask Price
            #         # -----------------------------------------------------+
            #         bid = symbol.bid
            #         ask = symbol.ask
            #         # -----------------------------------------------------+
            #         # * (END) Retriving Bid Ask Price
            #         # -----------------------------------------------------+

            #         if(order_type == ORDER_TYPE.BUY):
            #             price = ask
            #         elif(order_type == ORDER_TYPE.SELL):
            #             price = bid

            #         # ! Sets Take Profits and Stop Loss. Check against Stop Level Limitations.
            #         if isinstance(SL, int):
            #             # ! stop defined in pips
            #             if(order_type == ORDER_TYPE.BUY and SL != 0):
            #                 stoploss = symbol.normalize_price(
            #                     ask-SL*P*symbol.point)
            #                 stoploss = self.adjust_below_stop_level(
            #                     symbol, stoploss)

            #             elif(order_type == ORDER_TYPE.SELL and SL != 0):
            #                 stoploss = symbol.normalize_price(bid+SL*P*symbol.point,
            #                                                   symbol.digits)
            #                 stoploss = self.adjust_above_stop_level(
            #                     symbol, stoploss)
            #         elif isinstance(SL, float):
            #             # ! Stop loss defined with exact price
            #             if(order_type == ORDER_TYPE.BUY and SL != 0.00):
            #                 # stoploss = symbol.normalize_price(
            #                 #     ask-SL)
            #                 stoploss = self.adjust_below_stop_level(
            #                     symbol, SL)

            #             elif(order_type == ORDER_TYPE.SELL and SL != 0):
            #                 # stoploss = symbol.normalize_price(bid+SL)
            #                 stoploss = self.adjust_above_stop_level(
            #                     symbol, SL)
            #         if isinstance(TP, int):
            #             # ! TAKE PROFIT defined in pips
            #             if(order_type == ORDER_TYPE.BUY and TP != 0):
            #                 takeprofit = symbol.normalize_price(
            #                     ask+TP*P*symbol.point)
            #                 takeprofit = self.adjust_above_stop_level(
            #                     symbol, takeprofit)

            #             elif(order_type == ORDER_TYPE.SELL and TP != 0):
            #                 takeprofit = symbol.normalize_price(
            #                     bid-TP*P*symbol.point)
            #                 takeprofit = self.adjust_below_stop_level(
            #                     symbol, takeprofit)
            #         elif isinstance(TP, float):
            #             # ! TAKE PROFIT DEFINED IN PRICE
            #             if(order_type == ORDER_TYPE.BUY and TP != 0):
            #                 takeprofit = self.adjust_above_stop_level(
            #                     symbol, TP)
            #             elif(order_type == ORDER_TYPE.SELL and TP != 0):
            #                 takeprofit = self.adjust_below_stop_level(
            #                     symbol, TP)

            #         if(Journaling):
            #             print("EA Journaling: Trying to place a market order...")
            #         # HandleTradingEnvironment(Journaling, Retry_Interval);
            #         try:
            #             result = exc.market_order_send(symbol=symbol.name, price=price, volume=lot, stop_loss=stoploss, take_profit=takeprofit,
            #                                            order_type=order_type, slippage=slippage, magic=magic, comment=comment, expiration=None)
            #             # result = exc.market_order_send(symbol=symbol.name, price=price, volume=lot,
            #             #                                order_type=order_type, slippage=slippage, magic=magic, comment=comment)

            #             assert result.comment != MARKET_CLOSED, 'Market is closed trade at a later time'
            #             pos = exc.get_position_from_order_send_result(result)
            #             return pos
            #         except Exception as ex:
            #             print(ex.args)

            #         tries += tries

            # if(ECN):  # ! Edits stops and take profits after the market order is placed

            if(order_type == ORDER_TYPE.BUY):
                price = symbol.ask
            elif(order_type == ORDER_TYPE.SELL):
                price = symbol.bid

            if(Journaling):
                timezone = pytz.timezone('EET')

                print("EA Journaling: Trying to place a market order at ... ",
                      datetime.now(tz=timezone).time())
            pos = dict()
            try:
                result = await exc.market_order_send(symbol=symbol.name, volume=lot, price=price,
                                                     order_type=order_type, slippage=slippage, magic=magic, comment=comment, expiration=None)

                assert result.comment != MARKET_CLOSED, 'Market is closed trade at a later time'
                pos = exc.get_position_from_order_send_result(result)
                print("Order successfully placed at ",
                      pd.to_datetime(pos.time, unit='s'))
            except Exception as ex:
                print(ex.args)

            if(pos and ((SL != 0 and SL != None) or (TP != 0 and TP != None))):
                # ! Sets Take Profits and Stop Loss. Check against Stop Level Limitations.
                if sl_in_pip:
                    if(order_type == ORDER_TYPE.BUY and SL != 0):
                        stoploss = symbol.normalize_price(
                            min(pos.price_open, symbol.bid)-SL * P * symbol.point)
                        stoploss = self.adjust_below_stop_level(
                            symbol, stoploss)

                    elif(order_type == ORDER_TYPE.SELL and SL != 0):

                        stoploss = symbol.normalize_price(
                            max(pos.price_open, symbol.ask)+(SL * P * symbol.point))
                        stoploss = self.adjust_above_stop_level(
                            symbol, stoploss)
                if tp_in_pip:
                    if(order_type == ORDER_TYPE.BUY and (TP != 0 and TP != None)):
                        takeprofit = symbol.normalize_price(
                            max(pos.price_open, symbol.ask)+TP * P * symbol.point)
                        takeprofit = self.adjust_above_stop_level(
                            symbol, takeprofit)

                    elif(order_type == ORDER_TYPE.SELL and (TP != 0 and TP != None)):
                        takeprofit = symbol.normalize_price(
                            min(pos.price_open, symbol.bid)-TP * P * symbol.point)
                        takeprofit = self.adjust_below_stop_level(
                            symbol, takeprofit)

                ModifyOpen = dict()
                while(not ModifyOpen) and tries <= Max_Retries_Per_Tick:
                    try:
                        ModifyOpen = exc.modify_sl_tp(
                            takeprofit, stoploss, pos)
                        return exc.get_position_with_ticket_id(pos.ticket)
                    except Exception as ex:
                        print(ex.args)
                    tries += 1
                return exc.get_position_with_ticket_id(pos.ticket)

            if pos:
                return pos

        return dict()

    # -----------------------------------------------------+
    # * (END) OPEN FROM MARKET
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START) OPEN PENDING ORDERS
    # -----------------------------------------------------+
    async def OpenPendingPosition(self, symbol: Symbol, lot, open_price: float, order_type: Entry, SL: Union[int, None], TP: Union[int, None], Journaling: bool, Max_Retries_Per_Tick: int, ECN: bool = False, sl_in_pip: bool = True, tp_in_pip: bool = True, expiration=None):
        """
        This function submits new orders
        >>> `oreder_type`: POSITION_TYPE.BUY,POSITION_TYPE.SELL
        >>> `lot`: lot is volume for order
        >>> `SL`: stop loss in point
        >>> `TP`: take profit in point
        >>> `Journaling`: To print information
        >>> `P`: P value for pair
        >>> `Max_Retries_Per_Tick`: max tries on error
        >>> `ECN`: If broker is a ECN broker, order will be placed first, than we will modify with SL & TP
        >>> `Expiration`: for how long the order will be live, in hours (CAN'T USE IT YET)
        """
        exc = self.exchange
        magic = self.magic_number
        P = symbol.p_value
        slippage = self.slipaage * P

        # -----------------------------------------------------+
        # * (START)  Trade Info
        # -----------------------------------------------------+
        account_info = exc.get_account_info()
        tries = 0
        # expiration = datetime.today() + expiration
        stoploss = SL
        takeprofit = TP
        price = 0
        # -----------------------------------------------------+
        # * (END)  Trade Info
        # -----------------------------------------------------+

        # -----------------------------------------------------+
        # * (START)  Retriving Bid Ask Price
        # -----------------------------------------------------+
        if(order_type == Entry.Buy):
            price = symbol.ask
            if open_price > price:
                order_type = ORDER_TYPE.BUY_STOP
            elif open_price < price:
                order_type = ORDER_TYPE.BUY_LIMIT
            else:
                order_type = ORDER_TYPE.BUY
        elif(order_type == Entry.Sell):
            price = symbol.bid
            if open_price > price:
                order_type = ORDER_TYPE.SELL_LIMIT
            elif open_price < price:
                order_type = ORDER_TYPE.SELL_STOP
            else:
                order_type = ORDER_TYPE.SELL

        # -----------------------------------------------------+
        # * (END) Retriving Bid Ask Price
        # -----------------------------------------------------+
        com_buy = order_type.name
        comment = ""+com_buy+"(#"+str(magic)+")"

        # -----------------------------------------------------+
        # * (START)  check margin available
        # -----------------------------------------------------+

        is_margin_available = exc.validate_order_margin(
            order_type, symbol, lot, open_price)

        if not is_margin_available:
            print("Can not open a trade. Not enough free margin to open " +
                  lot+" on "+symbol)
            return dict()
        # -----------------------------------------------------+
        # * (END) check margin available
        # -----------------------------------------------------+

        # -----------------------------------------------------+
        # * (START)  STOP LOSS Take Profit
        # -----------------------------------------------------+

        # ! Sets Take Profits and Stop Loss. Check against Stop Level Limitations.
        if((SL != 0 and SL != None) or (TP != 0 and TP != None)):
            if sl_in_pip:
                if order_type == ORDER_TYPE.BUY_LIMIT or order_type == ORDER_TYPE.BUY_STOP and SL != 0:
                    stoploss = symbol.normalize_price(
                        open_price - (SL * P * symbol.point))
                    stoploss = self.adjust_below_stop_level(
                        symbol, stoploss)
                elif order_type == ORDER_TYPE.SELL_LIMIT or order_type == ORDER_TYPE.SELL_STOP and SL != 0:
                    stoploss = symbol.normalize_price(
                        open_price + (SL * P * symbol.point))
                    stoploss = self.adjust_above_stop_level(
                        symbol, stoploss)
            if tp_in_pip:
                if order_type == ORDER_TYPE.BUY_LIMIT or order_type == ORDER_TYPE.BUY_STOP and TP != 0:
                    takeprofit = symbol.normalize_price(
                        open_price + (TP * P * symbol.point))
                    takeprofit = self.adjust_above_stop_level(
                        symbol, takeprofit)
                if order_type == ORDER_TYPE.SELL_LIMIT or order_type == ORDER_TYPE.SELL_STOP and TP != 0:
                    takeprofit = symbol.normalize_price(
                        open_price - (TP * P * symbol.point))
                    takeprofit = self.adjust_below_stop_level(
                        symbol, takeprofit)

        # -----------------------------------------------------+
        # * (END)  STOP LOSS Take Profit
        # -----------------------------------------------------+

        if(Journaling):
            timezone = pytz.timezone('EET')

            print(f"EA Journaling: Trying to place a pending {order_type.name} order at ... ",
                  datetime.now(tz=timezone).time())

        pos = dict()
        try:
            # ! Note: We did not modify Open Price if it breaches the Stop Level Limitations as Open Prices are sensitive and important. It is unsafe to change it automatically.
            result = await exc.market_order_send(symbol=symbol.name, action=TRADE_ACTION.PENDING, price=open_price, volume=lot, stop_loss=stoploss, take_profit=takeprofit, order_type=order_type, slippage=slippage, magic=magic, comment=comment, type_time=ORDER_TIME.GTC, expiration=expiration)

            assert result.comment != MARKET_CLOSED, 'Market is closed trade at a later time'
            ticket = result.order
            all_pen = exc.get_all_pending_position()
            pos = filter(lambda position: position.ticket == ticket
                         and position.symbol == symbol.name, all_pen)
            pos = list(pos)[0]
            print("Order successfully placed at ",
                  pd.to_datetime(pos.time_setup, unit='s'))
        except Exception as ex:
            print(ex.args)

        return pos

    # -----------------------------------------------------+
    # * (END) OPEN PENDING ORDERS
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (START)  CLOSE/DELETE ORDERS AND POSITIONS
    # -----------------------------------------------------+

    # -----------------------------------------------------+
    # * (END)
    # -----------------------------------------------------+


def main():
    symbol = mt5.symbol_info('GBPUSD')
    pos = sell(symbol, volume=0.01)
    modify_sl(pos.identifier, 300)
    modify_tp(pos.identifier, 200)
    # assert pos and pos.sl and pos.tp  # and pos.volume == 1.0

    time.sleep(2)
    r = close_position(pos)
    # ! checking if the retcode is done
    assert r.retcode == mt5.TRADE_RETCODE.DONE
    # ! checking if any other open position for this symbol
    assert not mt5.positions_get(symbol=symbol)


if __name__ == '__main__':
    conn = connected()
    with conn:
        ticks = mt5.copy_rates('GBPUSD', mt5.const.TIMEFRAME_H1)
        # create DataFrame out of the obtained data
        ohlcv = pd.DataFrame(ticks)
        # convert time in seconds into the datetime format
        ohlcv['time'] = pd.to_datetime(ohlcv['time'], unit='s')
        ohlcv.set_index('time', drop=True, inplace=True)
        spreads_df = ohlcv['2020-01-01':'2020-10-20'].sort_values(
            'spread', ascending=False)
        main()
        # deal = mt5.history_deals_get()
        # pos = mt5.positions_get(ticket=deal.position_id)[0]

    # trade = Trade('GBPUSD', magic=23458)
