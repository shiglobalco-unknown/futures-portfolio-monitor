#!/usr/bin/env python3
"""
AI Trading Assistant for Futures Portfolio Monitor
Uses dedicated OpenAI API key for intelligent trading analysis and signals
"""

import os
import openai
from datetime import datetime, timedelta
import json
import asyncio
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FuturesTradingAI:
    """AI Trading Assistant for Futures Markets"""
    
    def __init__(self):
        # Use dedicated futures trading API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = openai.OpenAI(api_key=api_key)
        
        # Focus instruments for TopStep
        self.instruments = ["ES", "NQ", "CL", "GC"]
        
        # System prompt for futures trading
        self.system_prompt = """
You are an expert futures trading AI assistant specializing in TopStep funded accounts. 
Your expertise covers:

- E-mini S&P 500 (ES) and NASDAQ (NQ) futures
- Crude Oil (CL) and Gold (GC) futures  
- TopStep combine rules and risk management
- Intraday trading strategies and signals
- Risk/reward analysis and position sizing

Focus on:
1. Providing clear, actionable trading signals
2. Risk management within TopStep rules
3. Market analysis based on technical indicators
4. Entry/exit strategies for intraday trades
5. Daily P&L targets and loss limits compliance

Always consider TopStep rules:
- Daily loss limits ($2K/$3K/$4.5K depending on account)
- Profit targets ($3K/$6K/$9K depending on account)  
- Position size limits (5/10/15 contracts)
- Consistency requirements

Respond with professional, institutional-grade analysis.
"""

    async def analyze_market_conditions(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current market conditions and provide trading insights"""
        
        try:
            prompt = f"""
Current Market Analysis Request:
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S ET')}

Market Data Available:
- ES (S&P 500): Current session data
- NQ (NASDAQ): Current session data  
- CL (Crude Oil): Current session data
- GC (Gold): Current session data

Please provide:
1. Overall market sentiment (Bullish/Bearish/Neutral)
2. Key support/resistance levels for each instrument
3. Intraday bias and preferred trading direction
4. Risk factors to watch
5. Recommended position sizing for TopStep account

Format as JSON with clear actionable insights.
"""

            response = await self._get_ai_response(prompt)
            return self._parse_market_analysis(response)
            
        except Exception as e:
            return {
                "error": str(e),
                "fallback_analysis": {
                    "sentiment": "Neutral",
                    "recommendation": "Monitor market conditions before trading",
                    "risk_level": "Medium"
                }
            }

    async def generate_trading_signals(self, symbol: str, timeframe: str = "5m") -> Dict[str, Any]:
        """Generate specific trading signals for a symbol"""
        
        try:
            prompt = f"""
Trading Signal Generation for {symbol}:
Timeframe: {timeframe}
Current Time: {datetime.now().strftime('%H:%M ET')}

Analyze {symbol} and provide:
1. Signal Direction: LONG/SHORT/NEUTRAL
2. Entry Price Level
3. Stop Loss Level  
4. Take Profit Target
5. Position Size (1-5 contracts for 50K account)
6. Signal Confidence (1-10)
7. Risk/Reward Ratio
8. Market Context and Reasoning

Consider:
- TopStep daily loss limits
- Optimal risk management
- Current market volatility
- Typical intraday ranges for {symbol}

Respond in JSON format with clear trade parameters.
"""

            response = await self._get_ai_response(prompt)
            return self._parse_trading_signal(response, symbol)
            
        except Exception as e:
            return {
                "symbol": symbol,
                "signal": "NEUTRAL", 
                "confidence": 0,
                "error": str(e)
            }

    async def analyze_trade_performance(self, trades: List[Dict]) -> Dict[str, Any]:
        """Analyze recent trading performance and suggest improvements"""
        
        if not trades:
            return {"message": "No trades to analyze"}
            
        try:
            trades_summary = self._summarize_trades(trades)
            
            prompt = f"""
Trading Performance Analysis:

Recent Trading Summary:
{json.dumps(trades_summary, indent=2)}

Please analyze and provide:
1. Performance Assessment (Excellent/Good/Needs Improvement)
2. Win Rate Analysis  
3. Average Risk/Reward
4. Biggest Strengths
5. Areas for Improvement
6. Specific Recommendations for Next Trades
7. TopStep Progress Assessment

Focus on actionable insights to improve trading consistency and profitability.
Respond in JSON format.
"""

            response = await self._get_ai_response(prompt)
            return self._parse_performance_analysis(response)
            
        except Exception as e:
            return {
                "error": str(e),
                "basic_analysis": self._basic_trade_analysis(trades)
            }

    async def risk_management_check(self, account_data: Dict[str, Any], proposed_trade: Dict[str, Any]) -> Dict[str, Any]:
        """Check if proposed trade meets TopStep risk management rules"""
        
        try:
            prompt = f"""
Risk Management Analysis:

Account Status:
{json.dumps(account_data, indent=2)}

Proposed Trade:
{json.dumps(proposed_trade, indent=2)}

Evaluate:
1. Daily Loss Limit Compliance
2. Position Size Appropriateness  
3. Portfolio Risk Impact
4. TopStep Rule Compliance
5. Risk/Reward Assessment
6. Trade Approval: APPROVED/REJECTED/MODIFY

Provide specific feedback on risk factors and recommended adjustments.
Respond in JSON format.
"""

            response = await self._get_ai_response(prompt)
            return self._parse_risk_analysis(response)
            
        except Exception as e:
            return {
                "approval": "REJECTED",
                "reason": f"Risk analysis error: {str(e)}",
                "recommendation": "Manual review required"
            }

    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3  # Lower temperature for more consistent analysis
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"AI API error: {str(e)}")

    def _parse_market_analysis(self, response: str) -> Dict[str, Any]:
        """Parse market analysis response"""
        try:
            # Try to parse JSON response
            return json.loads(response)
        except:
            # Fallback parsing
            return {
                "sentiment": "Neutral",
                "analysis": response,
                "timestamp": datetime.now().isoformat()
            }

    def _parse_trading_signal(self, response: str, symbol: str) -> Dict[str, Any]:
        """Parse trading signal response"""
        try:
            return json.loads(response)
        except:
            return {
                "symbol": symbol,
                "signal": "NEUTRAL",
                "confidence": 5,
                "analysis": response,
                "timestamp": datetime.now().isoformat()
            }

    def _parse_performance_analysis(self, response: str) -> Dict[str, Any]:
        """Parse performance analysis response"""
        try:
            return json.loads(response)
        except:
            return {
                "assessment": "Analysis completed",
                "details": response,
                "timestamp": datetime.now().isoformat()
            }

    def _parse_risk_analysis(self, response: str) -> Dict[str, Any]:
        """Parse risk analysis response"""
        try:
            return json.loads(response)
        except:
            return {
                "approval": "MANUAL_REVIEW",
                "details": response,
                "timestamp": datetime.now().isoformat()
            }

    def _summarize_trades(self, trades: List[Dict]) -> Dict[str, Any]:
        """Summarize recent trades for analysis"""
        total_pnl = sum(trade.get('pnl', 0) for trade in trades)
        winning_trades = sum(1 for trade in trades if trade.get('pnl', 0) > 0)
        
        return {
            "total_trades": len(trades),
            "total_pnl": total_pnl,
            "winning_trades": winning_trades,
            "win_rate": winning_trades / len(trades) if trades else 0,
            "avg_pnl_per_trade": total_pnl / len(trades) if trades else 0,
            "recent_trades": trades[-5:]  # Last 5 trades
        }

    def _basic_trade_analysis(self, trades: List[Dict]) -> Dict[str, Any]:
        """Basic trade analysis fallback"""
        if not trades:
            return {"message": "No trades to analyze"}
            
        total_pnl = sum(trade.get('pnl', 0) for trade in trades)
        winning_trades = sum(1 for trade in trades if trade.get('pnl', 0) > 0)
        
        return {
            "total_trades": len(trades),
            "total_pnl": total_pnl,
            "win_rate": f"{(winning_trades / len(trades) * 100):.1f}%",
            "status": "Good" if total_pnl > 0 else "Needs Improvement"
        }

async def test_ai_assistant():
    """Test the AI trading assistant"""
    print("🤖 Testing AI Trading Assistant...")
    
    ai = FuturesTradingAI()
    
    # Test market analysis
    print("📊 Getting market analysis...")
    market_analysis = await ai.analyze_market_conditions({})
    print(f"Market Analysis: {json.dumps(market_analysis, indent=2)}")
    
    # Test trading signal
    print("📡 Generating ES trading signal...")  
    es_signal = await ai.generate_trading_signals("ES")
    print(f"ES Signal: {json.dumps(es_signal, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_ai_assistant())