import plotly.graph_objects as go
import plotly.io as pio

try:
    print("Testing Kaleido image generation...")
    fig = go.Figure(data=go.Scatterpolar(r=[1, 2, 3], theta=['a', 'b', 'c']))
    # Try to generate image bytes
    img_bytes = fig.to_image(format="png")
    print("Success: Image generated.")
except Exception as e:
    print(f"Error: {e}")
