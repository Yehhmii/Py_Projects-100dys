import plotly.graph_objects as go
import plotly.offline as pyo
from components.highscore import load_scores

def plot_stats():
    data = load_scores()
    if not data:
        # Create a blank figure with a “No scores” annotation
        fig = go.Figure()
        fig.add_annotation(
            text="No scores yet",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=24),
            xref="paper", yref="paper"
        )
        # Write to HTML and open it
        pyo.plot(fig, filename='stats.html', auto_open=True)
        return

    labels, vals = zip(*sorted(data.items(), key=lambda x: x[0]))

    fig = go.Figure(go.Bar(
        x=vals,
        y=labels,
        orientation='h',
        marker=dict(color='skyblue')
    ))
    fig.update_layout(
        title='High Scores by Mode & Difficulty',
        xaxis_title='WPM',
        height=50 * len(labels) + 100,
        margin=dict(l=120, r=20, t=50, b=20)
    )

    # This will generate a local HTML file (stats.html) and immediately open it:
    pyo.plot(fig, filename='stats.html', auto_open=True)

