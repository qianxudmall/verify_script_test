#!usr/bin/python 2.7
# -*- coding: UTF-8 -*-
#练习gi
#git练习2，推送
import frappe
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename="logging.log"
    )

# dic_oprt = {'1':"自营",'3':"联营"}
# dic_mang = {'1':"单品", '2':"金额", '3':"售价金额"}
# dic_merch = {'1':"标准",'2':"AOC", '3':"耗材",'4':"生鲜原材料",'5':"生鲜",'6':"服务",'7':"包装"}
# # dic_tax = {'0.17':"销项税%17-dmall",'0.13':"销项税%13-dmall",'0.07':"销项税%7-dmall"}

dict_type = {
    '0': '单一商品',
    '1': '共性商品',
    '2': '变式商品',
    '3': '销售设备',
    '4': '预包装',
    '5': '展示商品',
    '6': '组件商品',
}


dict_item= {
    'item_code': 'MerchID',
    'item_name': 'MerchName',
    'brand': 'Trademark',
    'packing_name': 'PackingName',
    'spec_count': 'Specification',
    'spec_unit': 'SpecUnit',
    'production_location': 'ProducingArea',
    'barcode': 'Barcode',
    'shelf_life': 'ShelfLife',
    'length': 'Length',
    'width': 'Width',
    'height': 'High',
    'net_weight': 'Weight',
    'type': 'Type',
    'mini_sale_unit': 'IsMiniSale ',
    'remark': 'Remark',
    'packing_qty': 'SubUnit',
}


def test_record(record):
    item_code = record.find('MerchID').text
    logging.info('对比门店商品: %s' % item_code)
    # print '对比商品主数据: %s' % item_code
    # 若长度为9且有100的前缀, 则去掉100前缀
    if len(item_code) == 9 and item_code.startswith('100'):
        item_code = item_code[3:]
    try:
        item = frappe.get_doc('Item',item_code)
    except Exception as e:
        logging.info(e)
    else:
        for key,value in dict_item.items():
            if item.get(key) != record.find(value).text:
                logging.info('不一致field: %s' % key)
                # print '不一致field: %s' % key
        temp = item.get('type')
        temp1 = int(record.find('Type').text)
        if temp != temp1:
            logging.info('商品类型不一样:%s和%s' %(dict_type[temp],dict_type[temp1]))
            # print '商品类型不一样:%s和%s' %(dict_type[temp],dict_type[temp1])


def parseXML(filename ):
    '''
    解析xml,并比较字段
    '''
    tree = ET.parse(filename)
    dataroot = tree.getroot()
    data = dataroot[0][0].findall('REC_Merchandise')
    for rec in data:
        test_record(rec)

def main():
    '''
    遍历数据文件夹,查找相应xml,并解析
    '''
    data_dir = '/home/dmallerp/data/'
    file_count = 0
    for xml_file in os.listdir(data_dir):
        if xml_file.find('REC_Merchandise') != -1:
            file_count += 1
            filename = os.path.join(data_dir, xml_file)
            logging.info('处理第[%s]个文件: %s' % (file_count, filename))
            # print '处理第[%s]个文件: %s' % (file_count, filename)

            parseXML(filename)
    if file_count == 0:
        logging.info('当前日期没有OrgMerch文件!')
        # print '当前日期没有OrgMerch文件!'


if __name__ == "__main__":
    try:
        frappe.connect('dmall')
        logging.info('connected to local site')
        # print 'connected to local site'

        main()

    except Exception as e:
        logging.warning(e)
        # print e
    finally:
        frappe.destroy()
        logging.info('frappe destroyed')
        # print 'frappe destroyed'
