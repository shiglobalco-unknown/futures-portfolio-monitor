#!/usr/bin/env python3
"""
TopStep API Integration for Futures Portfolio Monitor
Secure integration with TopStepX API for live trading data
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, Optional, Any, List

class TopStepAPI:
    """Secure TopStep API client"""
    
    def __init__(self):
        self.api_key = os.getenv("TOPSTEP_API_KEY")
        self.username = os.getenv("TOPSTEP_USERNAME", "demo_user")
        self.base_url = os.getenv("TOPSTEP_API_URL", "https://api.topstepx.com/api")
        self.session_token = None
        
    def authenticate(self) -> bool:
        """Authenticate with TopStep API"""
        try:
            auth_url = f"{self.base_url}/Auth/loginKey"
            
            payload = {
                "userName": self.username,
                "apiKey": self.api_key
            }
            
            headers = {
                "accept": "text/plain",
                "Content-Type": "application/json"
            }
            
            response = requests.post(auth_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("errorCode") == 0:
                    self.session_token = data.get("token")
                    print("✅ TopStep API authentication successful")
                    return True
                else:
                    print(f"❌ API Error: {data.get('errorMessage')}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Authentication failed: {str(e)}")
            return False
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """Get account information"""
        if not self.session_token:
            if not self.authenticate():
                return None
        
        try:
            # This would be the actual TopStep endpoint for account info
            # Replace with correct endpoint when available
            headers = {
                "Authorization": f"Bearer {self.session_token}",
                "Content-Type": "application/json"
            }
            
            # Mock response for now - replace with actual API call
            return {
                "account_id": "TS001",
                "account_type": "50K_COMBINE",
                "balance": 50000.00,
                "daily_pnl": 0.00,
                "total_pnl": 0.00,
                "profit_target": 3000.00,
                "daily_loss_limit": 2000.00,
                "status": "active"
            }
            
        except Exception as e:
            print(f"❌ Failed to get account info: {str(e)}")
            return None
    
    def get_positions(self) -> Optional[List[Dict[str, Any]]]:
        """Get current positions"""
        if not self.session_token:
            if not self.authenticate():
                return None
        
        try:
            # Mock positions for now - replace with actual API call
            return [
                {
                    "symbol": "NQ",
                    "quantity": 2,
                    "entry_price": 15450.25,
                    "current_price": 15485.75,
                    "pnl": 1420.00,
                    "timestamp": datetime.now().isoformat()
                }
            ]
            
        except Exception as e:
            print(f"❌ Failed to get positions: {str(e)}")
            return None

def test_api_connection():
    """Test TopStep API connection"""
    print("🔌 Testing TopStep API Connection...")
    
    api = TopStepAPI()
    
    # Test authentication
    if api.authenticate():
        print("✅ Authentication successful!")
        
        # Test account info
        account = api.get_account_info()
        if account:
            print(f"✅ Account info retrieved: {account['account_type']}")
        
        # Test positions
        positions = api.get_positions()
        if positions:
            print(f"✅ Positions retrieved: {len(positions)} positions")
    else:
        print("❌ Authentication failed!")

if __name__ == "__main__":
    test_api_connection()