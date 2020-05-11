import os
from py2neo import Graph, Node
import csv

import sys

# Path_Source = "../source/test.xml"
Path_Product_Node = "../product/node.csv"
Path_Product_Way = "../product/way.csv"
Path_Product_Relation = "../product/relation.csv"

csv.field_size_limit(sys.maxsize)


class OSMGraph():
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'Nodes/data.json')
        self.g = Graph(
            host='127.0.0.1',
            http_port=7474,
            user='neo4j',
            password='yuan@1004',
        )

    def loadCsv(self, path):
        with open(path, 'r') as csv_file:
            lines = csv.reader(csv_file)
            nodes = [line for line in lines]
        # print(nodes)
        return nodes

    def create_node(self, nodes):
        for node in nodes[1:]:
            '''
            节点属性：id name lat lon prop
            id: 34111073
            name: 星巴克咖啡
            lat: 30.2863469
            lon: 120.1478979
            prop: "{'amenity': 'cafe', 'name:en': 'Starbucks', 'name:zh': '星巴克咖啡', 'name:zh_pinyin': 'Xīngbākè Kāfēi'}"
            '''
            osm = Node('OSMNode',
                       id=str(node[0]),
                       name=str(node[1]),
                       lat=str(node[2]),
                       lon=str(node[3]),
                       prop=str(node[4]),
                       )
            print(node)
            self.g.create(osm)

    def create_way(self, nodes):
        for node in nodes[1:]:
            '''
            节点属性：id name member prop
            id: 656873019
            name: 延安路 Yan'an Road
            member: "['3439411272', '5460863339', '6453609475', '3439411271']"
            prop: "{'abutters': 'retail', 'cycleway': 'lane', 'highway': 'secondary', 'lanes': '2', 'lit': 'yes', 'name:en': ""Yan'an Road"", 'name:zh': '延安路', 'name:zh_pinyin': ""Yán'ān Lù"", 'oneway': 'yes', 'source': 'survey'}"
            '''
            osm = Node('OSMWay',
                       id=str(node[0]),
                       name=str(node[1]),
                       member=str(node[2]),
                       prop=str(node[3]),
                       )
            print(node)
            self.g.create(osm)

    def create_relation(self, nodes):
        for node in nodes[1:]:
            '''
            节点属性：id name type member prop
            id: 11076298
            type: route
            member: "[('node', '7492697369', 'stop'), ('node', '7492697365', 'stop'), ('node', '7492697361', 'stop'), ('node', '7492697363', 'stop'), ('node', '7255102051', 'stop'), ('way', '777463049', ''), ('way', '801051201', ''), ('way', '777463051', ''), ('way', '801051198', ''), ('way', '801051197', '')]"
            prop: "{'from': '九州街', 'name:en': 'Hangzhou Metro Line 16 (Jiuzhou Street->Lvting Road)', 'ref': '16', 'route': 'subway', 'to': '绿汀路'}"
            '''
            osm = Node('OSMRelation',
                       id=str(node[0]),
                       name=str(node[1]),
                       type=str(node[2]),
                       member=str(node[3]),
                       prop=str(node[4]),
                       )
            print(node)
            self.g.create(osm)

    def create_graph(self):
        nodes = self.loadCsv(Path_Product_Node)
        ways = self.loadCsv(Path_Product_Way)
        relations = self.loadCsv(Path_Product_Relation)
        self.create_node(nodes)
        print("create_node over")
        self.create_way(ways)
        print("create_way over")
        self.create_relation(relations)
        print("create_relation over")


handler = OSMGraph()
handler.create_graph()
