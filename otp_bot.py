import discord
from discord import app_commands
from imap_tools import MailBox, AND
import asyncio
import os
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OTPBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.synced = False

    async def on_ready(self):
        """Called when the bot is logged in and ready"""
        print(f'✅ Logged in as {self.user} (ID: {self.user.id})')
        print('🔍 Loading slash commands...')
        
        if not self.synced:
            await self.tree.sync()
            self.synced = True
            print('✅ Slash commands synced!')
        
        print('🎯 Bot is ready! Use /otp or /quick_otp to get started.')

    def extract_otp_from_email(self, email_subject, email_text):
        """
        Extract OTP codes from email content using multiple patterns
        Supports various OTP formats from different services
        """
        search_text = f"{email_subject} {email_text}"
        
        # Enhanced OTP patterns for different services
        patterns = [
            # Instacart style: "147477 is your instacart verification code"
            r'(\d{6})\s+is\s+your\s+[\w\s]+\s+verification\s+code',
            
            # Bolded codes like **147477**
            r'\*\*(\d{4,8})\*\*',
            
            # Standalone 4-8 digit codes
            r'\s(\d{4,8})\s',
            
            # Common OTP phrases
            r'code:?\s*[:\-]?\s*(\d{4,8})',
            r'verification\s+code:?\s*[:\-]?\s*(\d{4,8})',
            r'OTP:?\s*[:\-]?\s*(\d{4,8})',
            r'one.time.*?code:?\s*[:\-]?\s*(\d{4,8})',
            r'your.*?code.*?is:?\s*[:\-]?\s*(\d{4,8})',
            
            # Fallback: any 4-8 digit number
            r'\b\d{4,8}\b'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, search_text, re.IGNORECASE)
            if matches:
                print(f"🔑 OTP found with pattern: {matches[0]}")
                return matches[0]
        
        return None

    async def search_otp_in_emails(self, target_email, timeout_minutes=2):
        """
        Search for OTP codes in existing emails
        """
        try:
            # Get email configuration from environment
            email_address = os.getenv('EMAIL_ADDRESS')
            email_password = os.getenv('EMAIL_PASSWORD')
            imap_server = os.getenv('IMAP_SERVER')

            if not all([email_address, email_password, imap_server]):
                print("❌ Email configuration missing. Check your .env file.")
                return None

            print(f"📧 Searching emails for: {target_email}")

            with MailBox(imap_server).login(email_address, email_password, 'INBOX') as mailbox:
                start_time = datetime.now()
                end_time = start_time + timedelta(minutes=timeout_minutes)
                
                while datetime.now() < end_time:
                    # Search for emails to the target address
                    messages = mailbox.fetch(
                        AND(to=target_email),
                        reverse=True,  # Newest first
                        limit=10
                    )
                    
                    for msg in messages:
                        otp_code = self.extract_otp_from_email(msg.subject, msg.text)
                        if otp_code:
                            print(f"✅ OTP found: {otp_code}")
                            return otp_code
                    
                    # Wait before checking again
                    await asyncio.sleep(5)
                
                return None
                
        except Exception as e:
            print(f"❌ Error searching emails: {e}")
            return None

    async def wait_for_otp_email(self, target_email, timeout_minutes=2):
        """
        Wait for new OTP emails to arrive
        """
        try:
            email_address = os.getenv('EMAIL_ADDRESS')
            email_password = os.getenv('EMAIL_PASSWORD')
            imap_server = os.getenv('IMAP_SERVER')

            print(f"⏳ Waiting for new OTP email to: {target_email}")
            
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=timeout_minutes)
            
            while datetime.now() < end_time:
                with MailBox(imap_server).login(email_address, email_password, 'INBOX') as mailbox:
                    # Check recent emails
                    messages = list(mailbox.fetch(
                        AND(to=target_email),
                        reverse=True,
                        limit=5
                    ))
                    
                    for msg in messages:
                        # Only check very recent emails (last 2 minutes)
                        if datetime.now() - msg.date < timedelta(minutes=2):
                            otp_code = self.extract_otp_from_email(msg.subject, msg.text)
                            if otp_code:
                                print(f"✅ New OTP received: {otp_code}")
                                return otp_code
                
                await asyncio.sleep(5)
            
            return None
            
        except Exception as e:
            print(f"❌ Error waiting for OTP: {e}")
            return None

# Initialize bot
bot = OTPBot()

@bot.tree.command(name="otp", description="Get OTP code from your email (2 minute search)")
@app_commands.describe(email="The email address to check for OTP codes")
async def otp_command(interaction: discord.Interaction, email: str):
    """
    Search for OTP codes sent to a specific email address
    """
    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        await interaction.response.send_message(
            "❌ Please provide a valid email address.", 
            ephemeral=True
        )
        return
    
    await interaction.response.send_message(
        f"🔍 Searching for OTP codes sent to: `{email}`\n"
        "⏰ I'll check for 2 minutes...",
        ephemeral=True
    )
    
    # Search existing emails
    existing_otp = await bot.search_otp_in_emails(email, timeout_minutes=1)
    
    if existing_otp:
        await interaction.followup.send(
            f"✅ OTP code found: `{existing_otp}`",
            ephemeral=True
        )
        return
    
    # Wait for new email
    await interaction.followup.send(
        "⏳ No existing OTP found. Waiting for new email...",
        ephemeral=True
    )
    
    otp_code = await bot.wait_for_otp_email(email, timeout_minutes=1)
    
    if otp_code:
        await interaction.followup.send(
            f"✅ New OTP code received: `{otp_code}`",
            ephemeral=True
        )
    else:
        await interaction.followup.send(
            "❌ No OTP code found.\n"
            "**Troubleshooting:**\n"
            "• Check if the service sent the email\n"
            "• Verify the email address is correct\n"
            "• Ensure emails are forwarded to your main inbox\n"
            "• Try again in a moment",
            ephemeral=True
        )

@bot.tree.command(name="quick_otp", description="Quick OTP search (1 minute)")
@app_commands.describe(email="The email address to check for OTP codes")
async def quick_otp_command(interaction: discord.Interaction, email: str):
    """
    Quick search for OTP codes
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        await interaction.response.send_message(
            "❌ Please provide a valid email address.", 
            ephemeral=True
        )
        return
    
    await interaction.response.send_message(
        f"⚡ Quick searching: `{email}`\n"
        "⏰ Checking for 1 minute...",
        ephemeral=True
    )
    
    otp_code = await bot.search_otp_in_emails(email, timeout_minutes=1)
    
    if otp_code:
        await interaction.followup.send(
            f"✅ OTP code found: `{otp_code}`",
            ephemeral=True
        )
    else:
        await interaction.followup.send(
            "❌ No OTP code found within 1 minute.",
            ephemeral=True
        )

@bot.tree.command(name="ping", description="Check if the bot is responsive")
async def ping_command(interaction: discord.Interaction):
    """Simple ping command to test bot responsiveness"""
    await interaction.response.send_message(
        "✅ Bot is online and responsive!", 
        ephemeral=True
    )

if __name__ == "__main__":
    # Validate required environment variables
    required_vars = ['DISCORD_BOT_TOKEN', 'EMAIL_ADDRESS', 'EMAIL_PASSWORD', 'IMAP_SERVER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("💡 Please check your .env file and make sure all variables are set.")
        exit(1)
    
    # Start the bot
    print("🚀 Starting OTP Bot...")
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))