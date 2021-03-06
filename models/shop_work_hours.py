# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class eyecraft_work_days(models.Model):
    _name = "eyecraft.work.days"
    _description = "Shops Work Hours"

    name = fields.Char("Work days")


class paeriod_of_time(models.Model):
    _name = "period.of.time"
    _description = "Period of Time"


    _sql_constraints = [
        (
            'start_end_time_check',
            'check (start_time<end_time)',
            'End of period can\'t be less than or equal to start of period!'
        ),
    ]

    @api.multi
    @api.depends('start_time', 'end_time')
    def _compute_name(self):
        for period in self:
            period.name = "{start} - {end}".format(
                start=('%.2f' % self.start_time).replace('.', ':'),
                end=('%.2f' % self.end_time).replace('.', ':'),
            )

    name = fields.Char("Period of Time", compute="_compute_name", store=True)
    start_time = fields.Float("Since", required=True)
    end_time = fields.Float("To", required=True)


class shop_work_hours(models.Model):
    _name = "shop.work.hours"
    _description = "Shops Work Hours"

    name = fields.Char("Name")
    work_days_id = fields.Many2one(
        "eyecraft.work.days",
        "Week days",
        help="Period of week in which the shop works in set hours",
	reqiured=True,
    )
    period_ids = fields.Many2many(
        "period.of.time",
        "work_hours_periods_rel",
        "work_hours_id",
        "period_id",
        "Periods of Time",
	required=True,
    )
    shop_id = fields.Many2one(
        "eyekraft.shop",
        "Shop",
    )
