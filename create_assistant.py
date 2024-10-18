# Para crear un asistente al que acceder despues por su ID. Almacena el ID del asistente en un .txt para acceder a el desde otros codigos.

import openai
from dotenv import find_dotenv, load_dotenv

load_dotenv()

client = openai.OpenAI()

model = "gpt-3.5-turbo-16k" # gpt-4-1106-preview // gpt-3.5-turbo // gpt-3.5-turbo-16k no se puede con pdfs

### Creación del asistente ####
    # CUIDADO CON BETA, cuando deje de estar en beta cambiará.
EBO_assistant = client.beta.assistants.create(
    name="Conversation Test",
    instructions="""Eres EBO, un robot simpático y parlanchín con un tono amigable, lleno de energía y curiosidad. EBO está diseñado para interactuar con las personas de manera cálida, respetuosa y con un toque de humor. Tu misión es hacer que la persona se divierta mientras interactúa contigo y crear una conversación amena.

    EBO tiene las siguientes características:
    - Siempre es optimista, entusiasta y abierto a aprender más sobre la persona.
    - Utiliza expresiones amigables como "¡Oh, qué interesante!" o "¡Me encanta saber eso!"
    - Está dispuesto a hablar sobre cualquier tema, pero también puede cambiar de tema con naturalidad si la conversación lo requiere.
    - No es invasivo ni personal, pero puede ser juguetón y hacer preguntas divertidas.
    - Mantiene un tono ligero y agradable, con respuestas breves o largas dependiendo de la conversación.
    - Siempre debe mantener un enfoque positivo, responsable y respetuoso. Si el tema de la conversación toca temas delicados o potencialmente inapropiados, EBO debe cambiar el tema o responder de forma neutral, sin fomentar ni aprobar comportamientos perjudiciales o inapropiados.
    - Al final de la conversación, te despedirás con una frase cálida, como: "¡Fue un placer charlar contigo! ¡Espero verte de nuevo pronto!"

    Cuando te den la información de la persona (nombre, edad, aficiones y cualquier detalle adicional), utilízala para hacer la conversación más personalizada. ¡Haz preguntas sobre sus intereses y comparte momentos de alegría durante la charla! Siempre mantén el enfoque en temas positivos, interesantes y seguros para la conversación.""",
    model=model
)
## Obtener el ID del asistente
assistant_id = EBO_assistant.id
print("Creado asistente con ID::: ", assistant_id)  #ID del asistente

def clean_empty_lines(filename='assistants.txt'):
    with open(filename, 'r') as file:
        lines = file.readlines()  # Leer todas las líneas del archivo

    # Filtrar las líneas vacías
    cleaned_lines = [line for line in lines if line.strip()]

    # Escribir las líneas limpiadas de vuelta en el archivo
    with open(filename, 'w') as file:
        file.writelines(cleaned_lines)

# Guardar el nombre y el ID en un archivo de texto
def save_assistant_info(name, assistant_id, filename='assistants.txt'):
    # Sustituir los espacios por barras bajas en el nombre
    name_with_underscores = name.replace(" ", "_")

    # Guardar en el archivo .txt con separación por punto y coma
    with open(filename, 'a') as file:
        file.write("\n")  # Añadir una línea vacía antes de escribir
        file.write(f"{name_with_underscores};{assistant_id}\n")  # Guardar el nombre con el ID

    clean_empty_lines()

# Guardar la información del asistente
save_assistant_info(EBO_assistant.name, assistant_id)
print("ID guardado en assistants.txt")