# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function, unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from fluo.db import models


class ServiceNotFound(Exception):
    pass


class ServiceQuerySet(models.QuerySet):
    def default(self):
        return self.get(default=True)


class ServiceManager(models.Manager.from_queryset(ServiceQuerySet)):
    use_for_related_fields = True


@python_2_unicode_compatible
class Service(models.StatusModel, models.OrderedModel):
    objects = ServiceManager()

    name = models.CharField(
        unique=True,
        max_length=255,
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        editable=False,
        verbose_name=_("slug"),
        help_text=('A "slug" is a unique URL-friendly title for the object automatically generated from the "name" field.'),
    )
    default = models.BooleanField(
        default=False,
        verbose_name=_("default"),
        help_text=_("Is the default one?"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Service, self).save(*args, **kwargs)
        if self.default:
            for c in self._default_manager.exclude(pk=self.id):
                c.default = False
                c.save(*args, **kwargs)
        try:
            c = self._default_manager.get(default=True)
        except models.ObjectDoesNotExist:
            self.default = True
            super(Service, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Email(models.Model):
    service = models.ForeignKey(
        Service,
        related_name="emails",
        verbose_name=_("service"),
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("name"),
    )
    email = models.EmailField(
        max_length=255,
        verbose_name=_("email"),
    )

    class Meta:
        unique_together = [("service", "email")]
        verbose_name = _("Service email")
        verbose_name_plural = _("Service email")

    def __str__(self):
        return _("Email for {name}: {email}").format(
            name=self.service.name,
            email=self.email,
        )

