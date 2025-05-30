from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TemplateMessage,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    TextMessage,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
import os

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == '文字':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="這是文字訊息")]
                )
            )
        elif text == '表情符號':
            emojis = [
                Emoji(index=0, product_id="5ac1bfd5040ab15980c9b435", emoji_id="001"),
                Emoji(index=12, product_id="5ac1bfd5040ab15980c9b435", emoji_id="002")
            ]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text='$ LINE 表情符號 $', emojis=emojis)]
                )
            )
        elif text == '貼圖':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(package_id="6362", sticker_id="11087923")]
                )
            )
        elif text == '圖片':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        elif text == '影片':
            url = request.url_root + 'static/video.mp4'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        VideoMessage(original_content_url=url, preview_image_url=url)
                    ]
                )
            )
        elif text == '音訊':
            url = request.url_root + 'static/music.mp3'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            duration = 10000  # in milliseconds
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        AudioMessage(original_content_url=url, duration=duration)
                    ]
                )
            )
        elif text == '位置':
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(title='Location', address="Taipei", latitude=24.9472391, longitude=121.2289817)
                    ]
                )
            )

        # 確認卡
        elif text == '確認卡':
            confirm_template = ConfirmTemplate(
                text='確認卡有出現嗎?',
                actions=[
                    MessageAction(label='是', text='讚喔'),
                    MessageAction(label='否', text='否!')
                ]
            )
            template_message = TemplateMessage(
                alt_text='Confirm alt text',
                template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # 圖片資訊卡
        elif text == '圖片資訊卡':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title='標題',
                text='詳細說明',
                actions=[
                    # URIAction(label='連結', uri='https://www.facebook.com/NTUEBIGDATAEDU'),
                    # PostbackAction(label='回傳值', data='ping', displayText='傳了'),
                    # MessageAction(label='傳"哈囉"', text='哈囉'),
                    # DatetimePickerAction(label="選擇時間", data="時間", mode="datetime"),
                    CameraAction(label='拍照'),
                    CameraRollAction(label='選擇相片'),
                    LocationAction(label='選擇位置')
                ]
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template",
                template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[template_message]
                )
            )
        # 左右滑動 圖片資訊卡
        elif text == '左右滑動 圖片資訊卡':
            url = request.url_root + 'static/Logo.jpg'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            carousel_template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=url,
                        title='第一項',
                        text='這是第一項的描述',
                        actions=[
                            URIAction(
                                label='按我前往 Google',
                                uri='https://www.google.com'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url=url,
                        title='第二項',
                        text='這是第二項的描述',
                        actions=[
                            URIAction(
                                label='按我前往 Yahoo',
                                uri='https://www.yahoo.com'
                            )
                        ]
                    )
                ]
            )

            carousel_message = TemplateMessage(
                alt_text='這是 Carousel Template',
                template=carousel_template
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages =[carousel_message]
                )
            )

        # 一列式圖片資訊卡
        elif text == '一列式圖片資訊卡':
            url = request.url_root + 'static/'
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=url+'facebook.png',
                        action=URIAction(
                            label='造訪FB',
                            uri='https://www.facebook.com/NTUEBIGDATAEDU'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=url+'instagram.png',
                        action=URIAction(
                            label='造訪IG',
                            uri='https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y='
                        )
                    ),
                    ImageCarouselColumn(
                        image_url=url+'youtube.png',
                        action=URIAction(
                            label='造訪YT',
                            uri='https://www.youtube.com/@bigdatantue'
                        )
                    ),
                ]
            )

            image_carousel_message = TemplateMessage(
                alt_text='圖片輪播範本',
                template=image_carousel_template
            )

            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_carousel_message]
                )
            )
        
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)]
                )
            )

if __name__ == "__main__":
    app.run()