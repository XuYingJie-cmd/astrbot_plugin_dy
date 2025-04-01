from astrbot.api import event
from astrbot.api.all import *
import aiohttp
import logging
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.message_components import Video, Plain, Image

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def mp4(url):
    logger.info(f"检测到抖音: {url}")
    api_url = f"https://api.yujn.cn/api/dy_jx.php?msg={url}"
    result = MessageChain()
    try:
        logger.info("开始下载")
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                logger.info(f"返回结果，状态码: {response.status}")
                try:
                    response_json = await response.json()

                    # 优先处理错误信息
                    if response_json.get('msg') == '解析失败！💦':
                        result.chain = [
                            Plain("😢解析失败！请检查抖音链接是否正确。"),
                        ]
                        return result

                    # 优先发送图片集合（如果存在）
                    if 'images' in response_json and len(response_json['images']) > 0:
                        result.chain = [
                            Plain("🎞️检测到图集内容："),
                            Plain(f"📝标题: {response_json.get('title', '无标题')}"),
                        ]
                        for img_url in response_json['images']:
                            result.chain.append(Image.fromURL(img_url))
                        return result

                    # 发送视频（如果存在）
                    if 'video' in response_json and response_json['video']:
                        video_url = response_json['video']
                    elif 'play_video' in response_json and response_json['play_video']:
                        video_url = response_json['play_video']
                    else:
                        result.chain = [
                            Plain("😔未找到有效内容"),
                        ]
                        return result

                    # 构造成功响应
                    result.chain = [
                        Plain("🎉抖音视频解析成功,正在发送!💬️"),
                        Plain(f"🎬标题: {response_json.get('title', '无标题')}"),
                        Video.fromURL(video_url)
                    ]
                    logger.info(f"视频链接: {video_url}")
                    return result

                except ValueError:
                    text = await response.text()
                    result.chain = [
                        Plain("😣响应不是有效的JSON格式"),
                    ]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"😫请求异常: {e}")]
    return result