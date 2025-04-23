# 🐶 Only Doggy

A Python-based AI tool to detect a dog breed from an image and provide detailed facts and characteristics about the breed. It leverages **LLaMA Vision Models** via the **Groq API** and integrates with the **API Ninjas Dog API** to return real-time, breed-specific information.

## 📌 Features

- 🖼️ Identifies dog breed from an uploaded image using a vision language model.
- 📊 Fetches detailed facts like energy level, shedding, protectiveness, barking tendency, and more.
- 📋 Automatically generates a readable assessment of the breed using LLaMA-3.
- 🔧 Built-in support for future tool/function integration using structured tool-calls.

## 🚀 Tech Stack

- Python 3.12+
- [Groq API](https://groq.com/)
- [API Ninjas - Dog Facts](https://api-ninjas.com/api/dogs)
- LLaMA 3.2-11B Vision Preview model
- Open-source tools: `requests`, `dotenv`, `base64`, `IPython.display`

## 📁 Directory Structure

```
only_doggy_base.py         # Main Python script
.env                       # Environment variables (GROQ_API_KEY, NINJA_API_KEY)
assets/
└── your_image.jpeg        # Sample image input
```

## ⚙️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Sahil1030/only-doggy.git
   cd only-doggy
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file:

   ```
   GROQ_API_KEY=your_groq_api_key
   NINJA_API_KEY=your_api_ninjas_key
   ```

4. Replace the image path with your own image:

   ```python
   image_path = "path_to_your_dog_image.jpg"
   ```

## 🧪 How It Works

1. Encodes an image to base64 format.
2. Sends the image and a prompt to the Groq LLaMA model.
3. Extracts the breed name from the model's output.
4. Queries API Ninjas for that breed's characteristics.
5. Uses the Groq model again to generate a natural-language assessment of the breed.

## 📊 Output Example

- Breed Identified: **German Shepherd**
- Traits:
  - Shedding: 4/5
  - Barking: 3/5
  - Energy: 5/5
  - Protectiveness: 5/5
- Assessment: *"The German Shepherd is highly intelligent, protective, and energetic. Ideal for active families or as working dogs..."*

## 📌 To-Do

- Add support for cat breeds.
- Improve error handling for API responses.
- UI version using Streamlit or Gradio.

## 📜 License

This project is licensed under the MIT License.

