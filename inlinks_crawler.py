import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import networkx as nx
import plotly.graph_objects as go
from dash import Dash, dcc, html
import webbrowser
from threading import Timer
import logging
import os

### Configura il logging
log_file = os.path.join(os.path.dirname(__file__), "crawler_log.txt")
logging.basicConfig(
    filename=log_file,
    filemode='w',  # Sovrascrive il file ogni volta che esegui lo script
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

### Funzione per verificare se un link è valido
def is_valid_link(link, base_url):
    invalid_extensions = (".jpg", ".jpeg", ".png", ".gif", ".css", ".js", ".pdf", ".webp",
                          ".svg", ".ico", ".xml", ".xlsx", ".json", "tel:", ".zip", "#")
    parsed = urlparse(link)
    return (link and not link.endswith(invalid_extensions)
            and urlparse(link).netloc in ["", urlparse(base_url).netloc]
            and "/out/" not in parsed.path
            and "mailto:" not in link
            and "/feed/" not in parsed.path
            and "site:" not in parsed.path)

# Funzione per estrarre i link interni
def extract_links(url, base_url):
    try:
        response = requests.get(url, timeout=10, verify=True, allow_redirects=True)
        
        # Controlla se il dominio della destinazione del redirect è diverso da quello base
        if urlparse(response.url).netloc != urlparse(base_url).netloc:
            logging.info(f"URL rediretto a un dominio esterno: {response.url}")
            return [], False

        if response.status_code != 200:
            return [], False
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = urljoin(base_url, a_tag["href"])
            if is_valid_link(href, base_url):
                logging.info(f"Trovato link: {href}")  # Logga i link trovati
                links.add(href.split("#")[0])  # Rimuove ancore interne
        return links, True
    except requests.RequestException as e:
        logging.error(f"Errore durante la richiesta di {url}: {e}")
        return [], False

# Funzione principale del crawler
def crawl_website(start_url):
    visited = set()
    graph = nx.DiGraph()

    to_visit = [start_url]

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue

        logging.info(f"Scansionando: {current_url}")
        links, success = extract_links(current_url, start_url)

        if success:
            visited.add(current_url)
            graph.add_node(current_url)

            for link in links:
                graph.add_edge(current_url, link)
                if link not in visited:
                    to_visit.append(link)

    return graph

### Funzione per convertire il grafo in un formato Plotly
def create_plotly_graph(graph):
    pos = nx.kamada_kawai_layout(graph)  # Utilizzo del layout Kamada-Kawai per ridurre le sovrapposizioni

    # Calcolo del PageRank
    pagerank = nx.pagerank(graph)
    pagerank_values = list(pagerank.values())

    # Normalizzazione della grandezza dei nodi
    min_size = 10
    max_size = 50
    sizes = [
        min_size + (max_size - min_size) * ((pr - min(pagerank_values)) / (max(pagerank_values) - min(pagerank_values)))
        for pr in pagerank_values
    ]

    # Creazione degli edge
    edges_x = []
    edges_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edges_x.extend([x0, x1, None])
        edges_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edges_x,
        y=edges_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    # Creazione dei nodi
    nodes_x = []
    nodes_y = []
    text = []
    for node in graph.nodes():
        x, y = pos[node]
        nodes_x.append(x)
        nodes_y.append(y)
        text.append(f"{node}<br>PageRank: {pagerank[node]:.4f}")

    node_trace = go.Scatter(
        x=nodes_x,
        y=nodes_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=sizes,
            color=pagerank_values,
            colorscale='YlGnBu',
            showscale=True,
            colorbar=dict(
                title="PageRank",
                thickness=15,
                xanchor='left',
                titleside='right'
            ),
        ),
        text=text
    )

    return [edge_trace, node_trace]

# Funzione per avviare l'app Dash
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def run_dash_app(graph):
    app = Dash(__name__)

    traces = create_plotly_graph(graph)

    fig = go.Figure(data=traces,
                    layout=go.Layout(
                        title='Grafo dei link interni',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    app.layout = html.Div([
        html.H1("Visualizzazione del Grafo del Sito"),
        dcc.Graph(figure=fig)
    ])

    Timer(1, open_browser).start()
    app.run_server(debug=False)

if __name__ == "__main__":
    # URL iniziale da scansionare
    start_url = input("Inserisci l'URL iniziale: ").strip()

    # Verifica che l'URL sia valido
    if not start_url.startswith("http"):
        logging.error("L'URL deve iniziare con http o https.")
    else:
        # Effettua la scansione
        graph = crawl_website(start_url)

        logging.info(f"Numero totale di nodi scansionati: {len(graph.nodes)}")

        # Avvia l'app Dash per visualizzare il grafo
        run_dash_app(graph)
