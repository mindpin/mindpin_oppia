# Copyright 2012 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Controllers for the gallery page."""

__author__ = 'sll@google.com (Sean Lip)'

import collections

import oppia.apps.exploration.services as exp_services
from oppia.controllers.base import BaseHandler

from google.appengine.api import users


class GalleryPage(BaseHandler):
    """The exploration gallery page."""

    def get(self):
        """Handles GET requests."""
        self.values.update({
            'nav_mode': 'gallery',
        })
        self.render_template('gallery/gallery.html')


class GalleryHandler(BaseHandler):
    """Provides data for the exploration gallery."""

    def get(self):
        """Handles GET requests."""
        if users.is_current_user_admin():
            explorations = exp_services.get_all_explorations()
            editable_exploration_ids = [e.id for e in explorations]
        elif self.user_id:
            explorations = exp_services.get_viewable_explorations(self.user_id)
            editable_exploration_ids = [
                e.id for e in exp_services.get_editable_explorations(
                    self.user_id)
            ]
        else:
            explorations = exp_services.get_public_explorations()
            editable_exploration_ids = []

        categories = collections.defaultdict(list)

        for exploration in explorations:
            categories[exploration.category].append({
                'can_edit': exploration.id in editable_exploration_ids,
                'can_fork': self.user_id and exploration.is_demo,
                'id': exploration.id,
                'image_id': exploration.image_id,
                'is_owner': (users.is_current_user_admin() or
                             exploration.is_owned_by(self.user_id)),
                'title': exploration.title,
            })

        self.values.update({
            'categories': categories,
        })
        self.render_json(self.values)