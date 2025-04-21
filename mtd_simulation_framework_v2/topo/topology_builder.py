# topo/topology_builder.py
import json
import networkx as nx

class TopologyBuilder:
    def __init__(self, topology_file="topo/topology_json/default.json"):
        self.graph = nx.Graph()
        self.load_topology(topology_file)

    def load_topology(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        for node in data['nodes']:
            self.graph.add_node(node['id'], type=node['type'])
        for edge in data['edges']:
            self.graph.add_edge(edge['source'], edge['target'])
        print(f"[TOPOLOGY] Loaded {len(self.graph.nodes)} nodes and {len(self.graph.edges)} edges.")

    def visualize(self):
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        node_colors = ['red' if self.graph.nodes[n]['type'] == 'honeypot' else 'blue' for n in self.graph.nodes]
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, node_size=1500)
        plt.title("Drone Fleet Topology")
        plt.show()

if __name__ == "__main__":
    topo = TopologyBuilder()
    topo.visualize()