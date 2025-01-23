import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os
from PIL import Image
import io
import base64
import plotly.graph_objs as go

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Anemia Insight Hub"

UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def parse_contents(contents):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        # Load image using PIL
        image = Image.open(io.BytesIO(decoded))

        # Resize large images
        max_size = (800, 800)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Convert resized image to base64
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        buffer.seek(0)
        encoded_image = base64.b64encode(buffer.read()).decode()
        return f"data:image/jpeg;base64,{encoded_image}"
    except Exception as e:
        return f"Error processing image: {e}"

# Layout
app.layout = dbc.Container(
    [
        html.H1("Anemia Insight Dashboard", className="text-center mt-4 mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Upload(
                            id="upload-image",
                            children=html.Div(
                                [
                                    "Drag and Drop or ",
                                    html.A("Select an Image File"),
                                ]
                            ),
                            style={
                                "width": "100%",
                                "height": "60px",
                                "lineHeight": "60px",
                                "borderWidth": "1px",
                                "borderStyle": "dashed",
                                "borderRadius": "5px",
                                "textAlign": "center",
                                "marginBottom": "10px",
                            },
                            multiple=False,
                        ),
                        html.Div(id="error-message", className="text-danger mt-2"),
                        html.Div(id="image-display"),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(id="graph"),
                        html.Div("Graph visualization placeholder", className="text-muted"),
                    ],
                    width=6,
                ),
            ]
        ),
    ],
    fluid=True,
)

# Callbacks
@app.callback(
    [Output("image-display", "children"), Output("error-message", "children")],
    [Input("upload-image", "contents")],
)
def update_output(content):
    if content:
        image_data = parse_contents(content)
        if "Error processing image" in image_data:
            return None, image_data  # Display error message
        return html.Img(src=image_data, style={"width": "100%", "height": "auto"}), ""
    return None, "No image uploaded."

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
