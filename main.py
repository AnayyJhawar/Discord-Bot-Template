import sys
from urllib.parse import quote_plus
from asyncio import sleep
from PIL.Image import core as _imaging
import disnake
from disnake.ext import commands
import os
import typing as typ
from typing import Union, Optional, List
import json
import _json
import random
import datetime
import asyncio
import aiohttp
import time
from dotenv import load_dotenv
import io
from io import BytesIO
from petpetgif import petpet as petpetgif

load_dotenv()

intents = disnake.Intents.all()
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='.')
bot.remove_command('help')

