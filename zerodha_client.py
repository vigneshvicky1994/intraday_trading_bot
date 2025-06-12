from kiteconnect import KiteConnect
import pickle
import os

class ZerodhaClient:
    def __init__(self, api_key, api_secret, token_cache_path="kite_token.pkl"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_cache_path = token_cache_path
        self.kite = KiteConnect(api_key=api_key)
        self.access_token = None
        self._load_token_from_cache()

    def _load_token_from_cache(self):
        if os.path.exists(self.token_cache_path):
            with open(self.token_cache_path, "rb") as f:
                data = pickle.load(f)
                self.access_token = data["access_token"]
                self.kite.set_access_token(self.access_token)

    def _save_token_to_cache(self, token_data):
        with open(self.token_cache_path, "wb") as f:
            pickle.dump(token_data, f)

    def authenticate(self, request_token):
        data = self.kite.generate_session(request_token, api_secret=self.api_secret)
        self.access_token = data["access_token"]
        self.kite.set_access_token(self.access_token)
        self._save_token_to_cache(data)

    def get_price(self, symbol, exchange="NSE"):
        instrument = f"{exchange}:{symbol}"
        ltp = self.kite.ltp([instrument])
        return ltp[instrument]["last_price"]

    def place_order(self, symbol, quantity, txn_type="BUY", product="MIS", exchange="NSE"):
        return self.kite.place_order(
            variety=self.kite.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=symbol,
            transaction_type=self.kite.TRANSACTION_TYPE_BUY if txn_type.upper() == "BUY" else self.kite.TRANSACTION_TYPE_SELL,
            quantity=quantity,
            order_type=self.kite.ORDER_TYPE_MARKET,
            product=product
        )
