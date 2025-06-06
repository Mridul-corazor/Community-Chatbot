from config import model
from prompts import PROMPTS

def call_gemini(prompt_key, context_vars=None, max_tok=None):
    """
    Calls the Gemini API with a structured prompt.

    Args:
        prompt_key (str): The key for the desired prompt in the PROMPTS dictionary.
        context_vars (dict, optional): Variables to format the prompt string. Defaults to None.
        max_tok (int, optional): Overrides the default max_output_tokens. Defaults to None.

    Returns:
        str: The generated text from the model or an error message.
    """
    try:
        if prompt_key not in PROMPTS:
            return f"⚠️ Error: Prompt key '{prompt_key}' not found."

        prompt_config = PROMPTS[prompt_key]
        prompt_template = prompt_config["prompt"]
        
        # Format the prompt with context variables if provided
        final_prompt = prompt_template.format(**context_vars) if context_vars else prompt_template

        # Determine max tokens
        max_output_tokens = max_tok if max_tok is not None else prompt_config["max_tokens"]

        # Generate content
        response = model.generate_content(
            final_prompt,
            generation_config={"max_output_tokens": max_output_tokens}
        )
        return response.text.strip()

    except Exception as e:
        return f"⚠️ An error occurred with the Gemini API: {e}"