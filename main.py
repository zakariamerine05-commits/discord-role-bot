import discord
from discord.ext import commands
import os

# TOKEN من Railway Variables
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# ===== الأدوار اللي عندك =====
CONFIG = {
    'welcome_channel': 'الترحيب',
    'roles': {
        'Stumble Guys': 1498668611051458621,
        'Study': 1498668090706104531,
        'Movies': 1498668166014959777,
        'Among Us': 1498668019176439918,
        'PES': 1498667862393491566,
        'FIFA': 1498667736782602382,
        'GTA': 1498667648647692319
    }
}

@bot.event
async def on_ready():
    print(f'✅ ZM#4509 يعمل 24/7 مع {len(CONFIG["roles"])} دور!')
    print(f'📺 قناة الترحيب: {CONFIG["welcome_channel"]}')

class RoleSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label=name, 
                description=f'قناة {name}',
                emoji='🎮' if any(x in name.lower() for x in ['stumble', 'among', 'pes', 'fifa', 'gta']) 
                      else '📚' if name == 'Study' 
                      else '🎥',
                value=str(role_id)
            )
            for name, role_id in CONFIG['roles'].items()
        ]
        super().__init__(placeholder='🎮 اختر دورك...', options=options, max_values=1)
    
    async def callback(self, interaction: discord.Interaction):
        role_id = int(self.values[0])
        role = interaction.guild.get_role(role_id)
        
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                f'✅ **تم!**\n🎉 حصلت على دور **{role.name}**\n📺 الآن تشوف القنوات الخاصة!', 
                ephemeral=True
            )
            print(f'✅ {interaction.user} → {role.name}')
        else:
            await interaction.response.send_message(
                '❌ **خطأ!**\nالدور غير موجود\n⚙️ تحدث مع الإدارة', 
                ephemeral=True
            )

class RoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)  # 10 دقائق
        self.add_item(RoleSelect())

@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name=CONFIG['welcome_channel'])
    
    if not channel:
        print(f'❌ قناة "{CONFIG["welcome_channel"]}" غير موجودة في {guild.name}')
        return
    
    embed = discord.Embed(
        title=f'🎉 مرحباً بك {member.mention}!',
        description='**اختر اللي تهتم فيه عشان نحصلك على الدور المناسب:**',
        color=0x00FF88
    )
    embed.add_field(
        name='🎮 الخيارات المتاحة:',
        value='**Stumble Guys** | **Study** | **Movies**\n**Among Us** | **PES** | **FIFA** | **GTA**',
        inline=False
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text="اضغط على القائمة أسفل 👇")
    
    view = RoleView()
    await channel.send(embed=embed, view=view)
    print(f'🎉 رسالة ترحيب مرسلة لـ {member} في {guild.name}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    print(f'خطأ: {error}')

if __name__ == "__main__":
    if not TOKEN:
        print("❌ TOKEN مفقود! ضعه في Railway Variables")
    else:
        bot.run(TOKEN)
