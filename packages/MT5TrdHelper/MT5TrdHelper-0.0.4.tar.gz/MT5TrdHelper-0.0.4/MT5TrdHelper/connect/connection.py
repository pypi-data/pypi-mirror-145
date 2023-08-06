import pymt5adapter as mt5
import logging


class Connection(object):
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
        connection base class for all trading related work
        """
        self.connected = None
        self.connected = self.connect(path=path,
                                      portable=portable,
                                      server=server,
                                      login=login,
                                      password=password,
                                      timeout=timeout,
                                      logger=logger,  # default is None
                                      ensure_trade_enabled=ensure_trade_enabled,  # default is False
                                      enable_real_trading=enable_real_trading,  # default is False
                                      raise_on_errors=raise_on_errors,  # default is False
                                      return_as_dict=return_as_dict,  # default is False
                                      return_as_native_python_objects=return_as_native_python_objects,  # default is False
                                      )

    def connect(
        self,
        path,
        portable=False,
        server='XMGlobal-MT5 2',
        login=64158516,
        password='qM0PyD9sjsIg',
        timeout=5000,
        logger=None,  # default is None
        ensure_trade_enabled=True,  # default is False
        enable_real_trading=False,  # default is False
        raise_on_errors=True,  # default is False
        return_as_dict=False,  # default is False
        return_as_native_python_objects=False  # default is False
    ):
        """
        function to get a connection to mt5
        """

        # LOGPATH = './my_mt5_log.log'
        # ! If you need logger uncomment below code, but logger takes too much space, and it isn't that useful to me still, that's why I commented out below code.
        # logger = mt5.get_logger(loglevel=logging.DEBUG,
        #                         path_to_logfile=logger)

        mt5_connected = mt5.connected(
            # path=r'C:\Program Files\XM Global MT5\terminal64.exe',
            path=path,
            portable=portable,
            server=server,
            login=login,
            password=password,
            timeout=timeout,
            logger=logger,  # default is None
            ensure_trade_enabled=ensure_trade_enabled,  # default is False
            enable_real_trading=enable_real_trading,  # default is False
            raise_on_errors=raise_on_errors,  # default is False
            return_as_dict=return_as_dict,  # default is False
            return_as_native_python_objects=return_as_native_python_objects,  # default is False
        )
        return mt5_connected
