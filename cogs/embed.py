from discord.ext import commands
import discord
import shlex

class EmbedCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='embed', desciption="Generates an embed with given params.")
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, args):
        """A simple command which generate embeds using keywords.
        Named parameters:
            - title (str)
            - descr (str)
            - colour (int)
            - img (url)
            - author_icon (url)
            - author_name (str)
            - author_url (url)
            - print_dict (bool)
            - footer_test (str)
            - footer_icon (url)
        Examples:
        wd-embed title="title";descr="description"
        wd-embed title="title";descr="description";print_dict=True
        wd-embed title="title";descr="description";url="https://google.com"
        """

        args_dict = {}

        for arg in shlex.split(args):
            print(arg)
            splitted_arg = arg.split("=")
            args_dict[splitted_arg[0]] = splitted_arg[1].strip('"').strip("'")

        def build_embed(**kwargs):

            title = kwargs.pop('title', "Title")
            descr = kwargs.pop('descr', "Description")
            colour = kwargs.pop('colour', ctx.author.color)
            img = kwargs.pop('img', None)
            author_icon = kwargs.pop('author_icon', ctx.author.avatar_url)
            author_name = kwargs.pop('author_name', ctx.author.name)
            author_url = kwargs.pop('author_url', ctx.author.avatar_url)
            print_dict = kwargs.pop('print_dict', False)
            footer_text = kwargs.pop('footer_text', None)
            footer_icon = kwargs.pop('footer_icon', None)
            content = ''

            embed = discord.Embed(
                title=title,
                description=descr,
                colour=colour
            )
            embed.set_author(
                icon_url=author_icon,
                name=author_name,
                url=author_url
            )

            if img:
                embed.set_image(url=img)

            if footer_text or footer_icon:
                embed.set_footer(text=footer_text, icon_url=footer_icon)

            for key, value in kwargs.items():
                embed.add_field(name=key, value=value, inline=True)

            if print_dict:
                content = embed.to_dict()

            return content, embed

        content, embed = build_embed(**args_dict)
        await ctx.send(content=content, embed=embed)

    #
    # ERROR HANDLER
    #
    @embed.error
    async def getparam_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Title",
                description="Description",
                colour=ctx.author.color
            )
            await ctx.send(content='', embed=embed)


def setup(client):
    client.add_cog(EmbedCommands(client))