# Discord OTP Bot

A powerful Discord bot that automatically retrieves OTP (One-Time Password) codes from your email and sends them directly to your Discord DMs. Perfect for developers, power users, and anyone who needs quick access to verification codes without switching between apps.

![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![IMAP](https://img.shields.io/badge/IMAP-Email-orange?style=for-the-badge)

---

## ✨ Features

- 🔍 **Automated OTP Detection** – Scans emails for verification codes
- 📧 **Multi-Provider Support** – Works with Gmail, Outlook, Yahoo, and all IMAP email services
- 🔒 **Secure & Private** – All OTP responses are ephemeral
- ⚡ **Fast & Efficient** – Intelligent pattern matching
- 🎯 **Slash Commands** – `/otp`, `/quick_otp`, `/ping`
- 🛠️ **Environment-Based Setup**
- 🔄 **Real-time New OTP Monitoring**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Discord server
- Email with IMAP enabled

---

## 📥 Installation

### 1. Clone repository
```bash
git clone https://github.com/2577mamneet/discord-otp-bot.git
cd discord-otp-bot
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Inside `.env`:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

---

## 🤖 Discord Bot Setup

### Create a Discord Application
1. Open **Discord Developer Portal**
2. Click **New Application**
3. Name it (e.g., OTP Bot)

### Add Bot User
1. Go to **Bot** tab  
2. Click **Add Bot**  
3. Enable **MESSAGE CONTENT INTENT**

### Add Bot to Server
1. Go to **OAuth2 → URL Generator**
2. Scopes:
   - `bot`
   - `applications.commands`
3. Permissions:
   - View Channels
   - Send Messages
   - Read Message History
   - Use Slash Commands

Invite with generated URL.

---

## 📧 Email Setup (Gmail Example)

### Enable IMAP + App Password
1. Enable **2-Step Verification**
2. Go to **App Passwords**
3. Choose "Mail"
4. Generate password
5. Paste into `.env`

---

## ▶️ Running the Bot

```bash
python otp_bot.py
```

Expected log:
```
✅ Logged in as OTP Bot
🔍 Loading slash commands...
✅ Slash commands synced!
🎯 Bot is ready!
```

---

## 📖 Commands

| Command | Description |
|--------|-------------|
| `/otp <email>` | Deep scan (up to 2 min) |
| `/quick_otp <email>` | Quick scan (1 min) |
| `/ping` | Check bot latency |

Example DM:
```
✅ OTP code found: 468450
```

---

## 🛠️ Supported Email Providers

| Provider | IMAP Server | Port |
|---------|-------------|------|
| Gmail | imap.gmail.com | 993 |
| Outlook | imap-mail.outlook.com | 993 |
| Yahoo | imap.mail.yahoo.com | 993 |
| iCloud | imap.mail.me.com | 993 |
| AOL | imap.aol.com | 993 |

---

## 🔧 Configuration Options

| Variable | Description | Example |
|----------|-------------|---------|
| DISCORD_BOT_TOKEN | Discord bot token | abc123 |
| EMAIL_ADDRESS | IMAP email address | your@gmail.com |
| EMAIL_PASSWORD | App Password | abcd efgh ijkl mnop |
| IMAP_SERVER | IMAP host | imap.gmail.com |
| IMAP_PORT | IMAP port | 993 |

### OTP Pattern Matching Supports:
- “147477 is your instacart verification code”
- Bolded: `**123456**`
- “Your code is: 123456”
- Any **4–8 digit numeric OTP**

---

## 🛡️ Security

- 🔐 Uses **secure app passwords**
- 👁️ OTP sent only in **ephemeral DMs**
- 📧 Bot is **read-only**, never modifies mail
- 🔒 No saved data or logs containing sensitive info

---

## ❓ Troubleshooting

### Bot doesn’t reply
- Wait 1–2 hours for global slash command sync  
- Reinvite with correct permissions  

### Interaction failed
- Verify `.env`
- Ensure Message Content Intent is enabled

### No OTP found
- Confirm email reached inbox  
- Try `/quick_otp`

### IMAP login issues
- Ensure IMAP is enabled  
- Regenerate app password  

### Debug logs
```
🔍 Searching emails for: example@mail.com
🔑 OTP found using pattern: 123456
```

---

## 🤝 Contributing

1. Fork project  
2. Create feature branch:
```bash
git checkout -b feature/YourFeature
```
3. Commit changes:
```bash
git commit -m "Add YourFeature"
```
4. Push:
```bash
git push origin feature/YourFeature
```
5. Submit PR

---

## 📄 License
This project is licensed under **MIT License**.

---

## ⭐ Support
If this project helps you, please **star ⭐ the repo**!

> **Disclaimer:** Use this bot only with accounts you own.
