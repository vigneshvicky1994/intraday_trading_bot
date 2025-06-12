from gemini_client import GeminiClient
from zerodha_client import ZerodhaClient
from intraday_trading import IntraDayTrading
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    gemini = GeminiClient(api_key="your_gemini_api_key")
    zerodha = ZerodhaClient(api_key="your_zerodha_api_key", api_secret="your_zerodha_api_secret")

    bot = IntraDayTrading(gemini, zerodha, budget=10000)
    bot.run()
