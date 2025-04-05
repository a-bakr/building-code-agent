import base64
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI


vis_model_id = 'gemini-2.0-flash'
vision_llm = ChatGoogleGenerativeAI(model=vis_model_id)

@tool
def text_extraction(img_path: str):
    """Extract text from an image  file using a multimodal model.
    
    Args:
        llm: The multimodal model to use for text extraction.
        img_path (str): The path to the image file.
        
    Returns:
        str: The extracted text from the image.    
    """
    
    print(f"Extracting text from image: {img_path}")
    
    all_text = ""
    
    try:
        # Read image adn encode as base64
        with open(img_path, 'rb') as image_file:
            image_bytes = image_file.read()

        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Prepare the prompt including the base64 image data
        message = [
            HumanMessage(content=[
                {
                    'type': 'text',
                    'text': ("Extract all the text from this image. convert it into english. Return only the extracted text, no explanations.")
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"
                    },
                },
            ])
        ]
        
        # Call the vision-capable model
        res = vision_llm.invoke(message)
        
        # Append extracted text
        all_text += str(res.content) + "\n\n"
        return all_text.strip()

    except Exception as e:
        error_mes = f"Error extracting text: {str(e)}"
        print(error_mes)
        return ""