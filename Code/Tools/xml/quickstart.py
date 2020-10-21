# coding: utf-8
# Author: wanhui0729@gmail.com

import os
import sys
if sys.version_info[0] == 2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET

xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'example.xml')

'''
相关方法在做查找节点等操作时，和层级没有关系，可以直接跳级查找
'''
if __name__ == '__main__':
    root = ET.parse(xml_path).getroot()
    # 获取节点tag
    print("=" * 10)
    print(root.tag)
    # 获取子节点
    print("=" * 10)
    for child in root:
        print(child.tag)
    # 查找感兴趣的节点
    print("=" * 10)
    for child in root.iter('object'):
        # 获取属性值
        print("Name: {}".format(child.find('name').text))