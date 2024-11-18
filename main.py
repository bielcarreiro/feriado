import google.generativeai as genai # GG Gemini
import speech_recognition as sr # Motor de reconhecimento de voz
import pyttsx3 # Transforma o Texto em Aúdio
import os # Ninguém se importa
from dotenv import load_dotenv # Conecta minhas var com as API 
import datetime # Faz o L
import notícias # Importa o módulo criado da news
 

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API do arquivo .env
chave = os.getenv("GOOGLE_API_KEY")

# Configura a API Generative AI com a chave carregada
genai.configure(api_key=chave)

generation_config = {
    'candidate_count': 1,
    'temperature': 0.7,
}

# Configurações para gerar texto com o modelo Gemini 1.5 flash

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              generation_config=generation_config
                              )

# Carrega o modelo Gemini 1.0 Pro com as configurações definidas
chat = model.start_chat(history=[])


# Inicializa o mecanismo de sistese de voz.
motor_de_sistese_de_fala = pyttsx3.init()

# Obtém todas as vozes disponíveis no sistema
voices = motor_de_sistese_de_fala.getProperty('voices')

# Define a voz a ser usada pelo robô como a segunda voz
motor_de_sistese_de_fala.setProperty('voice', voices[0].id)


# Usa o motor de síntese de fala para falar
def falar(frase):
    motor_de_sistese_de_fala.say(frase)
    motor_de_sistese_de_fala.runAndWait()
    motor_de_sistese_de_fala.stop()


# Remove os caracteres especiais do texto gerado
def remover_caracteres_especiais(texto):
    texto_sem_asteriscos = ""
    for caractere in texto:
        if caractere not in "*!@$%&''-+.*/=+-_":
            texto_sem_asteriscos += caractere
    return texto_sem_asteriscos



# Define uma função para reconhecer a fala do usuário.
def reconhecer_fala():
    # Inicializa o reconhecedor de fala.
    microfone = sr.Recognizer()

    # Configura o microfone como fonte de áudio.
    with sr.Microphone() as source:
        # Ajusta o reconhecimento para o ruído ambiente.
        microfone.adjust_for_ambient_noise(source)
        # Escuta o áudio do microfone.
        audio = microfone.listen(source)

        # Tenta reconhecer a fala 5 vezes.

        for _ in range(5):
            try:
                # Reconhece a fala do usuário usando o Google Speech Recognition.
                frase_reconhecida = microfone.recognize_google(audio, language='pt')

                # Retorna a frase reconhecida.

                return frase_reconhecida

            except sr.UnknownValueError:
                falar('Desculpe, mas eu não entendi o que você disse.')
                break
            except sr.RequestError as e:
                falar(f'Ocorreu um erro ao reconhecer a fala: {e}')

    return None


# Saudação inicial
hora_atual = datetime.datetime.now().hour
if hora_atual < 12 and hora_atual > 6:
    falar('Bom dia Gabriel como eu posso te ajudar nessa manhã?')
elif 12 <= hora_atual < 18:
    falar('Boa tarde Gabriel como eu posso te ajudar nessa tarde?')
elif hora_atual == 0 and hora_atual < 6:
    falar('Como eu posso te ajudar nessa madrugada Gabriel?')
else:
    falar('Boa noite Gabriel como eu poderei te ajudar nessa noite')


# Loop principal da conversa
def iniciar_conversa():
    # Controla a primeira interação
    primeira_interação = True

    while True:
        # Reconhece a fala do usuário
        prompt = reconhecer_fala()
       
        if prompt and 'notícias' in prompt.lower():
            noticias_atualizadas = notícias.obter_noticias()
            falar(noticias_atualizadas)    
        
        # Verifica se o usuário quer encerrar
        if prompt and 'isso é tudo feriado' in prompt.lower():
            falar('Até mais, senhor.')
            break

        if prompt:
            # Gera a resposta com o modelo
            response = chat.send_message(prompt)

            # Fala a resposta ao usuário
            falar(remover_caracteres_especiais(response.text))

            if primeira_interação:
                # Atualiza para não repetir a mensagem na próxima interação
                primeira_interação = False
            else:
                # Exibe a mensagem "No que mais eu posso ajudar?" apenas após a primeira resposta
                falar('No que mais eu posso ajudar?')
        else:
            # Caso a entrada seja inválida ou não entendida
            falar('Por favor, repita. Não consegui entender.')


iniciar_conversa()