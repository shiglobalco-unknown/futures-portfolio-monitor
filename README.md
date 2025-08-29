# 🏛️ Futures Portfolio Monitor

**Professional Futures Portfolio Monitoring and Trading Dashboard**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Real-time P&L tracking • Risk compliance monitoring • Performance analytics*

## 🌟 Features

### 📊 **Live Performance Dashboard**
- **Real-time P&L tracking** with profit target progress
- **Daily P&L monitoring** with loss limit compliance
- **Unrealized P&L** for open positions
- **Evaluation progress** tracking

### ⚡ **Professional Trading Interface**
- **Demo trade execution** with market simulation
- **Position management** with real-time updates
- **Risk validation** before trade execution
- **Focus instruments**: NQ, ES, CL, GC

### 🛡️ **Advanced Risk Management**
- **TopStep rule compliance** monitoring
- **Daily loss limit** tracking with visual indicators
- **Position size** validation
- **Emergency controls** for risk management

### 🎯 **TopStep Integration**
- **50K & 150K Combine** account configurations
- **Complete rule enforcement** for evaluation phase
- **Consistency rule** monitoring
- **Professional compliance** dashboard

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation & Launch

```bash
# Clone the repository
git clone https://github.com/shi-ventures/futures-portfolio-monitor.git
cd futures-portfolio-monitor

# Install dependencies
pip install -r requirements.txt

# Launch the application
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## 🖥️ Screenshots

### Main Dashboard
![Dashboard Preview](docs/images/dashboard-preview.png)

### Trading Interface  
![Trading Interface](docs/images/trading-interface.png)

### Risk Management
![Risk Management](docs/images/risk-management.png)

## 📈 Account Configurations

### 50K Combine Account
- **Account Size**: $50,000
- **Profit Target**: $3,000
- **Daily Loss Limit**: $2,000
- **Max Position Size**: 5 contracts
- **Evaluation Days**: 30

### 150K Combine Account
- **Account Size**: $150,000
- **Profit Target**: $9,000
- **Daily Loss Limit**: $6,000
- **Max Position Size**: 10 contracts
- **Evaluation Days**: 30

## 🎯 Focus Instruments

| Symbol | Name | Point Value | Category |
|--------|------|-------------|----------|
| **NQ** | NASDAQ E-mini | $20.00 | Primary |
| **ES** | S&P 500 E-mini | $50.00 | Primary |
| **CL** | Crude Oil | $1,000.00 | Defensive |
| **GC** | Gold | $100.00 | Defensive |

## 🛡️ TopStep Compliance

### Evaluation Phase Rules
- ✅ Achieve profit target within 30 days
- ✅ Never exceed daily loss limit ($2K/$6K)
- ✅ Maintain trailing drawdown limits
- ✅ Respect position size restrictions (5/10 contracts)
- ✅ Best day cannot exceed 50% of total profit
- ✅ Trade minimum 5 days during evaluation

### Real-time Monitoring
- **Continuous compliance checking**
- **Automated violation alerts**
- **Risk level assessment**
- **Performance progress tracking**

## 🔧 Technical Stack

- **Frontend**: Streamlit with custom CSS styling
- **Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas & NumPy
- **Styling**: Professional dark theme with institutional design
- **Real-time Updates**: Automatic 3-second refresh cycle

## 📁 Project Structure

```
futures-portfolio-monitor/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── .gitignore           # Git ignore rules
├── docs/                # Documentation assets
│   └── images/          # Screenshots and diagrams
├── deploy/              # Deployment configurations
│   ├── streamlit_config.toml
│   └── docker/          # Docker deployment files
└── tests/               # Unit tests (future)
```

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Fork this repository
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy directly from GitHub

### Docker
```bash
# Build image
docker build -t topstep-monitor .

# Run container
docker run -p 8501:8501 topstep-monitor
```

### Heroku
```bash
# Install Heroku CLI and login
heroku create your-app-name
git push heroku main
```

## ⚠️ Important Disclaimers

### Demo Version
- **This is a DEMONSTRATION** version with simulated data
- **No real money** or actual trading is involved
- **Market data is SIMULATED** for educational purposes
- **Position management is for TESTING ONLY**

### Production Integration
- For **live trading**, integrate with actual TopStep API
- Implement **real market data** feeds
- Add **broker connectivity** for live execution
- Enable **proper risk management** systems

### Risk Warning
⚠️ **Futures trading involves substantial risk of loss and may not be suitable for all investors. Past performance is not indicative of future results. Only trade with risk capital you can afford to lose.**

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/shi-ventures/futures-portfolio-monitor.git
cd futures-portfolio-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.runOnSave true
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support the Project

If you find this project helpful, please consider:

- ⭐ **Starring** the repository
- 🍴 **Forking** for your own projects
- 🐛 **Reporting bugs** and requesting features
- 💡 **Contributing** improvements and enhancements

## 📞 Contact & Support

### Technical Support
- 📧 **Email**: support@shi-ventures.com
- 💬 **Discord**: [Shi Ventures Community](https://discord.gg/shi-ventures)
- 📱 **Twitter**: [@ShiVentures](https://twitter.com/ShiVentures)

### Professional Services
- 🏢 **Custom Development**: Enterprise trading solutions
- 🔌 **API Integration**: Real-time data and broker connectivity
- 📊 **Risk Management**: Institutional-grade compliance systems
- 🎓 **Training**: Professional trading technology workshops

---

**Built with ❤️ by [Shi Ventures](https://github.com/shi-ventures) • Professional Trading Technology**

*Empowering traders with institutional-grade technology and real-time market intelligence.*