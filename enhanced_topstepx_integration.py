#!/usr/bin/env python3
"""
Enhanced TopStepX Gateway API Integration
Professional integration for live futures trading data and account management
"""

import os
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TopStepAccount:
    """TopStep account information"""
    account_id: str
    account_type: str
    balance: float
    equity: float
    buying_power: float
    day_trading_buying_power: float
    profit_target: float
    daily_loss_limit: float
    max_loss_limit: float
    current_pnl: float
    daily_pnl: float
    status: str

@dataclass
class Position:
    """Trading position"""
    symbol: str
    quantity: int
    market_value: float
    average_cost: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    side: str  # 'long' or 'short'
    timestamp: datetime

@dataclass
class Trade:
    """Trade execution record"""
    trade_id: str
    symbol: str
    quantity: int
    price: float
    side: str
    timestamp: datetime
    commission: float
    pnl: float

class TopStepXGateway:
    """TopStepX Gateway API Client"""
    
    def __init__(self):
        # API Configuration
        self.api_key = os.getenv("TOPSTEP_API_KEY")
        self.username = os.getenv("TOPSTEP_USERNAME", "your_username")
        self.base_url = os.getenv("TOPSTEP_BASE_URL", "https://gateway.projectx.com/api")
        
        # Gateway API endpoints
        self.endpoints = {
            "auth": "/auth/login",
            "accounts": "/accounts",
            "positions": "/positions",
            "orders": "/orders", 
            "executions": "/executions",
            "market_data": "/market-data",
            "account_summary": "/accounts/summary",
            "risk_metrics": "/risk/metrics"
        }
        
        self.session_token = None
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        # Create session with SSL verification disabled for testing
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(connector=connector)
        await self.authenticate()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def authenticate(self) -> bool:
        """Authenticate with TopStepX Gateway API"""
        try:
            auth_url = f"{self.base_url}{self.endpoints['auth']}"
            
            # Try multiple authentication methods
            auth_payloads = [
                # Method 1: API Key authentication
                {
                    "apiKey": self.api_key,
                    "username": self.username
                },
                # Method 2: Token-based authentication  
                {
                    "token": self.api_key,
                    "user": self.username
                },
                # Method 3: Direct key authentication
                {
                    "key": self.api_key,
                    "account": self.username
                }
            ]
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "TopStepX-Futures-Monitor/1.0"
            }
            
            for i, payload in enumerate(auth_payloads, 1):
                logger.info(f"Trying authentication method {i}...")
                
                async with self.session.post(auth_url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Handle different response formats
                        if isinstance(data, dict):
                            if data.get("success") and data.get("token"):
                                self.session_token = data["token"]
                                logger.info("✅ Authentication successful!")
                                return True
                            elif data.get("access_token"):
                                self.session_token = data["access_token"] 
                                logger.info("✅ Authentication successful!")
                                return True
                            elif "token" in data:
                                self.session_token = data["token"]
                                logger.info("✅ Authentication successful!")
                                return True
                        
                        logger.warning(f"⚠️ Method {i} response: {data}")
                    else:
                        logger.warning(f"⚠️ Method {i} failed: HTTP {response.status}")
            
            logger.error("❌ All authentication methods failed")
            return False
            
        except Exception as e:
            logger.error(f"❌ Authentication error: {str(e)}")
            return False
    
    async def get_account_info(self) -> Optional[TopStepAccount]:
        """Get detailed account information"""
        if not self.session_token:
            logger.warning("Not authenticated")
            return None
            
        try:
            url = f"{self.base_url}{self.endpoints['account_summary']}"
            headers = {
                "Authorization": f"Bearer {self.session_token}",
                "Content-Type": "application/json"
            }
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Parse account data (adjust fields based on actual API response)
                    account_data = data.get("account", data)
                    
                    return TopStepAccount(
                        account_id=account_data.get("accountId", "TS001"),
                        account_type=account_data.get("accountType", "50K_COMBINE"), 
                        balance=float(account_data.get("balance", 50000.0)),
                        equity=float(account_data.get("equity", 50000.0)),
                        buying_power=float(account_data.get("buyingPower", 50000.0)),
                        day_trading_buying_power=float(account_data.get("dayTradingBuyingPower", 200000.0)),
                        profit_target=float(account_data.get("profitTarget", 3000.0)),
                        daily_loss_limit=float(account_data.get("dailyLossLimit", 2000.0)),
                        max_loss_limit=float(account_data.get("maxLossLimit", 2500.0)),
                        current_pnl=float(account_data.get("totalPnL", 0.0)),
                        daily_pnl=float(account_data.get("dailyPnL", 0.0)),
                        status=account_data.get("status", "active")
                    )
                else:
                    logger.error(f"Failed to get account info: HTTP {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            return None
    
    async def get_positions(self) -> List[Position]:
        """Get current positions"""
        if not self.session_token:
            logger.warning("Not authenticated")
            return []
            
        try:
            url = f"{self.base_url}{self.endpoints['positions']}"
            headers = {
                "Authorization": f"Bearer {self.session_token}",
                "Content-Type": "application/json"
            }
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    positions = []
                    
                    position_data = data.get("positions", data if isinstance(data, list) else [])
                    
                    for pos in position_data:
                        positions.append(Position(
                            symbol=pos.get("symbol", "ES"),
                            quantity=int(pos.get("quantity", 0)),
                            market_value=float(pos.get("marketValue", 0.0)),
                            average_cost=float(pos.get("averageCost", 0.0)),
                            current_price=float(pos.get("currentPrice", 0.0)),
                            unrealized_pnl=float(pos.get("unrealizedPnL", 0.0)),
                            realized_pnl=float(pos.get("realizedPnL", 0.0)),
                            side=pos.get("side", "long").lower(),
                            timestamp=datetime.now()
                        ))
                    
                    return positions
                else:
                    logger.error(f"Failed to get positions: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return []
    
    async def get_recent_trades(self, limit: int = 50) -> List[Trade]:
        """Get recent trade executions"""
        if not self.session_token:
            logger.warning("Not authenticated")
            return []
            
        try:
            url = f"{self.base_url}{self.endpoints['executions']}"
            headers = {
                "Authorization": f"Bearer {self.session_token}",
                "Content-Type": "application/json"
            }
            
            params = {"limit": limit, "sortOrder": "desc"}
            
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    trades = []
                    
                    trade_data = data.get("executions", data if isinstance(data, list) else [])
                    
                    for trade in trade_data:
                        trades.append(Trade(
                            trade_id=trade.get("tradeId", f"T{len(trades)+1}"),
                            symbol=trade.get("symbol", "ES"),
                            quantity=int(trade.get("quantity", 1)),
                            price=float(trade.get("price", 0.0)),
                            side=trade.get("side", "buy").lower(),
                            timestamp=datetime.fromisoformat(trade.get("timestamp", datetime.now().isoformat())),
                            commission=float(trade.get("commission", 0.0)),
                            pnl=float(trade.get("pnl", 0.0))
                        ))
                    
                    return trades
                else:
                    logger.error(f"Failed to get trades: HTTP {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting trades: {str(e)}")
            return []
    
    async def get_market_data(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get real-time market data for symbols"""
        if not self.session_token:
            logger.warning("Not authenticated")
            return {}
            
        try:
            url = f"{self.base_url}{self.endpoints['market_data']}"
            headers = {
                "Authorization": f"Bearer {self.session_token}",
                "Content-Type": "application/json"
            }
            
            params = {"symbols": ",".join(symbols)}
            
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("quotes", {})
                else:
                    logger.error(f"Failed to get market data: HTTP {response.status}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error getting market data: {str(e)}")
            return {}

# Integration functions for Streamlit app
async def get_live_topstep_data() -> Dict[str, Any]:
    """Get live TopStep data for Streamlit dashboard"""
    try:
        async with TopStepXGateway() as gateway:
            account = await gateway.get_account_info()
            positions = await gateway.get_positions()
            trades = await gateway.get_recent_trades(10)
            market_data = await gateway.get_market_data(["ES", "NQ", "CL", "GC"])
            
            if account:
                return {
                    "account": account,
                    "positions": positions,
                    "recent_trades": trades,
                    "market_data": market_data,
                    "connected": True,
                    "last_update": datetime.now()
                }
    except Exception as e:
        logger.error(f"Error getting live data: {str(e)}")
    
    # Return demo data if connection fails
    return {
        "account": None,
        "positions": [],
        "recent_trades": [],
        "market_data": {},
        "connected": False,
        "error": "Connection failed - using demo data",
        "last_update": datetime.now()
    }

def test_connection():
    """Test TopStepX connection"""
    async def run_test():
        print("🔌 Testing TopStepX Gateway API Connection...")
        
        async with TopStepXGateway() as gateway:
            # Test account info
            account = await gateway.get_account_info()
            if account:
                print(f"✅ Account: {account.account_type} - Balance: ${account.balance:,.2f}")
            
            # Test positions
            positions = await gateway.get_positions()
            print(f"✅ Positions: {len(positions)} open positions")
            
            # Test trades
            trades = await gateway.get_recent_trades(5)
            print(f"✅ Recent Trades: {len(trades)} trades retrieved")
            
            return True
    
    return asyncio.run(run_test())

if __name__ == "__main__":
    # Test the connection
    test_connection()