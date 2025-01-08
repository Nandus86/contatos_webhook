# -*- coding: utf-8 -*-
from odoo import models, fields
class WebhookConfig(models.Model):
    _name = 'contatos_webhook.config'
    _description = 'Configurações do Webhook'

    text = fields.Char(string='Texto Padrão')
    text_2 = fields.Char(string='Texto Padrão 2')
    text_3 = fields.Char(string='Texto Padrão 3')
    text_4 = fields.Char(string='Texto Padrão 4')
    use_text_2 = fields.Boolean(string='Usar Texto 2')
    use_text_3 = fields.Boolean(string='Usar Texto 3')
    use_text_4 = fields.Boolean(string='Usar Texto 4')
    webhook_url = fields.Char(string='URL do Webhook')