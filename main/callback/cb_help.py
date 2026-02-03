from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton
from pyrogram.errors import MessageNotModified
from pykeyboard import InlineKeyboard
from main.helpers.utils.handler import BOT

import os
import importlib
import math

def load_modules():
    modules = {}
    commands_dir = os.path.join('main', 'commands')
    if not os.path.exists(commands_dir):
        print(f"Directory not found: {commands_dir}")
        return modules
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = filename[:-3]
            module = importlib.import_module(f'main.commands.{module_name}')
            if hasattr(module, '__MODULE__') and hasattr(module, '__DESCRIPTION__'):
                commands = getattr(module, '__COMMANDS__', "No commands available.")
                modules[module.__MODULE__] = {
                    'description': module.__DESCRIPTION__,
                    'commands': commands
                }
    return modules

MODULES = load_modules()

def create_module_keyboard(page=1):
    keyboard = InlineKeyboard()
    modules_list = list(MODULES.items())
    modules_per_page = 4  # 2x2 grid
    total_pages = math.ceil(len(modules_list) / modules_per_page)
    start = (page - 1) * modules_per_page
    end = start + modules_per_page
    
    for i in range(start, min(end, len(modules_list)), 2):
        row = []
        for j in range(i, min(i+2, len(modules_list))):
            module_name, module_info = modules_list[j]
            button_text = module_name
            row.append(InlineKeyboardButton(button_text, callback_data=f"CB_HELP_MODULE_{module_name}"))
        keyboard.row(*row)
    
    nav_row = []
    if page > 1:
        nav_row.append(InlineKeyboardButton("Prev", callback_data=f"CB_HELP_PAGE_{page-1}"))
    nav_row.append(InlineKeyboardButton("Back", callback_data="CB_START"))
    if page < total_pages:
        nav_row.append(InlineKeyboardButton("Next", callback_data=f"CB_HELP_PAGE_{page+1}"))
    if nav_row:
        keyboard.row(*nav_row)
    
    keyboard.row(InlineKeyboardButton("Close", callback_data="CB_CLOSE"))
    return keyboard

@BOT.CALLBACK("^CB_HELP$")
async def help_callback(client: Client, callback: CallbackQuery):
    free_modules = len(MODULES)
    text = f"Total modules : {free_modules}"
    keyboard = create_module_keyboard()
    try:
        await callback.edit_message_text(text, reply_markup=keyboard)
    except MessageNotModified:
        pass  

@BOT.CALLBACK("^CB_HELP_PAGE_")
async def help_page_callback(client: Client, callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])
    free_modules = len(MODULES)
    text = f"Total modules : {free_modules}"
    keyboard = create_module_keyboard(page)
    try:
        await callback.edit_message_text(text, reply_markup=keyboard)
    except MessageNotModified:
        pass

@BOT.CALLBACK("^CB_HELP_MODULE_")
async def module_callback(client: Client, callback: CallbackQuery):
    module_name = callback.data.split('_')[3]
    module_info = MODULES.get(module_name, {"description": "No description available.", "commands": "No commands available."})
    description = module_info['description']
    commands = module_info['commands']
    
    # Create a new keyboard with a back button
    keyboard = InlineKeyboard()
    keyboard.row(InlineKeyboardButton("Back", callback_data="CB_BACK_HELP"))
    try:
        await callback.message.edit_text(
            f"{description}\n\n"
            f"{commands}",
            reply_markup=keyboard
        )
    except MessageNotModified:
        pass

@BOT.CALLBACK("^CB_BACK_HELP$")
async def back_help_callback(client: Client, callback: CallbackQuery):
    free_modules = len(MODULES)
    text = f"Total modules : {free_modules}"
    keyboard = create_module_keyboard()
    try:
        await callback.message.edit_text(text, reply_markup=keyboard)
    except MessageNotModified:
        pass


@BOT.CALLBACK(".*")
async def debug_callback(client: Client, callback: CallbackQuery):
    print(f"Received callback data: {callback.data}")

print(f"Loaded modules: {MODULES} Support Channel @Dzdisni")
