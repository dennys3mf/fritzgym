"""Curated exercise guides. Source videos remain embedded on their publishers' channels."""

import unicodedata


NSU_LIBRARY = 'https://www.rec.nova.edu/recreational-complex/exercise-library.html'
NSU_AUTHOR = 'Nova Southeastern University RecWell'


def normalizar_nombre(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold())
                   if not unicodedata.combining(c)).strip()


def guia(nombre, grupo, video, resumen, pasos, errores, aliases=(), autor=NSU_AUTHOR,
         fuente=NSU_LIBRARY, videos_originales=None):
    return dict(nombre=nombre, grupo=grupo, video=video, resumen=resumen, pasos=pasos,
                errores=errores, aliases=aliases, autor=autor, fuente=fuente,
                videos_originales=videos_originales or {})


GUIAS = [
    guia('Máquina Smith', 'PI', 'BtfMX4WqUBo',
         'Sentadilla guiada para trabajar piernas y glúteos. Ajusta los topes de seguridad y practica el recorrido con poca carga antes de empezar.',
         ['Coloca la barra sobre la parte alta de la espalda, sin apoyarla en el cuello, y ajusta los seguros.',
          'Busca una posición de pies que te permita mantener toda la planta apoyada durante el recorrido.',
          'Flexiona caderas y rodillas de forma controlada, sin perder el apoyo de los pies.',
          'Empuja el suelo para volver a la posición inicial y vuelve a bloquear la barra antes de salir.'],
         ['Bajar más de lo que puedes controlar.', 'Levantar los talones o dejar que las rodillas colapsen hacia dentro.', 'Empezar sin colocar los topes de seguridad.'],
         aliases=('Maquina Smith', 'Sentadilla en Smith'), autor='Muscle & Strength',
         fuente='https://www.muscleandstrength.com/exercises/smith-machine-squat.html'),
    guia('Press de pecho en máquina', 'PE', 'rlsqcb_YueM',
         'Empuje guiado para pectorales, con participación de tríceps y hombros. La altura del asiento y un regreso controlado ayudan a mantener una ejecución estable.',
         ['Regula el asiento para que las empuñaduras queden a la altura del pecho.',
          'Apoya la espalda en el respaldo, coloca los pies firmes y mantén las muñecas alineadas.',
          'Empuja las empuñaduras sin separar la espalda del apoyo ni elevar los hombros.',
          'Regresa lentamente a una posición cómoda, sin dejar caer las placas.'],
         ['Arquear la espalda para mover más carga.', 'Doblar las muñecas o encoger los hombros.', 'Dejar que las placas golpeen al regresar.'],
         aliases=('Maquina para pectorales', 'Máquina para pectorales', 'Chest press')),
    guia('Extensión de piernas', 'PI', '6itzUh4wAXc',
         'Trabajo guiado de cuádriceps. Ajusta el respaldo y el rodillo antes de mover la carga para que la rodilla acompañe el eje de la máquina.',
         ['Ajusta el respaldo para alinear la rodilla con el eje de giro.',
          'Sitúa el rodillo en la parte baja de la pierna, por encima del tobillo.',
          'Sujeta los agarres y extiende las piernas de manera controlada.',
          'Baja despacio sin despegar la cadera ni dejar caer las placas.'],
         ['Balancear el cuerpo para levantar el peso.', 'Colocar el rodillo sobre el pie.', 'Dar una patada brusca al final del recorrido.'],
         aliases=('Leg Extension', 'Extensiones de cuádriceps')),
    guia('Aperturas en máquina', 'PE', 'COSR3raZpec',
         'Movimiento de aproximación de brazos para trabajar pectorales. Mantén el tronco apoyado y un ángulo de codo cómodo durante toda la repetición.',
         ['Ajusta el asiento para que los apoyos o agarres queden a la altura del pecho.',
          'Apoya la espalda y conserva una ligera flexión de codos.',
          'Acerca los brazos al frente sin inclinar el cuerpo para ayudarte.',
          'Vuelve despacio, limitando la apertura a un rango que puedas controlar.'],
         ['Llevar los brazos demasiado atrás.', 'Encoger los hombros o separar la espalda.', 'Rebotar para iniciar cada repetición.'],
         aliases=('Pec deck',), videos_originales={'QHrIO139sWc': 'Maru lekhal'}),
    guia('Jalón al pecho', 'ES', 'C8C4BpxCQqQ',
         'Tirón vertical para la musculatura de la espalda. Ajusta el apoyo de muslos y dirige el movimiento con los codos, manteniendo el tronco estable.',
         ['Ajusta el asiento y el apoyo de muslos para mantener una posición firme.',
          'Toma la barra con un agarre cómodo y mantén el pecho orientado al frente.',
          'Lleva los codos hacia abajo, acercando la barra a la zona alta del pecho.',
          'Deja subir la barra de forma controlada, sin soltar la tensión de golpe.'],
         ['Llevar la barra detrás de la nuca.', 'Balancear el torso para mover el peso.', 'Tirar solo con las manos y encoger los hombros.'],
         aliases=('Lat pull down', 'Jalón en polea')),
    guia('Remo sentado en polea', 'ES', 'tl8HYV9syxs',
         'Tirón horizontal para la espalda. La posición del tronco y el regreso controlado permiten concentrar el trabajo sin convertir el movimiento en un balanceo.',
         ['Siéntate con los pies apoyados y las rodillas ligeramente flexionadas.',
          'Sujeta el agarre manteniendo la espalda en una posición estable.',
          'Lleva los codos hacia atrás y acerca el agarre al abdomen.',
          'Extiende los brazos lentamente, evitando redondear la espalda.'],
         ['Echar el tronco hacia atrás para tirar.', 'Elevar los hombros.', 'Soltar la carga al extender los brazos.'],
         aliases=('Cable row', 'Remo en polea baja')),
    guia('Curl de bíceps en máquina', 'BR', 'c1xKUR79ktU',
         'Flexión de codo guiada para trabajar bíceps. Ajusta el asiento y los apoyos para mantener los brazos estables durante la subida y la bajada.',
         ['Regula el asiento y apoya los brazos según el diseño de la máquina.',
          'Sujeta el agarre con las muñecas alineadas y los hombros relajados.',
          'Flexiona los codos sin despegar los brazos del apoyo.',
          'Desciende lentamente sin forzar una extensión excesiva del codo.'],
         ['Levantar los hombros para ayudar al movimiento.', 'Doblar las muñecas hacia atrás.', 'Dejar caer la carga en la bajada.'],
         aliases=('Bicep curl', 'Curl de biceps en maquina')),
    guia('Extensión de tríceps en polea', 'BR', 'uxDEpUFUi8Q',
         'Extensión de codos para tríceps con polea alta. Mantén los brazos cerca del cuerpo y mueve el agarre sin usar el peso del tronco.',
         ['Coloca la polea arriba y elige un agarre cómodo.',
          'Acércate lo suficiente para mantener los codos junto al torso.',
          'Extiende los codos hacia abajo con las muñecas alineadas.',
          'Permite que el agarre suba despacio sin desplazar los brazos hacia delante.'],
         ['Balancearse encima del agarre.', 'Separar los codos en cada repetición.', 'Usar una carga que impida controlar la subida.'],
         aliases=('Tricep push down', 'Jalón de tríceps')),
    guia('Press de hombros en máquina', 'HO', 'HmHs1UzeBz8',
         'Empuje guiado para hombros, con ayuda de tríceps. Ajusta la altura de los agarres y mantén la espalda apoyada durante el recorrido.',
         ['Regula el asiento para empezar con los agarres en una posición cómoda junto a los hombros.',
          'Apoya la espalda y coloca ambos pies firmes en el suelo.',
          'Empuja hacia arriba sin levantar la cadera ni arquear la zona lumbar.',
          'Baja con control hasta la posición inicial, sin forzar el recorrido.'],
         ['Compensar arqueando la espalda.', 'Encoger el cuello entre los hombros.', 'Bajar a una posición que no puedes controlar.'],
         aliases=('Shoulder press',)),
    guia('Elevaciones laterales en máquina', 'HO', '0dwOyP_pnv0',
         'Elevación lateral guiada para hombros. Mantén el cuerpo estable y adapta el asiento y los apoyos al diseño de la máquina.',
         ['Ajusta el asiento y sitúa los brazos sobre los apoyos.',
          'Mantén el torso apoyado y los hombros alejados de las orejas.',
          'Eleva los brazos hacia los lados hasta un rango cómodo.',
          'Regresa lentamente, manteniendo el control de la resistencia.'],
         ['Inclinar el torso para ayudar al movimiento.', 'Encoger los hombros al subir.', 'Dejar caer los apoyos de golpe.'],
         aliases=('Lateral raise',)),
    guia('Abdominales en máquina', 'AB', 'kLyXnHGuJO4',
         'Flexión de tronco guiada para el abdomen. Ajusta los apoyos y acompaña el movimiento sin tirar del cuello ni convertirlo en un impulso de brazos.',
         ['Regula asiento, respaldo y apoyos según el modelo.',
          'Toma los agarres de manera suave, manteniendo el cuello alineado.',
          'Acerca el tronco a la pelvis con un movimiento corto y controlado.',
          'Vuelve despacio sin perder el apoyo ni dejar caer las placas.'],
         ['Tirar de los agarres con los brazos.', 'Adelantar la cabeza bruscamente.', 'Usar el impulso en lugar de controlar el movimiento.'],
         aliases=('Abdominal crunch machine',)),
    guia('Multi abductor', 'PI', '830CzAeOaqw',
         'Abducción de cadera para trabajar la musculatura lateral de los glúteos. Ajusta los apoyos y usa un recorrido que puedas controlar sin balancearte.',
         ['Ajusta la posición inicial y sitúa las piernas en los apoyos.',
          'Mantén la pelvis estable y apoya el tronco según el modelo.',
          'Separa las piernas de forma gradual, sin dar un impulso inicial.',
          'Vuelve lentamente, evitando que las placas golpeen entre sí.'],
         ['Balancear el tronco para abrir más.', 'Usar una carga que impida frenar el regreso.', 'Forzar la apertura más allá de un rango cómodo.'],
         aliases=('Abductores en máquina', 'Hip abduction'), videos_originales={'Iqi-hXErUE0': 'Karen Zárate'}),
    guia('Curl femoral acostado', 'PI', '6JQflLWhKfg',
         'Flexión de rodillas para trabajar isquiotibiales. Alinea la rodilla con el eje del equipo y mantén la pelvis apoyada durante la repetición.',
         ['Ajusta el rodillo para apoyarlo en la parte baja de las piernas, por encima de los tobillos.',
          'Comprueba la posición de las rodillas respecto al eje y sujeta los agarres.',
          'Flexiona las rodillas acercando los talones sin levantar la pelvis.',
          'Extiende lentamente sin dejar caer el peso.'],
         ['Despegar la cadera del banco.', 'Usar un tirón para iniciar el movimiento.', 'Apoyar el rodillo directamente sobre el talón.'],
         autor='Karen Zárate', fuente='https://www.youtube.com/watch?v=6JQflLWhKfg'),
    guia('Abdominales en Ab Coaster', 'AB', 'xLUAXHVM90E',
         'Movimiento guiado de rodillas hacia el tronco para el abdomen. Empieza con un recorrido corto y evita balancear el carro con los brazos.',
         ['Apoya las rodillas en la plataforma y coloca las manos en los agarres.',
          'Mantén el cuello cómodo y los hombros relajados.',
          'Acerca las rodillas hacia el tronco con control, sin tirar bruscamente de los agarres.',
          'Devuelve el carro lentamente a su posición de inicio.'],
         ['Impulsar el carro con todo el cuerpo.', 'Tirar del cuello hacia delante.', 'Soltar la plataforma en el descenso.'],
         aliases=('ABDOMINALES EN AB COASTER',), autor='G Personal Trader',
         fuente='https://www.youtube.com/watch?v=xLUAXHVM90E'),
    guia('Zancadas con mancuernas', 'PI', '8h4nhwC-tHU',
         'Trabajo unilateral de piernas y glúteos con mancuernas. Busca una longitud de paso que te permita mantener el equilibrio y el apoyo del pie delantero.',
         ['Sujeta las mancuernas a ambos lados con el tronco estable.',
          'Da un paso hacia delante y flexiona ambas rodillas con control.',
          'Baja hasta un rango cómodo, manteniendo la rodilla delantera alineada con el pie.',
          'Empuja con el pie delantero para regresar sin perder el equilibrio.'],
         ['Dar un paso que no te permite mantener el equilibrio.', 'Dejar caer el cuerpo sobre la rodilla trasera.', 'Usar más carga de la que puedes controlar.'],
         autor='ONE MIN GYM', fuente='https://www.youtube.com/watch?v=8h4nhwC-tHU'),
]

POR_NOMBRE = {normalizar_nombre(name): item for item in GUIAS
              for name in (item['nombre'], *item['aliases'])}

GRUPOS = {
    'PE': ('Pecho', 'Aprende a ajustar los apoyos y a controlar los movimientos de empuje y apertura.'),
    'ES': ('Espalda', 'Compara tirones verticales y horizontales. Mantén el tronco estable y controla el regreso.'),
    'PI': ('Pierna', 'Encuentra guías de rodilla y cadera. Revisa los ejes, rodillos y seguros antes de empezar.'),
    'BR': ('Brazo', 'Trabaja la flexión y la extensión de codo con apoyos estables y sin balancear el cuerpo.'),
    'HO': ('Hombro', 'Ajusta la altura del asiento y el recorrido. Evita usar el tronco para mover la carga.'),
    'AB': ('Abdomen', 'Prioriza un movimiento controlado del tronco y la pelvis, sin tirar del cuello.'),
}


def obtener_guia(maquina):
    item = POR_NOMBRE.get(normalizar_nombre(maquina.nombre))
    if not item:
        return None
    # An unrelated manually edited video must not inherit the curated attribution.
    video_id = maquina.youtube_id
    if video_id not in {item['video'], *item['videos_originales']}:
        return None
    return {**item, 'autor': item['videos_originales'].get(video_id, item['autor']),
            'url_video': f'https://www.youtube.com/watch?v={video_id}'}
