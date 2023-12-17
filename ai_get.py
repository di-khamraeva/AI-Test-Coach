import g4f
from g4f.Provider import (
    Poe,
    You,
    GptGo,
    Bing,
    Aichat
)
def ai_savol(savol=str):
    '''
    savol=>str
    savol bo'yicha javobni generatsiya qiladi
    '''
    promt = f"ответь на русском. обясни {savol} коротко и ясно"
    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": promt}],
        stream=True,
    )
    msg=""
    for message in response:
        msg+=message
    return msg

