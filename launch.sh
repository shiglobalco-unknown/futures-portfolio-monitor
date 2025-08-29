#!/bin/bash

# Futures Portfolio Monitor - Launch Script
# Professional futures trading dashboard for GitHub deployment

echo "================================================"
echo "🏛️ Futures Portfolio Monitor - Shi Ventures"
echo "================================================"
echo "Professional Futures Trading Dashboard"
echo "GitHub: https://github.com/shi-ventures/futures-portfolio-monitor"
echo "================================================"

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    echo "Please install Python 3.7+ from https://python.org"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found${NC}"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is required but not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 found${NC}"

# Install requirements
echo -e "${YELLOW}📦 Installing requirements...${NC}"
pip3 install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All packages installed successfully${NC}"
else
    echo -e "${RED}❌ Package installation failed${NC}"
    exit 1
fi

# Launch information
echo ""
echo -e "${BLUE}🚀 Launching Futures Portfolio Monitor...${NC}"
echo ""
echo -e "${YELLOW}📊 Dashboard Features:${NC}"
echo "  • Real-time P&L tracking"
echo "  • Strategy management with manual override"
echo "  • Risk compliance monitoring"
echo "  • Focus instruments (NQ, ES, CL, GC)"
echo "  • Professional institutional design"
echo ""
echo -e "${GREEN}🌐 Access the dashboard at: http://localhost:8501${NC}"
echo -e "${YELLOW}⚠️  This is a DEMO with simulated data${NC}"
echo ""
echo -e "${BLUE}🌟 Star us on GitHub: https://github.com/shi-ventures/futures-portfolio-monitor${NC}"
echo ""

# Launch Streamlit
streamlit run app.py