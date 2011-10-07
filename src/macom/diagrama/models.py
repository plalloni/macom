# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink

class Base(models.Model):
    @permalink
    def get_absolute_url(self):
        return ('admin:%s_%s_change' %(self._meta.app_label, self._meta.module_name), [self.id])
    class Meta:
        abstract = True
        db_tablespace = 'macom'

class System(Base):
    name = models.CharField(_('name'), help_text=_('system-name-help'), max_length=100)
    description = models.TextField(_('description'), help_text=_('description-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    external = models.BooleanField(_('external'), help_text=_('external-help'))
    class Meta:
        verbose_name = _('system')
        ordering = ['name']
    def __unicode__(self):
        return self.name

class Module(Base):
    CRITICITY = (
        (u'H', _('high')),
        (u'M', _('medium')),
        (u'L', _('low')),
    )
    system = models.ForeignKey('System', verbose_name=_('system'), null=True)
    name = models.CharField(_('name'), help_text=_('module-name-help'), max_length=100)
    goal = models.TextField(_('goal'), help_text=_('module-goal-help'))
    external = models.BooleanField(_('external'), help_text=_('external-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    criticity = models.CharField(_('criticity'), help_text=_('criticity-help'), max_length=2, choices=CRITICITY)
    dependencies = models.ManyToManyField('Interface', through='Dependency', related_name='dependencies')
    class Meta:
        verbose_name = _('module')
        ordering = ['system__name']
    def __unicode__(self):
        return "%s:%s" % (unicode(self.system), self.name)

class Interface(Base):
    name = models.CharField(_('name'), help_text=_('interface-name-help'), max_length=100)
    goal = models.TextField(_('goal'), help_text=_('interface-goal-help') )
    technology = models.CharField(_('technology'), help_text=_('technology-help') , max_length=200, blank=True)
    referents = models.TextField(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    direction_inbound = models.BooleanField(_('Inbound'), help_text=_('interface-inbound-help'))
    direction_outbound = models.BooleanField(_('Outbound'), help_text=_('interface-outbound-help'))
    module = models.ForeignKey(Module, verbose_name = _('module'))
    class Meta:
        verbose_name = _('interface')
        verbose_name_plural = _('interfaces')
        ordering = ['module__system__name']
    def __unicode__(self):
        return "%s:%s" % (unicode(self.module), self.name)

class Dependency(Base):
    module = models.ForeignKey(Module, verbose_name = _('module'))
    interface = models.ForeignKey(Interface, verbose_name = _('interface'))
    goal = models.TextField(_('goal'), help_text=_('dependency-goal-help') , blank=True)
    direction_inbound = models.BooleanField(_('Inbound'), help_text=_('dependency-inbound-help'))
    direction_outbound = models.BooleanField(_('Outbound'), help_text=_('dependency-outbound-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help') , blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help') , blank=True)
    technology = models.CharField(_('technology'), help_text=_('technology-help') , max_length=200, blank=True)
    loadestimate = models.CharField(_('loadestimate'), help_text=_('loadestimate-help') , max_length=200, blank=True)
    class Meta:
        verbose_name = _('dependency')
        verbose_name_plural = _('dependencies')
        ordering = ['module__system__name']
    def __unicode__(self):
        return "%s:(%s)" % (unicode(self.module), unicode(self.interface))
