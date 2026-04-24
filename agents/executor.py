class Executor:
    def execute(self, plan, symbol, analysis=None, decision=None):

        print("\n" + "="*50)
        print(f"📊 STOCK REPORT: {symbol}")
        print("="*50)

        # Basic info
        if analysis:
            print(f"\n💰 Current Price: {analysis.get('price')}")
            print(f"📈 Signal: {analysis.get('signal')}")

        # Decision
        print(f"\n🧠 Strategy Decision: {decision}")

        # Risk / Trade Plan
        if isinstance(plan, dict):
            print("\n📌 Trade Plan:")
            print(f"Action: {plan['action']}")
            print(f"Stop Loss: {plan['stop_loss']:.2f}")
            print(f"Take Profit: {plan['take_profit']:.2f}")
        else:
            print("\n⚠️ No Trade Recommended")

        print("\n" + "="*50)