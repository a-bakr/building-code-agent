import gradio as gr
from agent import run_agent
import os

def process_query(image, question):
    """Process the user query using the agent"""
    if image is None:
        return "Please upload an image", "", ""
    
    # Save the image temporarily
    temp_image_path = "temp_image.png"
    image.save(temp_image_path)
    
    # Run the agent
    try:
        result = run_agent(temp_image_path, question)
        
        # Get tool outputs
        tool_outputs = result.get('tool_outputs', {})
        extracted_text = tool_outputs.get('text_extraction', "No text extracted")
        building_code = tool_outputs.get('building_code_retriever', "No building code retrieved")
        
        # Get final answer
        answer = result.get('result', "No answer generated")
        
        return answer, extracted_text, building_code
    except Exception as e:
        return f"Error: {str(e)}", "", ""
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)

# Create the Gradio interface
with gr.Blocks(title="Building Code Assistant") as demo:
    gr.Markdown("# Building Code Assistant")
    gr.Markdown("Upload an architectural plan and ask questions about building codes and regulations.")
    
    with gr.Row():
        with gr.Column(scale=1):
            image_input = gr.Image(type="pil", label="Upload Architectural Plan")
            question_input = gr.Textbox(
                label="Your Question", 
                placeholder="What are the building code requirements for this plan?",
                lines=2
            )
            submit_btn = gr.Button("Submit", variant="primary")
        
        with gr.Column(scale=2):
            answer_output = gr.Markdown(label="Answer", elem_id="answer_box")

            with gr.Accordion("Detailed Information", open=False):
                with gr.Tab("Extracted Text"):
                    text_output = gr.Textbox(label="Extracted Text", lines=10)
                with gr.Tab("Building Code"):
                    code_output = gr.Textbox(label="Retrieved Building Code", lines=10)
    
    submit_btn.click(
        fn=process_query,
        inputs=[image_input, question_input],
        outputs=[answer_output, text_output, code_output],
        show_progress="full"
    )
    
    gr.Examples(
        examples=[
            ["samples/01.png", "هل هذة الغرف مطابقة لاشتراطات البناء؟"],
            ["samples/02.png", "Is the Bedroom comply with building code?"],
            ["samples/03.png", "Is the bedroom's area  sufficient base on the building code?"],
        ],
        inputs=[image_input, question_input]
    )
    
    gr.Markdown("""
    ## How to use this app
    1. Upload an architectural plan or blueprint
    2. Ask a question about building codes or regulations
    3. The system will analyze the plan and provide information based on Egyptian building codes
    
    You can ask questions in English or Arabic.
    """)

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
