import torch
from PIL import Image
import torchvision.transforms as transforms

# Define your model architecture (replace with your actual model)
class DeepfakeModel(torch.nn.Module):
    def __init__(self):
        super(DeepfakeModel, self).__init__()
        # Define your layers here
        self.conv1 = torch.nn.Conv2d(3, 16, kernel_size=3)
        self.relu = torch.nn.ReLU()
        self.pool = torch.nn.MaxPool2d(2, 2)
        self.fc = torch.nn.Linear(16 * 14 * 14, 1) # Example linear layer

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = x.view(-1, 16 * 14 * 14) # Flatten
        x = torch.sigmoid(self.fc(x))
        return x

# Load your trained model (replace with your actual path)
model_path = 'model/deepfake_model.pth'
model = DeepfakeModel()
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))) # Load to CPU if no GPU
model.eval()

# Define image transformations (adjust based on your model's requirements)
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_image(image_path):
    """Predicts if the given image is a deepfake."""
    try:
        image = Image.open(image_path).convert('RGB')
        image = transform(image).unsqueeze(0) # Add batch dimension

        with torch.no_grad():
            output = model(image)
            prediction = output.item() > 0.5
            confidence = output.item()

        return "Fake" if prediction else "Real", confidence
    except Exception as e:
        return "Error processing image", 0.0

# Add a similar function for video processing if your model handles videos directly
# You might need to extract frames from the video and process them.