import yfinance as yf
import pandas as pd

class RiskManager:
    def assess(self, decision, analysis):
        price = analysis.get("price")

        # If no valid price → skip
        if price is None:
            return "NO_ACTION"

        if decision == "GO_LONG":
            return {
                "action": "BUY",
                "stop_loss": price * 0.97,
                "take_profit": price * 1.05
            }

        elif decision == "GO_SHORT":
            return {
                "action": "SELL",
                "stop_loss": price * 1.03,
                "take_profit": price * 0.95
            }

        else:
            return "NO_ACTION"