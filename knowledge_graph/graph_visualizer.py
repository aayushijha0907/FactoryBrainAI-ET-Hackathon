"""
graph_visualizer.py
Creates beautiful interactive knowledge graph visualizations using PyVis.
"""

import os
import networkx as nx
from pyvis.network import Network
from typing import Optional, Dict, Any
from datetime import datetime


class GraphVisualizer:
    """
    Interactive Knowledge Graph Visualizer for FactoryBrain AI.
    """
    
    def __init__(self, height: str = "750px", width: str = "100%", bgcolor: str = "#f8fafc"):
        self.height = height
        self.width = width
        self.bgcolor = bgcolor
        self.network = None

    def _get_node_color(self, node_type: str) -> str:
        """Return color based on node type."""
        color_map = {
            "Document": "#4F46E5",      # Indigo
            "Equipment": "#10B981",     # Emerald
            "Component": "#14B8A6",
            "Procedure": "#F59E0B",     # Amber
            "Person": "#EF4444",        # Red
            "Insight": "#8B5CF6",
            "Location": "#06B6D4",      # Cyan
            "Unknown": "#6B7280"
        }
        return color_map.get(node_type, "#6B7280")

    def load_graph(self, graph: nx.Graph, title: str = "FactoryBrain Knowledge Graph"):
        """Load a NetworkX graph into PyVis."""
        self.network = Network(
            height=self.height,
            width=self.width,
            bgcolor=self.bgcolor,
            font_color="#1F2937",
            directed=False,
            notebook=False
        )

        # Add nodes
        for node, attrs in graph.nodes(data=True):
            node_type = attrs.get("node_type", "Unknown")
            label = node if len(node) < 25 else node[:22] + "..."
            
            self.network.add_node(
                node,
                label=label,
                title=f"<b>{node}</b><br>Type: {node_type}",
                color=self._get_node_color(node_type),
                size=25,
                font={"size": 14, "face": "Arial"}
            )

        # Add edges
        for source, target, attrs in graph.edges(data=True):
            relation = attrs.get("relation", "related")
            self.network.add_edge(
                source,
                target,
                title=relation,
                label=relation if len(relation) < 15 else relation[:12] + "...",
                color="#94A3B8",
                width=2.2
            )

        # Configure physics & layout
        self.network.barnes_hut(
            gravity=-3000,
            central_gravity=0.3,
            spring_length=200,
            spring_strength=0.05,
            damping=0.85
        )
        
        self.network.set_options("""
        {
            "nodes": {
                "borderWidth": 2,
                "shadow": true
            },
            "edges": {
                "smooth": true,
                "shadow": true
            },
            "physics": {
                "enabled": true,
                "solver": "barnesHut"
            }
        }
        """)

        return self.network

    def save(self, filename: str = "knowledge_graph.html") -> str:
        """Save the graph as an interactive HTML file."""
        output_dir = "assets"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        if self.network:
            self.network.save_graph(filepath)
            return filepath
        else:
            raise ValueError("No graph loaded. Call load_graph() first.")

    def generate(self, graph: nx.Graph, filename: str = "knowledge_graph.html") -> str:
        """Full pipeline: load → configure → save."""
        self.load_graph(graph)
        return self.save(filename)

    def show_info(self):
        """Print basic info about the visualizer."""
        if self.network:
            print("✅ Interactive Knowledge Graph ready!")
            print(f"   Nodes: {len(self.network.nodes)}")
            print(f"   Edges: {len(self.network.edges)}")


# =====================================================
# Demo
# =====================================================
if __name__ == "__main__":
    # Create sample graph
    G = nx.Graph()
    
    G.add_node("Pump A", node_type="Equipment")
    G.add_node("Valve X", node_type="Equipment")
    G.add_node("Maintenance Manual v2", node_type="Document")
    G.add_node("Safety SOP", node_type="Procedure")
    G.add_node("Technician Raj", node_type="Person")
    G.add_node("Leakage Analysis", node_type="Insight")

    G.add_edge("Pump A", "Maintenance Manual v2", relation="mentions")
    G.add_edge("Pump A", "Valve X", relation="connected_to")
    G.add_edge("Pump A", "Safety SOP", relation="follows")
    G.add_edge("Technician Raj", "Maintenance Manual v2", relation="authored")
    G.add_edge("Pump A", "Leakage Analysis", relation="has_issue")

    # Visualize
    visualizer = GraphVisualizer(height="800px")
    html_path = visualizer.generate(G, filename="factory_knowledge_graph.html")
    
    print(f"🎉 Knowledge Graph successfully generated!")
    print(f"📍 Saved at: {html_path}")
    visualizer.show_info()
