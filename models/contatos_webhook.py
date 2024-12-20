# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
import json

class ContatosWebhook(models.Model):
    _name = 'x_contatos_webhook'
    _description = 'Contatos Recebidos por Webhook'
    _module = 'contatos_webhook'

    # Colunas da Tabela
    name = fields.Char(string='Nome', required=True)
    whatsapp = fields.Char(string='WhatsApp')
    email = fields.Char(string='E-mail')
    use_default_text = fields.Boolean(string='Texto Padrão')
    custom_text = fields.Text(string='Texto Personalizado')
    status = fields.Selection([
        ('not_sent', 'Não Utilizado'),
        ('sent', 'Utilizado'),
    ], string='Status de Envio', default='not_sent', readonly=True)
    
    resend = fields.Boolean(string='Reenviar', default=False)
    
    # Relacionamento com res.partner
    partner_id = fields.Many2one('res.partner', string='Contato', ondelete='set null')
    
    # Campo Computado para usar texto padrão
    @api.depends('use_default_text')
    def _compute_default_text(self):
        for record in self:
             if record.use_default_text:
                 record.default_text = self.env['ir.config_parameter'].sudo().get_param('x_contatos_webhook.default_text', default='')
             else:
                 record.default_text = False

    default_text = fields.Text(string='Texto Padrão', compute='_compute_default_text', store=False)


    # Campo Computado para Concatenar Textos
    @api.depends('use_default_text','default_text','custom_text')
    def _compute_combined_text(self):
        for record in self:
            combined_text = ""
            if record.use_default_text and record.default_text:
                combined_text += record.default_text
            if record.custom_text:
                 if combined_text:
                    combined_text +="\n"
                 combined_text += record.custom_text
            record.combined_text = combined_text

    combined_text = fields.Text(string='Texto Combinado', compute='_compute_combined_text', store=False)

    
    def mark_as_sent(self):
        for record in self:
            record.status = 'sent'

    def mark_as_not_sent(self):
        for record in self:
            record.status = 'not_sent'

    def reset_status(self):
        for record in self:
            record.status = 'not_sent'
            record.resend = False
            
    # Campo que armazena o texto enviado
    sent_text = fields.Text(string="Texto Enviado")
    
    # Método para enviar via webhook
    def send_webhook(self):
        # colocar aqui código para enviar para webhook
        return True

    # Método para carregar dados do webhook
    def load_webhook_data(self):
        url = self.env['ir.config_parameter'].sudo().get_param('x_contatos_webhook.webhook_url')
        if url:
          response = requests.get(url)
          if response.status_code == 200:
             data = json.loads(response.text)
             if isinstance(data, list):
                for item in data:
                    name = item.get('name')
                    whatsapp = item.get('whatsapp')
                    email = item.get('email')

                    if name:
                         self.create({
                            'name': name,
                            'whatsapp': whatsapp,
                            'email': email
                         })
          else:
             raise Exception(f'Erro ao buscar dados do webhook: {response.status_code}')

        else:
            raise Exception('URL do Webhook não configurada!')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_text = fields.Text(string="Texto Padrão", config_parameter='contatos_webhook.default_text')
    default_text_2 = fields.Text(string="Texto Padrão 2", config_parameter='contatos_webhook.default_text_2')
    default_text_3 = fields.Text(string="Texto Padrão 3", config_parameter='contatos_webhook.default_text_3')
    default_text_4 = fields.Text(string="Texto Padrão 4", config_parameter='contatos_webhook.default_text_4')
    use_default_text_2 = fields.Boolean(string="Usar Texto Padrão 2", config_parameter='contatos_webhook.use_default_text_2')
    use_default_text_3 = fields.Boolean(string="Usar Texto Padrão 3", config_parameter='contatos_webhook.use_default_text_3')
    use_default_text_4 = fields.Boolean(string="Usar Texto Padrão 4", config_parameter='contatos_webhook.use_default_text_4')
    webhook_url = fields.Char(string="URL do Webhook", config_parameter='contatos_webhook.webhook_url')