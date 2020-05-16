#! python3
# coding: utf-8

"""Writes all messages to db"""
import discord
import sqlite3
import asyncio
import traceback
import time
from discord.ext import commands
from .utils import logger



class message_log:

    def __init__(self, bot):
        self.bot = bot
        self.database = '/path/to/database.db'

    async def on_message(self, message):
        try:
            if message.channel.id == "220218672856170496" and message.clean_content != "": #replace channel id with the one you want to log for
                db = sqlite3.connect(self.database)
                cursor = db.cursor()
                user = cursor.execute("select * from users where user = ?", (message.author.id,)).fetchone()
                u = message.author
                if not user: #if user not in users table, add. Modifying when avatars change would be neat too but im lazy
                    try:
                        name = member.nick
                    except:
                        name = member.name
                    color = "#{0:06X}".format(16777215  if str(u.top_role) == "@everyone" else u.color.value)
                    cursor.execute("insert into users(user,name,discrim,avatar,color) values(?,?,?,?,?)", (u.id, name, u.discriminator, u.avatar_url, color))
                cursor.execute("insert into messages(time,message,user) values(?,?,?)", (time.time(),message.clean_content,u.id)) #push message
                db.commit()
                cursor.close()
                db.close()
        except Exception as e:
            await logger.errorLog(message.content, message.author, e, traceback.format_exc())



def setup(bot):
    bot.add_cog(message_log(bot))
