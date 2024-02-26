def exec(client, msg, **_):
    media_type = msg.media_type
    try:
        if ( msg.message_type == "text" or msg.is_media and media_type in ("image", "video")):
            media_message = x if (x := msg.quoted_message()) else msg
            if (
                    media_message.media_type == "video"
                    and media_message.raw_message.videoMessage.seconds > 10
                ):
                    msg.reply("Video duration too long")
                    return
            if media_message.is_media and media_message.media_type in (
                    "image",
                    "video",
                ):
                    media = client.download_any(media_message.raw_message)
                    client.send_sticker(
                        msg.to,
                        media,
                        msg.message,
                        "Celly",
                        "Chan",
                    )
            else:
                msg.reply("Send or reply a image or video")
    except Exception as err:
        print(err)
        

command = {
    "name": "sticker",
    "alias": ["stiker", "s"],
    "category": "general",
    "desc": "Create sticker from image or video",
    "async": False,
    "exec": exec
}