#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os
from datetime import date

from azure.servicemanagement.servicemanagementservice import ServiceManagementService as ServiceManagementServiceBase
from azure.servicemanagement.servicemanagementservice import _XmlSerializer


def _serialize_os_image_to_xml(
        label, media_link, name, os,
        description=u'', image_family=u'',
        icon_uri=u'', small_icon_uri=u'',
        eula=u'', privacy_uri=u'',
        language=u'',
        show_in_gui=True, published_date=None):
    return _XmlSerializer.doc_from_data(
        'OSImage',
        [
            ('Label', label),
            ('MediaLink', media_link),
            ('Name', name),
            ('OS', os),
            ('Eula', eula),
            ('Description', description),
            ('ImageFamily', image_family),
            ('ShowInGui', show_in_gui and 'true' or 'false'),
            ('PublishedDate', (published_date or date.today()).isoformat()),
            ('IconUri', icon_uri),
            ('PrivacyUri', privacy_uri),
            ('SmallIconUri', small_icon_uri),
            ('Language', language),
        ],
    )


class ServiceManagementService(ServiceManagementServiceBase):
    def add_os_image(self, *args, **kw):
        return self._perform_post(
            self._get_image_path(),
            _serialize_os_image_to_xml(*args, **kw),
            async=True)
