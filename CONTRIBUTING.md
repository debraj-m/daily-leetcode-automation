# Contributing to LeetCode Daily Solver

Thank you for interest in contributing! Please follow these guidelines.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/leetcode-solver.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make changes
5. Test thoroughly
6. Push to your fork
7. Create a Pull Request

## Development Setup

```bash
# Clone and setup
git clone https://github.com/your-username/leetcode-solver.git
cd leetcode-solver

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies + dev tools
pip install -r requirements.txt
pip install black flake8 pytest

# Create .env for testing
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Code Style

- Use **Black** for formatting: `black solver.py`
- Follow **PEP 8** style guide
- Use meaningful variable names
- Add docstrings to functions
- Max line length: 100 characters

```bash
black solver.py
flake8 solver.py
```

## Testing

Before submitting a PR:

1. Test manually: `python3 solver.py`
2. Verify submission logs to `solved_log.json`
3. Check different problem types work
4. Test with different browsers/OS if possible

## What to Contribute

✅ **Ideas Welcome**
- Bug fixes
- Performance improvements
- New language support (Python, Java, C#, etc.)
- Better documentation
- Code refactoring
- Error handling improvements

❌ **Please Don't**
- Submit credentials or API keys
- Make unrelated changes
- Remove safety/security features
- Change license without discussion

## Pull Request Process

1. **Title**: Clear, descriptive title
   - ✅ "Add Python language support"
   - ❌ "Fix stuff"

2. **Description**: Explain what and why
   ```
   ## What
   Adds support for solving problems in Python
   
   ## Why
   Users requested Python support
   
   ## How
   - Updated language detection
   - Added Python template extraction
   - Modified solution generation prompt
   ```

3. **Testing**: Include output/logs
   ```
   Tested successfully:
   - Problem: Two Sum (Easy)
   - Language: Python
   - Status: ACCEPTED
   ```

4. **Code Review**: Address feedback promptly

## Reporting Issues

Use GitHub Issues with:

**Title**: One-line summary
```
Login fails with "Browser timeout"
```

**Description**: Include
- Python version: `python3 --version`
- OS: macOS/Linux/Windows
- Error message (full traceback)
- Steps to reproduce
- Expected vs actual behavior

**Example**:
```
**Python**: 3.9.10
**OS**: macOS 12.2
**Error**: 
```
selenium.common.exceptions.TimeoutException: Browser failed to open
```

**Steps**:
1. Run `python3 solver.py`
2. Wait for browser to open
3. Login doesn't appear

**Expected**: Browser opens to LeetCode login
**Actual**: Chrome crashes silently
```

## Language Support

To add a new language (e.g., Python):

1. **Update `get_language_template()`** - Extract Python snippet
2. **Update `generate_solution()`** - Modify prompt for Python
3. **Update language detection** - Change from C++ to Python
4. **Test thoroughly** - Verify with multiple problems
5. **Document** - Update README with new language

Example for Python:

```python
def get_python_template(self, code_snippets):
    """Extract Python code template."""
    for snippet in code_snippets:
        if snippet['langSlug'] == 'python3':
            return snippet['code']
    return None
```

## Documentation

Help improve docs:
- Fix typos
- Clarify instructions
- Add examples
- Update troubleshooting

Changes to:
- `README.md` - Main documentation
- Docstrings in `solver.py` - Code documentation
- `CONTRIBUTING.md` - This file

## Commit Messages

Good commits are:
- **Specific**: What changed and why
- **Clear**: Anyone can understand
- **Concise**: 50 char limit for title

```bash
# ✅ Good
git commit -m "Add timeout configuration for submission waiting"

# ❌ Bad  
git commit -m "fix" or "Update code"
```

## Performance

- Keep API calls minimal
- Optimize JavaScript injection  
- Cache where possible
- Profile slow operations

## Security

- Never log credentials
- Don't commit `.env`
- Validate user inputs
- Use HTTPS for APIs
- Keep dependencies updated

## Questions?

- Check existing issues
- Read README thoroughly
- File a new issue with context
- Be patient and respectful

## Code of Conduct

- Be respectful and inclusive
- No harassment, discrimination, or abuse
- Welcome all skill levels
- Give credit appropriately
- Assume good intentions

## Thank You! 🙏

Your contributions make this project better!
