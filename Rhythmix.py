import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Definir las variables difusas
estado_animo = ctrl.Antecedent(np.arange(0, 11, 1), 'estado_animo')
tiempo_disponible = ctrl.Antecedent(np.arange(0, 61, 1), 'tiempo_disponible')
situacion = ctrl.Antecedent(np.arange(0, 4, 1), 'situacion')
recomendacion = ctrl.Consequent(np.arange(0, 11, 1), 'recomendacion')

# Funciones de pertenencia manuales para estado_animo
estado_animo['triste'] = fuzz.trimf(estado_animo.universe, [0, 0, 5])
estado_animo['neutral'] = fuzz.trimf(estado_animo.universe, [0, 5, 10])
estado_animo['feliz'] = fuzz.trimf(estado_animo.universe, [5, 10, 10])

# Funciones de pertenencia para las otras variables
tiempo_disponible['poco'] = fuzz.trimf(tiempo_disponible.universe, [0, 0, 15])
tiempo_disponible['moderado'] = fuzz.trimf(tiempo_disponible.universe, [10, 30, 50])
tiempo_disponible['mucho'] = fuzz.trimf(tiempo_disponible.universe, [40, 60, 60])
situacion['trabajo'] = fuzz.trimf(situacion.universe, [0, 0, 1])
situacion['conduciendo'] = fuzz.trimf(situacion.universe, [1, 1, 2])
situacion['relajado'] = fuzz.trimf(situacion.universe, [1, 2, 3])
situacion['fiesta'] = fuzz.trimf(situacion.universe, [2, 3, 3])
situacion['escuela'] = fuzz.trimf(situacion.universe, [3, 4, 4])

# Funciones de pertenencia para la recomendación
recomendacion['tranquila'] = fuzz.trimf(recomendacion.universe, [0, 2, 4])
recomendacion['moderada'] = fuzz.trimf(recomendacion.universe, [3, 5, 7])
recomendacion['intensa'] = fuzz.trimf(recomendacion.universe, [6, 8, 10])

# Reglas difusas
reglas = [
    # Triste
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['poco'] & situacion['trabajo'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['poco'] & situacion['conduciendo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['poco'] & situacion['relajado'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['poco'] & situacion['fiesta'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['poco'] & situacion['escuela'], recomendacion['tranquila']),
    
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['moderado'] & situacion['trabajo'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['moderado'] & situacion['conduciendo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['moderado'] & situacion['relajado'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['moderado'] & situacion['fiesta'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['moderado'] & situacion['escuela'], recomendacion['tranquila']),
    
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['mucho'] & situacion['trabajo'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['mucho'] & situacion['conduciendo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['mucho'] & situacion['relajado'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['mucho'] & situacion['fiesta'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['triste'] & tiempo_disponible['mucho'] & situacion['escuela'], recomendacion['tranquila']),
    
    # Neutral
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['poco'] & situacion['trabajo'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['poco'] & situacion['conduciendo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['poco'] & situacion['relajado'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['poco'] & situacion['fiesta'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['poco'] & situacion['escuela'], recomendacion['tranquila']),
    
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['moderado'] & situacion['trabajo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['moderado'] & situacion['conduciendo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['moderado'] & situacion['relajado'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['moderado'] & situacion['fiesta'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['moderado'] & situacion['escuela'], recomendacion['moderada']),
    
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['mucho'] & situacion['trabajo'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['mucho'] & situacion['conduciendo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['mucho'] & situacion['relajado'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['mucho'] & situacion['fiesta'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['neutral'] & tiempo_disponible['mucho'] & situacion['escuela'], recomendacion['moderada']),
    
    # Feliz
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['poco'] & situacion['trabajo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['poco'] & situacion['conduciendo'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['poco'] & situacion['relajado'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['poco'] & situacion['fiesta'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['poco'] & situacion['escuela'], recomendacion['moderada']),
    
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['moderado'] & situacion['trabajo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['moderado'] & situacion['conduciendo'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['moderado'] & situacion['relajado'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['moderado'] & situacion['fiesta'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['moderado'] & situacion['escuela'], recomendacion['moderada']),
    
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['mucho'] & situacion['trabajo'], recomendacion['moderada']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['mucho'] & situacion['conduciendo'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['mucho'] & situacion['relajado'], recomendacion['tranquila']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['mucho'] & situacion['fiesta'], recomendacion['intensa']),
    ctrl.Rule(estado_animo['feliz'] & tiempo_disponible['mucho'] & situacion['escuela'], recomendacion['moderada']),
]

# Crear el sistema de control difuso
sistema_ctrl = ctrl.ControlSystem(reglas)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# ----------- PASO 3: Definir Recomendaciones de Canciones y Artistas ----------- 
# Diccionario de recomendaciones
recomendaciones = {
    'pop': {
        'tranquila': ['The Night We Met-Lord Huron', 'All I Want-Kodaline', 'Fine Line-Harry Styles','My Tears Ricochet-Taylor Swift','Homesick-Dua Lipa','Still-Niall Horan'],
        'moderada': ['Levitating-Dua Lipa', 'Adore You-Harry Styles','The Man Who Can´t be moved-The Script','Iris-Goo Goo Dolls','Look After You-The Fray','Bad Omens-5SOS'],
        'intensa': ['Blank Space-Taylor Swift', 'Shut Up and Dance-WALK THE MOON','Uptown Funk-Mark Ronson feat. Bruno Mars','Wanna Be Starting Something-Michael Jackson','Bad Romance-Lady Gaga','Ready for it?-Taylor Swift']
    },
    'rock': {
        'tranquila': ['Going to California - Led Zeppelin', 'The Scientist - Coldplay', 'Black - Pearl Jam', 'Love of My Life - Queen', 'The Ghost of You - My Chemical Romance', 'Tears in Heaven - Eric Clapton'],
        'moderada': ['Sweet Child O´ Mine - Guns n´ Roses', 'Radioactive - Imagine Dragons', 'Somebody to Love - Queen', 'Come Together - The Beatles', 'Helena - My Chemical Romance', 'Heartbreak Hotel - Elvis Presley'],
        'intensa': ['Immigrant Song - Led Zeppelin', 'Bohemian Rhapsody - Queen', 'Welcome to the Black Parade - My Chemical Romance', 'Hound Dog - Elvis Presley', 'Back in Black - AC/DC', 'Smells Like Teen Spirit - Nirvana']

    },
    'metal': {
        'tranquila': ['Nothing Else Matters - Metallica', 'Fade to Black - Metallica', 'Hallowed Be Thy Name - Iron Maiden', 'The Trooper - Iron Maiden', 'Aerials - System of a Down', 'Watchtower - Blind Guardian'],
        'moderada': ['Paranoid - Black Sabbath', 'Holy Wars... The Punishment Due - Megadeth', 'Fear of the Dark - Iron Maiden', 'Dani California - Red Hot Chili Peppers', 'Enter Sandman - Metallica', 'Painkiller - Judas Priest'],
        'intensa': ['Master of Puppets - Metallica', 'One - Metallica', 'Raining Blood - Slayer', 'Ace of Spades - Motörhead', 'Paranoid Android - Radiohead', 'Roots Bloody Roots - Sepultura']

    },
    'jazz': {
        'tranquila': ['Take Five - Dave Brubeck', 'So What - Miles Davis', 'My Funny Valentine - Chet Baker', 'Blue in Green - Miles Davis', 'Autumn Leaves - Bill Evans', 'In a Sentimental Mood - Duke Ellington & John Coltrane'],
        'moderada': ['Sing, Sing, Sing - Benny Goodman', 'Moanin\' - Charles Mingus', 'Freddie Freeloader - Miles Davis', 'All of Me - Billie Holiday', 'Birdland - Weather Report', 'A Night in Tunisia - Dizzy Gillespie'],
        'intensa': ['A Love Supreme - John Coltrane', 'Salt Peanuts - Dizzy Gillespie', 'Take the "A" Train - Duke Ellington', 'Cherokee - Charlie Parker', 'Giant Steps - John Coltrane', 'Caravan - Duke Ellington']

    },
    'clasico': {
        'tranquila': ['Clair de Lune - Claude Debussy', 'Adagio for Strings - Samuel Barber', 'The Four Seasons: Winter - Antonio Vivaldi', 'Nocturne in E-flat Major, Op. 9, No. 2 - Frédéric Chopin', 'Gymnopédies No. 1 - Erik Satie', 'Pavane pour une infante défunte - Maurice Ravel'],
        'moderada': ['Symphony No. 5 - Ludwig van Beethoven', 'Piano Concerto No. 21 in C Major, K. 467: Andante - Wolfgang Amadeus Mozart', 'Eine kleine Nachtmusik - Wolfgang Amadeus Mozart', 'Rhapsody in Blue - George Gershwin', 'The Nutcracker Suite: Dance of the Sugar Plum Fairy - Pyotr Ilyich Tchaikovsky', 'Serenade for Strings in E Major, Op. 22: II. Tempo di Valse - Antonín Dvořák'],
        'intensa': ['The Four Seasons: Summer - Antonio Vivaldi', 'Requiem - Wolfgang Amadeus Mozart', 'O Fortuna from Carmina Burana - Carl Orff', 'Ride of the Valkyries - Richard Wagner', 'Mars, the War Bringer from The Planets - Gustav Holst', 'Symphony No. 7 - Antonín Dvořák']

    }
}

# ----------- PASO 4: Integrar Recomendaciones en el Chatbot ----------- 

# Función que maneja el comando /start
async def start(update: Update, context: CallbackContext):
    print("El comando /start ha sido recibido.")  # Mensaje de depuración
    context.user_data.clear()  # Limpiar datos del usuario
    await update.message.reply_text('¡Hola! Soy TheMagicMusicianBot, un bot de recomendaciones musicales. \n ¿Cuál es tu género musical favorito?')

# Función que maneja los mensajes del usuario sobre el género favorito
async def recibir_genero(update: Update, context: CallbackContext):
    print("Recibiendo género favorito...")  # Mensaje de depuración
    genero = update.message.text.lower()

    if genero not in recomendaciones:
        await update.message.reply_text('Género no reconocido. Por favor elige entre pop, rock, metal, jazz, o clásico.')
        return

    context.user_data['genero'] = genero
    await update.message.reply_text('¡Que bien!. ¿Cómo te sientes en este momento? (feliz, triste, neutral, enojado, malhumorado)')
    context.user_data['next_step'] = recibir_estado_animo

# Función que maneja los mensajes del usuario sobre el estado de ánimo
async def recibir_estado_animo(update: Update, context: CallbackContext):
    print("Recibiendo estado de ánimo...")  # Mensaje de depuración
    estado_animo_usuario = update.message.text.lower()

    if estado_animo_usuario not in ['feliz', 'triste', 'neutral', 'enojado', 'malhumorado']:
        await update.message.reply_text('Estado de ánimo no reconocido. Por favor elige entre feliz, triste, neutral, enojado, o malhumorado.')
        return

    context.user_data['estado_animo'] = estado_animo_usuario
    await update.message.reply_text('¿Cuánto tiempo tienes disponible para escuchar música? (Ejemplo: poco, moderado, mucho)')
    context.user_data['next_step'] = recibir_tiempo

# Función que maneja los mensajes del usuario sobre el tiempo disponible
async def recibir_tiempo(update: Update, context: CallbackContext):
    print("Recibiendo tiempo disponible...")  # Mensaje de depuración
    tiempo_disponible_usuario = update.message.text.lower()

    if tiempo_disponible_usuario not in ['poco', 'moderado', 'mucho']:
        await update.message.reply_text('Tiempo disponible no reconocido. Por favor elige entre poco, moderado, o mucho.')
        return

    context.user_data['tiempo_disponible'] = tiempo_disponible_usuario
    await update.message.reply_text('¿En qué situación estarías escuchando la música? (Ejemplo: trabajo, conduciendo, relajado, fiesta, escuela)')
    context.user_data['next_step'] = recibir_situacion

# Función que maneja los mensajes del usuario sobre la situación
async def recibir_situacion(update: Update, context: CallbackContext):
    print("Recibiendo situación...")  # Mensaje de depuración
    situacion_usuario = update.message.text.lower()

    if situacion_usuario not in ['trabajo', 'conduciendo', 'relajado', 'fiesta', 'escuela']:
        await update.message.reply_text('Situación no reconocida. Por favor elige entre trabajo, conduciendo, relajado, escuela o fiesta.')
        return

    context.user_data['situacion'] = situacion_usuario

    # Ejecutar el sistema difuso
    try:
        sistema.input['estado_animo'] = estado_animo[context.user_data['estado_animo']]
        sistema.input['tiempo_disponible'] = tiempo_disponible[context.user_data['tiempo_disponible']]
        sistema.input['situacion'] = situacion[context.user_data['situacion']]
        sistema.compute()

        nivel_recomendacion = sistema.output['recomendacion']

        # Determinar el tipo de recomendación
        if nivel_recomendacion <= 4:
            tipo_recomendacion = 'tranquila'
        elif nivel_recomendacion <= 7:
            tipo_recomendacion = 'moderada'
        else:
            tipo_recomendacion = 'intensa'

        # Obtener recomendaciones del género y tipo de recomendación correspondiente
        genero = context.user_data['genero']
        canciones_recomendadas = recomendaciones[genero][tipo_recomendacion]

        # Enviar las recomendaciones al usuario
        mensaje_recomendacion = f"Te recomiendo escuchar estas canciones de {genero} ({tipo_recomendacion}):\n"
        for cancion in canciones_recomendadas:
            mensaje_recomendacion += f"- {cancion}\n"

        await update.message.reply_text(mensaje_recomendacion)
    except KeyError as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Función principal para manejar mensajes
async def handle_message(update: Update, context: CallbackContext):
    print("Manejando mensaje del usuario...")  # Mensaje de depuración
    if 'next_step' in context.user_data:
        await context.user_data['next_step'](update, context)
    else:
        await recibir_genero(update, context)

# Configurar el bot de Telegram
def main():
    TOKEN = '7505794621:AAGhgDUPV_C5TvfUYzJ5NJISi9Qo1nPt18k'  # Reemplaza esto con tu token real
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot está corriendo...")  # Mensaje de depuración

    application.run_polling()

if __name__ == '__main__':
    main()
