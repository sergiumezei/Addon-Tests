#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Bebe <florin.strugariu@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alin Trif <alin.trif@softvision.ro>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from unittestzero import Assert
from addons_homepage import AddonsHomePage
import pytest


class TestHomePage:

    def test_that_verifies_the_tooltip_for_Other_Applications(self, mozwebqa):
        """
        Litmus 22925
        https://litmus.mozilla.org/show_test.cgi?id=22925
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        Assert.equal(amo_home_page.header.other_applications_tooltip, 'Find add-ons for other applications')

    def test_that_checks_the_most_popular_section_exists(self, mozwebqa):
        """
        Litmus 25807
        https://litmus.mozilla.org/show_test.cgi?id=25807
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        Assert.true(amo_home_page.is_most_popular_list_visible)
        Assert.contains('Most Popular', amo_home_page.most_popular_list_heading)
        Assert.equal(amo_home_page.most_popular_count, 10)

    def test_that_checks_the_tooltip_for_amo_logo(self, mozwebqa):
        """
        Litmus 22924
        https://litmus.mozilla.org/show_test.cgi?id=22924
        """
        amo_home_page = AddonsHomePage(mozwebqa)
   #     Assert.true(amo_home_page.is_amo_logo_visible)
        Assert.equal(amo_home_page.amo_logo_title, "Return to the Firefox Add-ons homepage")
uyu
    def test_that_checks_the_image_for_amo_logo(self, mozwebqa):
        """
        Litmus 25742
        https://litmus.mozilla.org/show_test.cgi?id=25742
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        Assert.true(amo_home_page.is_amo_logo_image_visible)
        Assert.contains("-cdn.allizom.org/media/img/app-icons/med/firefox.png", amo_home_page.amo_logo_image_source)

    def test_that_clicking_mozilla_logo_loads_mozilla_dot_org(self, mozwebqa):
        """
        Litmus 22922
        https://litmus.mozilla.org/show_test.cgi?id=22922
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        Assert.true(amo_home_page.is_mozilla_logo_visible)
        amo_home_page.click_mozilla_logo()
        Assert.equal(amo_home_page.get_url_current_page(), "http://www.mozilla.org/")

    def test_that_clicking_on_addon_name_loads_details_page(self, mozwebqa):
        """ Litmus 25812
            https://litmus.mozilla.org/show_test.cgi?id=25812"""
        amo_home_page = AddonsHomePage(mozwebqa)
        amo_details_page = amo_home_page.click_on_first_addon()
        Assert.true(amo_details_page.is_the_current_page)

    def test_that_featured_personas_exist_on_the_homepage(self, mozwebqa):
        '''
        Litmus29698
        https://litmus.mozilla.org/show_test.cgi?id=29698
        '''
        amo_home_page = AddonsHomePage(mozwebqa)

        Assert.true(amo_home_page.is_featured_personas_visible, "Featured Personas region is not visible")
        Assert.equal(amo_home_page.fetaured_personas_title, u"Featured Personas See all \xbb", "Featured Personas region title doesn't match")

        Assert.equal(amo_home_page.featured_personas_count, 6)

    def test_that_clicking_see_all_personas_link_works(self, mozwebqa):
        """
        Litmus 29699
        https://litmus.mozilla.org/show_test.cgi?id=29699
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        featured_persona_page = amo_home_page.click_featured_personas_see_all_link()

        Assert.true(featured_persona_page.is_the_current_page)
        Assert.equal(featured_persona_page.persona_header, 'Personas')

    def test_that_other_applications_link_has_tooltip(self, mozwebqa):
        """ Litmus 22925
            https://litmus.mozilla.org/show_test.cgi?id=29698 """
        amo_home_page = AddonsHomePage(mozwebqa)
        tooltip = amo_home_page.get_title_of_link('Other applications')
        Assert.equal(tooltip, 'Find add-ons for other applications')

    def test_that_extensions_link_loads_extensions_page(self, mozwebqa):
        """
        Litmus 25746
        https://litmus.mozilla.org/show_test.cgi?searchType=by_id&id=25746
        """
        amo_home_page = AddonsHomePage(mozwebqa)
        extensions_page = amo_home_page.click_extensions()
        Assert.true(extensions_page.is_the_current_page)
