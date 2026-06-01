# discord-otp-bot

Discord bot that checks your email over IMAP and DMs you OTP codes. I made this because I got tired of alt-tabbing to Gmail for 6-digit codes.

Uses slash commands: `/otp`, `/quick_otp`, `/ping`. Gmail/Outlook/Yahoo/etc. as long as IMAP works.

## setup

**You need:** Python 3.8+, a Discord bot token, email with IMAP on.

```bash
git clone https://github.com/2577manmeet/discord-otp-bot.git
cd discord-otp-bot
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env`:

```env
DISCORD_BOT_TOKEN=your_token
EMAIL_ADDRESS=you@gmail.com
EMAIL_PASSWORD=your_app_password
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
```

### discord side

1. [Developer Portal](https://discord.com/developers/applications) → New Application
2. Bot tab → Add Bot → turn on **Message Content Intent**
3. OAuth2 → URL Generator → scopes `bot` + `applications.commands`, invite to your server

### gmail

Turn on 2FA, then make an [App Password](https://myaccount.google.com/apppasswords) for Mail. Put that in `EMAIL_PASSWORD`, not your normal password.

### run

```bash
python otp_bot.py
```

Slash commands can take an hour or two to show up globally after first deploy. If the bot ignores you, re-invite with the right perms.

## commands

| command | what it does |
|---------|----------------|
| `/otp <email>` | scan inbox, up to ~2 min |
| `/quick_otp <email>` | faster scan, ~1 min |
| `/ping` | latency check |

OTP replies are ephemeral (only you see them).

## imap servers

| provider | server | port |
|----------|--------|------|
| Gmail | imap.gmail.com | 993 |
| Outlook | imap-mail.outlook.com | 993 |
| Yahoo | imap.mail.yahoo.com | 993 |
| iCloud | imap.mail.me.com | 993 |

## when stuff breaks

- **no OTP** — check the email actually landed in inbox, try `/quick_otp`
- **IMAP login fail** — app password wrong or IMAP disabled
- **interaction failed** — double-check `.env`, Message Content Intent on
- **commands missing** — wait for sync or re-invite bot

Bot only reads mail, doesn't delete or send anything.

## license

MIT. Only use this on accounts you own.
