import discord
from discord.ui import Button, View
from discord.ext import commands

PUG_MAX_PLAYER_COUNT = 12

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

# The list to store users who clicked the button
user_list = []

@bot.event
async def on_ready():
    guild_count = 0

    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count += 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

@bot.command()
async def send_button(ctx):
    # Create a button and add it to a view
    join_button = Button(style=discord.ButtonStyle.primary, label="Join.")
    remove_button = Button(style=discord.ButtonStyle.primary, label="Remove.")

    view = View()
    view.add_item(join_button)
    view.add_item(remove_button)

    # Send a message with the button
    message = await ctx.send("Click the button to join the list!", view=view)

    async def join_callback(interaction: discord.Interaction):
        try:
            user = interaction.user
            if user.id not in user_list and len(user_list) < PUG_MAX_PLAYER_COUNT:
                user_list.append(user.id)
                await interaction.response.send_message(f"{user.name} has joined the list!", ephemeral=True)
                # Set the message content for the original message (visible to everyone)
                await update_message_content(message)
            elif len(user_list) >= PUG_MAX_PLAYER_COUNT:
                await interaction.response.send_message("Pug is full. Added to next pug's queue.")
            else:
                await interaction.response.send_message("You are already signed up for this pug.")
        except Exception as e:
            print(f"Error in callback: {e}")

    async def remove_callback(interaction: discord.Interaction):
        try:
            user = interaction.user
            if user.id not in user_list:
                await interaction.response.send_message("You are not signed up for the pug.")
            else:
                user_list.remove(user.id)
                await interaction.response.send_message("You have been removed from the pug.", ephemeral=True)
                # Set the message content for the original message (visible to everyone)
                await update_message_content(message)
        except Exception as e:
            print(f"Error in callback: {e}")

    async def update_message_content(msg):
        # Update the message content with the current user list
        print(user_list)
        user_names = []
        for user_id in user_list:
            member = bot.get_user(user_id) or await bot.fetch_user(user_id)
            if member:
                user_names.append(member.name)

        if len(user_names) == 0:
            await msg.edit(content="No users in list.")
        else:
            await msg.edit(content=f"Current list: {', '.join(user_names)}")

    # Set the callback function for the button
    join_button.callback = join_callback
    remove_button.callback = remove_callback

bot.run("")
