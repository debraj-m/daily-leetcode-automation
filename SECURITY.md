# Security Policy

## Reporting Security Issues

Please **DO NOT** file public GitHub issues for security vulnerabilities.

Instead, email security concerns to: [your-email]

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We appreciate responsible disclosure and will:
- Acknowledge receipt within 24 hours
- Work on fix immediately
- Keep you informed of progress
- Credit you in advisory (if desired)

## Security Practices

### What This Tool Does NOT Do

✅ **Safe by Design**
- Does NOT store your LeetCode password
- Does NOT send credentials to external services
- Does NOT retain session tokens after exit
- Does NOT modify LeetCode's system
- Does NOT bypass security mechanisms

### What You Should Do

✅ **Your Responsibility**
- Keep `.env` file private (don't commit to git)
- Use unique, strong passwords
- Rotate API keys regularly
- Review generated code before submitting
- Don't share execution logs (may contain cookies)

### Secrets Management

**Never Commit**:
```bash
# ❌ Wrong
git add .env
echo "OPENAI_API_KEY=sk-..." > settings.txt

# ✅ Right
git add .env.example  # Template only
echo ".env" >> .gitignore
```

**Environment Variables**:
```bash
# ✅ Load from file (don't hardcode)
load_dotenv()

# ✅ Use during runtime
key = os.environ.get("OPENAI_API_KEY")
```

**API Keys**:
- Use environment variables only
- Never print keys in logs
- Rotate monthly
- Revoke unused keys
- Use restricted permissions

### Browser Security

**Session Handling**:
- Uses authenticated browser session
- Cookies extracted locally only
- Session cleared on script exit
- No cookies stored to disk

**Code Injection**:
- Injects only generated code
- Through established Monaco API
- No arbitrary JavaScript execution
- Validated for syntax before submission

## Cloudflare Bypass

This tool uses **manual login** because:
- ✅ Cloudflare blocks automated logins  
- ✅ Bot detection cannot be reliably bypassed
- ✅ Human verification is required
- ✅ This is the secure approach

We do NOT and WILL NOT:
- ❌ Try to bypass Cloudflare
- ❌ Use credential replay attacks
- ❌ Impersonate browsers
- ❌ Ignore security measures

## LeetCode Terms

This tool respects LeetCode's Terms of Service:
- ✅ Uses official GraphQL API
- ✅ Submits through web interface
- ✅ Doesn't spam or DOS servers
- ✅ One submission per run
- ✅ For personal learning only

❌ **Prohibited Uses**:
- Don't use to artificially boost metrics
- Don't share solutions publicly
- Don't sell/redistribute this tool
- Don't use for cheating or fraud

## Dependencies

### Security of Dependencies

- `requests` - HTTP library, widely used
- `openai` - Official OpenAI SDK
- `python-dotenv` - Standard env loader
- `selenium` - Industry-standard automation

### Keeping Dependencies Safe

```bash
# Check for vulnerabilities
pip audit

# Update safely
pip install --upgrade requests openai
pip install -r requirements.txt --upgrade

# Commit lock file
pip freeze > requirements.lock
```

## Monitoring

### What Gets Logged

✅ **Logged Safely**:
- Timestamp of submission
- Problem title and ID
- Difficulty level
- Result status
- Code length (anonymized)

❌ **Never Logged**:
- API keys
- Passwords
- Session cookies
- Generated code (to disk)
- Personal information

### Clearing Logs

```bash
# Keep only last N submissions
python3 -c "
import json
from pathlib import Path

# Load logs
logs = json.loads(Path('solved_log.json').read_text())

# Keep last 100
logs = logs[-100:]

# Save back
Path('solved_log.json').write_text(json.dumps(logs, indent=2))
"
```

## OpenAI Integration

### Data Privacy

Your data sent to OpenAI:
- Problem description (HTML stripped, text only)
- Difficulty level
- Problem title

NOT sent:
- Your personal information
- LeetCode credentials
- Session tokens

### Cost Control

- ~$0.01 per submission
- Set usage limits in OpenAI dashboard
- Monitor monthly bills
- Use gpt-3.5-turbo for lower cost

https://platform.openai.com/account/billing/limits

### Data Retention

- OpenAI stores data per their policy (30 days)
- Request deletion if concerned
- Disable data usage in API settings

## Browser Security

### Chrome Permissions

This tool requests:
- Access to LeetCode.com
- JavaScript execution
- Network access

It does NOT request:
- Your files or downloads
- Camera/microphone
- Extensions permission
- Full disk access

### Privacy Mode

Run in Incognito for extra privacy:

```python
options = Options()
options.add_argument("--incognito")
driver = webdriver.Chrome(options=options)
```

## Responsible Use

### Ethical Guidelines

- 🎓 **Learn** - Use solutions to learn algorithms
- 📚 **Understand** - Read and understand code
- ✍️ **Practice** - Write similar code yourself
- 🚫 **Don't cheat** - Earn your skills honestly

### Contest Policy

- ❌ Never use during official contests
- ❌ Never share solutions
- ✅ Use only for daily practice
- ✅ Use only your own account

## Vulnerability Disclosure

If you find a security issue:

1. **Do not** file public issue
2. Email with details
3. We will fix promptly
4. We will credit you (optional)
5. Advisory released after fix

## Security Updates

We will:
- Audit code regularly
- Update dependencies promptly
- Fix vulnerabilities immediately
- Notify users of security issues
- Provide migration guides

Subscribe to security advisories:
- Watch this repository (Star)
- Email notifications  
- Check releases page

## Questions?

For security questions (not vulnerabilities):
- Check this file thoroughly
- File GitHub discussion (not issue)
- Email if sensitive
- Don't post secrets publicly

---

**Thank you for helping keep this tool secure!** 🔒
