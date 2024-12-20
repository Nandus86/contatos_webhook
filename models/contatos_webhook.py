# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import requests

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
    text = fields.Text(string='Texto Final', compute='_compute_texts', store=True)
    text_2 = fields.Text(string='Texto Padrão 2', compute='_compute_texts', store=True)
    text_3 = fields.Text(string='Texto Padrão 3', compute='_compute_texts', store=True)
    text_4 = fields.Text(string='Texto Padrão 4', compute='_compute_texts', store=True)

    @api.depends('use_default_text', 'custom_text')
    def _compute_texts(self):
        for record in self:
            record.text = record.get_final_text()
            config = self.env['ir.config_parameter'].sudo()
            if config.get_param('contatos_webhook.use_default_text_2'):
                 record.text_2 = config.get_param('contatos_webhook.default_text_2', '')
            else:
                 record.text_2 = False
            if config.get_param('contatos_webhook.use_default_text_3'):
                 record.text_3 = config.get_param('contatos_webhook.default_text_3', '')
            else:
                 record.text_3 = False
            if config.get_param('contatos_webhook.use_default_text_4'):
                 record.text_4 = config.get_param('contatos_webhook.default_text_4', '')
            else:
                 record.text_4 = False


    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.name
            self.whatsapp = self.partner_id.mobile or self.partner_id.phone
            self.email = self.partner_id.email

    def action_send_selected(self):
        selected_records = self.search([('selected', '=', True), ('status', '=', 'not_sent')])
        for record in selected_records:
            record._send_webhook()
            record.write({
                'status': 'sent',
                'sent_text': record.get_final_text(),
                'selected': False
            })

    def action_send_single(self):
        self.ensure_one()
        if self._send_webhook():
            self.write({
                'status': 'sent',
                'sent_text': self.get_final_text(),
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

    def get_final_text(self):
        self.ensure_one()
        config = self.env['ir.config_parameter'].sudo()
        final_text = ""
        
        if self.use_default_text:
            default_text = config.get_param('contatos_webhook.default_text', '')
            final_text += default_text

            if config.get_param('contatos_webhook.use_default_text_2'):
                text2 = config.get_param('contatos_webhook.default_text_2', '')
                if text2:
                    final_text += "\n" + text2

            if config.get_param('contatos_webhook.use_default_text_3'):
                text3 = config.get_param('contatos_webhook.default_text_3', '')
                if text3:
                    final_text += "\n" + text3

            if config.get_param('contatos_webhook.use_default_text_4'):
                text4 = config.get_param('contatos_webhook.default_text_4', '')
                if text4:
                    final_text += "\n" + text4

        if self.custom_text:
            if final_text:
                final_text += "\n"
            final_text += self.custom_text

        return final_text

    def _send_webhook(self):
        webhook_url = self.env['ir.config_parameter'].sudo().get_param('contatos_webhook.webhook_url')
        if not webhook_url:
            raise UserError('URL do webhook não configurada!')

        data = {
            'name': self.name,
            'whatsapp': self.whatsapp,
            'email': self.email,
            'text': self.get_final_text()
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