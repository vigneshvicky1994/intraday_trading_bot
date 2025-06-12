import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key, model_name="gemini-1.5-flash", temperature=0.7):
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.model = None
        self.convo = None
        self._configure_model()

    def _configure_model(self):
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "top_p": 1.0,
                "top_k": 1,
                "max_output_tokens": 2048
            }
        )
        self.convo = self.model.start_chat(history=[])

    def reset_conversation(self):
        self.convo = self.model.start_chat(history=[])

    def send_prompt(self, prompt):
        response = self.convo.send_message(prompt)
        return response.text

    def get_history(self):
        return self.convo.history if self.convo else []

    def get_model_info(self):
        return {
            "model_name": self.model_name,
            "temperature": self.temperature
        }
