# inlink_graph
This repository contains a Python script to crawl a website and visualize its internal link structure as an interactive graph using Plotly and Dash. The script also logs the crawling process and validates links to avoid irrelevant or external resources.

## Features

- Crawls internal links starting from a given URL.
- Validates and filters out irrelevant links (e.g., images, external links, and certain file types).
- Visualizes the website's internal link structure as an interactive graph.
- Uses NetworkX to build the graph and calculate PageRank.
- Displays an interactive visualization using Dash and Plotly.
- Logs the crawling process for debugging and auditing purposes.

## Requirements

- Python 3.7+
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `networkx`
  - `plotly`
  - `dash`

You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/website-crawler.git
   cd website-crawler
   ```

2. Run the script:

   ```bash
   python crawler.py
   ```

3. Enter the starting URL when prompted:

   ```
   Inserisci l'URL iniziale: https://example.com
   ```

4. The script will:
   - Crawl the website starting from the provided URL.
   - Log the crawling process to `crawler_log.txt`.
   - Launch a Dash web app displaying the interactive link graph.

5. The Dash web app will automatically open in your default web browser. If it doesn't, visit [http://127.0.0.1:8050/](http://127.0.0.1:8050/).

## Logging

The script logs all crawling activities, including:

- Links found during crawling.
- Errors and warnings (e.g., inaccessible URLs).
- Redirects to external domains.

Logs are stored in `crawler_log.txt` in the script's directory.

## Graph Visualization

The internal link structure is visualized as a graph where:

- **Nodes** represent pages on the website.
- **Edges** represent links between pages.
- **Node size** is proportional to its PageRank value.
- **Color scale** represents the relative PageRank value.

The visualization is interactive, allowing you to hover over nodes for detailed information.

## File Structure

```
.
├── crawler.py        # Main script for crawling and visualization
├── requirements.txt  # Python dependencies
├── README.md         # Documentation
└── crawler_log.txt   # Log file generated during execution
```

## Configuration

You can modify the script to:

- Change the list of invalid link extensions in the `is_valid_link` function.
- Adjust the layout and styling of the graph in the `create_plotly_graph` function.
- Customize the logging format and output file.

## Contributing

Feel free to fork this repository and submit pull requests. Suggestions and improvements are always welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

