from openai import OpenAI
import config
import saveResponse


# Inicialización del cliente OpenAI
client = OpenAI(api_key=config.api_key)

# Función para inicializar el contexto del asistente
def init_context():
    return [{"role": "system", "content": "Eres un asistente que me va a ayudar a darme información sobre el tema que te diga para un podcast"}]

# Función para obtener respuesta de OpenAI
def get_openai_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# Función principal del programa
def main():
    messages = init_context()

    # Cargar la última respuesta si existe
    last_response = saveResponse.retrieveLastResponse()
    if isinstance(last_response, dict):
        messages.append(last_response)

    while True:

        content = input("¿Sobre que quieres hablar?\n")

        if content == "Adios":
            break

        messages.append({"role": "user", "content": content})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    
        messages.append({"role": "assitant", "content": response})

        print(response.choices[0].message.content)

    # Guardar la última respuesta al salir
    saveResponse.saveResponse(response)

if __name__ == "__main__":
    main()
