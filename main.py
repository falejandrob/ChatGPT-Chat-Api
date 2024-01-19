from openai import OpenAI
import config
import saveResponse
import typer
from rich import print
from rich.table import Table


#global variables

messages = []

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

    #imprime mensaje inicial
    print("💬 [bold green]ChatGPT API en Python[/bold green]")

    #Tabla comandos
    table = Table("Comando","Descripcion")
    table.add_row("exit","Salir de la aplicación")
    table.add_row("new","Empieza una conversacion nueva")

    print(table)
    
    messages = init_context()

    
    # Cargar la última respuesta si existe
    last_response = saveResponse.retrieveLastResponse()
    if last_response is not None:
        messages.extend(last_response)
    
    while True:

        content = _prompt()

        if content =="new":
            saveResponse.saveResponse(messages)
            messages = init_context()
            content = _prompt()
            print("🆕 Nueva conversación creada")

        __saveResponseUser(content)

        #print[f"[red]{content}[red]"]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        response_content = response.choices[0].message.content
    
        __saveResponseAssistant(response_content)

        print(f"[bold green]> [/bold green] [green]{response_content}[/green]")


def __saveResponseAssistant(response):
    messages.append({"role": "assistant", "content": response})

def __saveResponseUser(response):
    messages.append({"role": "user", "content": response})

def _prompt() -> str:
    prompt = typer.prompt("¿Sobre que quieres hablar?\n")
    if prompt == "exit":
        exit = typer.confirm("❗ ¿Estas Seguro?")
        if exit:
            print("👋 ¡Adios!")
            # Guardar la última respuesta al salir
            saveResponse.saveResponse(messages)
            raise typer.Abort()
        return _prompt()
    
    return prompt
    


if __name__ == "__main__":
    typer.run(main)
