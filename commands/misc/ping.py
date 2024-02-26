import subprocess
import re

def exec(client, msg, **_):
        host = "whatsapp.net"
        result = subprocess.run(['ping', '-n', '4', host], capture_output=True, text=True, check=True)
        ping_time_match = re.search(r'Average = (\d+ms)', result.stdout)

        if ping_time_match:
            ping_time = ping_time_match.group(1)
            msg.reply(f"Ping time for {host}: {ping_time}")
        else:
            msg.reply(f"Unable to extract ping time from output:\n{result.stdout}")

command = {
    "name": "ping",
    "category": "misc",
    "desc": "Bot response.",
    "async": False,
    "exec": exec
}