# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.

from cloudferrylib.base.action import convertor
from cloudferrylib.os.actions.utils import utils
from cloudferrylib.utils import utils as utl
__author__ = 'mirrorcoder'

LOG = utl.get_log(__name__)
CEPH = 'ceph'
ACTIVE = 'active'
BARE = "bare"
AVAILABLE = 'available'


class ConvertorImageToVolume(convertor.Convertor):

    def __init__(self):
        super(ConvertorImageToVolume, self).__init__()

    def run(self, images_info={}, cloud_current=None, **kwargs):
        resource_storage = cloud_current.resources['storage']
        resource_image = cloud_current.resources['image']
        volumes_info = dict(resource=resource_image, volumes=[])
        if not utils.require_methods(['uploud_to_image'], resource_storage):
            raise RuntimeError("No require methods")
        for vol in images_info['images']:
            volume = resource_storage.deploy(utils.convert_to_dest(vol, 'image', 'volume'))[0]
            volume = resource_storage.read_info({'id': volume.id})[0]
            vol['meta']['volume'] = volume
            volumes_info['volumes'].append(utils.convert_to_dest(vol, 'image', 'volume'))
        return {
            'volumes_info': volumes_info
        }

