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
#                 David Burns
#                 Marc George
#                 Dave Hunt <dhunt@mozilla.com>
#                 Alex Rodionov <p0deje@gmail.com>
#                 Joel Andersson <janderssn@gmail.com>
#                 Marlena Compton <mcompton@mozilla.com>
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alex Lakatos <alex@greensqr.com>
#                 Alin Trif <alin.trif@softvision.ro>
#                 Sergiu Mezei <sergiu.mezei@gmail.com>
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

from addons_base_page import AddonsBasePage
import re
from urllib2 import urlparse
from page import Page


class AddonsDetailsPage(AddonsBasePage):

    _breadcrumb_locator = "id=breadcrumbs"
    _current_page_breadcrumb_locator = "css=#breadcrumbs > ol > li:nth(2)"

    #addon informations
    _name_locator = "css=h1.addon"
    _version_number_locator = "css=span.version-number"
    _authors_locator = "//h4[@class='author']/a"
    _summary_locator = "id=addon-summary"
    _ratings_locator = "css=span[itemprop='rating']"
    _install_button_locator = "css=p[class='install-button'] > a"
    _contribute_button_locator = "css=a[id='contribute-button']"
    _addon_rating_locator = "css=span[itemprop='rating']"
    _whats_this_license_locator = "css=h5 > span > a"
    _description_locator = "css=div.prose"
    _register_link_locator = "css=li.account > a"
    _login_link_locator = "css=li.account > a:nth(1)"
    _other_applications_locator = "id=other-apps"
    _other_apps_dropdown_menu_locator = "css=ul.other-apps"

    _about_addon_locator = "css=section.primary > h2"
    _more_about_addon_locator = "id=more-about"
    _version_information_locator = "id=detail-relnotes"
    _version_information_heading_locator = "css=#detail-relnotes > h2"
    _release_version_locator = "css=div.version"
    _source_code_license_information_locator = "css=.source > li > a"
    _reviews_title_locator = "css=#reviews > h2"
    _tags_locator = "id=tagbox"
    _other_addons_header_locator = "css=h2.compact-bottom"
    _other_addons_list_locator = "css=.primary .listing-grid"
    _part_of_collections_locator = "css=#collections-grid"
    _icon_locator = "css=img.icon"
    _featured_image_locator = "css=#addon .featured .screenshot"
    _support_link_locator = "css=a.support"
    _review_details_locator = "css=.review .description"
    _all_reviews_link_locator = "css=a.more-info"
    _review_locator = "css=div.review:not(.reply)"
    _info_link_locator = "css=li > a.scrollto"

    _image_locator = "css=#preview.slider li.panel.active a"
    _image_viewer_locator = 'id=lightbox'

    #more about this addon
    _additional_images_locator = "css=#addon .article .screenshot"
    _website_locator = "css=.links a.home"
    #other_addons
    _other_addons_by_author_locator = 'css=#author-addons'
    _reviews_locator = "id=reviews"
    _add_review_link_locator = "id=add-review"
    _about_this_collection_locator = "css=.primary .featured"

    def __init__(self, testsetup, addon_name = None):
        #formats name for url
        AddonsBasePage.__init__(self, testsetup)
        if (addon_name != None):
            self.addon_name = addon_name.replace(' ', '-').lower()
            self.selenium.open("%s/addon/%s" % (self.site_version, self.addon_name))
            self._wait_for_reviews_and_other_addons_by_author_to_load()
        self._page_title = "%s :: Add-ons for Firefox" % self.current_page_breadcrumb

    @property
    def has_reviews(self):
        return self.selenium.get_css_count(self._review_details_locator) > 0

    def click_all_reviews_link(self):
        self.selenium.click(self._all_reviews_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def review_count(self):
        return self.selenium.get_css_count(self._review_locator)

    @property
    def breadcrumb(self):
        return self.selenium.get_text(self._breadcrumb_locator)

    @property
    def current_page_breadcrumb(self):
        return self.selenium.get_text(self._current_page_breadcrumb_locator)

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def name(self):
        return self.selenium.get_text(self._name_locator)

    @property
    def version_number(self):
        return self.selenium.get_text(self._version_number_locator)

    @property
    def source_code_license_information(self):
        return self.selenium.get_text(self._source_code_license_information_locator)

    @property
    def authors(self):
        return [self.selenium.get_text(self._authors_locator + "[ % s]" % (i + 1))
            for i in range(self.selenium.get_xpath_count(self._authors_locator))]

    @property
    def summary(self):
        return self.selenium.get_text(self._summary_locator)

    @property
    def rating(self):
        return self.selenium.get_text(self._addon_rating_locator)

    def click_whats_this_license(self):
        self.selenium.click(self._whats_this_license_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from addons_site import UserFAQPage
        return UserFAQPage(self.testsetup)

    @property
    def description(self):
        return self.selenium.get_text(self._description_locator)

    @property
    def register_link(self):
        return self.selenium.get_text(self._register_link_locator)

    @property
    def login_link(self):
        return self.selenium.get_text(self._login_link_locator)

    @property
    def other_apps(self):
        return self.selenium.get_text(self._other_applications_locator)

    @property
    def version_information_heading(self):
        return self.selenium.get_text(self._version_information_heading_locator)

    @property
    def version_information(self):
        return self.selenium.get_attribute("%s > a@href" % self._version_information_heading_locator)

    @property
    def release_version(self):
        return self.selenium.get_text(self._release_version_locator)

    @property
    def about_addon(self):
        return self.selenium.get_text(self._about_addon_locator)

    @property
    def review_title(self):
        return self.selenium.get_text(self._reviews_title_locator)

    @property
    def review_details(self):
        return self.selenium.get_text(self._review_details_locator)

    @property
    def often_used_with_header(self):
        return self.selenium.get_text(self._other_addons_header_locator)

    @property
    def is_register_visible(self):
        return self.selenium.is_visible(self._register_link_locator)

    @property
    def is_login_visible(self):
        return self.selenium.is_visible(self._login_link_locator)

    @property
    def is_other_apps_link_visible(self):
        return self.selenium.is_visible(self._other_applications_locator)

    @property
    def is_other_apps_dropdown_menu_visible(self):
        self.click_other_apps()
        return self.selenium.is_visible(self._other_apps_dropdown_menu_locator)

    @property
    def is_addon_name_visible(self):
        return self.selenium.is_visible(self._name_locator)

    @property
    def is_summary_visible(self):
        return self.selenium.is_visible(self._summary_locator)

    @property
    def is_about_addon_visible(self):
        return self.selenium.is_visible(self._about_addon_locator)

    @property
    def is_version_information_visible(self):
        return self.selenium.is_visible(self._version_information_locator)

    @property
    def is_version_information_heading_visible(self):
        return self.selenium.is_visible(self._version_information_heading_locator)

    @property
    def is_version_information_section_expanded(self):
        expand_info = self.selenium.get_attribute("%s@class" % self._version_information_locator)
        return ("expanded" in expand_info)

    @property
    def does_page_scroll_to_version_information_section(self):
        return (self.selenium.get_eval("window.pageYOffset")) > 2000

    @property
    def is_review_title_visible(self):
        return self.selenium.is_visible(self._reviews_title_locator)

    @property
    def is_often_used_with_header_visible(self):
        return self.selenium.is_visible(self._other_addons_header_locator)

    @property
    def is_often_used_with_list_visible(self):
        return self.selenium.is_visible(self._other_addons_list_locator)

    @property
    def are_tags_visible(self):
        return self.selenium.is_visible(self._tags_locator)

    @property
    def is_part_of_collections_header_visible(self):
        return self.selenium.is_visible('%s h2' % self._part_of_collections_locator)

    @property
    def is_part_of_collections_list_visible(self):
        return self.selenium.is_visible('%s ul' % self._part_of_collections_locator)

    @property
    def part_of_collections_header(self):
        return self.selenium.get_text('%s h2' % self._part_of_collections_locator)

    def click_other_apps(self):
        self.selenium.click(self._other_applications_locator)
        self.wait_for_element_visible(self._other_apps_dropdown_menu_locator)

    @property
    def icon_url(self):
        return self.selenium.get_attribute(self._icon_locator + "%s" % "@src")

    @property
    def website(self):
        return self.selenium.get_attribute("%s@href" % self._website_locator)

    def click_website_link(self):
        self.selenium.click(self._website_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def support_url(self):
        support_url = self.selenium.get_attribute(self._support_link_locator + "%s" % "@href")
        match = re.findall("http", support_url)
        #staging url
        if len(match) > 1:
            return self._extract_url_from_link(support_url)
        #production url
        else:
            return support_url

    def _extract_url_from_link(self, url):
        #parses out extra certificate stuff from urls in staging only
        return urlparse.unquote(re.search('\w+://.*/(\w+%3A//.*)', url).group(1))

    @property
    def other_addons_by_authors_text(self):
        return self.selenium.get_text("%s > h2" % self._other_addons_by_author_locator)

    @property
    def other_addons_count(self):
        return int(self.selenium.get_css_count('%s li' % self._other_addons_by_author_locator))

    def other_addons(self):
        return [self.OtherAddons(self.testsetup, i) for i in range(self.other_addons_count)]

    @property
    def previewer(self):
        return self.ImagePreviewer(self.testsetup)

    class ImagePreviewer(Page):

        #navigation
        _next_locator = 'css=section.previews.carousel > a.next'
        _prev_locator = 'css=section.previews.carousel > a.prev'

        _image_locator = 'css=#preview'

        def next_set(self):
            self.selenium.click(self._next_locator)

        def prev_set(self):
            self.selenium.click(self._prev_locator)

        def click_image(self, image_no = 0):
            self.selenium.click('%s li:nth(%s) a' % (self._image_locator, image_no))
            from image_viewer_region import ImageViewer
            image_viewer = ImageViewer(self.testsetup)
            image_viewer.wait_for_image_viewer_to_finish_animating()
            return image_viewer

        def image_title(self, image_no):
            return self.selenium.get_attribute('%s li:nth(%s) a@title' % (self._image_locator, image_no))

        def image_link(self, image_no):
            return self.selenium.get_attribute('%s li:nth(%s) a img@src' % (self._image_locator, image_no))

        @property
        def image_count(self):
            return int(self.selenium.get_css_count('%s li' % self._image_locator))

        @property
        def image_set_count(self):
            if self.image_count % 3 == 0:
                return self.image_count / 3
            else:
                return self.image_count / 3 + 1

    def review(self, lookup):
        return self.DetailsReviewSnippet(self.testsetup, lookup)

    def reviews(self):
        return [self.DetailsReviewSnippet(self.testsetup, i) for i in range(self.reviews_count)]

    @property
    def reviews_count(self):
        self.wait_for_element_visible(self._reviews_locator)
        return int(self.selenium.get_css_count(self._reviews_locator))

    @property
    def version_info_link(self):
        return self.selenium.get_attribute("%s@href" % self._info_link_locator)

    @property
    def is_version_info_link_visible(self):
        return self.selenium.is_visible(self._info_link_locator)

    def click_version_info_link(self):
        self.selenium.click(self._info_link_locator)

    class OtherAddons(Page):
        _other_addons_locator = 'css=#author-addons li'
        _name_locator = 'div.summary h3'
        _addon_link_locator = 'div.addon a'

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self._root_locator + relative_locator

        @property
        def _root_locator(self):
            self.wait_for_element_visible(self._other_addons_locator)
            if type(self.lookup) == int:
                # lookup by index
                return "%s:nth(%s) " % (self._other_addons_locator, self.lookup)
            else:
                # lookup by name
                return "%s:contains(%s) " % (self._other_addons_locator, self.lookup)

        @property
        def name(self):
            self.selenium.mouse_over(self.absolute_locator(self._name_locator))
            return self.selenium.get_text(self.absolute_locator(self._name_locator))

        def click_addon_link(self):
            self.selenium.click(self.absolute_locator(self._addon_link_locator))
            self.selenium.wait_for_page_to_load(self.timeout)

        @property
        def name_link_value(self):
            return self.selenium.get_attribute('%s@href' % self.absolute_locator(self._name_link_locator))

    class DetailsReviewSnippet(Page):

        _reviews_locator = "css=#reviews div"  # Base locator
        _username_locator = "p.byline a"

        def __init__(self, testsetup, lookup):
            Page.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self._root_locator + relative_locator

        @property
        def _root_locator(self):
            self.wait_for_element_visible(self._reviews_locator)
            if type(self.lookup) == int:
                # lookup by index
                return "%s:nth(%s) " % (self._reviews_locator, self.lookup)
            else:
                # lookup by name
                return "%s:contains(%s) " % (self._reviews_locator, self.lookup)

        @property
        def username(self):
            return self.selenium.get_text(self.absolute_locator(self._username_locator))

        def click_username(self):
            self.selenium.click(self.absolute_locator(self._username_locator))
            self.selenium.wait_for_page_to_load(self.timeout)
            from addons_user_page import AddonsUserPage
            return AddonsUserPage(self.testsetup)

    def click_to_write_review(self):
        self.selenium.click(self._add_review_link_locator)
        from addons_site import AddonsWriteReviewBlock
        return AddonsWriteReviewBlock(self.testsetup)

    def _wait_for_reviews_and_other_addons_by_author_to_load(self):
        self.wait_for_element_present(self._reviews_locator)
        self.wait_for_element_present(self._other_addons_by_author_locator)

    @property
    def part_of_collections_section_has_3_collections(self):
        x = self.selenium.get_css_count("%s > ul.listing-grid > section > li" % self._part_of_collections_locator)
        return x == 3

    def click_on_any_collection(self):
        self.selenium.click("%s > ul.listing-grid > section > li:nth(0) > div.hovercard > a" % self._part_of_collections_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return CollectionPage(self.testsetup)


class CollectionPage(AddonsBasePage):

    _page_title = 'Collections :: Add-ons for Firefox'

    @property
    def page_title(self):
        return self._page_title

    @property
    def selenium_page_title(self):
        return self.selenium.get_title()
