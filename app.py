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
        if not data or "Body" not in data:
            return jsonify({"error": "Requisição inválida. O campo 'Body' é obrigatório."}), 400

        user_message = data["Body"]

        # Chamada à API da OpenAI com modelo gpt-4o
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um assistente educacional."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response["choices"][0]["message"]["content"]
        return jsonify({"message": bot_response})

    except openai.error.RateLimitError:
        return jsonify({"error": "Você excedeu sua cota de uso da API da OpenAI. Verifique seu plano e billing."}), 429

    except openai.error.InvalidRequestError:
        return jsonify({"error": "Erro na requisição para a OpenAI. Verifique os parâmetros enviados."}), 400

    except Exception as e:
        return jsonify({"error": f"Erro interno do servidor: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
