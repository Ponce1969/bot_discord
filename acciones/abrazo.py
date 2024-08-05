import random



def abrazo_nadie(nombre: str) -> str:
    
    MENSAJE_SIN_NOMBRE = [
        f"No puedes abrazar al aire, {nombre}. ¿Por qué no abrazas a alguien en persona?",
        f"Oye, {nombre}, No puedes simplemente abrazar a la nada. !Ve y abraza a alguien!",
        f"¿Estás bien, {nombre}? No puedes abrazar a la nada. ¡O es alguien invisible!",
        f"{nombre}, ¿estás intentando abrazar tu imaginacion ?",
        f"!Es un abrazo fantasma, {nombre}!",
        f"¿Practicando tecnicas de abrazo, {nombre}?",
        f"{nombre}, ¿estás abrazando a los amigos imaginarios?",
        f"¿Estás abrazando algo que no vimos, {nombre}?",
        f"{nombre}, ¿estás abrazando la luz?",
        f"Creo que {nombre} está abrazando a la comunidad discord .",
        f"Sin {nombre}, ¿estás abrazando a los bots?",
        f"Sabes que no puedes abrazar a los bots, {nombre}?.",
        f"Si ya se {nombre}, abrazar a los bots es lo mejor.",
        f"Te entiendo {nombre}, abrazar a los que no estan tambien es valido .",
        f"{nombre}, ¿estábas abrazando un amigo y se fue hantes ?",
        f"{nombre}, Este abrazo parece un poco solitario.",
        f"{nombre}, ¿estás practicando algun tipo de abrazo nuevo ?",
        f"¿A avanzado tanto la inteligencia artificial que ya abraza, {nombre}.?",
        f"Entiendo tu ansiedad, {nombre}, pero no puedes abrazar a los bots.",
        f"{nombre}, ¿estás abrazando a los bots otra vez?",
        f"Parece un abrazo de otra dimension, ya que {nombre} abraza de esa manera .",
        f"Que lindo abrazo a la nada misma, {nombre}.",
    ]
    
    return random.choice(MENSAJE_SIN_NOMBRE)


def me_abrazo(nombre: str) -> str:
    
    MENSAJE_EGOCENTRICO = [
        f"{nombre} se abraza a si mismo. ¡Que egocéntrico!",
        f"Parece que {nombre}, disfruta de su propia compañia.",
        f"{nombre} Se da amor a si mismo con un abrazo.",
        f"UUUy, {nombre} se abraza a si mismo. ¡Que tierno!",
        f"Nececitas un abrazo{nombre}, aqui estamos.",
        f"Parece que {nombre} se abraza a si mismo. ¡Eso esta bien!",
        f"Aqui estamos para darte un abrazo grupal {nombre}.",
        f"¡Que lindo {nombre}, abrazando a su propio ser!",
        f"¡Que lindo {nombre}, nos muestra como quererse !",
        f"A veces {nombre} es su propio mejor amigo.",
        f"Tu puedes {nombre}, pero no te abrazes tanto.",
        f"Darte un auto-abrazo es valido {nombre}.",
        f"Cuidado {nombre}, no te vayas a lastimar, con tanto abrazo.",
        f"Un poco de amor propio no le hace mal a nadie {nombre}.",
        f"Todo esta bien {nombre}?, estamos aqui para abrazarte fuerte.!!!",
        f"!Esta bien que te abrazes {nombre}, a veces uno necesita quererse mas para repartirlo luego.",
        f"Muy buen abrazo {nombre}, pero no te olvides de los demas.",
        f"{nombre}, a veces uno debe ser su propio heroe.",
        f"{nombre}, no te parece mucho envolverte con tus brazos y mirandote en el espejo?.",
        f"Bueno {nombre}, si te abrazas a ti mismo, nosotros te abrazamos a ti.",
        f"{nombre}, no te olvides de que nosotros tambien te queremos mucho.",
        f"{nombre}, recuerda que al abrazarte a ti mismo es una forma de procesar tus emociones.",    
        
    ]
    return random.choice(MENSAJE_EGOCENTRICO)

def abrazo_con_nombre(abrazador: str, abrazado: str) -> str:
    
    MENSAJE_CON_AMOR = [
        f"!Que lindo {abrazador} abraza a {abrazado}!",
        f"{abrazador} envuelve a {abrazado} en un calido abrazo.",
        f"Que lindo ver a {abrazador} abrazando com fuerza a {abrazado}.",
        f"Lo mejor de la vida es ver a {abrazador} abrazando a {abrazado}.",
        f"{abrazador} abraza a {abrazado} con todo su amor.",
        f"!Que lindo ver a {abrazador} usando su abrazo de oso con  {abrazado}!",
        f"Abrazo espontaneo de {abrazador} a {abrazado}.",
        f"De un salto {abrazador} abraza a {abrazado}.",
        f"Sorpresa {abrazado}, {abrazador} te abraza.",
        f"{abrazador} abraza a {abrazado} esto fue epico.",
        f"Todos atentos esto es un abrazo de {abrazador} a {abrazado}.",
        f"{abrazador} y {abrazado} que lindo se ven abrazados!!!.",
        f"Es un lindo abrazo de {abrazador} a {abrazado}.",
        f"{abrazador} es una maquina de abrazar a {abrazado} .",
        f"{abrazador} abraza a {abrazado} y los bots se paran para verlo.",
        f"Un abrazo de {abrazador} a {abrazado} es lo mejor que veras hoy.",
        f"Con ese abrazo {abrazador} a {abrazado} se siente mejor.",
        f"Desde lejos {abrazador} abraza a {abrazado}.",
        f"Desde la inmensidad del espacio {abrazador} abraza a {abrazado}.",
        f"Las estrellas se alinean para ver a {abrazador} abrazar a {abrazado}.",
        f"La luna se pone celosa de ver a {abrazador} abrazar a {abrazado}.",
        f"el sol brilla mas al ver a {abrazador} abrazar a {abrazado}.",
        f"El universo se expande al ver a {abrazador} abrazar a {abrazado}.",
        f"El tiempo se detiene para ver a {abrazador} abrazar a {abrazado}.",
        f"El espacio se curva para ver a {abrazador} abrazar a {abrazado}.",
        f"La tierra se detiene para ver a {abrazador} abrazar a {abrazado}.",
        f"El viento sopla mas fuerte al ver a {abrazador} abrazar a {abrazado}.",
        f"El agua se calma al ver a {abrazador} abrazar a {abrazado}.",
        f"El fuego se apaga al ver a {abrazador} abrazar a {abrazado}.",
        f"La tierra se mueve al ver a {abrazador} abrazar a {abrazado}.",
        f"El aire se purifica al ver a {abrazador} abrazar a {abrazado}.",
        f"El fuego se enciende al ver a {abrazador} abrazar a {abrazado}.",
        f"El agua se agita al ver a {abrazador} abrazar a {abrazado}.",
        f"El viento se calma al ver a {abrazador} abrazar a {abrazado}.",
        f'Entre mate y mate {abrazador} abraza a {abrazado}.',
        f'Entre asado y asado {abrazador} abraza a {abrazado}.',
        f'Entre empanada y empanada {abrazador} abraza a {abrazado}.',
        f'Entre fernet y fernet {abrazador} abraza a {abrazado}.',
        f'Entre vino y vino {abrazador} abraza a {abrazado}.',
        f'Entre cerveza y cerveza {abrazador} abraza a {abrazado}.',
        f"El mejor inpulso de {abrazador} es abrazar a {abrazado}.",
        f"La mejor medicina de {abrazador} es abrazar a {abrazado}.",
        f"La mejor terapia de {abrazador} es abrazar a {abrazado}.",
        f"La mejor forma de decir te quiero de {abrazador} es abrazar a {abrazado}.",
        f"La mejor forma de decir gracias de {abrazador} es abrazar a {abrazado}.",
        f"La mejor forma de decir lo siento de {abrazador} es abrazar a {abrazado}.",
        f"{abrazador} te abraza {abrazado} ya no estas solo !!!.",
        f"No te pierdas el abrazo de {abrazador} a {abrazado}.",
        f"Corta con tanta dulzura!!! {abrazador} abraza a {abrazado}.",
        f"El abrazo de {abrazador} a {abrazado} es unico.",
        f"El abrazo de {abrazador} a {abrazado} es magico.",
        f"Ese abrazo que te quiebra las costillas de {abrazador} a {abrazado}.",
        f"El abrazo de {abrazador} a {abrazado} es de otro mundo.",
               
    ]
    return random.choice(MENSAJE_CON_AMOR)