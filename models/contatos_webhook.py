# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import json
import random

class ContatosWebhook(models.Model):
    _name = 'contatos.webhook'
    _description = 'Contatos Webhook'
    _order = 'status,create_date desc'
    _module = 'contatos_webhook'

    selected = fields.Boolean(string='Selecionado')
    name = fields.Char(string='Nome', required=True)
    whatsapp = fields.Char(string='WhatsApp')
    email = fields.Char(string='E-mail')
    use_default_text = fields.Boolean(string='Usar Texto Padrão')
    custom_text = fields.Text(string='Texto Personalizado')
    sent_text = fields.Text(string='Texto Enviado', readonly=True)
    status = fields.Selection([
        ('not_sent', 'Não Utilizado'),
        ('sent', 'Utilizado')
    ], string='Status', default='not_sent', readonly=True)
    resend = fields.Boolean(string='Reenviar')
    partner_id = fields.Many2one('res.partner', string='Contato')
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.name
            self.whatsapp = self.partner_id.mobile or self.partner_id.phone
            self.email = self.partner_id.email

    def action_send_selected(self):
        selected_records = self.search([('selected', '=', True), ('status', '=', 'not_sent')])
        for record in selected_records:
            if self._send_webhook(record):
                record.write({
                    'status': 'sent',
                    'sent_text': self._send_webhook(record),
                    'selected': False
            })


    def action_send_single(self):
        self.ensure_one()
        if self._send_webhook(self):
            self.write({
                'status': 'sent',
                'sent_text': self._send_webhook(self),
                'selected': False
            })

    def action_delete_selected(self):
        self.search([('selected', '=', True)]).unlink()

    def action_delete_single(self):
        self.ensure_one()
        self.unlink()

    def action_resend(self):
        self.ensure_one()
        self.write({
            'status': 'not_sent',
            'sent_text': False,
            'resend': False
        })

    def _send_webhook(self, record):
        webhook_url = self.env['ir.config_parameter'].sudo().get_param('contatos_webhook.webhook_url')
        if not webhook_url:
            raise UserError('URL do webhook não configurada!')
        
        config = self.env['ir.config_parameter'].sudo()
        final_text = "default"
        if record.use_default_text:
            texts = []
            default_text = config.get_param('contatos_webhook.default_text')
            if default_text:
                texts.append(default_text)
            for i in range(2, 5):
                if config.get_param(f'contatos_webhook.use_default_text_{i}'):
                    text = config.get_param(f'contatos_webhook.default_text_{i}')
                    if text:
                        texts.append(text)
            if texts:
                final_text = random.choice(texts)
        if record.custom_text:
            if final_text:
                final_text += "\n"
            final_text += record.custom_text

        data = {
            'name': record.name,
            'whatsapp': record.whatsapp,
            'email': record.email,
            'text': final_text
        }

        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()
            return True
        except Exception as e:
            raise UserError(f'Erro ao enviar webhook: {str(e)}')

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