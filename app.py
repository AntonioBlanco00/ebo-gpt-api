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

# assistant_name = "Conversation Game" # A futuro este assistan name se pasará por el DSR dependiendo del juego.
assistant_name = "Conversation Test"
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
Nombre: Antonio
Edad: 24 años
Aficiones: Recibir criticas constantes, y las gatitas
Información adicional: Bromista, le gusta recibir chascarrillos
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
    instructions="Para iniciar la conversación solo saluda al usuario y presentate como EBO, el robot mas simpatico del mundo."
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

### Borra el hilo utilizado al finalizar
# delete_thread(thread_id=thread_id)
def exit_program():
    print("-------------------- El programa ha terminado --------------------")
    delete_thread(thread_id=thread_id)
    print("-------------------- Hilo borrado --------------------")
    sys.exit()

def ask_user_for_input(prompt="Por favor, introduce tu mensaje: "):
    user_input = input(prompt)
    if user_input.strip().lower() == "salir":
        print("Saliendo del programa...")
        exit_program()
    return user_input


def send_message_to_assistant(client, thread_id, assistant_id, user_message):
    # Enviar el mensaje del usuario al asistente
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Ejecutar el asistente con instrucciones (si se proporcionan)
    # run = client.beta.threads.runs.create(
    #     thread_id=thread_id,
    #     assistant_id=assistant_id,
    #     instructions="Continua la conversación como tú sabes"
    # )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    run_id = run.id
    print(f"Mensaje enviado. Run ID: {run_id}")
    return run_id


def get_assistant_response(client, thread_id, run_id):
    # Esperar hasta que el asistente termine de procesar la respuesta
    print("Esperando la respuesta del asistente...")
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        time.sleep(1)

    # Recuperar los mensajes del asistente
    messages = client.beta.threads.messages.list(thread_id=thread_id)

    # Filtrar el mensaje del asistente
    assistant_messages = [
        message
        for message in messages.data
        if message.role == "assistant" and message.run_id == run_id
    ]

    if assistant_messages:
        # Extraer y devolver la respuesta
        assistant_response = assistant_messages[0].content[0].text.value
        return assistant_response
    else:
        return "No se recibió respuesta del asistente."

terminar_programa = False
while terminar_programa == False:
    user_message = ask_user_for_input()
    run_id = send_message_to_assistant(client, thread_id, assistant_id, user_message)
    response = get_assistant_response(client, thread_id, run_id)
    print(f"Respuesta del asistente: {response}")



