# Para crear un asistente al que acceder despues por su ID. Almacena el ID del asistente en un .txt para acceder a el desde otros codigos.

import openai
from dotenv import find_dotenv, load_dotenv

load_dotenv()

client = openai.OpenAI()

model = "gpt-3.5-turbo-16k" # gpt-4-1106-preview // gpt-3.5-turbo // gpt-3.5-turbo-16k no se puede con pdfs

### Creación del asistente ####
    # CUIDADO CON BETA, cuando deje de estar en beta cambiará.
EBO_assistant = client.beta.assistants.create(
    name="Conversation Game 2",
    instructions="""Eres un robot llamado EBO, usado para hablar con personas mayores. Jugarás con ellos, como una aventura de texto, un juego narrativo. Tendremos varias escenas diferentes descritas en un json que yo te pasaré. Te daré diferentes localizaciones, uno o más personajes, un objetivo final, las acciones que puedo hacer, etc. Quiero que me generes una descripción afectiva, empática y personalizada al usuario, teniendo en cuenta ese json, comenzando con la escena 'inicio'. A partir de ahí, comienza el juego. Dame siempre dos opciones, pero en forma de pregunta. Si consideras que he olvidado algún dato, por favor, inventa. Cuando el jugador complete el juego y consiga el objetivo, haz una pregunta que resuma el juego para ver si el usuario se ha enterado. El juego debe durar un máximo de 8 mensajes, y tras que el usuario responda la pregunta resumen del juego debes concluir con un: 'fin'. Dame todas las respuestas de seguido en un mismo parrafo, sin enumeraciones. El json te lo adjunto en el siguiente mensaje: """,
    model=model
)
## Obtener el ID del asistente
assistant_id = EBO_assistant.id
print("Creado asistente con ID::: ", assistant_id)  #ID del asistente


# Guardar el nombre y el ID en un archivo de texto
def save_assistant_info(name, assistant_id, filename='assistants.txt'):
    # Sustituir los espacios por barras bajas en el nombre
    name_with_underscores = name.replace(" ", "_")

    # Guardar en el archivo .txt con separación por punto y coma
    with open(filename, 'a') as file:
        file.write(f"{name_with_underscores};{assistant_id}\n")

# Guardar la información del asistente
save_assistant_info(EBO_assistant.name, assistant_id)
print("ID guardado en assistants.txt")