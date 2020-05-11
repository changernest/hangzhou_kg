import xml.etree.ElementTree as ET
import csv

'''
    tag:string      元素代表的数据种类。
    text:string     元素的内容。
    tail:string      元素的尾形。
    attrib:dictionary     元素的属性字典。
    
    ＃针对属性的操作
    clear()          清空元素的后代、属性、text和tail也设置为None。
    get(key, default=None)     获取key对应的属性值，如该属性不存在则返回default值。
    items()         根据属性字典返回一个列表，列表元素为(key, value）。
    keys()           返回包含所有元素属性键的列表。
    set(key, value)     设置新的属性键与值。
    
    ＃针对后代的操作
    find(match)                  寻找第一个匹配子元素，匹配对象可以为tag或path。
    findall(match)               寻找所有匹配子元素，匹配对象可以为tag或path。
    findtext(match)             寻找第一个匹配子元素，返回其text值。匹配对象可以为tag或path。
    insert(index, element)   在指定位置插入子元素。
    iter(tag=None)              生成遍历当前元素所有后代或者给定tag的后代的迭代器。＃python2.7新特性
    iterfind(match)              根据tag或path查找所有的后代。
    itertext()                       遍历所有后代并返回text值。
    append(subelement)     添加直系子元素。
    extend(subelements)    增加一串元素对象作为子元素。＃python2.7新特性
    remove(subelement)      删除子元素。
'''
Path_Source = "../source/test.xml"
Path_Product_Node = "../product/test_node.csv"
Path_Product_Way = "../product/test_way.csv"
Path_Product_Relation = "../product/test_relation.csv"

# 获取 XML 文档对象 ElementTree
tree = ET.parse(Path_Source)
# 获取 XML 文档对象的根结点 Element
root = tree.getroot()
# 打印根结点的名称
print(root.tag)
print(root.attrib)

# find查询有问题，返回直接为子节点列表；findall返回正常
nodes = []
# id name lat lon  prop
for node in root.findall('node'):
    # print(node.tag, node.attrib)
    prop = {}
    name = ""
    for tag in node.findall('tag'):
        # print(tag.tag, tag.attrib)
        if tag.get("k") == "name":
            name = tag.get("v")
        else:
            prop[tag.get("k")] = tag.get("v")
    # print(prop)
    nodes.append((node.get("id"), name, node.get("lat"), node.get("lon"), prop))
# print(nodes)

# id name lat lon  prop
with open(Path_Product_Node, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "lat", "lon", "prop"])
    for r in nodes:
        writer.writerow(r)

ways = []
# id name member prop
for way in root.findall('way'):
    # print(way.tag, node.attrib)
    member = []
    prop = {}
    name = ""
    for nd in way.findall('nd'):
        member.append(nd.get("ref"))
    # print(member)

    for tag in way.findall('tag'):
        # print(tag.tag, tag.attrib)
        if tag.get("k") == "name":
            name = tag.get("v")
        else:
            prop[tag.get("k")] = tag.get("v")
    # print(prop)
    ways.append((way.get("id"), name, member, prop))

# id name member prop
with open(Path_Product_Way, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "member", "prop"])
    for r in ways:
        writer.writerow(r)

relations = []
# id name type member prop
for rel in root.findall('relation'):
    # print(way.tag, node.attrib)
    member = []
    prop = {}
    name = ""
    type = ""
    for m in rel.findall('member'):
        # <member type="node" ref="7039952242" role=""/>
        member.append((m.get("type"), m.get("ref"), m.get("role")))
    # print(member)

    for tag in rel.findall('tag'):
        # print(tag.tag, tag.attrib)
        if tag.get("k") == "name":
            name = tag.get("v")
        elif tag.get("k") == "type":
            type = tag.get("v")
        else:
            prop[tag.get("k")] = tag.get("v")
    # print(prop)
    relations.append((rel.get("id"), name, type, member, prop))

# id name type member prop
with open(Path_Product_Relation, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "type", "member", "prop"])
    for r in relations:
        writer.writerow(r)
