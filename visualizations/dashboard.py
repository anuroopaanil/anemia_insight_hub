
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import base64
import io
from PIL import Image
import numpy as np
import plotly.express as px

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container(
    [
        # Page title
        dbc.Row(
            dbc.Col(html.H1("Anemia Insight Dashboard", className="text-center my-4"), width=12)
        ),
        
        # Image Upload Section
        dbc.Row(
            dbc.Col(
                dcc.Upload(
                    id='upload-image',
                    children=html.Button('Upload Image', className="btn btn-primary btn-lg"),
                    multiple=False
                ),
                width={"size": 6, "offset": 3},
                className="text-center my-2"
            ),
        ),
        
        # Display uploaded image
        dbc.Row(
            dbc.Col(
                html.Div(id='image-display', className="text-center my-4"),
                width=12
            ),
        ),
        
        # Graph Section
        dbc.Row(
            dbc.Col(
                dcc.Graph(id='graph', style={'height': '400px', 'margin-bottom': '30px'}),
                width=12
            ),
        ),
    ],
    fluid=True
)

# Callback to handle image upload and update graph
@app.callback(
    [Output('image-display', 'children'),
     Output('graph', 'figure')],
    [Input('upload-image', 'contents')]
)
def update_output(image_contents):
    if image_contents is None:
        return "No image uploaded", {}

    try:
        # Decode the uploaded image
        content_type, content_string = image_contents.split(',')
        decoded_image = base64.b64decode(content_string)
        image = Image.open(io.BytesIO(decoded_image))

        # Resize the image to a manageable size (e.g., 300px width)
        base_width = 300
        w_percent = (base_width / float(image.size[0]))
        h_size = int((float(image.size[1]) * float(w_percent)))
        image = image.resize((base_width, h_size), Image.Resampling.LANCZOS)  # Use LANCZOS filter

        # Convert the image into a format that can be displayed in HTML (base64 encoding)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Process the image (example: convert to grayscale)
        image = image.convert('L')
        np_image = np.array(image)

        # Create a histogram of pixel intensities
        fig = px.histogram(
            x=np_image.flatten(),
            nbins=50,
            title="Pixel Intensity Distribution",
            labels={'x': 'Pixel Intensity', 'y': 'Frequency'},
            template="plotly_white"
        )
        fig.update_layout(
            xaxis=dict(title='Pixel Intensity'),
            yaxis=dict(title='Frequency'),
            title_x=0.5,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)'
        )

        # Display the uploaded image
        image_html = html.Img(
            src=f"data:image/png;base64,{img_str}",
            style={
                'width': '100%',
                'max-width': '300px',
                'height': 'auto',
                'margin': 'auto',
                'display': 'block',
                'border': '1px solid #ddd',
                'border-radius': '5px',
                'padding': '5px',
            }
        )

        return image_html, fig

    except Exception as e:
        return f"Error processing image: {str(e)}", {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

