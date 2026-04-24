from agents.market_analyst import MarketAnalyst
from agents.strategist import Strategist
from agents.risk_manager import RiskManager
from agents.executor import Executor
import pandas as pd

def main():
    # List of stock symbols to process
    symbols = ['AAPL', 'TSLA', 'MSFT']
    
    # Instantiate agents (reusable across symbols)
    analyst = MarketAnalyst()
    strategist = Strategist()
    risk_manager = RiskManager()
    executor = Executor()
    
    # List to collect trade decision logs
    logs = []
    
    # Loop through each symbol
    for symbol in symbols:
        print(f"\n--- Processing {symbol} ---")
        
        # Step-by-step orchestration for each symbol
        # 1. MarketAnalyst: Fetch data and generate signal
        analysis = analyst.analyze_market(symbol)
        signal = analysis['signal']
        price = analysis['price']
        
        # 2. Strategist: Generate decision based on signal
        decision = strategist.generate_strategy(analysis)
        
        # 3. RiskManager: Assess risk and create plan
        risk_plan = risk_manager.manage_risk(decision, price, symbol)
        risk_output = risk_plan['message']
        
        # 4. Executor: Execute trade if approved
        if risk_plan['action'] in ['GO_LONG', 'GO_SHORT']:
            # Print trade alert
            print("\n🚨 TRADE ALERT 🚨")
            print(f"Symbol: {symbol}")
            print(f"Action: {'BUY' if risk_plan['action'] == 'GO_LONG' else 'SELL'}")
            print(f"Entry Price: {risk_plan['price']:.2f}")
            print(f"Stop Loss: {risk_plan['stop_loss']:.2f}")
            print(f"Take Profit: {risk_plan['take_profit']:.2f}")
            print("🚨 END ALERT 🚨\n")
            
            execution_result = executor.execute_trade(risk_plan)
        else:
            execution_result = risk_plan['message']
        
        # Collect log entry
        log_entry = {
            'symbol': symbol,
            'signal': signal,
            'decision': decision,
            'stop_loss': risk_plan.get('stop_loss', None),
            'take_profit': risk_plan.get('take_profit', None),
            'timestamp': pd.Timestamp.now()
        }
        logs.append(log_entry)
        
        # Print clear summary for the symbol
        print(f"\nTrading System Summary for {symbol}:")
        print(f"Signal: {signal}")
        print(f"Decision: {decision}")
        print(f"Risk Output: {risk_output}")
        print(f"Execution Result: {execution_result}")
    
    # Save logs to CSV
    df = pd.DataFrame(logs)
    df.to_csv('trade_decisions.csv', index=False)
    print("\nTrade decisions saved to trade_decisions.csv")

from agents.market_analyst import MarketAnalyst
from agents.strategist import Strategist
from agents.risk_manager import RiskManager
from agents.executor import Executor

class TradingTeam:
    def __init__(self):
        self.analyst = MarketAnalyst()
        self.strategist = Strategist()
        self.risk_manager = RiskManager()
        self.executor = Executor()

    def run(self, symbol):
        analysis = self.analyst.analyze(symbol)
        decision = self.strategist.decide(analysis)
        plan = self.risk_manager.assess(decision, analysis)
        self.executor.execute(plan, symbol, analysis, decision)


if __name__ == "__main__":
    team = TradingTeam()
    team.run("ONGC.NS")
