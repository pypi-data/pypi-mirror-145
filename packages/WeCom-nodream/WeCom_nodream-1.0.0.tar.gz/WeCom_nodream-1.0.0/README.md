# WeCom_API
# Initialize the object
```
// AGENTID: you can get it from the WeCom
// CORPID: you can get it from the WeCom
// CORPSECRET: you can get it from the WeCom
wx = wx = WeCom.WeCom(AGENTID,CORPID,CORPSECRET)
```
# Member methods
## uploadTemp
```
wx.uploadTemp(fileType,file,fileName='')
```
Upload temporary material

Parameters:

fileType:image, voice, video, file.

file:File buffer ( io.BufferedReader) or URL of the file

fileName: optional for file buffering, but the URL is required

## sendAppMsg
```
wx.sendAppMsg(msgType, content)
```
Send an application message

Parameters:

msgType:text, image, voice, video, file.

content: for text is text content, others are media id

## sendCardMsg
```
wx.sendCardMsg(title,description,url,btntxt)
```
Send a card message

Parameters:

title:title of the card

description:the content of the card

url:card jump address

btntxt:button text

## sendNewsMsg
```
wx.sendNewsMsg(title,description,url,picurl)
```
Send a graphic message

Parameters:

title: title of the graphic

description: text content of the graphic

url: click to jump link

picurl:picture link

##  sendMarkdownMsg
```
wx. sendMarkdownMsg(content)
```
Send markdown message

Parameters:

Content: markdown text