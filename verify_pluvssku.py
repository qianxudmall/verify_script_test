#!usr/bin/python 2.7
# -*- coding: UTF-8 -*-
import frappe
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import logging

'此解析文件设计三个doctype'


dict_plu_detail= {
    'item_barcode': 'PLU',
    'store': 'OrgNO',
    'sku_id': 'MerchID',
    'uom': 'UOM',
    'retail_price': 'RetailPrice',
    'unit_qty': 'IncludeSKU',
}

def test_record(record):
    sku_id = record.find('MerchID').text
    if len(sku_id) == 9 and sku_id.startswith('100'):
        item_code = sku_id[3:]
    item_price = frappe.get_doc('Item Price',{'item_code':item_code })
    if item_price is not None:
        if item_price.get('price_list_rate') != float(record.find('RetailPrice').text):
            # logging.info('不一致价格: %s' % item_price.get('price_list_rate'))
            print '不一致价格: %s和%s' % (item_price.get('price_list_rate'),record.find('RetailPrice').text)
    plu_vs_sku_doc = frappe.get_doc('Item Barcode',{'item_barcode':record.find('PLU').text})
    if plu_vs_sku_doc is not None:
        if plu_vs_sku_doc.get('sku_id') != int(record.find('MerchID').text):
            # logging.info('不一致物料编码: %s' % plu_vs_sku_doc.get('sku_id'))
            print '不一致物料编码: %s' % plu_vs_sku_doc.get('sku_id')
        if plu_vs_sku_doc.get('store') != record.find('OrgNO').text:
            # logging.info('不一致store: %s' % plu_vs_sku_doc.get('store'))
            print '不一致store: %s' % plu_vs_sku_doc.get('store')
        if plu_vs_sku_doc.get('unit_qty') != int(record.find('IncludeSKU').text):
            # logging.info('不一致unit_qty: %s' % plu_vs_sku_doc.get('unit_qty'))
            print '不一致unit_qty: %s' % plu_vs_sku_doc.get('unit_qty')


def parseXML(filename ):
    '''
    解析xml,并比较字段
    '''
    tree = ET.parse(filename)
    dataroot = tree.getroot()
    data = dataroot[0][0].findall('REC_PLUvsSKU')
    for rec in data:
        test_record(rec)

def main():
    '''
    遍历数据文件夹,查找相应xml,并解析
    '''
    data_dir = '/home/dmallerp/data/'
    file_count = 0
    for xml_file in os.listdir(data_dir):
        if xml_file.find('REC_PLUvsSKU') != -1:
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