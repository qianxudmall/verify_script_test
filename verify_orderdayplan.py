#!usr/bin/python 2.7
# -*- coding: UTF-8 -*-
import frappe
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging


# dic_oprt = {'1':"自营",'3':"联营"}
# dic_mang = {'1':"单品", '2':"金额", '3':"售价金额"}
# dic_merch = {'1':"标准",'2':"AOC", '3':"耗材",'4':"生鲜原材料",'5':"生鲜",'6':"服务",'7':"包装"}
# # dic_tax = {'0.17':"销项税%17-dmall",'0.13':"销项税%13-dmall",'0.07':"销项税%7-dmall"}
# erp 和 sap 商品类型的 mapping 关系

dict_order_cycle = {
    'OrgNO': 'org_no',
    'SupplierOrgNO': 'supplier_org_no',
    'Monday': 'monday',
    'Tuesday': 'tuesday',
    'Wednesday': 'wednesday',
    'Thursday': 'thursday',
    'Friday': 'friday',
    'Saturday': 'saturday',
    'Sunday': 'sunday'
}


def test_record(record):
    item_code = record.find('OrgNO').text
    # logging.info('门店编号: %s' % item_code)
    print '门店编号: %s' % item_code
    item = frappe.get_doc('Order Cycle',{'item_code':item_code})
    for key,value in dict_order_cycle.items():
        if item.get(key) != record.find(value).text:
            # logging.info('不一致field: %s' % key)
            print '不一致记录: %s和%s' % (item.get(key),record.find(value).text)

def parseXML(filename ):
    '''
    解析xml,并比较字段
    '''
    tree = ET.parse(filename)
    dataroot = tree.getroot()
    data = dataroot[0][0].findall('access')
    for rec in data:
        test_record(rec)

def main():
    '''
    遍历数据文件夹,查找相应xml,并解析
    '''
    data_dir = '/home/dmallerp/data/'
    file_count = 0
    for xml_file in os.listdir(data_dir):
        if xml_file.find('REC_OrderDayPlan') != -1:
            file_count += 1
            filename = os.path.join(data_dir, xml_file)
            #logging.info('处理第[%s]个文件: %s' % (file_count, filename))
            print '处理第[%s]个文件: %s' % (file_count, filename)

            parseXML(filename)
    if file_count == 0:
        # logging.info('当前目录没有OrderDayPlan文件!')
        print '当前目录没有OrderDayPlan文件!'


if __name__ == "__main__":
    try:
        frappe.connect('dmall')
        # logging.info('connected to local site')
        print 'connected to local site'

        main()

    except Exception as e:
        # logging.warning(e)
        print e
    finally:
        frappe.destroy()
        #logging.info('frappe destroyed')
        print 'frappe destroyed'