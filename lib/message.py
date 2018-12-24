# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 21:03:14 2018

@author: fukui
"""

def msgStart():
    msgStart =  \
        "===============================================\n" + \
        " monoget : Hello!! \n" +  \
        "===============================================\n" +  \
        "このウィンドウは閉じないでください Google Chrome が起動します\n"
    print(msgStart)


def msgAuthErr(flg):
    msgAuthErr =  \
        "==　==　==　==　==　==　==　==　==　==　==　==　==　==　==\n" + \
        "    認証が失敗しました\n"

    if flg == "missfile":
        msgAuthErr = msgAuthErr + \
            "    monohiro.license　ファイルを確認してください\n" +  \
            "==　==　==　==　==　==　==　==　==　==　==　==　==　==　==\n"
    elif flg == "wrong_userid":
        msgAuthErr = msgAuthErr + \
            "    ライセンスキーが間違っています\n" +  \
            "==　==　==　==　==　==　==　==　==　==　==　==　==　==　==\n"
    print(msgAuthErr)


def msgEnd():
    msgEnd =  \
        "===============================================\n" + \
        " monoget: Bye!\n" + \
        "===============================================\n"
    print(msgEnd)


if __name__ == "__main__":
    print(msgStart())
    print(msgEnd())

   