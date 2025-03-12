import os
import subprocess
import sys

# Function to install dependencies
def install(package):
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-cache-dir", "--force-reinstall", package], check=True)

# Ensure required dependencies are installed
required_packages = ["discord.py", "pynacl", "ffmpeg"]

for package in required_packages:
    try:
        __import__(package.replace("-", "_"))  # Import the package dynamically
    except ImportError:
        install(package)

# Now import everything after ensuring installation
import discord
import nacl
import random
import traceback
import requests
import json
import sqlite3
import wave
import subprocess
import asyncio
from discord import FFmpegPCMAudio
from discord.ui import Button, View
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta








# Replace with your actual Discord User ID(s)
ALLOWED_USERS = [1101467683083530331, 987654321098765432]

# Check if user is allowed
def is_allowed_user():
    async def predicate(ctx):
        if ctx.author.id not in ALLOWED_USERS:
            raise commands.CheckFailure  # Just raise the error, don't send a message
        return True
    return commands.check(predicate)



intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True  # Needed for role management & DMs
intents.presences = True  # Enables presence updates (required for status changes)

# Add rate limiting to prevent Discord API rate limits
import aiohttp
bot = commands.Bot(
    command_prefix=".", 
    intents=intents, 
    help_command=None,
    http_timeout=aiohttp.ClientTimeout(total=60)  # Longer timeout
)

# Do not create session at module level
# The session will be created properly by discord.py internally

old_invites = {}  # Dictionary to track invites

@bot.event
async def on_ready():
    global bot  
    await bot.wait_until_ready()

    print(f"✅ SHULKER BOT is online as {bot.user}!")

    # Fetch invites for all guilds the bot is in
    for guild in bot.guilds:
        try:
            old_invites[guild.id] = {invite.code: invite.uses for invite in await guild.invites()}
        except discord.Forbidden:
            print(f"❌ Missing permissions to fetch invites for {guild.name}.")

    # Sync application (slash) commands
    try:
        await bot.tree.sync()
        print("✅ Slash commands synced!")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

    # Wait before updating presence to avoid issues
    await asyncio.sleep(1)

    # Set bot status to Streaming
    activity = discord.Streaming(name="SHULKER SMP ⚔", url="https://www.twitch.tv/minecraft")
    await bot.change_presence(status=discord.Status.idle, activity=activity)

    print("✅ Status should now be updated!")


# Help Command
# Define the /help command
@bot.tree.command(name="help", description="Shows all available commands")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="📖 **SHULKER BOT HELP MENU**", color=discord.Color.gold())

    embed.add_field(name="💰 **ECONOMY COMMANDS**", value="> `/balance` - Check your balance.\n> `/daily` - Claim daily coins.\n> `/give <user> <amount>` - Give coins to another user.", inline=False)
    
    embed.add_field(name="🎰 **GAMBLING COMMANDS**", value="> `/blackjack <bet>` - Play Blackjack.\n> `/slots <bet>` - Spin the slot machine.\n> `/cf <amount> <heads/tails>` - Flip a coin.\n> `/dice <bet>` - Roll a dice.", inline=False)
    
    embed.add_field(name="⚔️ **MINECRAFT COMMANDS**", value="> `/mcstats <username>` - Get a player's Minecraft stats.\n> `/serverinfo` - Get details about Shulker SMP.", inline=False)
    
    embed.add_field(name="⚙️ **UTILITY COMMANDS**", value="> `/ping` - Check bot latency.\n> `/userinfo <user>` - Get user info.", inline=False)
    
    embed.set_footer(text="🔥 SHULKER BOT • Made for Shulker SMP", icon_url=interaction.client.user.avatar.url)
    
    await interaction.response.send_message(embed=embed)
    
# Help Command
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.user)  # 1 use every 3 seconds per user
async def help(ctx):
            embed = discord.Embed(title=" <a:star1:1345361132512088178> **SHULKER BOT COMMANDS** <a:star1:1345361132512088178> ", color=discord.Color.gold())
            embed.set_thumbnail(url=bot.user.avatar.url)

            embed.add_field(name="<:moderation:1345359844445524041> **Moderation**", 
                value="╭───────────⟡\n"
                      "│ <:kick:1345360371002900550> `.kick <user>`\n"
                      "│ <:ban:1345360761236488276> `.ban <user>`\n"
                      "│ <:unban:1345361440969724019> `.unban <user>`\n"
                      "│ <a:purge:1345361946324631644> `.purge <amount>`\n"
                      "│ <:dm:1345362152831320179> `.dm <user> <message>`\n"
                      "│ <:dm:1345362152831320179> `.dmall <message>`\n"
                      "│ <:timeout:1345362419475546173> `.timeout <user> <duration_in_seconds> [reason]`\n"
                      "│ <:tmremove:1345362837610168321> `.removetimeout <user>`\n"
                      "╰───────────⟡", inline=False)



            embed.add_field(name="<a:economy:1345373409659588661> **Economy**", 
                value="╭───────────⟡\n"
                      "│ <a:balance:1345373618070097982> `.balance / .bal`\n"
                      "│ <a:daily:1345377114223935519> `.daily`\n"
                      "│ <a:cf:1345374098427084922> `.cf <amount> <heads/tails> [X2 MONEY]`\n"
                      "│ <a:set:1345374633666416725> `.setbalance <user> <amount>`\n"
                      "│ <a:slots:1345374871734980608> `.slots <amount> [X5 MONEY]`\n"
                      "│ <:gcoin:1345375137100464168> `.give <user> <amount>`\n"
                      "│ <a:dice:1345375794490507274> `.dice <amount> [X2 MONEY]`\n"
                      "│ <a:trophy:1345379999999999999> `.top` (Leaderboard of richest users)\n"
                      "│ <:gcoin:1345375137100464168> `.blackjack <amount>` [Beat the dealer!]\n"
                      "╰───────────⟡", inline=False)




            embed.add_field(name="<:fun:1345375490965245996> **Fun**", 
                            value="╭───────────⟡\n"
                                  "│ <a:dice:1345375794490507274> `.roll`\n"
                                  "│ 🪙 `.flip`\n"
                                  "│ <:funny:1345378490358173819> `.joke`\n"
                                  "│ <:meme:1345378712907939902> `.meme`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="<a:gift1:1345383111877202021> **Giveaway**", 
                            value="╭───────────⟡\n"
                                  "│ <a:giveaway21:1345378924481347584> `.giveaway <duration_in_seconds> <prize>`\n"
                                  "│ <:refresh:1345379475638063115> `.reroll <message_id>`\n"
                                  "│ <:gend:1345379981672316998> `.gend <message_id>`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="📨 **Invites**", 
                            value="╭───────────⟡\n"
                                  "│ <:invites:1345380333222367285> `.invites <user>`\n"
                                  "│ <:rinvites:1345380642342572193> `.resetinvites <user>`\n"
                                  "│ <a:nuke:1345380973096734731> `.resetwholeserverinvite`\n"
                                  "╰───────────⟡", inline=False)


            embed.add_field(name="<:utility:1345381139354746984> **Utility**", 
                            value="╭───────────⟡\n"
                                  "│ <a:ping:1345381376433717269> `.ping`\n"
                                  "│ <:help:1345381592335646750> `.help`\n"
                                  "│ <a:message:1345402517277638762> `.say`\n"
                                  "│ <:embed:1345402784039571487> `.embed`\n"
                                  "│ <a:Serverinfo:1345403530701176873> `.serverinfo`\n"
                                  "╰───────────⟡", inline=False)

            embed.set_footer(text="🔥 BOT MADE BY SHREYANSH GAMETUBE! STAY ACTIVE ❤")

            await ctx.send(embed=embed)




# Server Info

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild

    embed = discord.Embed(
        title=f"Server Info - {guild.name}",
        color=discord.Color.blue()
    )

    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    embed.add_field(name="📌 Server Name", value=guild.name, inline=True)
    embed.add_field(name="🆔 Server ID", value=guild.id, inline=True)
    embed.add_field(name="👑 Owner", value=guild.owner, inline=True)
    embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Created On", value=guild.created_at.strftime("%B %d, %Y"), inline=True)
    embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="🔰 Roles", value=len(guild.roles), inline=True)

    await ctx.send(embed=embed)

# blackjack testing

class BlackjackButton(discord.ui.View):
    def __init__(self, player, bet):
        super().__init__()
        self.player = player
        self.bet = bet
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        random.shuffle(self.deck)
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.dealer_hand = [self.draw_card(), self.draw_card()]

    def draw_card(self):
        return self.deck.pop()

    def calculate_score(self, hand):
        score = sum(hand)
        aces = hand.count(11)
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    async def update_embed(self, interaction):
        embed = discord.Embed(title=f"🃏 Blackjack - {self.player.name}", color=discord.Color.gold())
        embed.add_field(name="Your Hand", value=f"{self.player_hand} (Total: {self.calculate_score(self.player_hand)})", inline=False)
        embed.add_field(name="Dealer's Hand", value=f"[{self.dealer_hand[0]}, ?]", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.player:
            return await interaction.response.send_message("You are not playing this game!", ephemeral=True)
        
        self.player_hand.append(self.draw_card())
        player_score = self.calculate_score(self.player_hand)
        
        if player_score > 21:
            await self.end_game(interaction, "You busted! Dealer wins.", False)
        else:
            await self.update_embed(interaction)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.player:
            return await interaction.response.send_message("You are not playing this game!", ephemeral=True)
        
        while self.calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw_card())
        
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        
        if dealer_score > 21 or player_score > dealer_score:
            await self.end_game(interaction, "Congratulations! You win!", True)
        elif player_score < dealer_score:
            await self.end_game(interaction, "Dealer wins!", False)
        else:
            await self.end_game(interaction, "It's a tie!", None)

    async def end_game(self, interaction, result, player_won):
        self.clear_items()
        embed = discord.Embed(title=f"🃏 Blackjack - {self.player.name}", color=discord.Color.gold())
        embed.add_field(name="Your Hand", value=f"{self.player_hand} (Total: {self.calculate_score(self.player_hand)})", inline=False)
        embed.add_field(name="Dealer's Hand", value=f"{self.dealer_hand} (Total: {self.calculate_score(self.dealer_hand)})", inline=False)
        embed.add_field(name="Result", value=result, inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

        conn = sqlite3.connect("economy.db")
        c = conn.cursor()
        if player_won:
            c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (self.bet * 2, self.player.id))  # **Changed from 3x to 2x**
        elif player_won is False:
            pass  # Coins were already deducted
        else:
            c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (self.bet, self.player.id))  # Refund on tie
        conn.commit()
        conn.close()


@bot.command()
async def blackjack(ctx, bet: int):
    user_id = ctx.author.id
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Ensure table exists
    c.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 500,
            last_daily INTEGER DEFAULT 0
        )
    """)

    # Fetch user's balance
    c.execute("SELECT balance FROM economy WHERE user_id=?", (user_id,))
    result = c.fetchone()

    if result is None:
        balance = 500  # Default balance for new users
        c.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, 0))
        conn.commit()
    else:
        balance = result[0]

    # Check if user has enough balance
    if balance < bet or bet <= 0:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to bet!")

    conn.close()  # Close DB here, we'll update it later after the game result.

    view = BlackjackButton(ctx.author, bet)
    embed = discord.Embed(title=f"🃏 Blackjack - {ctx.author.name}", color=discord.Color.gold())
    embed.add_field(name="Your Hand", value=f"{view.player_hand} (Total: {view.calculate_score(view.player_hand)})", inline=False)
    embed.add_field(name="Dealer's Hand", value=f"[{view.dealer_hand[0]}, ?]", inline=False)

    await ctx.send(embed=embed, view=view)


# Store invite data before restarts
old_invites = {}


# Initialize database
conn = sqlite3.connect("invites.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS invites (
             user_id INTEGER PRIMARY KEY,
             joins INTEGER DEFAULT 0,
             leaves INTEGER DEFAULT 0,
             fakes INTEGER DEFAULT 0,
             rejoins INTEGER DEFAULT 0)''')
conn.commit()
conn.close()

conn = sqlite3.connect("economy.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS economy (
             user_id INTEGER PRIMARY KEY,
             balance INTEGER DEFAULT 0)''')
conn.commit()
conn.close()

# Function to update invite stats
def update_invite_data(user_id, column):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO invites (user_id, joins, leaves, fakes, rejoins) VALUES (?, 0, 0, 0, 0)", (user_id,))
    c.execute(f"UPDATE invites SET {column} = {column} + 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# Function to add coins to inviter
def add_coins(user_id, amount):
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO economy (user_id, balance) VALUES (?, 0)", (user_id,))
    c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    conn.close()

@bot.event
async def on_member_join(member):
    """Triggered when a member joins."""
    guild = member.guild
    invites_before = old_invites.get(guild.id, {})  # Fetch stored invites
    invites_after = await guild.invites()  # Fetch updated invites
    old_invites[guild.id] = {invite.code: invite.uses for invite in invites_after}  # Update stored invites

    correct_inviter = None

    # Find the invite that was used
    for invite in invites_after:
        if invite.code in invites_before and invite.uses > invites_before[invite.code]:
            correct_inviter = invite.inviter
            break

    if correct_inviter:
        print(f"📢 {member.name} joined using {correct_inviter.name}'s invite!")

        # Check if this is a rejoin or new join
        conn = sqlite3.connect("invites.db")
        c = conn.cursor()
        c.execute("SELECT joins FROM invites WHERE user_id = ?", (member.id,))
        result = c.fetchone()
        conn.close()

        if result and result[0] > 0:
            update_invite_data(correct_inviter.id, "rejoins")  # Count as rejoin
        else:
            update_invite_data(correct_inviter.id, "joins")  # First-time join
            add_coins(correct_inviter.id, 500)  # Reward inviter with 500 coins
            await correct_inviter.send(f"🎉 You invited {member.name} and earned **500 coins**!")

    else:
        print(f"⚠️ Could not determine who invited {member.name}")

    await member.send("Welcome to the server!")

@bot.event
async def on_member_remove(member):
    """Triggered when a member leaves."""
    update_invite_data(member.id, "leaves")

    # Check if user should be marked as a fake
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == result[1]:  
        update_invite_data(member.id, "fakes")  # Mark as fake


# Fetch invite stats from the database
def get_invite_data(user_id):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves, fakes, rejoins FROM invites WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    return result if result else (0, 0, 0, 0)


# Add this auto-responder below on_ready()
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    await bot.process_commands(message)  # Allow commands to work
    # Auto-Response Dictionary
    auto_responses = {
        "hello": "Hello there! 👋",
        "how are you?": "I'm just a bot, but I'm doing great! 😃",
        "who made you?": "I was created by **Shreyansh GameTube**! 🔥",
        "what is lifesteal smp?": "Lifesteal SMP is a Minecraft mode where you **steal hearts** from enemies! ❤️⚔️",
        "good bot": "Thank you! 😊",
        "<@1101467683083530331>": "RESPECTIVELY, PLS DON'T PING THE **__OWNER!__**",
    }

    # Convert message to lowercase for case-insensitive matching
    user_message = message.content.lower()

    # Check if the message matches any auto-response
    for key in auto_responses:
        if key in user_message:
            await message.channel.send(auto_responses[key])
            break  # Stop checking after the first match

    # Note: bot.process_commands() is already called at the beginning of this function


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert seconds to milliseconds
    await ctx.send(f"<a:ping:1345381376433717269> Pong! {latency}ms")

# Moderation Commands
@bot.command()
@is_allowed_user()
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"✅ {member.mention} has been **kicked** for: `{reason}`")

@bot.command()
@is_allowed_user()
async def timeout(ctx, member: discord.Member, duration: int, *, reason="No reason provided"):
    """Timeouts a user for a specified duration (in seconds)."""
    try:
        await member.timeout(timedelta(seconds=duration), reason=reason)
        await ctx.send(f"⏳ {member.mention} has been **timed out** for `{duration} seconds`! Reason: `{reason}`")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to timeout this user!")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: `{e}`")

@bot.command()
@is_allowed_user()
async def removetimeout(ctx, member: discord.Member):
    """Removes timeout from a user."""
    try:
        await member.timeout(None)  # Removing timeout
        await ctx.send(f"✅ {member.mention}'s timeout has been **removed**!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to remove the timeout!")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: `{e}`")

@bot.command()
@is_allowed_user()
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 {member.mention} has been **banned** for: `{reason}`")

@bot.command()
@is_allowed_user()
async def unban(ctx, user_id: int):
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user)
    await ctx.send(f"🔄 {user.mention} has been **unbanned**!")


@bot.command()
@is_allowed_user()
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🗑️ Deleted `{amount}` messages!", delete_after=3)

@bot.command()
@is_allowed_user()
async def dm(ctx, user: discord.User, *, message):
    try:
        await user.send(message)
        await ctx.send(f"📩 Successfully sent a DM to {user.mention}!")
    except:
        await ctx.send(f"❌ Failed to send a DM to {user.mention}. They may have DMs disabled.")

# Note: We're using SQLite (economy.db) for all economy functions now
# These JSON functions aren't being used and can be removed

# Initialize economy database
def init_economy_db():
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER, last_daily INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS slots_history (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, bet_amount INTEGER, result TEXT, win_amount INTEGER, timestamp INTEGER)")
    conn.commit()
    conn.close()

# Initialize economy database at startup
init_economy_db()

@bot.command()
async def top(ctx):
    """Show the top 10 users with the highest coins."""
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Fetch the top 10 users sorted by balance (highest first)
    c.execute("SELECT user_id, balance FROM economy ORDER BY balance DESC LIMIT 10")
    top_users = c.fetchall()
    conn.close()

    if not top_users:
        await ctx.send("🚫 No users found in the leaderboard!")
        return

    # Create leaderboard embed
    embed = discord.Embed(title="🏆 **Top 10 Coin Leaderboard**", color=discord.Color.gold())
    
    for rank, (user_id, balance) in enumerate(top_users, start=1):
        user = bot.get_user(user_id)  # Fetch user object
        username = user.name if user else f"Unknown User ({user_id})"
        embed.add_field(name=f"#{rank} {username}", value=f"💰 {balance} coins", inline=False)

    embed.set_footer(text="🔥 Keep grinding to reach the top!")

    await ctx.send(embed=embed)

#slots

@bot.command()
async def slots(ctx, bet_amount: int):
    """Play a slot machine game! Bet your coins and try your luck."""
    
    if bet_amount <= 0:
        return await ctx.send("⚠️ Bet amount must be greater than zero!")

    user_id = ctx.author.id

    # Open Database Connection
    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Ensure economy table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 500,
            last_daily INTEGER DEFAULT 0
        )
    """)

    # Ensure slots history table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS slots_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            bet_amount INTEGER,
            result TEXT,
            win_amount INTEGER,
            timestamp INTEGER
        )
    """)

    # Fetch user's balance
    cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        balance = 500
        cursor.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, 0))
        conn.commit()
        result = (balance,)

    balance = result[0]

    if balance < bet_amount:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to play!")

    # Slot machine symbols
    symbols = ["🍎", "🍒", "🍋", "🍇", "🍊", "🍉", "🍓"]
    spin_result = [random.choice(symbols) for _ in range(3)]

    # Send spin result
    embed = discord.Embed(title="🎰 Slot Machine", color=discord.Color.gold())
    embed.add_field(name="Spin Result", value=f"**{spin_result[0]} | {spin_result[1]} | {spin_result[2]}**", inline=False)

    win_amount = 0
    if spin_result[0] == spin_result[1] == spin_result[2]:  # Jackpot (All 3 match)
        win_amount = bet_amount * 5
        new_balance = balance + win_amount
        embed.add_field(name="🎉 Jackpot!", value=f"You won **{win_amount} coins**!", inline=False)
    elif spin_result[0] == spin_result[1] or spin_result[1] == spin_result[2]:  # Small win (2 match)
        win_amount = bet_amount * 2
        new_balance = balance + win_amount
        embed.add_field(name="✨ Small Win!", value=f"You won **{win_amount} coins**!", inline=False)
    else:  # Loss
        new_balance = balance - bet_amount
        embed.add_field(name="💀 You Lost!", value=f"You lost **{bet_amount} coins**.", inline=False)

    embed.add_field(name="💰 New Balance", value=f"**{new_balance} coins**", inline=False)

    # Update balance
    cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (new_balance, user_id))

    # Save the game history
    current_time = int(datetime.utcnow().timestamp())
    result_str = f"{spin_result[0]}{spin_result[1]}{spin_result[2]}"
    cursor.execute("INSERT INTO slots_history (user_id, bet_amount, result, win_amount, timestamp) VALUES (?, ?, ?, ?, ?)", 
                  (user_id, bet_amount, result_str, win_amount, current_time))

    conn.commit()
    conn.close()

    await ctx.send(embed=embed)
#dm all command

OWNER_ID = 1101467683083530331  # Replace with your Discord ID


#vc record

@bot.command()
async def join(ctx):
    """Bot joins the voice channel."""
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("❌ You must be in a voice channel!")
        return
    
    channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await channel.connect()
        await ctx.send(f"✅ Joined `{channel.name}`")
    else:
        await ctx.voice_client.move_to(channel)
        await ctx.send(f"🔄 Moved to `{channel.name}`")

@bot.command()
async def leave(ctx):
    """Bot leaves the voice channel."""
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("❌ Left the voice channel!")
    else:
        await ctx.send("❌ I'm not in a voice channel!")

@bot.command()
async def record(ctx):
    """Starts recording the voice channel."""
    if ctx.author.voice is None or ctx.author.voice.channel is None:
        await ctx.send("❌ You must be in a voice channel!")
        return
    
    if ctx.voice_client is None:
        await ctx.send("❌ Bot is not in a voice channel! Use `.join` first.")
        return

    await ctx.send("🎙️ Recording started...")
    
    # Recording command using ffmpeg
    os.system("ffmpeg -y -f dshow -i audio=\"Stereo Mix (Realtek(R) Audio)\" -t 60 output.mp3")

    await asyncio.sleep(60)  # Recording for 60 seconds

    await ctx.send("✅ Recording stopped! Sending the file...")

    # Send the file
    await ctx.send(file=discord.File("output.mp3"))

@bot.command()
async def stop(ctx):
    """Stops the recording (not implemented properly yet)."""
    await ctx.send("❌ Recording stopped manually! (Stop command not properly implemented yet)")




@bot.command()
async def dmall(ctx, *, message: str = None):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("❌ You do not have permission to use this command!")

    if not message:
        return await ctx.send("⚠️ Missing arguments! Please provide a message to send.")

    sent_count = 0
    for member in ctx.guild.members:
        if not member.bot:  # Ignore bots
            try:
                await member.send(message)
                sent_count += 1
            except discord.Forbidden:
                pass  # Cannot DM this member (probably has DMs disabled)

    await ctx.send(f"✅ Successfully sent message to **{sent_count} members**!")


#Economy Commands


# Initialize invite tracking database
conn = sqlite3.connect("invites.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS invites (
             user_id INTEGER PRIMARY KEY,
             joins INTEGER DEFAULT 0,
             leaves INTEGER DEFAULT 0,
             fakes INTEGER DEFAULT 0,
             rejoins INTEGER DEFAULT 0)''')

conn.commit()
conn.close()

# Initialize economy database
conn = sqlite3.connect("economy.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS economy (
             user_id INTEGER PRIMARY KEY,
             balance INTEGER DEFAULT 0,
             last_daily INTEGER DEFAULT 0)''')

conn.commit()
conn.close()

# Function to update invite stats
def update_invite_data(user_id, column):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()

    # Ensure user exists in the database
    c.execute("INSERT OR IGNORE INTO invites (user_id) VALUES (?)", (user_id,))

    # Update the relevant column
    c.execute(f"UPDATE invites SET {column} = {column} + 1 WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

# Function to update inviter's coins
def add_coins(user_id, amount):
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Ensure user exists in the economy database
    c.execute("INSERT OR IGNORE INTO economy (user_id, balance) VALUES (?, 0)", (user_id,))

    # Add coins
    c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, user_id))

    conn.commit()
    conn.close()

# Function to get invite stats
def get_invite_data(user_id):
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves, fakes, rejoins FROM invites WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()

    return result if result else (0, 0, 0, 0)

# Function to find inviter
async def find_inviter(member):
    invites = await member.guild.invites()
    
    for invite in invites:
        if invite.uses > 0:
            return invite.inviter  # Return the user who created the invite

    return None  # No inviter found


    # Check if it's a rejoin
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] > 0:
        update_invite_data(member.id, "rejoins")  # Count as rejoin

@bot.event
async def on_member_remove(member):
    """Triggered when a member leaves."""
    update_invite_data(member.id, "leaves")

    # Check if user should be marked as a fake
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves FROM invites WHERE user_id = ?", (member.id,))
    result = c.fetchone()
    conn.close()

    if result and result[0] == result[1]:  
        update_invite_data(member.id, "fakes")  # Mark as fake

@bot.command()
async def invites(ctx, user: discord.Member = None):
    """Check a user's detailed invite stats from the database."""
    if user is None:
        user = ctx.author  # Default to the command caller

    # Fetch invite data from the database
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("SELECT joins, leaves, fakes, rejoins FROM invites WHERE user_id = ?", (user.id,))
    stats = c.fetchone()
    conn.close()

    if not stats:
        stats = (0, 0, 0, 0)  # Default values if user has no invites

    joins, leaves, fakes, rejoins = stats
    net_invites = joins - (leaves + fakes) + rejoins  # Net invites

    # Fetch coins earned only from inviting
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM economy WHERE user_id = ?", (user.id,))
    balance = c.fetchone()
    conn.close()

    balance = balance[0] if balance else 0  # Default to 0 if no record
    coins_from_invites = joins * 500  # Since each invite gives 500 coins

    embed = discord.Embed(title="📨 **Invite Log**", color=discord.Color.gold())
    embed.add_field(name="**User**", value=f"**{user.name}** has **{net_invites}** invites", inline=False)
    embed.add_field(name="✅ **Joins**", value=f"{joins}", inline=True)
    embed.add_field(name="❌ **Left**", value=f"{leaves}", inline=True)
    embed.add_field(name="⚠ **Fake**", value=f"{fakes}", inline=True)
    embed.add_field(name="🔄 **Rejoins**", value=f"{rejoins}", inline=True)
    embed.add_field(name="💰 **Coins Earned from Invites**", value=f"{coins_from_invites} 🪙", inline=False)
    embed.set_footer(text="🔥 Invite tracking by SHULKER BOT")

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def resetinvites(ctx, user: discord.Member):
    """Reset a specific user's invite stats in the database without affecting their coins."""
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("UPDATE invites SET joins = 0, leaves = 0, fakes = 0, rejoins = 0 WHERE user_id = ?", (user.id,))
    conn.commit()
    conn.close()

    await ctx.send(f"✅ Successfully reset invites for **{user.name}**!")


@bot.command()
@commands.has_permissions(administrator=True)
async def resetwholeserverinvite(ctx):
    """Reset invite stats for all users in the database without affecting their coins."""
    conn = sqlite3.connect("invites.db")
    c = conn.cursor()
    c.execute("DELETE FROM invites")  # Clears all invite data
    conn.commit()
    conn.close()

    await ctx.send("✅ Successfully reset **all invite records** for the server!")


@bot.command()
async def dice(ctx, bet: int):
    """Roll a dice against the bot! Highest number wins."""
    
    user_id = ctx.author.id
    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Ensure economy table exists
    cursor.execute("CREATE TABLE IF NOT EXISTS economy (user_id INTEGER PRIMARY KEY, balance INTEGER, last_daily INTEGER)")

    # Fetch user's balance
    cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None or result[0] < bet:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to bet that amount!")

    player_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)

    embed = discord.Embed(title="🎲 Dice Game!", color=discord.Color.blue())
    embed.add_field(name=f"{ctx.author.name}'s Roll", value=f"🎲 {player_roll}", inline=True)
    embed.add_field(name="Bot's Roll", value=f"🎲 {bot_roll}", inline=True)

    if player_roll > bot_roll:
        embed.add_field(name="🎉 Result", value=f"You **won** {bet} coins!", inline=False)
        new_balance = result[0] + bet
    elif player_roll < bot_roll:
        embed.add_field(name="💀 Result", value=f"You **lost** {bet} coins.", inline=False)
        new_balance = result[0] - bet
    else:
        embed.add_field(name="😲 Result", value="It's a **tie**! You keep your coins.", inline=False)
        new_balance = result[0]  # No change in balance

    # Update the database
    cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

    await ctx.send(embed=embed)
    
@bot.command(aliases=["bal"])
async def balance(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author  # Default to command user

    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Check if user exists
    c.execute("SELECT balance FROM economy WHERE user_id=?", (user.id,))
    data = c.fetchone()
    conn.close()

    balance = data[0] if data else 0  # Default balance is 0

    await ctx.send(f"<a:balance:1345373618070097982> {user.mention} has **{balance} coins**.")

    # **Debugging: Print the actual balance**
    print(f"DEBUG: {user.name}'s balance is {balance}")


@bot.command()
async def give(ctx, member: discord.Member, amount: int):
    """Transfer coins to another player securely."""
    
    if amount <= 0:
        return await ctx.send("❌ Amount must be greater than 0!")

    giver_id = ctx.author.id
    receiver_id = member.id

    if giver_id == receiver_id:
        return await ctx.send("❌ You cannot give coins to yourself!")

    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Ensure economy table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 500,
            last_daily INTEGER DEFAULT 0
        )
    """)

    # Ensure transactions table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            giver_id INTEGER,
            receiver_id INTEGER,
            amount INTEGER,
            timestamp TEXT
        )
    """)

    # Ensure both users exist in the economy table
    cursor.execute("INSERT OR IGNORE INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (giver_id, 500, 0))
    cursor.execute("INSERT OR IGNORE INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (receiver_id, 500, 0))

    # Fetch giver's balance
    cursor.execute("SELECT balance FROM economy WHERE user_id=?", (giver_id,))
    giver_balance = cursor.fetchone()[0]

    if giver_balance < amount:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to give!")

    # Perform transaction
    cursor.execute("UPDATE economy SET balance = balance - ? WHERE user_id = ?", (amount, giver_id))
    cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, receiver_id))

    # Log transaction
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    cursor.execute("INSERT INTO transactions (giver_id, receiver_id, amount, timestamp) VALUES (?, ?, ?, ?)", 
                   (giver_id, receiver_id, amount, timestamp))

    conn.commit()
    conn.close()

    # Create embed for transaction log
    embed = discord.Embed(title="💸 **Transaction Successful!**", color=discord.Color.green())
    embed.add_field(name="📤 **Payer**", value=f"{ctx.author.mention} (`{ctx.author.name}`)", inline=True)
    embed.add_field(name="📥 **Receiver**", value=f"{member.mention} (`{member.name}`)", inline=True)
    embed.add_field(name="💰 **Amount**", value=f"`{amount} 🪙`", inline=False)
    embed.add_field(name="📅 **Date & Time**", value=f"`{timestamp}`", inline=False)
    embed.set_footer(text="🔥 Secure transactions powered by SHULKER BOT")

    await ctx.send(embed=embed)


@bot.command()
async def setbalance(ctx, member: discord.Member, amount: int):
                            if ctx.author.id != 1101467683083530331:
                                await ctx.send("You don't have permission to use this command!")
                                return

                            conn = sqlite3.connect("economy.db")
                            c = conn.cursor()

                            # Ensure the user exists in the database
                            c.execute("INSERT OR IGNORE INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (member.id, 0, 0))

                            # Update balance
                            c.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (amount, member.id))

                            conn.commit()  # Save changes
                            conn.close()

                            await ctx.send(f"✅ Set {member.mention}'s balance to **{amount} coins**!")

                            # **Extra Debugging: Check if balance updated**
                            conn = sqlite3.connect("economy.db")
                            c = conn.cursor()
                            c.execute("SELECT balance FROM economy WHERE user_id=?", (member.id,))
                            new_balance = c.fetchone()
                            conn.close()

                            if new_balance:
                                print(f"DEBUG: {member.name}'s new balance is {new_balance[0]}")

#daily command

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    conn = sqlite3.connect("economy.db")
    c = conn.cursor()

    # Create the table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            last_daily INTEGER DEFAULT 0
        )
    """)

    # Fetch user data
    c.execute("SELECT balance, last_daily FROM economy WHERE user_id=?", (user_id,))
    data = c.fetchone()

    now = int(datetime.utcnow().timestamp())  # Current time in seconds

    if data:
        balance, last_daily = data
        if last_daily is None:
            last_daily = 0  # Handle possible NoneType error

        remaining_time = 86400 - (now - last_daily)
        if remaining_time > 0:  # If 24 hours haven't passed
            hours, remainder = divmod(remaining_time, 3600)
            minutes, _ = divmod(remainder, 60)
            await ctx.send(f"❌ You already claimed your daily reward! Try again in **{int(hours)}h {int(minutes)}m**.")
            conn.close()
            return
        
        balance += 100  # Add 100 coins
        c.execute("UPDATE economy SET balance=?, last_daily=? WHERE user_id=?", (balance, now, user_id))
    else:
        balance = 100  # First-time claim
        c.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, now))

    conn.commit()
    conn.close()

    await ctx.send(f"✅ {ctx.author.mention}, you claimed **100 coins**! Your new balance is **{balance} coins**.")







# CF Command

@bot.command()
async def cf(ctx, amount: int, choice: str):
    """Coinflip command: Bet an amount and choose heads or tails."""
    choice = choice.lower()
    if choice not in ["heads", "tails"]:
        return await ctx.send("⚠️ Invalid choice! Please choose heads or tails.")

    user_id = ctx.author.id

    # Open Database Connection
    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 500,
            last_daily INTEGER DEFAULT 0
        )
    """)

    # Fetch user's balance
    cursor.execute("SELECT balance FROM economy WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        # If user doesn't exist, insert them with a starting balance of 500
        balance = 500
        cursor.execute("INSERT INTO economy (user_id, balance, last_daily) VALUES (?, ?, ?)", (user_id, balance, 0))
        conn.commit()
    else:
        balance = result[0]

    # Check if user has enough balance
    if amount > balance or amount <= 0:
        conn.close()
        return await ctx.send("❌ You don't have enough coins to bet that amount!")

    # Flip the coin
    flip_result = random.choice(["heads", "tails"])

    if choice == flip_result:
        new_balance = balance + amount  # Win, add the bet amount
        await ctx.send(f"<:congrats:1345385894454100019> You won **{amount}** coins! <a:cf:1345374098427084922> The coin landed on **{flip_result}**! New balance: **{new_balance}** coins.")
    else:
        new_balance = balance - amount  # Lose, deduct the bet
        await ctx.send(f"<:sad:1345385609421656104> You lost **{amount}** coins. <a:cf:1345374098427084922> The coin landed on **{flip_result}**. New balance: **{new_balance}** coins.")

    # Update the user's balance in the database
    cursor.execute("UPDATE economy SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

# say and embed

@bot.command()
async def say(ctx, *, message=None):
    if ctx.author.id != 1101467683083530331:
        await ctx.send("❌ You are not allowed to use this command!")
        return

    if message is None:
        await ctx.send("❌ Please provide a message to say!")
    else:
        await ctx.send(message)

@bot.command()
async def embed(ctx, *, message=None):
    if ctx.author.id != 1101467683083530331:
        await ctx.send("❌ You are not allowed to use this command!")
        return

    if message is None:
        await ctx.send("❌ Please provide a message for the embed!")
    else:
        embed = discord.Embed(
            description=message,
            color=discord.Color.blue()  # You can change the color if needed
        )
        embed.set_footer(text=f"💘 BOT BY SHREYANSH GAMETUBE 💘")

        await ctx.send(embed=embed)


# Giveaway Command
@bot.command()
@is_allowed_user()
async def giveaway(ctx, duration: int, *, prize: str):
    embed = discord.Embed(title="🎉 **GIVEAWAY TIME!** 🎉", color=discord.Color.gold())
    embed.add_field(name="<a:gift1:1345383111877202021> **Prize:**", value=prize, inline=False)
    embed.add_field(name="<a:time:1345383309458538518> **Duration:**", value=f"{duration} seconds", inline=False)
    embed.set_footer(text="React with 🎉 to enter!")

    giveaway_message = await ctx.send(embed=embed)
    await giveaway_message.add_reaction("🎉")

    await asyncio.sleep(duration)

    new_message = await ctx.channel.fetch_message(giveaway_message.id)
    reaction = discord.utils.get(new_message.reactions, emoji="🎉")

    if reaction:
        users = [user async for user in reaction.users() if not user.bot]
    else:
        users = []

    if users:
        winner = random.choice(users)
        await ctx.send(f"🎊 Congratulations {winner.mention}, you won **{prize}**! 🎉")
    else:
        await ctx.send("❌ No one entered the giveaway!")

@bot.command()
@is_allowed_user()
async def gend(ctx, message_id: int):
    try:
        message = await ctx.channel.fetch_message(message_id)
        if not message.embeds:
            return await ctx.send("❌ That message doesn't contain a giveaway embed!")

        embed = message.embeds[0]
        if "🎉 **GIVEAWAY TIME!** 🎉" not in embed.title:
            return await ctx.send("❌ That message is not a giveaway!")

        reaction = discord.utils.get(message.reactions, emoji="🎉")
        if not reaction:
            return await ctx.send("❌ No one entered the giveaway!")

        users = [user async for user in reaction.users() if not user.bot]
        if not users:
            return await ctx.send("❌ No valid participants in the giveaway!")

        # Prevent duplicate messages by limiting selection to one winner announcement
        winner = random.choice(users)

        # Log to console to check if command is running multiple times
        print(f"[DEBUG] Winner selected: {winner}")

        await ctx.send(f"🎊 Congratulations {winner.mention}! You won **{embed.fields[0].value}**! 🎉")

    except discord.NotFound:
        await ctx.send("❌ Couldn't find a message with that ID!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to fetch messages!")
    except discord.HTTPException:
        await ctx.send("❌ An error occurred while fetching the message!")

@bot.command()
@is_allowed_user()
async def reroll(ctx, message_id: int):
    """Rerolls a giveaway to pick a new winner."""
    try:
        giveaway_message = await ctx.channel.fetch_message(message_id)

        # Get reactions from the giveaway message
        reaction = discord.utils.get(giveaway_message.reactions, emoji="🎉")
        if not reaction:
            return await ctx.send("❌ No valid giveaway reactions found!")

        # Get users who reacted (excluding bots)
        users = [user async for user in reaction.users() if not user.bot]

        if users:
            new_winner = random.choice(users)
            await ctx.send(f"🎊 **New winner:** {new_winner.mention}! Congratulations! 🎉")
        else:
            await ctx.send("❌ No valid participants to reroll the giveaway.")

    except discord.NotFound:
        await ctx.send("❌ Couldn't find the giveaway message. Make sure you provided the correct message ID!")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to fetch messages in this channel!")
    except Exception as e:
        await ctx.send(f"⚠️ An error occurred: `{e}`")

# Fun Commands
@bot.command()
async def roll(ctx):
    await ctx.send(f"🎲 You rolled a `{random.randint(1, 6)}`!")


@bot.command()
async def flip(ctx):
    await ctx.send(f"🪙 You got **{'Heads' if random.choice([True, False]) else 'Tails'}**!")

@bot.command()
async def joke(ctx):
    jokes = [
        "Why did the chicken cross the road? To get to the other side!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised!",
        "Why don’t skeletons fight each other? They don’t have the guts!",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my computer I needed a break, and now it won’t stop sending me vacation ads!",
        "Why don’t eggs tell jokes? Because they might crack up!",
        "Parallel lines have so much in common. It’s a shame they’ll never meet!",
        "I told my dog 10 jokes. He only laughed at one. Guess he’s not a paws-itively good audience!",
        "I asked my wife if I was the only one she’s been with. She said, 'Yes, the others were at least sevens or eights.'",
        "Did you hear about the restaurant on the moon? Great food, no atmosphere!",
        "Why did the golfer bring an extra pair of pants? In case he got a hole in one!",
        "What do you call fake spaghetti? An impasta!",
        "Why couldn't the bicycle stand up by itself? It was two-tired!",
        "I told my plants a joke. Now they’re rooted in laughter!",
        "How do you organize a space party? You planet!",
        "Why don’t some couples go to the gym? Because some relationships don’t work out!",
        "I only know 25 letters of the alphabet. I don’t know y.",
        "I used to be addicted to the hokey pokey, but then I turned myself around!"
    ]

    await ctx.send(f"🤣 {random.choice(jokes)}")

@bot.command()
async def meme(ctx):
    response = requests.get("https://meme-api.com/gimme/1")  # Corrected API URL
    if response.status_code == 200:
        meme_data = response.json()
        if 'memes' in meme_data and meme_data['memes']:  # Checking if memes exist
            meme = meme_data['memes'][0]  # Get the first meme
            embed = discord.Embed(title=meme['title'], url=meme['postLink'], color=discord.Color.random())
            embed.set_image(url=meme['url'])
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ No memes found. Try again later!")
    else:
        await ctx.send("❌ Couldn't fetch a meme. Try again later!")




@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return  # Prevents duplicate error handling

    if isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after, 2)
        await ctx.send(f"⏳ Command on cooldown! Try again in {remaining} seconds.", delete_after=5)

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing arguments! Please provide all required inputs.")

    elif isinstance(error, commands.CheckFailure):
        await ctx.send(f"❌ You don't have permission to use this command, {ctx.author.mention}!")

    else:
        # Log the error without sending it to the user
        print(f"Ignored error in command {ctx.command}: {error}")
        traceback.print_exc()  # Prints detailed error traceback for debugging








# Run the Bot
TOKEN = os.getenv("TOKEN")
if TOKEN is None:
    print("❌ ERROR: Discord bot token is missing! Set it in your environment variables.")
else:
    # Configure the http session with proper rate limiting
    bot.http.user_agent = 'ShulkerBot (https://discord.com, v1.0)'
    
    # More conservative approach with exponential backoff and session handling
    max_retries = 5
    retry_delay = 1800  # Start with 30 minutes (1800 seconds)
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            print(f"🚀 Starting bot with rate limit handling... (Attempt {retry_count+1}/{max_retries})")
            # Create a fresh client session each time
            if retry_count > 0:
                # Recreate client session to avoid "Session is closed" errors
                bot.http._HTTPClient__session = None  # Clear the existing session
            
            bot.run(TOKEN, reconnect=True)
            break  # If successful, exit the loop
        except discord.errors.HTTPException as e:
            if e.status == 429:
                retry_count += 1
                print(f"⚠️ Rate limit exceeded! Waiting for cooldown period ({retry_delay} seconds)...")
                import time
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the delay each time
                print("🔄 Attempting to restart bot...")
            else:
                print(f"❌ HTTP Error: {e}")
                break
        except Exception as e:
            print(f"❌ Error: {e}")
            if "Session is closed" in str(e):
                print("⚠️ Session closed error detected. Recreating session...")
                retry_count += 1
                time.sleep(60)  # Wait a minute before retry
                continue
            else:
                break
    
    if retry_count >= max_retries:
        print("❌ Maximum retry attempts reached. Please try again later.")
        print("⚠️ Discord may have temporarily blocked your bot due to rate limits.")
        print("⚠️ Consider waiting 24 hours before trying again.")


@bot.command()
async def slotsstats(ctx, user: discord.Member = None):
    """View slots statistics for a user"""
    if user is None:
        user = ctx.author

    user_id = user.id

    conn = sqlite3.connect("economy.db")
    cursor = conn.cursor()

    # Get total games played
    cursor.execute("SELECT COUNT(*) FROM slots_history WHERE user_id = ?", (user_id,))
    total_games = cursor.fetchone()[0]

    if total_games == 0:
        conn.close()
        return await ctx.send(f"{user.mention} hasn't played any slots games yet!")

    # Get wins
    cursor.execute("SELECT COUNT(*) FROM slots_history WHERE user_id = ? AND win_amount > 0", (user_id,))
    wins = cursor.fetchone()[0]

    # Get total bet and won amounts
    cursor.execute("SELECT SUM(bet_amount), SUM(win_amount) FROM slots_history WHERE user_id = ?", (user_id,))
    total_bet, total_won = cursor.fetchone()

    # Get biggest win
    cursor.execute("SELECT bet_amount, win_amount, result FROM slots_history WHERE user_id = ? ORDER BY win_amount DESC LIMIT 1", (user_id,))
    biggest_win_data = cursor.fetchone()

    conn.close()

    # Calculate win rate and profit/loss
    win_rate = (wins / total_games) * 100 if total_games > 0 else 0
    profit_loss = total_won - total_bet

    # Create an embed
    embed = discord.Embed(title=f"🎰 Slots Statistics for {user.name}", color=discord.Color.gold())
    embed.add_field(name="Games Played", value=f"{total_games}", inline=True)
    embed.add_field(name="Wins", value=f"{wins} ({win_rate:.1f}%)", inline=True)
    embed.add_field(name="Total Bet", value=f"{total_bet} coins", inline=True)
    embed.add_field(name="Total Won", value=f"{total_won} coins", inline=True)
    embed.add_field(name="Profit/Loss", value=f"{profit_loss} coins", inline=True)

    if biggest_win_data and biggest_win_data[1] > 0:
        embed.add_field(name="Biggest Win", value=f"{biggest_win_data[1]} coins (bet: {biggest_win_data[0]}, result: {biggest_win_data[2]})", inline=False)

    embed.set_footer(text="Keep playing to improve your stats!")

    await ctx.send(embed=embed)
