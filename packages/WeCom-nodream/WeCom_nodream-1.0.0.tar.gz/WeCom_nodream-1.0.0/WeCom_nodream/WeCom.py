import os
import io
import json
import logging
import requests
""" 
    @author:梦无念
    @description:企业微信接口
    @version:1.0
    @param:
"""
class WeCom:
    def __init__(self,agentid, corpid, corpsecret):
        self.baseUrl = "https://qyapi.weixin.qq.com"
        self.agentid = agentid
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.access_token = self.getAccessToken()

    # 获得access_token
    def getAccessToken(self):
        # 如果agentId,corpid,corpsecret为空，则获取终止
        if self.corpid == "" or self.corpsecret == "":
            print("corpid或corpsecret不能为空")
            return
        url = f"{self.baseUrl}/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
        response = requests.request("GET", url).json()
        try:
            return response["access_token"]
        except:
            print("获取access_token失败,请检查corpid和corpsecret是否正确")

    # 上传临时素材
    """ 上传临时素材
    :param fileType: 媒体文件类型,分别有图片(image)、语音(voice)、视频(video)和文件(file)
    :param file: url地址或者文件流(io.BufferedReader)
    :param fileName: 媒体文件名
    """
    def uploadTemp(self, fileType,file,fileName=''):
        if fileType == "":
            logging.error('type can not be empty')
            return
        if type(file) == str:
            fileSize = 0
            file = requests.get(file,stream=True)
            fileSize = int(file.headers['Content-Length'])/1024/1024
            file = file.content
        elif type(file) == io.BufferedReader:
            file = file.read()
            fileSize = len(file)/1024/1024
            if fileName == "":
                fileName = file.name
        else:
            logging.error('file type error')
            return
        # 文件大小判断
        if fileType == 'image' and fileSize > 10:
            logging.error('image size must less than 10M')
            return
        elif fileType == 'voice' and fileSize > 2:
            logging.error('voice size must less than 2M')
            return
        elif fileType == 'video' and fileSize > 10:
            logging.error('video size must less than 10M')
            return
        elif fileType == 'file' and fileSize > 20:
            logging.error('file size must less than 20M')
            return
        # 文件类型判断
        if fileType == 'image' and (fileName.split('.')[-1] != 'jpg' or fileName.split('.')[-1] != 'png'):
            logging.error('image must be jpg or png')
            return
        elif fileType == 'voice' and fileName.split('.')[-1] != 'AMR':
            logging.error('voice must be AMR')
            return
        elif fileType == 'video' and fileName.split('.')[-1] != 'mp4':
            logging.error('video must be mp4')
            return
        files=[
        (fileName,file)
        ]
        response = requests.request("POST", f"{self.baseUrl}/cgi-bin/media/upload?access_token={self.access_token}&type={fileType}", files=files).json()
        return response
    
    # 发送应用消息
    """
    :param msgType: 消息类型,分别有text、image、voice、video、file
    :param content/media_id: 消息内容或者媒体id
    """
    def sendAppMsg(self,msgType, content):
        if msgType == "":
            logging.error('type can not be empty')
            return
        data =  {}
        if msgType == 'text':
            data = json.dumps({
        "touser": "@all",
        "msgtype": "text",
        "agentid": self.agentid,
        "text": {
            "content": content
        }
        })
        else :
            data= json.dumps({
            "touser": "@all",
            "msgtype": msgType,
            "agentid": self.agentid,
            msgType:{
                "media_id": content
            }
        })
        response = requests.request("POST", f"{self.baseUrl}/cgi-bin/message/send?access_token={self.access_token}", data=data).json()
        return response

    # 发送卡片消息
    """
    :param title: 标题
    :param description: 描述
    :param url: 点击后跳转的链接
    :param btntxt: 按钮文字
    """
    def sendCardMsg(self,title,description,url,btntxt):
        data = json.dumps({
        "touser": "@all",
        "msgtype": "textcard",
        "agentid": self.agentid,
        "textcard": {
            "title": title,
            "description": description,
            "url": url,
            "btntxt": btntxt
        }
        })
        response = requests.request("POST", f"{self.baseUrl}/cgi-bin/message/send?access_token={self.access_token}", data=data).json()
        return response

    # 发送图文消息
    """
    :param title: 标题
    :param description: 描述
    :param url: 点击后跳转的链接
    :param picurl: 图片链接
    """
    def sendNewsMsg(self,title,description,url,picurl):
        data = json.dumps({
        "touser": "@all",
        "msgtype": "news",
        "agentid": self.agentid,
        "news": {
            "articles": [
                {
                    "title": title,
                    "description": description,
                    "url": url,
                    "picurl": picurl
                }
            ]
        }
        })
        response = requests.request("POST", f"{self.baseUrl}/cgi-bin/message/send?access_token={self.access_token}", data=data).json()
        return response

    # 发送markdown消息
    """
    :param content: markdown格式的消息内容
    """
    def sendMarkdownMsg(self,content):
        data = json.dumps({
        "touser": "@all",
        "msgtype": "markdown",
        "agentid": self.agentid,
        "markdown": {
            "content": content
        }
        })
        response = requests.request("POST", f"{self.baseUrl}/cgi-bin/message/send?access_token={self.access_token}", data=data).json()
        return response