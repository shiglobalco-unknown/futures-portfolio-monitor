"""
Futures Portfolio Monitor - Professional Trading Dashboard
Created by: Shi Ventures
GitHub: https://github.com/shi-ventures/futures-portfolio-monitor

Professional futures portfolio monitoring and trading dashboard
Real-time P&L tracking • Risk compliance monitoring • Performance analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import numpy as np
from typing import Dict, List, Any
import time

# Page configuration
st.set_page_config(
    page_title="Futures Portfolio Monitor | Shi Ventures",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced TopStep Configurations
TOPSTEP_CONFIGS = {
    "50K_COMBINE": {
        "account_size": 50000.0,
        "profit_target": 3000.0,
        "daily_loss_limit": 2000.0,
        "max_total_loss": 2500.0,
        "max_position_size": 5,
        "max_overnight_positions": 3,
        "consistency_requirement": 0.5,
        "evaluation_days": 30,
        "monthly_fee": 49.0
    },
    "100K_COMBINE": {
        "account_size": 100000.0,
        "profit_target": 6000.0,
        "daily_loss_limit": 3000.0,
        "max_total_loss": 4000.0,
        "max_position_size": 10,
        "max_overnight_positions": 5,
        "consistency_requirement": 0.5,
        "evaluation_days": 30,
        "monthly_fee": 99.0
    },
    "150K_COMBINE": {
        "account_size": 150000.0,
        "profit_target": 9000.0,
        "daily_loss_limit": 4500.0,
        "max_total_loss": 6000.0,
        "max_position_size": 15,
        "max_overnight_positions": 7,
        "consistency_requirement": 0.5,
        "evaluation_days": 30,
        "monthly_fee": 149.0
    }
}

# Trading Strategies Configuration
TRADING_STRATEGIES = {
    "AI_AUTONOMOUS": {
        "name": "AI Autonomous Trading",
        "description": "Fully automated AI-driven strategy with machine learning",
        "risk_level": "Medium",
        "time_frame": "Multiple",
        "instruments": ["NQ", "ES", "CL", "GC"],
        "color": "#2c5aa0",
        "features": [
            "Real-time market analysis",
            "Dynamic position sizing",
            "Multi-timeframe signals",
            "Adaptive risk management"
        ]
    },
    "MOMENTUM_BREAKOUT": {
        "name": "Momentum Breakout",
        "description": "Capitalize on strong price movements and breakouts",
        "risk_level": "High",
        "time_frame": "5m-15m",
        "instruments": ["NQ", "ES"],
        "color": "#ff6b35",
        "features": [
            "Volume confirmation",
            "Support/resistance levels",
            "Momentum indicators",
            "Quick profit targets"
        ]
    },
    "MEAN_REVERSION": {
        "name": "Mean Reversion",
        "description": "Trade counter-trend moves back to statistical mean",
        "risk_level": "Low",
        "time_frame": "15m-1h",
        "instruments": ["ES", "CL", "GC"],
        "color": "#4fc3f7",
        "features": [
            "Statistical analysis",
            "Overbought/oversold levels",
            "Risk-adjusted entries",
            "Conservative targets"
        ]
    },
    "SCALPING_PREMIUM": {
        "name": "Premium Scalping",
        "description": "High-frequency small profit captures",
        "risk_level": "Very High",
        "time_frame": "1m-5m",
        "instruments": ["NQ", "ES"],
        "color": "#ffa726",
        "features": [
            "Ultra-fast execution",
            "Level 2 data analysis",
            "Minimal drawdown",
            "High win rate focus"
        ]
    },
    "SWING_TRADING": {
        "name": "Swing Trading",
        "description": "Multi-day trend following strategy",
        "risk_level": "Medium",
        "time_frame": "4h-1D",
        "instruments": ["CL", "GC", "ES"],
        "color": "#ab47bc",
        "features": [
            "Trend identification",
            "Multi-day holds",
            "Fundamental analysis",
            "Lower frequency trades"
        ]
    },
    "NEWS_MOMENTUM": {
        "name": "News Momentum",
        "description": "Trade on economic news and events",
        "risk_level": "High",
        "time_frame": "1m-30m",
        "instruments": ["NQ", "ES", "CL"],
        "color": "#e91e63",
        "features": [
            "Economic calendar integration",
            "Volatility expansion",
            "Event-driven entries",
            "Quick reaction times"
        ]
    },
    "MANUAL_OVERRIDE": {
        "name": "Manual Override",
        "description": "Full manual control with strategy assistance",
        "risk_level": "Variable",
        "time_frame": "User Defined",
        "instruments": ["NQ", "ES", "CL", "GC"],
        "color": "#9c27b0",
        "features": [
            "Complete user control",
            "Strategy suggestions",
            "Risk validation",
            "Performance tracking"
        ]
    }
}

# Focus Instruments Configuration
FOCUS_INSTRUMENTS = {
    "NQ": {
        "name": "NASDAQ E-mini",
        "point_value": 20.0,
        "tick_size": 0.25,
        "margin": 16500.0,
        "color": "#00ff88",
        "priority": "primary"
    },
    "ES": {
        "name": "S&P 500 E-mini", 
        "point_value": 50.0,
        "tick_size": 0.25,
        "margin": 12650.0,
        "color": "#4fc3f7",
        "priority": "primary"
    },
    "CL": {
        "name": "Crude Oil",
        "point_value": 1000.0,
        "tick_size": 0.01,
        "margin": 4950.0,
        "color": "#ffa726",
        "priority": "defensive"
    },
    "GC": {
        "name": "Gold",
        "point_value": 100.0,
        "tick_size": 0.10,
        "margin": 9900.0,
        "color": "#ffd700",
        "priority": "defensive"
    }
}

# Professional CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
        color: #111827;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stActionButton {visibility: hidden;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    
    /* Schwab-style data cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        padding: 20px;
        margin: 10px 0;
    }
    
    .metric-card:hover {
        border-color: #2c5aa0;
    }
    
    /* Schwab-style buttons */
    .trading-button {
        background: #2c5aa0;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 14px;
        cursor: pointer;
    }
    
    .trading-button:hover {
        background: #1e40af;
    }
    
    /* Schwab-style data tables */
    .data-table {
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .table-header {
        background: #f8f9fa;
        border-bottom: 1px solid #e5e5e5;
        padding: 12px 16px;
        font-weight: 600;
        color: #111827;
    }
    
    .table-row {
        border-bottom: 1px solid #f1f1f1;
        padding: 12px 16px;
    }
    
    .table-row:last-child {
        border-bottom: none;
    }
    
    .position-card {
        background: #ffffff;
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        padding: 16px;
        margin: 8px 0;
    }
    
    .gain { 
        color: #10b981; 
        font-weight: 500; 
    }
    
    .loss { 
        color: #ef4444; 
        font-weight: 500; 
    }
    
    /* Monospace for prices */
    .mono {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }
    
    /* Schwab-style status text */
    .status-open { 
        color: #10b981; 
        font-weight: 600; 
    }
    
    .status-closed { 
        color: #6b7280; 
        font-weight: 600; 
    }
    
    .status-warning { 
        color: #f59e0b; 
        font-weight: 600; 
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Risk level indicators */
    .risk-critical {
        background: #ef4444;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
        animation: pulse 1.5s infinite;
    }
    
    .risk-high {
        background: #f59e0b;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
    }
    
    .risk-low {
        background: #10b981;
        color: #ffffff;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 12px;
    }

    /* GitHub link styling */
    .github-link {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: rgba(44, 90, 160, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 14px;
        color: #111827;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .github-link:hover {
        background: rgba(44, 90, 160, 0.2);
        transform: translateY(-2px);
        color: #2c5aa0;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

# Add GitHub link
st.markdown("""
<a href="https://github.com/shi-ventures/futures-portfolio-monitor" target="_blank" class="github-link">
    🌟 Star on GitHub
</a>
""", unsafe_allow_html=True)

class TopStepDashboard:
    def __init__(self):
        # Initialize session state
        if 'account_type' not in st.session_state:
            st.session_state.account_type = "50K_COMBINE"
        if 'positions' not in st.session_state:
            st.session_state.positions = []
        if 'daily_pnl' not in st.session_state:
            st.session_state.daily_pnl = 0.0
        if 'total_pnl' not in st.session_state:
            st.session_state.total_pnl = 0.0
        if 'alerts' not in st.session_state:
            st.session_state.alerts = []
        if 'trade_history' not in st.session_state:
            st.session_state.trade_history = []
        if 'current_strategy' not in st.session_state:
            st.session_state.current_strategy = "AI_AUTONOMOUS"
        if 'strategy_override' not in st.session_state:
            st.session_state.strategy_override = False
        if 'manual_signals' not in st.session_state:
            st.session_state.manual_signals = []
    
    def get_account_config(self):
        return TOPSTEP_CONFIGS[st.session_state.account_type]
    
    def add_alert(self, message, alert_type="info"):
        st.session_state.alerts.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "message": message,
            "type": alert_type,
            "timestamp": datetime.now()
        })
        if len(st.session_state.alerts) > 20:
            st.session_state.alerts = st.session_state.alerts[-20:]
    
    def get_real_time_data(self):
        """Simulate real-time market data updates"""
        config = self.get_account_config()
        
        # Update position prices with market simulation
        if st.session_state.positions:
            for pos in st.session_state.positions:
                # Simulate price movement
                volatility = 0.5 if pos["symbol"] in ["NQ", "ES"] else 0.2
                price_change = np.random.normal(0, volatility)
                pos["current_price"] += price_change
                
                # Recalculate P&L
                instrument = FOCUS_INSTRUMENTS.get(pos["symbol"], {})
                point_value = instrument.get("point_value", 50.0)
                
                if pos["quantity"] > 0:  # Long
                    pos["unrealized_pnl"] = (pos["current_price"] - pos["entry_price"]) * pos["quantity"] * point_value
                else:  # Short
                    pos["unrealized_pnl"] = (pos["entry_price"] - pos["current_price"]) * abs(pos["quantity"]) * point_value
        
        # Calculate current metrics
        unrealized_pnl = sum(pos.get("unrealized_pnl", 0) for pos in st.session_state.positions)
        current_daily_pnl = st.session_state.daily_pnl + unrealized_pnl
        current_total_pnl = st.session_state.total_pnl + unrealized_pnl
        
        return {
            "account_id": f"TS_{st.session_state.account_type}_001",
            "account_type": st.session_state.account_type,
            "current_balance": config["account_size"] + current_total_pnl,
            "total_pnl": current_total_pnl,
            "daily_pnl": current_daily_pnl,
            "unrealized_pnl": unrealized_pnl,
            "profit_target_progress": (current_total_pnl / config["profit_target"]) * 100,
            "days_remaining": 18,  # Mock value
            "daily_loss_used": abs(min(0, current_daily_pnl)) / config["daily_loss_limit"] * 100,
            "position_count": len(st.session_state.positions),
            "trade_count": len(st.session_state.trade_history),
            "last_update": datetime.now()
        }

def render_header():
    """Professional header with branding and account selection"""
    
    dashboard = TopStepDashboard()
    config = dashboard.get_account_config()
    data = dashboard.get_real_time_data()
    
    # Main title with GitHub attribution
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="font-size: 3.5rem; font-weight: 900; 
                   background: #10b981; 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   margin-bottom: 10px; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            Futures Portfolio Monitor
        </h1>
        <p style="font-size: 1.3rem; opacity: 0.8; margin-bottom: 5px;">
            Professional Trading Dashboard • 
            <a href="https://github.com/shi-ventures" style="color: #00ff88; text-decoration: none;">Shi Ventures</a>
        </p>
        <p style="font-size: 1rem; opacity: 0.6;">
            Real-time compliance • Risk management • Performance analytics
        </p>
        <p style="font-size: 0.9rem; opacity: 0.5; margin-top: 10px;">
            🌟 <a href="https://github.com/shi-ventures/futures-portfolio-monitor" 
                  style="color: #4fc3f7; text-decoration: none;">Open Source on GitHub</a> • 
            Demo Version with Simulated Data
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Account selector and status
    col1, col2, col3 = st.columns([2, 2, 3])
    
    with col1:
        new_account_type = st.selectbox(
            "Account Configuration",
            ["50K_COMBINE", "100K_COMBINE", "150K_COMBINE"],
            index=0 if st.session_state.account_type == "50K_COMBINE" else (1 if st.session_state.account_type == "100K_COMBINE" else 2),
            key="account_selector"
        )
        if new_account_type != st.session_state.account_type:
            st.session_state.account_type = new_account_type
            dashboard.add_alert(f"Switched to {new_account_type} configuration", "info")
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="margin: 0;">
            <div style="font-size: 14px; opacity: 0.8; margin-bottom: 8px;">ACCOUNT SIZE</div>
            <div style="font-size: 24px; font-weight: 800; color: #2c5aa0; margin-bottom: 5px;">
                ${config['account_size']:,.0f}
            </div>
            <div style="font-size: 12px; opacity: 0.7;">Daily Limit: ${config['daily_loss_limit']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_time = datetime.now().strftime("%H:%M:%S EST")
        market_status = " OPEN" if 9 <= datetime.now().hour < 16 else " CLOSED"
        
        st.markdown(f"""
        <div class="metric-card" style="margin: 0; text-align: center;">
            <div style="font-size: 20px; font-weight: 700; color: #2c5aa0; margin-bottom: 8px;">
                <span class="status-indicator status-live"></span>DEMO MODE
            </div>
            <div style="font-size: 16px; opacity: 0.9; margin-bottom: 3px;">{current_time}</div>
            <div style="font-size: 14px; opacity: 0.7;">{market_status}</div>
        </div>
        """, unsafe_allow_html=True)

def render_live_metrics():
    """Live metrics dashboard"""
    
    dashboard = TopStepDashboard()
    data = dashboard.get_real_time_data()
    config = dashboard.get_account_config()
    
    st.markdown("### 📈 Live Performance Dashboard")
    
    # Main metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        profit_progress = (data["total_pnl"] / config["profit_target"]) * 100
        progress_color = "#10b981" if data["total_pnl"] >= 0 else "#dc2626"
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 14px; opacity: 0.8;">TOTAL P&L</div>
                <div style="font-size: 12px; padding: 4px 8px; background: rgba(44,90,160,0.2); 
                            border-radius: 12px; color: #2c5aa0;">
                    {profit_progress:+.1f}%
                </div>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: {progress_color}; margin-bottom: 8px;">
                ${data["total_pnl"]:+,.2f}
            </div>
            <div style="font-size: 12px; opacity: 0.7;">
                Target: ${config["profit_target"]:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        daily_loss_used = data["daily_loss_used"]
        if daily_loss_used > 85:
            daily_status = "risk-critical"
            daily_color = "#dc2626"
        elif daily_loss_used > 60:
            daily_status = "risk-high"
            daily_color = "#f59e0b"
        else:
            daily_status = "risk-low"
            daily_color = "#10b981"
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-size: 14px; opacity: 0.8;">DAILY P&L</div>
                <div class="{daily_status}" style="font-size: 10px;">
                    {daily_loss_used:.1f}%
                </div>
            </div>
            <div style="font-size: 28px; font-weight: 800; color: {daily_color}; margin-bottom: 8px;">
                ${data["daily_pnl"]:+,.2f}
            </div>
            <div style="font-size: 12px; opacity: 0.7;">
                Limit: ${config["daily_loss_limit"]:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        unrealized_color = "#10b981" if data["unrealized_pnl"] >= 0 else "#dc2626"
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; opacity: 0.8; margin-bottom: 15px;">UNREALIZED P&L</div>
            <div style="font-size: 28px; font-weight: 800; color: {unrealized_color}; margin-bottom: 8px;">
                ${data["unrealized_pnl"]:+,.2f}
            </div>
            <div style="font-size: 12px; opacity: 0.7;">
                {data["position_count"]} open positions
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        days_remaining = data["days_remaining"]
        days_color = "#dc2626" if days_remaining < 7 else "#f59e0b" if days_remaining < 14 else "#10b981"
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 14px; opacity: 0.8; margin-bottom: 15px;">EVALUATION</div>
            <div style="font-size: 28px; font-weight: 800; color: {days_color}; margin-bottom: 8px;">
                {days_remaining} days
            </div>
            <div style="font-size: 12px; opacity: 0.7;">
                remaining of 30 total
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_strategy_section():
    """Strategy selection and override interface"""
    
    st.markdown("### Strategy Management")
    
    dashboard = TopStepDashboard()
    
    # Strategy overview
    current_strategy = TRADING_STRATEGIES[st.session_state.current_strategy]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Current strategy display
        st.markdown(f"""
        <div style="background: {current_strategy['color']}15;
                    border-left: 4px solid {current_strategy['color']}; border-radius: 12px; padding: 25px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <h4 style="color: {current_strategy['color']}; margin: 0;"> Active Strategy</h4>
                <div style="background: {current_strategy['color']}; color: #0f1419; padding: 4px 12px; 
                            border-radius: 20px; font-size: 12px; font-weight: 600;">
                    {current_strategy['risk_level']} Risk
                </div>
            </div>
            <div style="font-size: 20px; font-weight: 700; margin-bottom: 8px;">{current_strategy['name']}</div>
            <div style="font-size: 14px; opacity: 0.9; margin-bottom: 15px;">{current_strategy['description']}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; font-size: 13px;">
                <div><strong>Time Frame:</strong> {current_strategy['time_frame']}</div>
                <div><strong>Instruments:</strong> {', '.join(current_strategy['instruments'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Strategy features
        st.markdown("**Strategy Features:**")
        for feature in current_strategy['features']:
            st.markdown(f"• {feature}")
    
    with col2:
        # Strategy override toggle
        override_enabled = st.checkbox(
            "Manual Override", 
            value=st.session_state.strategy_override,
            help="Override AI strategy with manual control"
        )
        
        if override_enabled != st.session_state.strategy_override:
            st.session_state.strategy_override = override_enabled
            if override_enabled:
                st.session_state.current_strategy = "MANUAL_OVERRIDE"
                dashboard.add_alert("Manual override activated", "warning")
            else:
                st.session_state.current_strategy = "AI_AUTONOMOUS"
                dashboard.add_alert(" Returned to AI autonomous trading", "success")
            st.rerun()
        
        # Quick return to AI button
        if st.session_state.strategy_override:
            if st.button(" Return to AI Trading", type="secondary", key="return_to_ai"):
                st.session_state.strategy_override = False
                st.session_state.current_strategy = "AI_AUTONOMOUS"
                dashboard.add_alert(" Returned to AI autonomous trading", "success")
                st.rerun()
    
    st.markdown("---")
    
    # Strategy selection interface
    with st.expander("📋 Select Different Strategy", expanded=False):
        st.markdown("**Available Trading Strategies:**")
        
        # Strategy grid
        cols = st.columns(2)
        strategies = list(TRADING_STRATEGIES.keys())
        
        for i, strategy_key in enumerate(strategies):
            strategy = TRADING_STRATEGIES[strategy_key]
            
            with cols[i % 2]:
                # Strategy card
                is_active = strategy_key == st.session_state.current_strategy
                border_style = f"border: 2px solid {strategy['color']};" if is_active else "border: 1px solid rgba(255,255,255,0.1);"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); {border_style}
                            border-radius: 8px; padding: 15px; margin: 10px 0; cursor: pointer;
                            transition: all 0.3s ease;">
                    <div style="color: {strategy['color']}; font-weight: 700; font-size: 16px; margin-bottom: 8px;">
                        {strategy['name']} {'[ACTIVE]' if is_active else ''}
                    </div>
                    <div style="font-size: 13px; opacity: 0.8; margin-bottom: 10px;">
                        {strategy['description']}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px;">
                        <span style="background: {strategy['color']}20; padding: 2px 6px; border-radius: 4px;">
                            {strategy['risk_level']} Risk
                        </span>
                        <span style="opacity: 0.7;">{strategy['time_frame']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Strategy selection button
                if st.button(f"Select {strategy['name']}", key=f"select_{strategy_key}", disabled=is_active):
                    st.session_state.current_strategy = strategy_key
                    if strategy_key == "MANUAL_OVERRIDE":
                        st.session_state.strategy_override = True
                        dashboard.add_alert(f"Switched to {strategy['name']}", "warning")
                    else:
                        st.session_state.strategy_override = False
                        dashboard.add_alert(f"Strategy changed to {strategy['name']}", "info")
                    st.rerun()
    
    # Manual signals interface (only show if manual override is active)
    if st.session_state.strategy_override:
        st.markdown("---")
        st.markdown("###  Manual Trading Signals")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="background: rgba(0, 255, 136, 0.1); border-radius: 8px; padding: 15px;">
                <div style="color: #00ff88; font-weight: 600; margin-bottom: 8px;"> BULLISH SIGNALS</div>
                <div style="font-size: 13px; line-height: 1.5;">
                    • Volume breakout detected<br>
                    • RSI oversold recovery<br>
                    • Support level bounce<br>
                    • Bullish divergence forming
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255, 68, 68, 0.1); border-radius: 8px; padding: 15px;">
                <div style="color: #ff4444; font-weight: 600; margin-bottom: 8px;"> BEARISH SIGNALS</div>
                <div style="font-size: 13px; line-height: 1.5;">
                    • Resistance level rejection<br>
                    • RSI overbought condition<br>
                    • Volume declining<br>
                    • Bearish divergence spotted
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style="background: rgba(255, 167, 38, 0.1); border-radius: 8px; padding: 15px;">
                <div style="color: #ffa726; font-weight: 600; margin-bottom: 8px;">⚠️ NEUTRAL SIGNALS</div>
                <div style="font-size: 13px; line-height: 1.5;">
                    • Consolidation pattern<br>
                    • Mixed market sentiment<br>
                    • Low volatility environment<br>
                    • Awaiting catalyst
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Manual signal input
        st.markdown("**Add Manual Signal:**")
        signal_col1, signal_col2, signal_col3, signal_col4 = st.columns(4)
        
        with signal_col1:
            signal_instrument = st.selectbox("Instrument", ["NQ", "ES", "CL", "GC"], key="manual_signal_instrument")
        
        with signal_col2:
            signal_direction = st.selectbox("Signal", ["BULLISH", "BEARISH", "NEUTRAL"], key="manual_signal_direction")
        
        with signal_col3:
            signal_strength = st.selectbox("Strength", ["WEAK", "MODERATE", "STRONG"], key="manual_signal_strength")
        
        with signal_col4:
            st.write("")
            if st.button(" Add Signal", key="add_manual_signal"):
                new_signal = {
                    "instrument": signal_instrument,
                    "direction": signal_direction,
                    "strength": signal_strength,
                    "timestamp": datetime.now(),
                    "time_str": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state.manual_signals.append(new_signal)
                dashboard.add_alert(f" Manual {signal_direction} signal added for {signal_instrument}", "info")
                st.rerun()
        
        # Display recent manual signals
        if st.session_state.manual_signals:
            st.markdown("**Recent Manual Signals:**")
            recent_signals = st.session_state.manual_signals[-5:]  # Show last 5
            
            for signal in reversed(recent_signals):
                direction_color = {
                    "BULLISH": "#00ff88",
                    "BEARISH": "#ff4444", 
                    "NEUTRAL": "#ffa726"
                }[signal["direction"]]
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid {direction_color};
                            border-radius: 6px; padding: 10px; margin: 5px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: {direction_color}; font-weight: 600;">{signal['instrument']}</span>
                            <span style="margin: 0 10px;">•</span>
                            <span>{signal['direction']}</span>
                            <span style="margin: 0 10px;">•</span>
                            <span style="font-size: 12px; opacity: 0.8;">{signal['strength']} strength</span>
                        </div>
                        <div style="font-size: 12px; opacity: 0.7;">{signal['time_str']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_trading_interface():
    """Trading interface with position management"""
    
    st.markdown("### Trading Interface")
    
    dashboard = TopStepDashboard()
    config = dashboard.get_account_config()
    
    with st.expander("📈 Execute Demo Trade", expanded=False):
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            symbol = st.selectbox("Instrument", list(FOCUS_INSTRUMENTS.keys()))
        
        with col2:
            side = st.selectbox("Side", ["BUY", "SELL"])
        
        with col3:
            quantity = st.number_input("Contracts", min_value=1, max_value=config["max_position_size"], value=1)
        
        with col4:
            # Mock real-time prices
            current_prices = {"NQ": 16850.25, "ES": 4205.50, "CL": 78.45, "GC": 2025.30}
            base_price = current_prices[symbol]
            market_price = base_price + np.random.normal(0, base_price * 0.001)
            price = st.number_input("Price", value=market_price, step=0.25, format="%.2f")
        
        with col5:
            st.write("")
            st.write("")
            if st.button(" Execute Demo Trade", type="primary", key="execute_trade"):
                # Add position
                new_position = {
                    "id": f"POS_{len(st.session_state.positions) + 1}",
                    "symbol": symbol,
                    "quantity": quantity if side == "BUY" else -quantity,
                    "entry_price": price,
                    "current_price": price,
                    "unrealized_pnl": 0.0,
                    "entry_time": datetime.now().strftime("%H:%M:%S"),
                    "side": side,
                    "timestamp": datetime.now()
                }
                st.session_state.positions.append(new_position)
                st.session_state.trade_history.append({
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "symbol": symbol,
                    "side": side,
                    "quantity": quantity,
                    "price": price,
                    "status": "FILLED"
                })
                dashboard.add_alert(f"✅ {side} {quantity} {symbol} @ ${price:.2f}", "success")
                st.success(f"✅ Demo trade executed: {side} {quantity} {symbol} @ ${price:.2f}")
                time.sleep(1)
                st.rerun()

def render_disclaimer():
    """Important disclaimer about demo nature"""
    
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(255, 167, 38, 0.1); border: 2px solid #ffa726; border-radius: 12px; padding: 20px; margin: 20px 0;">
        <h4 style="color: #ffa726; margin-bottom: 15px;">⚠️ Important Disclaimer</h4>
        <div style="font-size: 14px; line-height: 1.6;">
            <p><strong>This is a DEMO application with simulated data for educational purposes only.</strong></p>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>No real money or actual trading is involved</li>
                <li>Market data and P&L calculations are simulated</li>
                <li>For production use, integrate with actual TopStep API</li>
                <li>Always follow proper risk management in live trading</li>
            </ul>
            <p style="margin-top: 15px; font-weight: 600;">
                🌟 <a href="https://github.com/shi-ventures/futures-portfolio-monitor" 
                     style="color: #00ff88; text-decoration: none;">Star this project on GitHub</a> 
                to support development!
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application"""
    
    # Header
    render_header()
    
    st.markdown("---")
    
    # Live metrics
    render_live_metrics()
    
    st.markdown("---")
    
    # Strategy section
    render_strategy_section()
    
    st.markdown("---")
    
    # Trading interface
    render_trading_interface()
    
    # Show positions if any exist
    if st.session_state.positions:
        st.markdown("### 📊 Current Positions")
        for i, pos in enumerate(st.session_state.positions):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                instrument = FOCUS_INSTRUMENTS.get(pos["symbol"], {})
                pnl_color = "#00ff88" if pos["unrealized_pnl"] >= 0 else "#ff4444"
                
                st.markdown(f"""
                <div class="position-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-size: 18px; font-weight: 700; color: {'#00ff88' if pos['quantity'] > 0 else '#ff4444'};">
                                {pos["symbol"]} {pos["side"]} • {abs(pos["quantity"])} contracts
                            </div>
                            <div style="font-size: 14px; opacity: 0.8;">
                                {instrument.get('name', pos["symbol"])} • Entry: ${pos["entry_price"]:.2f} • Current: ${pos["current_price"]:.2f}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 24px; font-weight: 800; color: {pnl_color};">
                                ${pos["unrealized_pnl"]:+.2f}
                            </div>
                            <div style="font-size: 12px; opacity: 0.7;">Opened: {pos["entry_time"]}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"Close", key=f"close_{i}"):
                    st.session_state.daily_pnl += pos["unrealized_pnl"]
                    st.session_state.total_pnl += pos["unrealized_pnl"]
                    st.session_state.positions.pop(i)
                    st.rerun()
    
    # Disclaimer
    render_disclaimer()
    
    # Auto-refresh
    time.sleep(3)
    st.rerun()

if __name__ == "__main__":
    main()