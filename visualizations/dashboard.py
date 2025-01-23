# import dash
# from dash import dcc, html
# import pandas as pd
# import plotly.express as px

# app = dash.Dash(__name__)
# df = pd.read_csv('data/preprocessed_data.csv')
# figure = px.scatter(df, x='%Red Pixel', y='Hb', title="Hemoglobin vs Red Pixel Percentage")


# app.layout = html.Div([
#     html.H1("Anemia Dashboard"),
#     dcc.Graph(
#         figure=px.scatter(
#             df, x='%Red Pixel', y='Hb', color='Anaemic',
#             title='%Red Pixel vs Hemoglobin Levels'
#         )
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)







# import dash
# from dash import dcc, html
# from dash import html
# import base64
# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.express as px
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# import io
# from PIL import Image
# # Load your data
# df = pd.read_csv('../data/anemia_data.csv')




# # Train a model
# X = df[['Hb', '%Red Pixel']]  # Add more features as needed
# y = df['Anaemic']  # Target variable
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Initialize your Dash app
# app = dash.Dash(__name__)

# # Create the layout for your dashboard
# app.layout = html.Div([
#     html.H1("Anemia Insight Hub"),

#     # Dropdown for selecting Hb levels
#     dcc.Dropdown(
#         id='hb-dropdown',
#         options=[{'label': str(i), 'value': i} for i in df['Hb'].unique()],
#         value=df['Hb'].min(),  # Default value
#         style={'width': '50%'}
#     ),

#     # Graph that will update based on selected Hb level
#     dcc.Graph(id='scatter-plot'),

#     # File upload component
#     dcc.Upload(
#         id='upload-image',
#         children=html.Button('Upload Image'),
#         multiple=False
#     ),
#     html.Div(id='output-image-upload')
# ])

# # Callback to update the graph based on selected Hb level
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     [Input('hb-dropdown', 'value')]
# )
# def update_graph(selected_hb):
#     filtered_df = df[df['Hb'] == selected_hb]
#     figure = px.scatter(filtered_df, x='%Red Pixel', y='Hb', title=f'Hb vs %Red Pixel (Hb: {selected_hb})')
#     return figure

# # Callback to handle image upload
# @app.callback(
#     Output('output-image-upload', 'children'),
#     [Input('upload-image', 'contents')]
# )
# def upload_image(contents):
#     if contents is None:
#         return 'No image uploaded yet.'
#     else:
#         # Process the image (you can add model prediction here)
#         return 'Image uploaded successfully'

# if __name__ == '__main__':
#     app.run_server(debug=True)
# app.layout = html.Div([
#     # Image Upload
#     dcc.Upload(
#         id='upload-image',
#         children=html.Button('Upload Image'),
#         multiple=False
#     ),
    
#     # Display uploaded image
#     html.Div(id='image-display'),
    
#     # Graph to display the result (e.g., feature extraction result)
#     dcc.Graph(id='graph')
# ])
# @app.callback(
#     [Output('image-display', 'children'),
#      Output('graph', 'figure')],
#     [Input('upload-image', 'contents')]
# )
# def update_output(image_contents):
#     if image_contents is None:
#         return "No image uploaded", {}

#     # Decode the image
#     content_type, content_string = image_contents.split(',')
#     decoded_image = base64.b64decode(content_string)
#     image = Image.open(io.BytesIO(decoded_image))

#     # Process the image (Example: Convert to grayscale)
#     image = image.convert('L')
#     np_image = np.array(image)

#     # You can now extract features or analyze the image here. For this example,
#     # let's just display a histogram of the pixel intensities.

#     # Create a histogram from the pixel data
#     fig = px.histogram(np_image.flatten(), title="Pixel Intensity Histogram")

#     # Display the uploaded image
#     image_html = html.Img(src=image_contents, style={'width': '300px'})

#     return image_html, fig
# if __name__ == '__main__':
#     app.run_server(debug=True)


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

