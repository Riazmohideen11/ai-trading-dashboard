class Strategist:
    def decide(self, analysis):
        signal = analysis.get("signal")

        if signal == "BUY":
            return "GO_LONG"
        elif signal == "SELL":
            return "GO_SHORT"
        else:
            return "NO_TRADE"