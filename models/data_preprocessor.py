import pandas as pd
import cv2
import os

def preprocess_data(csv_path, image_folder=None):
    # Load dataset
    try:
        df = pd.read_csv(csv_path)
        print("Columns in the dataset:", df.columns)  # Debugging statement
    except FileNotFoundError:
        print(f"Error: The file {csv_path} does not exist.")
        return

    # Check if the Hb column exists
    if 'Hb' not in df.columns:
        print("Error: 'Hb' column not found in the dataset.")
        return

    # Normalize Hb (Hemoglobin) levels
    df['Hb_Normalized'] = (df['Hb'] - df['Hb'].mean()) / df['Hb'].std()

    # Check if image folder exists
    if image_folder and os.path.isdir(image_folder):
        processed_images = []
        for idx, row in df.iterrows():
            img_path = os.path.join(image_folder, f"{row['Number']}.png")  # Example: Image filenames are '1.png', '2.png', etc.
            if os.path.exists(img_path):
                img = cv2.imread(img_path)
                if img is not None:
                    img_resized = cv2.resize(img, (128, 128))  # Resize to 128x128
                    processed_images.append(img_resized.flatten())
                else:
                    processed_images.append(None)  # Handle unreadable images
            else:
                processed_images.append(None)  # Handle missing images
        df['Processed_Images'] = processed_images
    else:
        print(f"Warning: Image folder '{image_folder}' does not exist or is not accessible.")
        df['Processed_Images'] = None

    # Save the preprocessed data
    preprocessed_path = os.path.join("data", "preprocessed_data.csv")
    os.makedirs(os.path.dirname(preprocessed_path), exist_ok=True)  # Ensure the directory exists
    df.to_csv(preprocessed_path, index=False)
    print(f"Preprocessing complete! Saved to '{preprocessed_path}'.")
    return df

if __name__ == "__main__":
    csv_path = "data/anemia_data.csv"  # Replace with your actual CSV file path
    image_folder = "data/images"  # Replace with your image folder path
    preprocess_data(csv_path, image_folder)
