# -*- coding: utf-8 -*-
from odoo import models, fields


class WebhookConfig(models.Model):
    _name = 'contatos_webhook.config'
    _description = 'Configurações do Webhook'

    name = fields.Char()  # Campo obrigatório para modelo base