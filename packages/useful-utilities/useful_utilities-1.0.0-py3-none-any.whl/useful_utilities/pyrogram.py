import time


def temp_reply(message, text, delay=5, quote=False, delete_original_message=False):
    try:
        reply = message.reply(text=text, quote=quote, disable_notification=True)
        time.sleep(delay)
        reply.delete(revoke=True)
        if delete_original_message:
            message.delete(revoke=True)
    except Exception as e:
        pass