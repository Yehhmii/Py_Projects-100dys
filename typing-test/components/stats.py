# ====== components/stats.py ======

import tempfile
import webbrowser
from tkinter import messagebox

from plotly.graph_objs import Bar, Figure, Layout
from plotly.offline import plot

from components.highscore import load_scores

def plot_stats():
    data = load_scores()
    if not data:
        messagebox.showinfo("No Data", "No scores yet!")
        return

    # Sort and unpack
    labels, vals = zip(*sorted(data.items(), key=lambda x: x[0]))

    # Build the figure
    fig = Figure(
        data=[Bar(x=vals, y=labels, orientation='h', marker=dict(color='skyblue'))],
        layout=Layout(
            title='High Scores by Mode & Difficulty',
            xaxis=dict(title='WPM'),
            margin=dict(l=120, r=20, t=50, b=20),
            height=50 * len(labels) + 100
        )
    )

    try:
        # Write to a real HTML file (with CDN plots) and open it
        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False) as tmp:
            fig.write_html(tmp.name, include_plotlyjs='cdn')
            webbrowser.open(tmp.name)
    except Exception as e:
        messagebox.showerror("Plot Error", f"Could not display stats:\n{e}")
