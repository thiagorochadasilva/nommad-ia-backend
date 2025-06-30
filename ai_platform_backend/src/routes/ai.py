from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import requests
import os
import json

ai_bp = Blueprint('ai', __name__)

# Configuração da API Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-api-key-here')
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

# Armazenamento em memória para conversas (em produção, usar banco de dados)
conversations = {}

@ai_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """
    Endpoint para processar mensagens de chat com a IA
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Mensagem não pode estar vazia'}), 400
        
        # Inicializar conversa se não existir
        if user_id not in conversations:
            conversations[user_id] = []
        
        # Adicionar mensagem do usuário ao histórico
        conversations[user_id].append({
            'role': 'user',
            'content': user_message
        })
        
        # Preparar payload para a API Gemini
        payload = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': user_message
                        }
                    ]
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Fazer requisição para a API Gemini
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            gemini_response = response.json()
            
            # Extrair resposta da IA
            if 'candidates' in gemini_response and len(gemini_response['candidates']) > 0:
                ai_message = gemini_response['candidates'][0]['content']['parts'][0]['text']
                
                # Adicionar resposta da IA ao histórico
                conversations[user_id].append({
                    'role': 'model',
                    'content': ai_message
                })
                
                return jsonify({
                    'response': ai_message,
                    'user_id': user_id,
                    'status': 'success'
                })
            else:
                return jsonify({'error': 'Resposta inválida da API Gemini'}), 500
        else:
            error_message = f"Erro na API Gemini: {response.status_code}"
            if response.text:
                error_message += f" - {response.text}"
            return jsonify({'error': error_message}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Timeout na requisição para a API Gemini'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro de conexão: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@ai_bp.route('/conversation/<user_id>', methods=['GET'])
@cross_origin()
def get_conversation(user_id):
    """
    Endpoint para obter o histórico de conversa de um usuário
    """
    try:
        conversation = conversations.get(user_id, [])
        return jsonify({
            'user_id': user_id,
            'conversation': conversation,
            'message_count': len(conversation)
        })
    except Exception as e:
        return jsonify({'error': f'Erro ao obter conversa: {str(e)}'}), 500

@ai_bp.route('/conversation/<user_id>', methods=['DELETE'])
@cross_origin()
def clear_conversation(user_id):
    """
    Endpoint para limpar o histórico de conversa de um usuário
    """
    try:
        if user_id in conversations:
            del conversations[user_id]
        
        return jsonify({
            'message': f'Conversa do usuário {user_id} foi limpa',
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': f'Erro ao limpar conversa: {str(e)}'}), 500

@ai_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    """
    Endpoint para verificar se o serviço está funcionando
    """
    return jsonify({
        'status': 'healthy',
        'service': 'AI Platform Backend',
        'version': '1.0.0'
    })

