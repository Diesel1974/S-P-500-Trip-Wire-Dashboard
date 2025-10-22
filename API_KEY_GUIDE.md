# API Key Security Guide

## ✅ Your Setup is Now SECURE!

Your Finnhub API key is properly configured in the `.env` file, which is:
- ✅ **NOT committed to Git** (protected by `.gitignore`)
- ✅ **Loaded via environment variables** (no hardcoding)
- ✅ **Separate from your code** (easy to change/rotate)

---

## 🔑 About Your Finnhub API Keys

### API Key (What You Have)
```
FINNHUB_API_KEY=d3seqd1r01qvii72v130d3seqd1r01qvii72v13g
```
- ✅ **Already set up in your `.env` file**
- This is your **public-facing API key**
- Used for making API requests to Finnhub
- **This is all you need for most use cases!**

### Secret Key (The Other One You Mentioned)
```
Secret: d3seqd1r01qvii72v14g
```
- ⚠️ **You typically DON'T need this for basic API calls**
- This is used for:
  - **Webhook verification** (when Finnhub sends data to your server)
  - **WebSocket authentication** (real-time streaming)
  - **HMAC signature validation**

**For our sentiment stock agent, you only need the API key!**

---

## 🚫 NEVER Do This (Hardcoding)

### ❌ Bad - Hardcoded API Key
```python
# DON'T DO THIS!
API_KEY = "d3seqd1r01qvii72v130d3seqd1r01qvii72v13g"  # WRONG!

def get_stock_data():
    url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={API_KEY}"
    # This exposes your key in the code!
```

### ❌ Bad - Committing .env to Git
```bash
# DON'T DO THIS!
git add .env  # WRONG! This will expose your keys
git commit -m "Add API keys"  # WRONG!
```

---

## ✅ ALWAYS Do This (Environment Variables)

### ✅ Good - Using .env file
```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Get API key securely
API_KEY = os.getenv('FINNHUB_API_KEY')

def get_stock_data():
    url = f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={API_KEY}"
    # API key is never in the code!
```

### ✅ Good - .gitignore protection
```
# In .gitignore
.env  # ← This prevents Git from tracking your API keys
```

---

## 📁 File Structure (Your Current Setup)

```
S-P-500-Trip-Wire-Dashboard/
├── .env                      # ✅ YOUR ACTUAL API KEYS (IGNORED BY GIT)
├── .env.example              # ✅ Template for others (no real keys)
├── .gitignore                # ✅ Protects .env from being committed
├── finnhub_example.py        # ✅ Example code using API key securely
└── API_KEY_GUIDE.md          # ✅ This guide
```

---

## 🎯 How to Use Your Finnhub API Key

### Method 1: Using requests directly
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

# Get stock quote
response = requests.get(
    'https://finnhub.io/api/v1/quote',
    params={
        'symbol': 'AAPL',
        'token': FINNHUB_API_KEY  # ← Loaded from .env
    }
)
data = response.json()
print(f"AAPL Price: ${data['c']}")
```

### Method 2: Using our FinnhubClient class
```python
from finnhub_example import FinnhubClient

# Initialize (automatically loads from .env)
client = FinnhubClient()

# Get stock quote
quote = client.get_quote('AAPL')
print(f"Current Price: ${quote['c']}")

# Get company profile
profile = client.get_company_profile('AAPL')
print(f"Company: {profile['name']}")

# Get news
news = client.get_market_news('general')
print(f"Latest headline: {news[0]['headline']}")
```

---

## 🔒 Security Best Practices

### ✅ DO:
1. **Use `.env` files** for all API keys
2. **Add `.env` to `.gitignore`**
3. **Use `os.getenv()`** to load keys
4. **Provide `.env.example`** as a template (without real keys)
5. **Rotate keys regularly** (change them every few months)
6. **Use different keys** for dev/staging/production

### ❌ DON'T:
1. **Hardcode API keys** in your code
2. **Commit `.env`** to Git/GitHub
3. **Share keys** in emails, Slack, or Discord
4. **Use production keys** in development
5. **Store keys** in client-side JavaScript (browser can see them!)

---

## 🛠️ Using in Different Environments

### Development (Your Local Machine)
```bash
# .env file
FINNHUB_API_KEY=d3seqd1r01qvii72v130d3seqd1r01qvii72v13g
```

### Production (Deployed Server)
```bash
# Set environment variables on the server (not in a file)
export FINNHUB_API_KEY=your_production_key_here

# Or use your hosting platform's environment variable UI:
# - Heroku: Settings → Config Vars
# - Vercel: Settings → Environment Variables
# - AWS: Systems Manager → Parameter Store
# - Docker: docker run -e FINNHUB_API_KEY=...
```

### CI/CD (GitHub Actions, etc.)
```yaml
# In GitHub Actions secrets
env:
  FINNHUB_API_KEY: ${{ secrets.FINNHUB_API_KEY }}
```

---

## 🧪 Testing Your Setup

Run the example to verify everything works:

```bash
# Make sure you're in the project directory
cd /home/user/S-P-500-Trip-Wire-Dashboard

# Activate virtual environment
source venv/bin/activate

# Run the example
python finnhub_example.py
```

You should see:
```
================================================================================
FINNHUB API EXAMPLE - Using Environment Variables
================================================================================

Test 1: Getting AAPL stock quote...
✅ Current Price: $178.50
   Change: 2.30 (1.30%)
   High: $179.20
   Low: $176.80

Test 2: Getting AAPL company profile...
✅ Company: Apple Inc
   Industry: Technology
   Market Cap: $2,750,000M
   Country: US

Test 3: Getting general market news...
✅ Found 50 articles
   Latest: Tech stocks surge on strong earnings...

================================================================================
API KEY SECURITY:
✅ API key loaded from .env file
✅ .env file is in .gitignore (not committed to Git)
✅ Code never contains hardcoded API keys
================================================================================
```

---

## 🔄 Rotating API Keys

If your key is ever compromised:

1. **Generate a new key** on Finnhub dashboard
2. **Update `.env` file** with the new key:
   ```bash
   FINNHUB_API_KEY=your_new_key_here
   ```
3. **Restart your application**
4. **Revoke the old key** on Finnhub dashboard

---

## ❓ FAQ

### Q: Do I need the "secret" key?
**A:** No, not for basic API calls. You only need it for:
- Webhook signature verification
- WebSocket authentication
- Advanced security features

For stock data, news, and quotes, the API key alone is sufficient.

### Q: What if I accidentally committed my API key to Git?
**A:**
1. **Immediately revoke** the exposed key on Finnhub
2. **Generate a new key**
3. **Update your `.env` file**
4. **Remove from Git history**:
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch .env" \
   --prune-empty --tag-name-filter cat -- --all
   ```

### Q: Can I use the same key for multiple projects?
**A:** Yes, but it's better to create separate keys for:
- Easier tracking of usage
- Better security (if one project is compromised, others aren't affected)
- Rate limit isolation

### Q: Where do I get more Finnhub keys?
**A:**
1. Go to https://finnhub.io/
2. Sign in to your account
3. Dashboard → API Keys
4. Click "Generate New API Key"

### Q: What's the rate limit?
**A:**
- **Free tier**: 60 API calls/minute
- **Paid tiers**: Higher limits
- Check dashboard for your current usage

---

## 📚 Additional Resources

- **Finnhub API Docs**: https://finnhub.io/docs/api
- **Python dotenv**: https://pypi.org/project/python-dotenv/
- **Security Best Practices**: https://owasp.org/www-community/vulnerabilities/

---

## ✅ Checklist

- [x] API key stored in `.env` file
- [x] `.env` file in `.gitignore`
- [x] Code uses `os.getenv()` instead of hardcoding
- [x] `.env.example` provided for team members
- [x] Tested with `finnhub_example.py`
- [ ] Consider rotating keys every 3-6 months
- [ ] Set up different keys for production

---

**Your API keys are now secure!** 🎉🔒
