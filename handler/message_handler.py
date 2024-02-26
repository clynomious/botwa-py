from datetime import datetime
from termcolor import colored
import asyncio
from lib.serialize import Serialize


now = datetime.now()
formatted_time = now.strftime('%H:%M')

def print_log(cmd_name, push_name, sender, gc_name, is_group):
    log_message = f'[{formatted_time}] {cmd_name} by {push_name} : {sender.split("@")[0]}'
    if is_group:
        log_message += f' in {gc_name}'
    log_color = colored(log_message, 'white', 'on_blue')
    print("\n" + log_color)

def message_handler(client, message):
    try:
        msg = Serialize(client, message).simplified()
        msg_info = message.Info.MessageSource
        push_name = message.Info.Pushname
        prefix = client.config['prefix']
        
        group_info = client.get_group_info(message.Info.MessageSource.Chat)
        gc_name = group_info.GroupName.Name if group_info and group_info.GroupName else ""
        is_group = message.Info.MessageSource.IsGroup
  
        def find_command_by_alias(alias):
            for command_name, command_info in client.commands.items():
                if alias == command_name or (command_info.get('alias') and alias in command_info['alias']):
                    return command_info
            return None

        if msg.text.startswith(prefix):
            args = msg.text[len(prefix):].split(' ')
            cmd_name = args[0].lower() if args else ''
            arg = msg.text[len(cmd_name) + 1:]
            sender = msg_info.Sender.User
            is_owner = sender in client.config['ownerNumber']

            cmd = client.commands.get(cmd_name) or find_command_by_alias(cmd_name)
            if not cmd:
               return

            if 'owner' in cmd and cmd['owner'] == True:
                if not is_owner:
                    client.reply_message("You are not my owner", quoted=message)
                    return

            # Log
            print_log(cmd_name, push_name, sender, gc_name, is_group)

            # Execute command
            if cmd["async"] == True:
                asyncio.run(cmd['exec'](client=client, msg=msg, args=args, arg=arg, is_owner=is_owner))
            else:
                cmd['exec'](client=client, msg=msg, args=args, arg=arg, is_owner=is_owner)

    except Exception as err:
        print(f"Error: {err}")
