# -*- coding: utf-8 -*-

"""

Created on Wed Dec 12 11:20:36 2018

@author: takano.hiroyuki

"""

import os
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

import csv
from collections import defaultdict

from time import sleep
from lib import monoauth, monolog, message

class monoGet:
    home = os.getcwd()
    csv_path = home + u'\\target.csv'
    url = 'http://mnrate.com'
    no = 1
    program_name = "monoget"
    user_id = ""
    driver = ""
    
    def __init__(self):
        message.msgStart()
        ## 認証実施
        Autentication = monoauth.monoAuth()
        if Autentication[0] == False:
            raise Exception('Authentication faild.....')
        self.asin_list = self._csvLoad()
        self.user_id = Autentication[1]   
        self._getDriver()


    def _csvLoad(self):
        columns = defaultdict(list) # each value in each column is appended to a list
        
        with open(monoGet.csv_path) as f:
            reader = csv.DictReader(f) # read rows into a dictionary format
            for row in reader: # read a row as {column1: value1, column2: value2,...}
                for (k,v) in row.items(): # go over each column name and value 
                    columns[k].append(v) # append the value into the appropriate list
                                         # based on column name k
        target_list = columns['asincd'] 
        return(target_list)
        
    def _getDriver(self):
        driver_path = self.home + u'\\driver\\chromedriver.exe'
        # Driver オブジェクトの作成
        options = webdriver.ChromeOptions()
        options.add_extension(self.home + u'\\driver\\monozon.crx') ## Chrome Ext :: monozon
        self.driver = webdriver.Chrome(driver_path, chrome_options = options)
        # 商品のURLへアクセス
        self.driver.get(self.url)
        self._wait()


    def main(self):
        #scr.htmlparse(asin_cd)
        exec_date = datetime.datetime.now().strftime('%Y%m%d%H%M')
        out_csv = (os.getcwd() + u'\\' + exec_date + '-dataset' + '.csv')
        
        ## 出力用ファイルの作成
        f = open(out_csv, 'w', newline='')
        writer = csv.writer(f)    
        ## 行ヘッダー
        col_header = ( \
                'No', 'ASINコード', '商品名', '商品カテゴリー', \
                '新品過去1ヶ月目販売数', '新品過去2ヶ月目販売数', '新品過去3ヶ月目販売数', '新品平均月間販売数', \
                '中古過去1ヶ月目販売数', '中古過去2ヶ月目販売数', '中古過去3ヶ月目販売数', '中古平均月間販売数' \
                )
        # Create Header ------------------------------
        writer.writerow(col_header)
    
        ## Print Message
        str_df_length = str(len(self.asin_list))
        print(str_df_length + "件 のデータを取得します")
        
        ## monolog Insert
        monolog.monogetLogInsert(userid = self.user_id, prgname = self.program_name, count = str_df_length )
    
        ## monoget の実行\
        # Write Rows  ------------------------------
        for i in range(0, len(self.asin_list)):
            asin_cd = self.asin_list[i]            
            print(str(i+1) + "/" + str_df_length + " ISINコード : " + str(asin_cd) )
            try:
                wk_item_list = self._accessHTML(asin_cd)
                writer.writerow(wk_item_list)
            except:
                print("  ASINコードが間違っています")
        f.close()


    def _accessHTML(self, asin_cd):

        # 検索したいワードを入力フォームに入力する
        self.driver.find_element_by_name('kwd').send_keys(asin_cd)

        # 検索ボタンを実行する
        self.driver.find_element_by_id('_graph_search_btn').click() 

        try:
            # テーブル内容取得 
            tableElem = self.driver.find_element_by_class_name("table-bordered")
            trs = tableElem.find_elements(By.TAG_NAME, "tr")
                    
            ## 商品名を取得する
            org_link_list = self.driver.find_elements_by_class_name("original_link")
            item_name = org_link_list[4].text
            
            ## 商品カテゴリを取得する
            strong = self.driver.find_elements_by_class_name("_strong")
            item_categoly_name = strong[0].text
            
    
            ## ディメンション用 データフレームを作る ASIN:商品名:商品カテゴリ
            item_list = []
            item_list = [self.no, asin_cd, item_name, item_categoly_name]
    
            ## 対象行 : 2行目と3行目
            for i in range(2,4):
                tds = trs[i].find_elements(By.TAG_NAME, "td")    
                ## 行
                for j in range(1,5):
                    val = tds[j].text
                    item_list.append(val)
            return(item_list)
        except:
            print("次の処理を実施します")
        
        self.no+=1
        self._wait()    

    def _wait(self):
        sleep(2)
       
    def __del__(self):
        self.driver.close()
        message.msgEnd()

if __name__ == "__main__":
    mono = monoGet()
    mono.main()
    del mono
    #except:
    #    print("monoget の起動に失敗しました")

