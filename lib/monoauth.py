# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 21:29:57 2018

@author: fukui
"""

import urllib.request
import json
from lib import message

def _readLicense():
    """
    Lambda 関数起動して有効なライセンスかどうかチェックする
    """
    ## 失敗したらライセンス認証失敗
    try:
        ## monohiro.license ファイルの読み込み
        f = open("monohiro.license")
        s = json.load(f)
        user_id = s["userId"]
        return(user_id)
        
    except:
        message.msgAuthErr("missfile")
        raise Exception('Error!')

 
def monoAuth():
    user_id = _readLicense()
    url = "https://13gwgepmkk.execute-api.ap-northeast-1.amazonaws.com/prod/monoauth"
    
    params = {
        'user_id': user_id
        #'user_id': "AB12CD34"
    }
    
    ## Get Request
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)))
    with urllib.request.urlopen(req) as res:
        body = res.read()
        t = body.decode()
    result = str(json.loads(t)["statusCode"])
    
    if result == "200":
        print("認証成功")
        return True, user_id
    else:
        message.msgAuthErr("wrong_userid")
        return False, user_id

    
if __name__ == "__main__":
    try:
        res = monoAuth()
        print(res)
    except:
        print("miss")
    