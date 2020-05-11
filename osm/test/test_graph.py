import os
from py2neo import Graph, Node
import csv

import sys

# Path_Source = "../source/test.xml"
Path_Product_Node = "../product/test_node.csv"
Path_Product_Way = "../product/test_way.csv"
Path_Product_Relation = "../product/test_relation.csv"


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
            # id name lat lon prop
            osm = Node('OSMNode',
                       id=str(node[0]),
                       name=str(node[1]),
                       lat=str(node[2]),
                       lon=str(node[3]),
                       prop=str(node[4]),
                       )
            self.g.create(osm)

    def create_way(self, nodes):
        for node in nodes[1:]:
            # id name member prop
            osm = Node('OSMWay',
                       id=str(node[0]),
                       name=str(node[1]),
                       member=str(node[2]),
                       prop=str(node[3]),
                       )
            self.g.create(osm)

    def create_relation(self, nodes):
        for node in nodes[1:]:
            # id name type member prop
            osm = Node('OSMRelation',
                       id=str(node[0]),
                       name=str(node[1]),
                       type=str(node[2]),
                       member=str(node[3]),
                       prop=str(node[4]),
                       )
            self.g.create(osm)

    def create_graph(self):
        nodes = self.loadCsv(Path_Product_Node)
        ways = self.loadCsv(Path_Product_Way)
        relations = self.loadCsv(Path_Product_Relation)
        self.create_node(nodes)
        self.create_way(ways)
        self.create_relation(relations)


handler = OSMGraph()
handler.create_graph()
