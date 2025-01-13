import networkx as nx
from LogseqMdPy.utils import name_to_filename

def create_networkx_directed_graph_from_pages(pages):
    G = nx.DiGraph()

    for page in pages:
        node_name = page.get_page_name()
        G.add_node(node_name)
        refs = page.get_all_references_in_blocks()
        for ref in refs:
            other_node_name = ref[1]
            if node_name != other_node_name:
                G.add_edge(node_name, other_node_name)
        prop_refs = page.get_all_prop_refs()
        for ref in prop_refs:
            if ref[1] != node_name:
                G.add_edge(node_name, ref[1], label = ref[0])
    return G

def create_gephi_file_from_pages(pages):
    graph = create_networkx_directed_graph_from_pages(pages)
    nx.write_gexf(graph, "graph.gexf")
    print("Graph exported successfully as graph.gexf")

def create_mermaid_flow_chart_TODO(pages):
    mermaid_flowchart = "flowchart\n"
    graph = create_networkx_directed_graph_from_pages(pages)
    node_ids = {}
    id = 0
    for node in graph:
        node_ids[node] = id
        id += 1
        mermaid_flowchart += "\t" + f'N{id}[{node}]' +"\n"
    for edge in graph.edges:
        (n1, n2) = edge
        mermaid_flowchart += "\t" +  f'N{node_ids[n1]}' +" --> " + f'N{node_ids[n2]}' + "\n"
    return mermaid_flowchart