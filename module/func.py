from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction, ImageSendMessage, TemplateSendMessage, ButtonsTemplate, URITemplateAction, ConfirmTemplate, PostbackTemplateAction

from func5api.models import fix,users

from django.db.models import Q

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendFix(event, user_id):    #修繕表單申請
    try:
        if not (fix.objects.filter(fid=user_id).filter(status__exact = '未處理').exists()):  #沒有訂房記錄
            message = TemplateSendMessage(
                alt_text = "修繕申請",
                template = ButtonsTemplate(
                    thumbnail_image_url='https://i.imgur.com/1NSDAvo.jpg',
                    title='修繕申請',
                    text='您目前沒有未完成的修繕申請，可以開始填寫表單。',
                    actions=[
                        URITemplateAction(label='修繕表單填寫',
                         uri='line://app/1653654903-myrYZGgb')
                        #開啟LIFF讓使用者輸入訂房資料
                    ]
                )
            )
        else:  #已有訂房記錄
            message = TextSendMessage(
                text = '您目前已有申請修繕並還未修繕，一個人不能同時申請兩次。'
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def fix_inquire(event, user_id):    #維修表單進度查詢
    try:
        if fix.objects.filter(fid=user_id).exists():
            fixdata = fix.objects.filter(fid=user_id).latest('created_time')   #讀取修繕的資料
            name = fixdata.cName
            room = fixdata.room
            item = fixdata.item
            status = fixdata.status
            text1 = "您最新申請的修繕記錄如下:"
            text1 += "\n姓名：" + name
            text1 += "\n房間：" + room
            text1 += "\n物品：" + item
            text1 += "\n\n目前修繕進度：" + status
            
            message = TextSendMessage(   #顯示修繕的資料
                text = text1
            )
            line_bot_api.reply_message(event.reply_token,message)
        else:
            message = TextSendMessage(
                text = '您目前沒有修繕申請的紀錄喔！'
            )
            line_bot_api.reply_message(event.reply_token,message)
    except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            


#處理修繕表單輸入得值，並上傳到資料庫中
def manageForm(event, mtext, user_id):
    try:
        flist = mtext[2:].split('/')
        
        name = flist[0]
        student_id = flist[1]
        room = flist[2]
        item = flist[3]
        description = flist[4]
        
        unit = fix.objects.create(fid = user_id, cName = name, student_number = student_id, room = room, item = item, description = description, status = '未處理')
        
        unit.save()
        
        
        text1 = '姓名：' + name + '\n'
        text1 += '學號：' + student_id + '\n'
        text1 += '房間：' + room + '\n'
        text1 += '修繕物品：' + item + '\n'
        text1 += '修繕物品描述：' + description
        message = TextSendMessage(   #顯示修繕的資料
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


#使用者基本資料的填寫
def personData(event, mtext, user_id):
    try:
        if users.objects.filter(uid=user_id).exists():
        
            ulist = mtext[3:].split('/')
            
            user_id = ulist[0]
            name= ulist[1]
            student_id = ulist[2]
            
            users.objects.filter(uid=user_id).update(name = name, student_number = student_id)
            
            text1 = '姓名：' + name + '\n'
            text1 += '學號：' + student_id + '\n\n'
            text1 += '感謝您的填寫，現在您可以享有完整的宿舍服務！'
            
            message = TextSendMessage(
                text = text1
            )
            
            line_bot_api.reply_message(event.reply_token,message)
            
        else:
            ulist = mtext[3:].split('/')
            
            user_id = ulist[0]
            name= ulist[1]
            student_id = ulist[2]
            
            unit = users.objects.create(uid = user_id, name = name, student_number = student_id)
            
            unit.save()
            
            text1 = '姓名：' + name + '\n'
            text1 += '學號：' + student_id + '\n\n'
            text1 += '感謝您的填寫，現在您可以享有完整的宿舍服務！'
            
            message = TextSendMessage(
                text = text1
            )
            
            line_bot_api.reply_message(event.reply_token,message)
            
            
            
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def pushMessage_all(event, mtext):  #推播訊息給所有使用者
    try:
        msg = mtext[6:]  #取得訊息
        userall = users.objects.all()
        for user in userall:  #逐一推播
            message = TextSendMessage(
                text = msg
            )
            line_bot_api.push_message(to=user.uid, messages=[message])  #推播訊息
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))


def pushMessage_specify(event, mtext):  #推播訊息給特定使用者
    try:
        slist = mtext[2:].split(' /')
        slist = slist[:-1]
        
        message = TextSendMessage(
            text = '同學您好，您有包裹送達宿舍，請儘速持學生證到櫃台簽收！'
        )
        
        for i in slist:
            
            line_bot_api.push_message(to=i, messages=[message])
        
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def adminMode(event, user_id):
    try:
        message = TextSendMessage(
            text = 'line://app/1653654903-e6GxJ4Pd'
        )
        
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
