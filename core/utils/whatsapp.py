"""
Utilitário para envio de mensagens via WhatsApp.
"""

import pywhatkit
import datetime
import time
import logging
from django.conf import settings

# Configurar logging
logger = logging.getLogger(__name__)

def enviar_mensagem_whatsapp(numero_telefone, mensagem, aguardar_segundos=15, fechar_apos_segundos=10):
    """
    Envia uma mensagem via WhatsApp Web usando a biblioteca pywhatkit.
    
    Args:
        numero_telefone (str): Número de telefone do destinatário (formato: +5511999999999)
        mensagem (str): Conteúdo da mensagem a ser enviada
        aguardar_segundos (int): Tempo de espera para carregar o WhatsApp Web
        fechar_apos_segundos (int): Tempo de espera após enviar a mensagem
        
    Returns:
        bool: True se a mensagem foi enviada com sucesso, False caso contrário
    """
    try:
        # Formatar o número de telefone (remover caracteres não numéricos)
        numero_formatado = ''.join(filter(str.isdigit, numero_telefone))
        
        # Adicionar código do país se não estiver presente
        if len(numero_formatado) <= 11:  # DDD + número sem o código do país
            numero_formatado = '+55' + numero_formatado
        elif not numero_formatado.startswith('+'):
            numero_formatado = '+' + numero_formatado
            
        # Obter hora atual
        agora = datetime.datetime.now()
        
        # Enviar mensagem
        pywhatkit.sendwhatmsg(
            numero_formatado,
            mensagem,
            agora.hour,
            agora.minute + 1,  # Enviar no próximo minuto
            wait_time=aguardar_segundos,
            tab_close=True,
            close_time=fechar_apos_segundos
        )
        
        logger.info(f"Mensagem enviada com sucesso para {numero_formatado}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem via WhatsApp: {str(e)}")
        return False


def enviar_mensagem_em_lote(lista_destinatarios, mensagem_template, personalizar_func=None):
    """
    Envia mensagens em lote para uma lista de destinatários.
    
    Args:
        lista_destinatarios (list): Lista de objetos com atributo 'telefone'
        mensagem_template (str): Template da mensagem a ser enviada
        personalizar_func (callable, optional): Função para personalizar a mensagem para cada destinatário
        
    Returns:
        dict: Dicionário com resultados do envio (sucesso, falha, total)
    """
    resultados = {
        'sucesso': 0,
        'falha': 0,
        'total': len(lista_destinatarios)
    }
    
    for destinatario in lista_destinatarios:
        try:
            # Personalizar mensagem se a função for fornecida
            if personalizar_func:
                mensagem = personalizar_func(destinatario, mensagem_template)
            else:
                mensagem = mensagem_template
                
            # Enviar mensagem
            sucesso = enviar_mensagem_whatsapp(destinatario.telefone, mensagem)
            
            if sucesso:
                resultados['sucesso'] += 1
            else:
                resultados['falha'] += 1
                
            # Aguardar um pouco entre os envios para evitar bloqueios
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Erro ao processar destinatário {destinatario}: {str(e)}")
            resultados['falha'] += 1
    
    return resultados
