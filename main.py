from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import re

from astrbot.core.star.filter.event_message_type import EventMessageType
from data.plugins.astrbot_plugin_dy.api_collection import video


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.event_message_type(EventMessageType.ALL)
    async def helloworld(self, event: AstrMessageEvent):
        message_str = event.message_str # 用户发的纯文本消息字符串
        match = re.search(r'(https?://v\.douyin\.com/[\w-]+)', message_str)
        if match:
            logger.info(match)
            url = match.group(1)
            result = await video.mp4(url)
            await event.send(result)

