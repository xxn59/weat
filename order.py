# -*- coding: utf-8 -*-
import time
from flask import Flask,g,request,make_response
import hashlib
import xml.etree.ElementTree as ET
app = Flask(__name__)
app.debug=True
@app.route('/',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='weatorg'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
#        echostr = data.get('echostr','')
        echostr = data.get('echostr')
        print 'ech0str:',echostr
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            print 'signature correct'
#            return make_response('5838479218127813673')
            make_response(echostr)
            return 'ok'
        else:
            print 'signature err'
            print hashlib.sha1(s).hexdigest()
            print signature
            return 'error'
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())), content))
        response.content_type='application/xml'
        return response
