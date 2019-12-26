from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage
from module import func
from urllib.parse import parse_qsl
from func5api.models import users
from django.shortcuts import render

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                user_id = event.source.user_id      #取得user_id
                if not(users.objects.filter(uid = user_id).exists()):  #將user_id存入資料庫中
                    unit = users.objects.create(uid = user_id)
                    unit.save()    #將user_id上傳至資料庫
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@修繕申請':
                        func.sendFix(event, user_id)
                    elif mtext =='@修繕查詢':
                        func.fix_inquire(event, user_id)
                    elif mtext == 'admin_mode':
                         func.adminMode(event, user_id)
                    elif mtext[:6] == '123456' and len(mtext) > 6:
                         func.pushMessage_all(event, mtext)
                    elif mtext[:2] == '++' and len(mtext) > 2:
                         func.pushMessage_specify(event, mtext)
                    elif mtext[:2] == '##' and len(mtext) > 2:
                         func.manageForm(event, mtext, user_id)
                    elif mtext[:3] == '!!!' and len(mtext) > 3:
                         func.personData(event, mtext, user_id)
    
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
        
def listall(request):
        user = users.objects.all().order_by('name')
        return render(request, "listall.html", locals())
