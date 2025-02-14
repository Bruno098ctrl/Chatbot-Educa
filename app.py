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
    try:
        data = request.json
        user_message = data.get("mensagem", "").strip()

        if not user_message:
            return jsonify({"error": "Nenhuma mensagem recebida"}), 400

        # Enviar a mensagem para a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente educacional."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response["choices"][0]["message"]["content"]
        return jsonify({"resposta": bot_response})

    except openai.error.OpenAIError as e:
        return jsonify({"error": f"Erro na OpenAI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render usa a porta definida na variável PORT
    app.run(host="0.0.0.0", port=port)
