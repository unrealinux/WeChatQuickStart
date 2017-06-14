# -*- coding: utf-8 -*-
from django.http import HttpResponse
import hashlib
from . import reply
from . import receive
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        token = 'circle'

        hashlist = [token, timestamp, nonce]
        hashlist.sort()

        hashstr = ''.join([s for s in hashlist])

        hashstr = hashlib.sha1(hashstr).hexdigest()

        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse('success')

    try:
        webData = request.body
        # 后台打日志
        # print "Handle Post webdata is ", webData
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = recMsg.Content
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.send())
        elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'image':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            mediaId = recMsg.MediaId
            replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
            return HttpResponse(replyMsg.send())
        else:
            # print "暂且不处理"
            return HttpResponse('success')
    except Exception:
        return HttpResponse('success')

