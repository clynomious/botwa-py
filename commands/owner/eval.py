def exec(msg, arg, **_):
    try:
        evaled = eval(arg)
        if not isinstance(evaled, str):
                evaled = str(evaled)
                msg.reply(f"{evaled}")
    except Exception as e:
        error_message = f'Error: {str(e)}'
        msg.reply(error_message, quoted=msg.message)

command = {
    "name": "eval",
    "alias": ["ev"],
    "category": "owner",
    "desc": "Eval code",
    "async": False,
    "owner": True,
    "exec": exec
}