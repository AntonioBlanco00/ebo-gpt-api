import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime
import os
import sys
load_dotenv()

# openai.api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()    # Si no va, descomentar la key y añadirla en este paréntesis
# model = "gpt-3.5-turbo-16k"

### Función y lectura del ID del asistente según el nombre del mismo

def get_assistant_id_by_name(name, filename='assistants.txt'):
    # Reemplazar los espacios en el nombre por barras bajas
    name_with_underscores = name.replace(" ", "_")

    # Leer el archivo y buscar el asistente por nombre
    with open(filename, 'r') as file:
        for line in file:
            stored_name, stored_id = line.strip().split(';')
            if stored_name == name_with_underscores:
                return stored_id
    return None  # Si no se encuentra el asistente

assistant_name = "Conversation Game" # A futuro este assistan name se pasará por el DSR dependiendo del juego.
assistant_id = get_assistant_id_by_name(assistant_name)
if assistant_id:
    print(f"El ID del asistente '{assistant_name}' es: {assistant_id}")
else:
    print(f"No se encontró un asistente con el nombre '{assistant_name}'")
    sys.exit()  # Termina la ejecución del programa

### Creación del hilo de conversación
thread = client.beta.threads.create()
thread_id = thread.id
print(f"Thread creado con ID: {thread_id}")

def delete_thread(thread_id):
    client.beta.threads.delete(thread_id)
    print(f"El hilo con ID: {thread_id} ha sido eliminado.")

### Creación de un mensaje
message = """
{
  "goal": "preparar un zumo de naranja",
  "nivel de la descripción de las escenas": "Descripciones detalladas de máximo 75 palabras. Preguntas cortas y concisas",
  "nombre del jugador":"Luis",
  "aficiones":["manualidades con cerámica","salir con los amigos y viajar"],
  "edad":65,
  "scenes":
[
    "id", 0,
    "name","cocina",
    "actions",
    [
      "buscar en el armario",
      "leer un libro de cocina",
      "mirar en el frigorífico"
    ],
    "props", "Tu hermana Nuria",
    "emotion", "feliz",
    
    "id", 1,
    "name", "salón",
    "actions",
    [
      "encender la televisión",
      "encender la luz", 
      "escuchar música"
    ],
    "props", "",
    
    "id", 2,
    "name", "dormitorio",
    "actions",
    [
      "echarte en la cama",
      "escuchar música",
      "apagar la luz"
    ],
    "props", "",
    
    "id", 3,
    "name", "entrada",
    "actions",
    [
      "abrir la puerta de la calle hacia el jardín", "revisar las fotos del mueble"
    ],
    "props", "",
    
    "id", 5,
    "name", "jardín",
    "actions",
    [
      "coger una naranja",
      "coger un limón"
    ],
    "props", ""
  ],
  "inicio": "entrada"
}
"""

# Primer mensaje, el cual envia el json y la respuesta es el inicio del juego
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content=message
)

### Ejecución del asistente ###
run = client.beta.threads.runs.create(
    assistant_id=assistant_id,
    thread_id=thread_id,
    instructions="Ten en cuenta los datos del json. Empieza ya con el juego y recuerda describir la escena y siempre darle al usuario a elegir entre dos opciones, pero no las numeres, haz todo el texto de seguido"
)
run_id = run.id

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=1):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)

### Ejecución ###
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run_id)

### Ver los logs ###
run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run_id
)
print(f"Steps---> {run_steps.data[0]}")

delete_thread(thread_id=thread_id)

