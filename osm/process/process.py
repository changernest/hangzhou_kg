import xml.etree.ElementTree as ET
import csv

Path_Source = "../source/osm_hangzhou.xml"
Path_Product_Node = "../product/node.csv"
Path_Product_Way = "../product/way.csv"
Path_Product_Relation = "../product/relation.csv"

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
