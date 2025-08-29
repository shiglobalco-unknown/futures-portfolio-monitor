#!/usr/bin/env python3
"""
Multi-Source Market Data Integration
Combines TopStepX API, email data, and market news with manipulation awareness
"""

import os
import asyncio
import aiohttp
import imaplib
import email
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import feedparser

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MarketDataSource:
    """Market data from various sources"""
    source: str
    timestamp: datetime
    data: Dict[str, Any]
    reliability_score: float  # 0-1, accounts for potential manipulation
    confidence: float

class MultiSourceMarketData:
    """Comprehensive market data aggregation with manipulation detection"""
    
    def __init__(self):
        # TopStep credentials
        self.topstep_username = os.getenv("TOPSTEP_USERNAME", "onitrades")
        self.topstep_password = os.getenv("TOPSTEP_PASSWORD", "Super$-Ant2010")
        self.topstep_api_key = os.getenv("TOPSTEP_API_KEY")
        
        # Email credentials (if provided)
        self.email_server = os.getenv("EMAIL_SERVER", "imap.gmail.com")
        self.email_username = os.getenv("EMAIL_USERNAME")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        
        # Focus instruments
        self.instruments = ["ES=F", "NQ=F", "CL=F", "GC=F"]  # Yahoo Finance format
        
        # Market manipulation indicators
        self.manipulation_keywords = [
            "unprecedented", "never seen before", "historic", "shocking",
            "emergency", "crisis", "crash", "bubble", "moon", "rocket"
        ]
        
        # Reliable sources (higher trust score)
        self.trusted_sources = [
            "federalreserve.gov", "cmegroup.com", "sec.gov", "treasury.gov",
            "reuters.com", "bloomberg.com", "wsj.com"
        ]
        
        # Session for API calls
        self.session = None
        self.topstep_token = None

    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(connector=connector)
        await self.authenticate_topstep()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    async def authenticate_topstep(self) -> bool:
        """Authenticate with TopStepX using username/password"""
        try:
            # Try multiple authentication endpoints
            auth_endpoints = [
                "/auth/login",
                "/login", 
                "/authenticate",
                "/api/auth/login"
            ]
            
            base_urls = [
                "https://gateway.projectx.com/api",
                "https://api.topstepx.com",
                "https://topstepx.com/api"
            ]
            
            for base_url in base_urls:
                for endpoint in auth_endpoints:
                    try:
                        auth_url = f"{base_url}{endpoint}"
                        
                        # Try different payload formats
                        payloads = [
                            {
                                "username": self.topstep_username,
                                "password": self.topstep_password
                            },
                            {
                                "userName": self.topstep_username,
                                "password": self.topstep_password,
                                "apiKey": self.topstep_api_key
                            },
                            {
                                "email": self.topstep_username,
                                "password": self.topstep_password
                            }
                        ]
                        
                        headers = {
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                            "User-Agent": "TopStepX-Monitor/1.0"
                        }
                        
                        for payload in payloads:
                            async with self.session.post(auth_url, json=payload, headers=headers) as response:
                                if response.status in [200, 201]:
                                    data = await response.json()
                                    
                                    # Look for token in various formats
                                    token = data.get("token") or data.get("access_token") or data.get("authToken")
                                    
                                    if token:
                                        self.topstep_token = token
                                        logger.info(f"✅ TopStep authentication successful via {base_url}{endpoint}")
                                        return True
                                        
                    except Exception as e:
                        continue
            
            logger.warning("⚠️ TopStep authentication failed - using demo mode")
            return False
            
        except Exception as e:
            logger.error(f"TopStep auth error: {str(e)}")
            return False

    async def get_topstep_data(self) -> Optional[Dict[str, Any]]:
        """Get data from TopStepX API"""
        if not self.topstep_token:
            return None
            
        try:
            headers = {
                "Authorization": f"Bearer {self.topstep_token}",
                "Content-Type": "application/json"
            }
            
            # Try different account endpoints
            endpoints = ["/accounts", "/account", "/positions", "/portfolio"]
            
            for endpoint in endpoints:
                try:
                    url = f"https://gateway.projectx.com/api{endpoint}"
                    async with self.session.get(url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            return {
                                "source": "TopStepX",
                                "endpoint": endpoint,
                                "data": data,
                                "timestamp": datetime.now(),
                                "reliability_score": 1.0  # Direct from broker
                            }
                except:
                    continue
                    
            return None
            
        except Exception as e:
            logger.error(f"TopStep data error: {str(e)}")
            return None

    def get_market_data_yahoo(self) -> Dict[str, Any]:
        """Get real-time market data from Yahoo Finance"""
        try:
            data = {}
            
            for symbol in self.instruments:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    hist = ticker.history(period="1d", interval="5m")
                    
                    if not hist.empty:
                        current_price = hist['Close'].iloc[-1]
                        change = current_price - hist['Close'].iloc[0]
                        change_pct = (change / hist['Close'].iloc[0]) * 100
                        
                        data[symbol.replace("=F", "")] = {
                            "price": current_price,
                            "change": change,
                            "change_percent": change_pct,
                            "volume": hist['Volume'].iloc[-1],
                            "high": hist['High'].max(),
                            "low": hist['Low'].min(),
                            "timestamp": datetime.now()
                        }
                        
                except Exception as e:
                    logger.warning(f"Failed to get {symbol}: {str(e)}")
                    continue
            
            return {
                "source": "Yahoo Finance",
                "data": data,
                "reliability_score": 0.85,  # Generally reliable but can have delays
                "timestamp": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Yahoo Finance error: {str(e)}")
            return {}

    def get_market_news(self) -> List[Dict[str, Any]]:
        """Get market news with manipulation detection"""
        try:
            news_sources = [
                "https://feeds.finance.yahoo.com/rss/2.0/headline",
                "https://www.federalreserve.gov/feeds/press_all.xml",
                "https://www.cmegroup.com/rss/all-press-releases.xml"
            ]
            
            all_news = []
            
            for source_url in news_sources:
                try:
                    feed = feedparser.parse(source_url)
                    
                    for entry in feed.entries[:10]:  # Limit to recent 10
                        title = entry.get('title', '')
                        summary = entry.get('summary', entry.get('description', ''))
                        
                        # Detect potential manipulation
                        manipulation_score = self.detect_manipulation(title + " " + summary)
                        
                        # Calculate reliability based on source
                        reliability = self.calculate_source_reliability(source_url)
                        
                        all_news.append({
                            "title": title,
                            "summary": summary,
                            "source": source_url,
                            "published": entry.get('published'),
                            "manipulation_score": manipulation_score,
                            "reliability_score": reliability,
                            "timestamp": datetime.now()
                        })
                        
                except Exception as e:
                    logger.warning(f"Failed to parse {source_url}: {str(e)}")
                    continue
            
            return sorted(all_news, key=lambda x: x['reliability_score'], reverse=True)
            
        except Exception as e:
            logger.error(f"News gathering error: {str(e)}")
            return []

    def detect_manipulation(self, text: str) -> float:
        """Detect potential market manipulation in news/data"""
        text_lower = text.lower()
        
        manipulation_indicators = 0
        total_checks = 0
        
        # Check for sensational keywords
        for keyword in self.manipulation_keywords:
            total_checks += 1
            if keyword in text_lower:
                manipulation_indicators += 1
        
        # Check for excessive capitalization
        if text.isupper():
            manipulation_indicators += 1
        total_checks += 1
        
        # Check for excessive punctuation
        if text.count('!') > 2 or text.count('?') > 2:
            manipulation_indicators += 1
        total_checks += 1
        
        # Return manipulation score (0 = likely authentic, 1 = likely manipulated)
        return manipulation_indicators / total_checks if total_checks > 0 else 0

    def calculate_source_reliability(self, source_url: str) -> float:
        """Calculate reliability score based on source"""
        for trusted_domain in self.trusted_sources:
            if trusted_domain in source_url:
                return 0.9
        
        # Default reliability for unknown sources
        return 0.6

    async def get_comprehensive_market_analysis(self) -> Dict[str, Any]:
        """Get comprehensive market analysis from all sources"""
        try:
            # Gather data from all sources
            topstep_data = await self.get_topstep_data()
            yahoo_data = self.get_market_data_yahoo()
            news_data = self.get_market_news()
            
            # Combine and analyze
            analysis = {
                "timestamp": datetime.now(),
                "sources": {
                    "topstep": topstep_data,
                    "yahoo": yahoo_data,
                    "news": news_data
                },
                "market_summary": self.create_market_summary(yahoo_data),
                "manipulation_alerts": self.create_manipulation_alerts(news_data),
                "trading_recommendations": self.create_trading_recommendations(yahoo_data, news_data)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {str(e)}")
            return {"error": str(e), "timestamp": datetime.now()}

    def create_market_summary(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create market summary from price data"""
        if not market_data.get('data'):
            return {"status": "No market data available"}
        
        summary = {
            "overall_sentiment": "NEUTRAL",
            "instruments": {},
            "market_strength": 0
        }
        
        positive_moves = 0
        total_instruments = 0
        
        for symbol, data in market_data['data'].items():
            change_pct = data.get('change_percent', 0)
            
            if change_pct > 0.5:
                sentiment = "BULLISH"
                positive_moves += 1
            elif change_pct < -0.5:
                sentiment = "BEARISH"
            else:
                sentiment = "NEUTRAL"
            
            summary['instruments'][symbol] = {
                "sentiment": sentiment,
                "change_percent": change_pct,
                "strength": abs(change_pct)
            }
            
            total_instruments += 1
        
        # Overall market sentiment
        if total_instruments > 0:
            bullish_ratio = positive_moves / total_instruments
            if bullish_ratio > 0.6:
                summary['overall_sentiment'] = "BULLISH"
            elif bullish_ratio < 0.4:
                summary['overall_sentiment'] = "BEARISH"
        
        return summary

    def create_manipulation_alerts(self, news_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create alerts for potential market manipulation"""
        alerts = []
        
        for news_item in news_data:
            if news_item.get('manipulation_score', 0) > 0.3:
                alerts.append({
                    "level": "HIGH" if news_item['manipulation_score'] > 0.6 else "MEDIUM",
                    "title": news_item['title'],
                    "manipulation_score": news_item['manipulation_score'],
                    "reliability_score": news_item['reliability_score'],
                    "recommendation": "Exercise caution - potential market manipulation detected"
                })
        
        return alerts

    def create_trading_recommendations(self, market_data: Dict[str, Any], news_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create trading recommendations based on all data"""
        if not market_data.get('data'):
            return {"recommendation": "HOLD", "reason": "Insufficient market data"}
        
        # Calculate overall market strength
        total_strength = 0
        instrument_count = 0
        
        for symbol, data in market_data['data'].items():
            total_strength += abs(data.get('change_percent', 0))
            instrument_count += 1
        
        avg_strength = total_strength / instrument_count if instrument_count > 0 else 0
        
        # Check for manipulation alerts
        high_manipulation_alerts = sum(1 for alert in self.create_manipulation_alerts(news_data) 
                                     if alert.get('level') == 'HIGH')
        
        if high_manipulation_alerts > 0:
            return {
                "recommendation": "CAUTION",
                "reason": f"{high_manipulation_alerts} high-risk manipulation alerts detected",
                "confidence": 0.3
            }
        elif avg_strength > 1.0:
            return {
                "recommendation": "ACTIVE",
                "reason": f"Strong market movement detected (avg: {avg_strength:.1f}%)",
                "confidence": 0.8
            }
        else:
            return {
                "recommendation": "MONITOR",
                "reason": "Low volatility environment",
                "confidence": 0.6
            }

async def test_multi_source_data():
    """Test the multi-source market data system"""
    print("🔍 Testing Multi-Source Market Data System...")
    
    async with MultiSourceMarketData() as market_data:
        # Get comprehensive analysis
        analysis = await market_data.get_comprehensive_market_analysis()
        
        print(f"📊 Analysis Complete:")
        print(f"Market Summary: {analysis.get('market_summary', {}).get('overall_sentiment', 'N/A')}")
        print(f"Manipulation Alerts: {len(analysis.get('manipulation_alerts', []))}")
        print(f"Trading Recommendation: {analysis.get('trading_recommendations', {}).get('recommendation', 'N/A')}")
        
        return analysis

if __name__ == "__main__":
    # Test the system
    result = asyncio.run(test_multi_source_data())
    print(json.dumps(result, indent=2, default=str))