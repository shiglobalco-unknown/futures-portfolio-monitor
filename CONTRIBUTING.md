# Contributing to Futures Portfolio Monitor

Thank you for your interest in contributing to Futures Portfolio Monitor! This document provides guidelines and information for contributors.

## 🤝 Ways to Contribute

### 🐛 Bug Reports
- Use the GitHub issue tracker
- Include detailed steps to reproduce
- Provide system information (OS, Python version, etc.)
- Include error messages and screenshots

### ✨ Feature Requests
- Check existing issues first
- Describe the feature clearly
- Explain the use case and benefits
- Consider implementation complexity

### 💻 Code Contributions
- Fork the repository
- Create a feature branch
- Follow coding standards
- Include tests if applicable
- Update documentation

## 🚀 Development Setup

### Prerequisites
- Python 3.7 or higher
- Git
- Text editor or IDE

### Local Development
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/futures-portfolio-monitor.git
cd futures-portfolio-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.runOnSave true
```

## 📝 Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings for functions and classes
- Keep functions focused and small

### Streamlit Best Practices
- Use session state for persistent data
- Implement proper error handling
- Optimize performance with caching
- Maintain responsive design

### Code Structure
```python
def function_name(param: type) -> return_type:
    """
    Brief description of function.
    
    Args:
        param: Description of parameter
        
    Returns:
        Description of return value
    """
    # Implementation here
```

## 🔧 Technical Guidelines

### File Organization
- Keep main app logic in `app.py`
- Use helper functions for complex operations
- Separate configuration from logic
- Group related functionality

### Performance Considerations
- Minimize API calls and data processing
- Use Streamlit caching where appropriate
- Optimize chart rendering
- Handle large datasets efficiently

### UI/UX Standards
- Maintain consistent styling
- Ensure responsive design
- Use clear, professional language
- Provide helpful error messages

## 🧪 Testing

### Manual Testing
- Test all interactive features
- Verify responsive design
- Check error handling
- Validate calculations

### Automated Testing (Future)
```bash
# Run tests when available
pytest tests/

# Check code style
flake8 app.py

# Type checking
mypy app.py
```

## 📋 Pull Request Process

### Before Submitting
1. **Test thoroughly** - Ensure your changes work
2. **Update documentation** - Modify README if needed
3. **Check code style** - Follow Python conventions
4. **Verify dependencies** - Update requirements.txt if needed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Manual testing completed
- [ ] No breaking changes
- [ ] Documentation updated

## Screenshots (if applicable)
Include screenshots for UI changes
```

### Review Process
1. Automated checks must pass
2. Code review by maintainers
3. Testing on different environments
4. Merge after approval

## 🌟 Recognition

### Contributors
All contributors will be recognized in:
- GitHub contributors list
- README acknowledgments
- Release notes (for significant contributions)

### Types of Contributions
- 💻 **Code** - Implementation and fixes
- 📖 **Documentation** - README, guides, comments
- 🎨 **Design** - UI/UX improvements
- 🐛 **Testing** - Bug reports and testing
- 💡 **Ideas** - Feature suggestions and feedback

## 📞 Getting Help

### Communication Channels
- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - General questions and ideas
- **Email** - Direct contact for sensitive issues

### Response Times
- Issues: 1-3 business days
- Pull Requests: 3-7 business days
- Questions: 1-2 business days

## 📜 Code of Conduct

### Our Standards
- Use welcoming and inclusive language
- Respect different viewpoints and experiences
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Unacceptable Behavior
- Harassment or discriminatory language
- Personal attacks or trolling
- Spam or off-topic discussions
- Sharing private information without permission

## 🎯 Development Priorities

### Current Focus Areas
1. **Performance Optimization** - Faster load times
2. **Mobile Responsiveness** - Better mobile experience
3. **Real-time Features** - Enhanced live updates
4. **Testing Coverage** - Automated test suite

### Future Enhancements
- Integration with real trading APIs
- Advanced charting capabilities
- User authentication system
- Portfolio analytics

## 📚 Resources

### Streamlit Documentation
- [Streamlit Docs](https://docs.streamlit.io/)
- [API Reference](https://docs.streamlit.io/library/api-reference)
- [Best Practices](https://docs.streamlit.io/library/advanced-features)

### Python Resources
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Python Typing](https://docs.python.org/3/library/typing.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Trading & Finance
- [TopStep Documentation](https://www.topsteptrader.com/)
- [Futures Trading Basics](https://www.cmegroup.com/education)
- [Risk Management Principles](https://www.investopedia.com/risk-management/)

---

**Thank you for contributing to Futures Portfolio Monitor! Together, we're building better trading technology.** 🚀

*For questions about contributing, please contact: contribute@shi-ventures.com*