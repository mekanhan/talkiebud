import matplotlib
matplotlib.use("TkAgg")  # Use Tkinter-based backend

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout  # Import Graphviz layout

# Create a directed graph
G = nx.DiGraph()

# Define nodes (representing different files and processes)
nodes = {
    "User": "🎤 User Speaks",
    "SpeechRecognition": "📝 Convert Speech to Text\n(speech_recognition_helper.py)",
    "Chatbot": "🤖 Send Text to ChatGPT\n(chatbot.py)",
    "ChatbotResponse": "🗨️ AI Generates Response",
    "TextToSpeech": "🔊 Convert Text to Speech\n(text_to_speech.py)",
    "AudioPlayback": "▶️ Play AI Response",
    "GUI": "🖥️ Display Response & Loop\n(gui.py)",
}

# Define edges (representing flow of data)
edges = [
    ("User", "SpeechRecognition"),
    ("SpeechRecognition", "Chatbot"),
    ("Chatbot", "ChatbotResponse"),
    ("ChatbotResponse", "TextToSpeech"),
    ("TextToSpeech", "AudioPlayback"),
    ("AudioPlayback", "GUI"),
    ("GUI", "User"),  # Loop back for continuous interaction
]

# Add nodes and edges to the graph
for node, label in nodes.items():
    G.add_node(node, label=label)
G.add_edges_from(edges)

# Use Graphviz layout for vertical top-down alignment
try:
    pos = graphviz_layout(G, prog="dot")  # Ensures strict top-down hierarchy
except ImportError:
    pos = {
        "User": (0, 6),
        "SpeechRecognition": (0, 5),
        "Chatbot": (0, 4),
        "ChatbotResponse": (0, 3),
        "TextToSpeech": (0, 2),
        "AudioPlayback": (0, 1),
        "GUI": (0, 0),
    }  # Manual vertical positioning as fallback

# Increase figure size
plt.figure(figsize=(8, 12))  # Taller figure to fit vertical layout

# Draw graph with adjusted settings
nx.draw(G, pos, with_labels=False, node_color="lightblue", edge_color="gray", node_size=3500)

# Ensure labels are visible
labels = {node: nodes[node] for node in G.nodes}
nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")

# Display the flowchart
plt.title("AI Communication Robot - Vertical Flowchart", fontsize=14)
plt.show()
