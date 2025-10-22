# Quick Start Guide - Stock Sentinel

## 🚀 Get Running in 5 Minutes

### Step 1: Check Your Files

You should have these files in your directory:
```
S-P-500-Trip-Wire-Dashboard/
├── stock_gui.html              ← The cool stock GUI (open this!)
├── index.html                  ← Original dashboard
├── sentiment_stock_agent.py    ← AI sentiment engine
├── api.py                      ← Backend API server
├── requirements.txt            ← Python dependencies
└── run_sentiment_agent.sh      ← Easy startup script
```

### Step 2: Install Python Dependencies

**Option A: Use the Easy Script (Recommended)**

**On Linux/Mac:**
```bash
chmod +x run_sentiment_agent.sh
./run_sentiment_agent.sh
```

**On Windows:**
```bash
run_sentiment_agent.bat
```

The script will:
- Create a virtual environment
- Install all dependencies
- Download required NLTK data
- Start the API server automatically

---

**Option B: Manual Installation**

If the script doesn't work, do it manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate          # On Linux/Mac
# OR
venv\Scripts\activate             # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data for sentiment analysis
python -c "import nltk; nltk.download('brown'); nltk.download('punkt')"

# 5. Start the API server
python api.py
```

### Step 3: Verify API is Running

You should see:
```
Starting Sentiment Stock Agent API...
API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Test it in your browser:**
Go to: http://localhost:5000

You should see API documentation.

### Step 4: Open the Stock GUI

**Method 1: Double-click the file**
- Just double-click `stock_gui.html` in your file explorer
- It will open in your default browser

**Method 2: Open from browser**
- Open your web browser (Chrome, Firefox, Safari, Edge)
- Press `Ctrl+O` (or `Cmd+O` on Mac)
- Navigate to the folder and select `stock_gui.html`

**Method 3: Use a local server (optional, better for development)**
```bash
# Python 3
python -m http.server 8000

# Then visit: http://localhost:8000/stock_gui.html
```

### Step 5: Watch It Work!

Once the GUI opens, you'll see:

1. **Top right corner**: Should show "API ONLINE" in green
   - If it shows "API OFFLINE" in red, the API isn't running
   - Go back to Step 2

2. **Left panel (Watchlist)**: Will auto-load with stocks
   - NVDA, MSFT, GOOGL, META, TSLA, AAPL, AMZN, AMD

3. **Click any stock**: Full analysis loads
   - Main chart updates
   - Sentiment gauge animates
   - Recommendation appears
   - News feed loads

### Step 6: Try It Out

**Search for a stock:**
1. Type a ticker in the search box (e.g., "TSLA")
2. Click "ANALYZE"
3. Watch the magic happen!

**Add to watchlist:**
1. Type a ticker
2. Click "ADD TO WATCHLIST"
3. It appears in the left panel

**Refresh data:**
- Click "REFRESH" button in top right
- Or wait 60 seconds (auto-refreshes)

---

## 🔧 Troubleshooting

### Problem: "API OFFLINE" in red

**Solution:**
```bash
# Check if API is running
curl http://localhost:5000/health

# If nothing happens, start the API:
python api.py
```

### Problem: "ModuleNotFoundError"

**Solution:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: Stock GUI shows no data

**Solutions:**
1. Make sure API is running (see above)
2. Check browser console for errors (F12 → Console tab)
3. Try a different browser (Chrome works best)
4. Disable any ad-blockers that might block localhost

### Problem: News not loading

This is normal! The free tier has limits:
- **Without News API key**: Uses Google News RSS (slower but works)
- **With News API key** (recommended): 100 requests/day free

**Get a free API key:**
1. Go to https://newsapi.org/
2. Sign up (free)
3. Copy your API key
4. Create `.env` file:
   ```bash
   cp .env.example .env
   nano .env  # or use any text editor
   ```
5. Add your key:
   ```
   NEWS_API_KEY=your_key_here
   ```
6. Restart API: `python api.py`

### Problem: CORS errors in browser console

**Solution:**
This shouldn't happen since we have CORS enabled, but if it does:
```bash
# Restart the API
# Make sure you're accessing via file:// or http://localhost:
```

---

## 📊 What Each File Does

| File | Purpose |
|------|---------|
| `stock_gui.html` | **The cool trading terminal** - Open this in browser |
| `index.html` | Original S&P 500 trip-wire dashboard |
| `api.py` | Backend API server (must be running) |
| `sentiment_stock_agent.py` | AI sentiment analysis engine |
| `requirements.txt` | Python dependencies list |
| `run_sentiment_agent.sh` | Auto-setup script (Linux/Mac) |
| `run_sentiment_agent.bat` | Auto-setup script (Windows) |

---

## 🎯 Quick Commands Cheat Sheet

```bash
# Start API (manual)
python api.py

# Start API (with script)
./run_sentiment_agent.sh

# Check if API is running
curl http://localhost:5000/health

# Test stock validation
curl http://localhost:5000/validate/NVDA

# Test sentiment analysis
curl http://localhost:5000/analyze/NVDA

# Stop API
Ctrl+C (in the terminal where it's running)
```

---

## 💡 Pro Tips

1. **Keep API running**: Leave the terminal open where `python api.py` is running
2. **Use Chrome/Firefox**: Best compatibility with the GUI
3. **Get News API key**: For better news coverage (free at newsapi.org)
4. **Check console**: Press F12 in browser to see debug info
5. **Refresh manually**: Click the REFRESH button if data seems stale

---

## 🎨 Features to Try

1. **Watchlist**: Click different stocks to see their analysis
2. **Search**: Try AAPL, TSLA, AMZN, GOOGL
3. **Sentiment Gauge**: Watch it animate when you select stocks
4. **Recommendations**: See BUY/SELL/HOLD signals
5. **News Feed**: Read latest tech news with sentiment
6. **Sector Overview**: Check AI, Data Centers, Power sentiment

---

## 📱 Access from Another Device

Want to view on your phone/tablet on same network?

1. Find your computer's IP address:
   ```bash
   # Linux/Mac
   ifconfig | grep inet

   # Windows
   ipconfig
   ```

2. Start API with network access (already configured):
   ```bash
   python api.py
   # API runs on 0.0.0.0:5000 (accessible from network)
   ```

3. Update `stock_gui.html` line 945:
   ```javascript
   // Change this:
   const API_URL = 'http://localhost:5000';

   // To this (use your computer's IP):
   const API_URL = 'http://192.168.1.XXX:5000';
   ```

4. Open `stock_gui.html` on other device

---

## 🆘 Still Having Issues?

1. Check the main README.md
2. Check SENTIMENT_AGENT_README.md for API details
3. Make sure Python 3.8+ is installed: `python3 --version`
4. Make sure port 5000 isn't used by another app
5. Try restarting your computer (seriously, it helps sometimes!)

---

## ✅ Success Checklist

- [ ] API running (terminal shows "Running on http://0.0.0.0:5000")
- [ ] Browser open with stock_gui.html
- [ ] "API ONLINE" showing in green
- [ ] Watchlist loaded with stocks
- [ ] Can click stocks and see data
- [ ] Sentiment gauge animates
- [ ] News feed shows articles
- [ ] Having fun! 🎉

---

**Need more help?** Check the detailed docs:
- [SENTIMENT_AGENT_README.md](SENTIMENT_AGENT_README.md) - API documentation
- [README.md](README.md) - Project overview
