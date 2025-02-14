from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Configuração da chave da API da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Pegando a chave das variáveis de ambiente

@app.route("/", methods=["GET"])
def home():
    return "Chatbot está rodando!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    user_message = data.get("mensagem", "")

    if not user_message:
        return jsonify({"erro": "Nenhuma mensagem recebida"}), 400

    try:
        # Modelo padrão como gpt-3.5-turbo para evitar erro de cota
        modelo = "gpt-3.5-turbo"

        response = openai.ChatCompletion.create(
            model=modelo,
            messages=[
                {"role": "system", "content": "Você é um assistente educacional."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response["choices"][0]["message"]["content"]
        return jsonify({"resposta": bot_response})

    except openai.error.OpenAIError as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
