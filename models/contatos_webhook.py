# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json

class ContatosWebhook(models.Model):
    _name = 'x_contatos_webhook'   # Nome do modelo no Odoo
    _description = 'Contatos Recebidos por Webhook' # Descrição do modelo

    # Colunas da Tabela (Campos do modelo)
    name = fields.Char(string='Nome', required=True)   # Campo de texto para o nome do contato
    whatsapp = fields.Char(string='WhatsApp')            # Campo de texto para o número de WhatsApp
    email = fields.Char(string='E-mail')              # Campo de texto para o endereço de email
    use_default_text = fields.Boolean(string='Texto Padrão') # Checkbox para usar o texto padrão
    custom_text = fields.Text(string='Texto Personalizado') # Campo de texto para o texto personalizado
    status = fields.Selection([                       # Campo de seleção para o status do envio
        ('not_sent', 'Não Utilizado'),
        ('sent', 'Utilizado'),
    ], string='Status de Envio', default='not_sent', readonly=True)
    
    resend = fields.Boolean(string='Reenviar', default=False) # Checkbox para reenviar

    # Relacionamento com res.partner
    partner_id = fields.Many2one('res.partner', string='Contato', ondelete='set null') # Campo Many2one para relacionar com res.partner

     # Campo Computado para usar texto padrão
    @api.depends('use_default_text') # Define que o campo depende do use_default_text
    def _compute_default_text(self): # Função para definir o valor do campo default_text
        for record in self: # Percorre todos os registros
             if record.use_default_text: # Verifica se a checkbox está marcada
                 record.default_text = self.env['ir.config_parameter'].sudo().get_param('x_contatos_webhook.default_text', default='') # Busca texto padrão da configuração
             else:
                 record.default_text = False # Se a checkbox não estiver marcada, o valor é falso

    default_text = fields.Text(string='Texto Padrão', compute='_compute_default_text', store=False) # Campo computado do texto padrão

    # Campo Computado para Concatenar Textos
    @api.depends('use_default_text','default_text','custom_text') # Define que o campo depende do use_default_text, default_text e custom_text
    def _compute_combined_text(self): # Função para concatenar os textos
        for record in self: # Percorre todos os registros
            combined_text = "" # Cria uma string vazia
            if record.use_default_text and record.default_text:  # Verifica se a checkbox está marcada e se o texto padrão existe
                combined_text += record.default_text # Adiciona o texto padrão
            if record.custom_text: # Verifica se existe texto personalizado
                 if combined_text: # Verifica se existe algum texto anterior
                    combined_text +="\n" # Adiciona uma quebra de linha
                 combined_text += record.custom_text # Adiciona texto personalizado
            record.combined_text = combined_text # Define o texto concatenado no campo

    combined_text = fields.Text(string='Texto Combinado', compute='_compute_combined_text', store=False) # Campo computado para o texto combinado

    
    def mark_as_sent(self): # Função para marcar o status como enviado
        for record in self: # Percorre todos os registros
            record.status = 'sent'  # Define o status como 'enviado'

    def mark_as_not_sent(self):  # Função para marcar o status como não enviado
        for record in self: # Percorre todos os registros
            record.status = 'not_sent' # Define o status como 'não enviado'

    def reset_status(self): # Função para resetar o status do envio
        for record in self: # Percorre todos os registros
            record.status = 'not_sent' # Define o status como 'não enviado'
            record.resend = False # Define a checkbox reenviar como falso
            
    # Campo que armazena o texto enviado
    sent_text = fields.Text(string="Texto Enviado") # Campo para armazenar o texto enviado
    
    # Método para enviar via webhook
    def send_webhook(self): # Método para enviar os dados para o webhook
        # colocar aqui código para enviar para webhook
        return True
    
    # Método para carregar dados do webhook
    def load_webhook_data(self):
        url = self.env['ir.config_parameter'].sudo().get_param('x_contatos_webhook.webhook_url') # Pega a URL do webhook das configurações
        if url: # Verifica se existe URL
          response = requests.get(url) # Faz a requisição para o webhook
          if response.status_code == 200: # Verifica se a requisição foi bem sucedida
             data = json.loads(response.text) # Converte o texto JSON para um objeto Python
             if isinstance(data, list):  # Verifica se o objeto é uma lista
                for item in data: # Percorre todos os itens
                    name = item.get('name')  # Pega o valor do nome
                    whatsapp = item.get('whatsapp') # Pega o valor do whatsapp
                    email = item.get('email') # Pega o valor do email

                    if name: # Se existir o nome
                         self.create({   # Cria os dados no modelo
                            'name': name,  
                            'whatsapp': whatsapp,
                            'email': email
                         })
          else: # Se a requisição não foi bem sucedida
             raise Exception(f'Erro ao buscar dados do webhook: {response.status_code}') # Mostra um erro

        else: # Se não existe a URL do webhook
            raise Exception('URL do Webhook não configurada!') # Mostra um erro

class ResConfigSettings(models.TransientModel): # Classe para herdar o modelo de configurações
    _inherit = 'res.config.settings'  # Define qual modelo iremos herdar

    default_text = fields.Text(string="Texto Padrão", config_parameter='x_contatos_webhook.default_text')  # Campo de configuração para o texto padrão
    default_text_2 = fields.Text(string="Texto Padrão 2", config_parameter='x_contatos_webhook.default_text_2') # Campo de configuração para o texto padrão 2
    default_text_3 = fields.Text(string="Texto Padrão 3", config_parameter='x_contatos_webhook.default_text_3') # Campo de configuração para o texto padrão 3
    default_text_4 = fields.Text(string="Texto Padrão 4", config_parameter='x_contatos_webhook.default_text_4')  # Campo de configuração para o texto padrão 4
    use_default_text_2 = fields.Boolean(string="Usar Texto Padrão 2", config_parameter='x_contatos_webhook.use_default_text_2') # Campo de configuração para usar o texto padrão 2
    use_default_text_3 = fields.Boolean(string="Usar Texto Padrão 3", config_parameter='x_contatos_webhook.use_default_text_3')# Campo de configuração para usar o texto padrão 3
    use_default_text_4 = fields.Boolean(string="Usar Texto Padrão 4", config_parameter='x_contatos_webhook.use_default_text_4') # Campo de configuração para usar o texto padrão 4
    webhook_url = fields.Char(string="URL do Webhook", config_parameter='x_contatos_webhook.webhook_url') # Campo de configuração para a URL do webhook