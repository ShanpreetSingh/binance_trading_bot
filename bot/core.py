import logging
from typing import Dict, Optional, Type
from binance import Client
from binance.exceptions import BinanceAPIException

from .order_types import OrderType, MarketOrder, LimitOrder, StopLimitOrder, OCOOrder
from .exceptions import TradingBotError, APIError, InsufficientBalanceError, OrderExecutionError
from .utils import setup_logger, retry_on_failure, validate_symbol, validate_quantity, validate_price

class BasicBot:
    """Main trading bot class"""
    
    ORDER_TYPES = {
        'market': MarketOrder,
        'limit': LimitOrder,
        'stop_limit': StopLimitOrder,
        'oco': OCOOrder,
    }
    
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """Initialize the trading bot"""
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.logger = setup_logger('trading_bot', 'logs/trading_bot.log')
        self._initialize_order_types()
        
    def _initialize_order_types(self):
        """Initialize all order type handlers"""
        self.order_handlers = {
            name: handler(self.client) for name, handler in self.ORDER_TYPES.items()
        }
        for handler in self.order_handlers.values():
            handler.set_logger(self.logger)
            
    @retry_on_failure()
    def get_account_info(self) -> Dict:
        """Get futures account information"""
        try:
            return self.client.futures_account()
        except BinanceAPIException as e:
            if 'Account has insufficient balance' in str(e):
                raise InsufficientBalanceError(str(e)) from e
            raise APIError(f"Failed to get account info: {str(e)}") from e
            
    @retry_on_failure()
    def get_symbol_info(self, symbol: str) -> Dict:
        """Get information about a trading symbol"""
        validate_symbol(symbol)
        try:
            info = self.client.futures_exchange_info()
            for s in info['symbols']:
                if s['symbol'] == symbol:
                    return s
            raise InvalidOrderError(f"Symbol {symbol} not found")
        except BinanceAPIException as e:
            raise APIError(f"Failed to get symbol info: {str(e)}") from e
            
    def execute_order(self, order_type: str, **kwargs) -> Dict:
        """Execute an order of the specified type"""
        if order_type not in self.order_handlers:
            raise InvalidOrderError(f"Unsupported order type: {order_type}")
            
        try:
            return self.order_handlers[order_type].execute(**kwargs)
        except BinanceAPIException as e:
            if 'Account has insufficient balance' in str(e):
                raise InsufficientBalanceError(str(e)) from e
            raise OrderExecutionError(f"Order execution failed: {str(e)}") from e
            
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """Check the status of an order"""
        validate_symbol(symbol)
        try:
            return self.client.futures_get_order(symbol=symbol, orderId=order_id)
        except BinanceAPIException as e:
            raise APIError(f"Failed to get order status: {str(e)}") from e
            
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """Cancel an existing order"""
        validate_symbol(symbol)
        try:
            return self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
        except BinanceAPIException as e:
            raise APIError(f"Failed to cancel order: {str(e)}") from e