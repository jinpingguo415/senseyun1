#coding=utf-8
#模块名称：run
#测试模块：清除上次运行结果result.txt，运行所有测试集合
#开发者：zhangyn
import unittest
import os
import csv
from scripts import common
from scripts import result
from scripts import clean

#函数名称：creatsuite
#参数：测试用例对应的py文件路径
#函数说明：#获取单个测试集中所有测试用例
def creatsuite(test_dir):    
    testunit=unittest.TestSuite() 
    discover= unittest.TestLoader().discover(test_dir,
                                             pattern ='test*.py',
                                             top_level_dir= None)    
    
    for test_suite in discover:        
        for test_case in test_suite: 
                      
            testunit.addTests(test_case)
    return testunit        

if __name__ == '__main__':
    currentPath = os.getcwd()
    result.cleanResult()
    clean.delAll()
    testsuites_file = currentPath+"\\testsuites\\testsuites.csv"
    common.resultCSV('用例名称','测试集名称','结果','原因','测试内容')
    #获取需要运行的测试集，测试集记录在testsuites.csv文件中
    if os.path.exists(testsuites_file):
        with open(testsuites_file,newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')            
            for row in spamreader:                                
                test_dir=currentPath+'\\testsuites\\'+row[0]       
                print(test_dir)                      
                runner =unittest.TextTestRunner()
                alltestnames = creatsuite(test_dir)
                #运行所有测试用例
                runner.run(alltestnames)
                