def exec(client, msg, args, arg, is_owner, **_):
    def find_command_by_alias(alias):
            for command_name, command_info in client.commands.items():
                if alias == command_name or (command_info.get('alias') and alias in command_info['alias']):
                    return command_info
            return None
        
    if arg:
        data = []
        name = args[1].lower()
        prefix = client.config["prefix"]  
        cmd = client.commands.get(name) or find_command_by_alias(name)
        if not cmd or (cmd.get('category') == 'owner' and not is_owner):
            msg.reply("No command found for " + name)
        else:
            data.append(f"*Cmd:* {cmd['name']}")
            if 'alias' in cmd:
                data.append(f"*Alias:* {', '.join(cmd['alias'])}")
            if 'desc' in cmd:
                data.append(f"*Desc:* {cmd['desc']}")
            if 'use' in cmd:
                data.append(f"*Usage:* ```{prefix}{cmd['name']} {cmd['use']}```\n\nNote: [] = optional, | = or, <> = must filled")
            msg.reply('\n'.join(data))
    else:
        cmds = [cmd for cmd in client.commands.values() if cmd.get('category') and cmd['category'] != 'owner' and not cmd.get('owner')]
        category = {}
            
        for cmd in cmds:
            info_category = cmd['category']
            if info_category in category:
                category[info_category].append(cmd)
            else:
                category[info_category] = [cmd]
                
        data = f"Hello, {msg.pushname} i am {msg.botname}\n*This is My Command List*\n\n"
        keys = list(category.keys())
        for key in keys:
            data += f"> *{key.upper()}*\n"
            data += '\n'.join(f"{idx + 1}. {client.config["prefix"]}{cmd['name']}" for idx, cmd in enumerate(category[key]))
            data += "\n\n"
            
        data += f"send {client.config["prefix"]}help with command name for command details.\nex. {client.config["prefix"]}help ping"
            
        msg.reply(data)

command = {
    "name": "help",
    "alias": ["menu"],
    "category": "general",
    "async": False,
    "exec": exec
}