"""
Test suite for the volunteers module.
"""

import unittest
from django.test import TestCase
from django.contrib.auth.models import User


class VolunteerTest(TestCase):
    fixtures = ["test_users.json"]

    def testLogin(self):
        c = self.client
        self.failUnlessEqual(c.login(username="conman", password=""), False)
        self.failUnlessEqual(c.login(username="jdoe", password=""), False)
        self.failUnlessEqual(c.login(username="conman", password="utos"), True)
        self.failUnlessEqual(c.login(username="jdoe", password="utos"), True)

    def testLoginRequired(self):
        response = self.client.get("/volunteer/")
        self.failIfEqual(response.status_code, 200)
        self.failUnlessEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/volunteer/")

        self.client.login(username="jdoe", password="utos")
        response = self.client.get("/volunteer/")
        self.client.logout()

        self.failIfEqual(response.status_code, 302)
        self.failUnlessEqual(response.status_code, 200)

    def testBasePage(self):
        self.client.login(username="jdoe", password="utos")
        response = self.client.get("/volunteer/")
        self.client.logout()
        self.assertContains(response, '<option value="1">Room Manager</option>')

