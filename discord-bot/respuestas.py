import random
import opciones



def handle_response(msg) -> str:
    p_msg = msg.lower()

    if p_msg in opciones.lista_holas:
        return opciones.resp_holas[random.randint(0, len(opciones.resp_holas)-1)]
    
    if p_msg in opciones.lista_4:
        return opciones.resp_te_puse[random.randint(0, len(opciones.resp_te_puse)-1)]
    
    if p_msg in opciones.lista_ayudas:
        return opciones.resp_ayudas[random.randint(0, len(opciones.resp_ayudas)-1)]
    
    else:
        print('Mensaje fuera de mis opciones')