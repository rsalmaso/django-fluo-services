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
from django.test import TestCase
from .models import ServiceNotFound, Service, Email
from . import get_service_emails


class ServiceTest(TestCase):
    def setUp(self):
        self.service1 = Service.objects.create(
            name="default",
            slug="default",
            status="active",
            ordering=2,
            default=True,
        )
        self.service2 = Service.objects.create(
            name="contacts",
            slug="contacts",
            status="active",
            ordering=1,
            default=False,
        )
        self.service3 = Service.objects.create(
            name="registration",
            slug="registration",
            status="active",
            ordering=3,
            default=False,
        )
        Email.objects.create(
            service=self.service1,
            email="info@example.com",
        )
        Email.objects.create(
            service=self.service2,
            email="contacts@example.com",
        )
        Email.objects.create(
            service=self.service3,
            email="registration@example.com",
        )

    def test_create_a_new_service(self):
        TEST_EMAILS = [
            "test-1@example.com",
            "test-2@example.com",
            "test-3@example.com",
            "test-4@example.com",
        ]

        self.assertEquals(3, Service.objects.all().count())
        service = Service(
            name="test",
        )
        service.save()
        for email in TEST_EMAILS:
            mail = Email(
                service=service,
                email=email,
            )
            mail.save()
        emails = get_service_emails("test")
        emails.sort()
        self.assertEquals(emails, TEST_EMAILS)

    def test_get_service_emails_should_returns_a_list_of_emails(self):
        self.assertEquals(3, Service.objects.all().count())
        emails = get_service_emails("contacts")
        self.assertEquals(emails, ["contacts@example.com"])

    def test_get_service_email_with_no_arguments_must_returns_the_defautl_service(self):
        emails = get_service_emails()
        self.assertEquals(emails, ["info@example.com"])

    def test_get_service_email_with_contacts_argument_must_returns_the_contacts_service_emails(self):
        emails = get_service_emails("contacts")
        self.assertEquals(emails, ["contacts@example.com"])

    def test_get_service_email_with_invalid_service_name_must_raise_an_exception(self):
        with self.assertRaises(ServiceNotFound):
            get_service_emails("unknown")
