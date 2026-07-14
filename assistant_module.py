# Simple text AI assistant. Replace with advanced chatbot if you wish.
def get_assistant_response(message, user_mode):
    # You could connect to OpenAI/GPT/etc. for advanced behavior.
    # For now, handle some basics
    help_responses = {
        "blind": "You can use your keyboard and screen reader to navigate. Use Enter, arrow keys, and listen for form fields.",
        "deaf": "All instructions are shown as text. Visual cues and sign language video are available.",
        "normal": "Use your mouse or keyboard to fill the form. Contact support for extra help."
    }
    message = message.lower()
    if "help" in message or "how" in message:
        return help_responses.get(user_mode, help_responses["normal"])
    return "I'm here to guide you! Describe your issue or question."
