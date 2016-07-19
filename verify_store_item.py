#usr/bin/python
# -*- coding: UTF-8 -*-
import frappe
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import conf
import logging

SYNC_DATE = conf.DATE_TO_SYNC if not conf.DEFAULT_SYN_DATE else datetime.now().strftime('%Y%m%d')


dic_oprt = {'1':"自营",'3':"联营"}
dic_mang = {'1':"单品", '2':"金额", '3':"售价金额"}
dic_merch = {'1':"标准",'2':"AOC", '3':"耗材",'4':"生鲜原材料",'5':"生鲜",'6':"服务",'7':"包装"}
# dic_tax = {'0.17':"销项税%17-dmall",'0.13':"销项税%13-dmall",'0.07':"销项税%7-dmall"}


dict_store_item={
    'store_id':'OrgNO',
    'item_code':'MerchID',
    # 'category':'ClsCode',
    'short_name':'SimpleName',
    # 'operation_mode':'OperationMode',
    # 'management_style':'ManagementStyle',
    # 'high_stock_days':'HighStockDays' ,
    # 'safe_stock_days':'SafeStockDays',
    'first_purchase_date':'FirstPurchaseDate',
    'last_purchase_date':'LastPurchaseDate',
    # 'price_top_limit':'PriceUpLimit',
    # 'price_bottom_limit':'PriceLowLimit',
    'chg_steelyard_price':'ChgSteelyardPrice',
    'is_steelyard_count':'IsSteelyardCount',
    'is_steelyard_sale':'IsSteelyardSale',
    'default_supplier':'DefaultSupOrgNO  ',
    'default_dc_org_no':'DefaultDCOrgNO',
    # 'merch_style':'MerchStyle',
    'can_order':'CanOrder',
    'can_change_retail_price':'CanChangeRetailPrice',
    'can_sale':'CanSale',
    'can_return':'CanReturn',
    'item_status':'Status'
}


def test_record(record):
    item_code = record.find('MerchID').text
    logging.info('对比门店商品: %s' % item_code)
    item = frappe.get_doc('Store Item',item_code)
    for key,value in dict_store_item.items():
        if item.get(key) != record.find(value).text:
            logging.info('不一致field: %s' % key)

    main_item = frappe.get_doc('Item',{'item_code':item_code})
    if main_item.get('item_group') != record.find('ClsCode').text:
        logging.info('不一致的filed: item_group')
    if item.get('operation_mode') != dic_oprt[record.find('OperationMode').text]:
        logging.info('不一致field: operation_mode')

    if item.get('management_style') != dic_oprt[record.find('ManagementStyle').text]:
        logging.info('不一致field: management_style')

    if item.get('merch_style') != dic_oprt[record.find('MerchStyle').text]:
        logging.info('不一致field: merch_style')

    if int(item.get('high_stock_days')) != int(record.find('HighStockDays')):
        logging.info('不一致field: height_stock_days')

    if int(item.get('safe_stock_days')) != int(record.find('SafeStockDays')):
        logging.info('不一致field: safe_stock_days')

    if float(item.get('price_top_limit')) != float(record.find('PriceUpLimit')):
        logging.info('不一致field: PriceUpLimit')

    if float(item.get('price_bottom_limit')) != float(record.find('PriceLowLimit')):
        logging.info('不一致field: PriceLowLimit')

def parseXML(filename ):
    '''
    解析xml,并比较字段
    '''
    tree = ET.parse(filename)
    dataroot = tree.getroot()
    data = dataroot[0][0].findall('REC_OrgMerch')
    for rec in data:
        test_record(rec)

def main():
    '''
    遍历数据文件夹,查找相应xml,并解析
    '''
    data_dir = '/home/ubuntu/data/%s' % SYNC_DATE
    file_count = 0
    for xml_file in os.listdir(data_dir):
        if xml_file.find('REC_OrgMerch') != -1:
            file_count += 1
            filename = os.path.join(data_dir, xml_file)
            logging.info('处理第[%s]个文件: %s' % (file_count, filename))
            parseXML(filename)
    if file_count == 0:
        logging.info('当前日期没有OrgMerch文件!')

if __name__ == "__main__":
    try:
        frappe.connect(conf.SITE_NAME)
        logging.info('connected to local site')

        main()

    except Exception as e:
        logging.warning(e)
    finally:
        frappe.destroy()
        logging.info('frappe destroyed')