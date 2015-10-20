# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os

from azure.storage.blob.blobservice import BlobService as BlobServiceBase

from .chunking import PageBlobChunkUploader
from .vhd import VHDFooter


class BlobService(BlobServiceBase):
    def put_rawimage_from_path(self, container_name, blob_name, file_path, progress_stream):
        size_image = os.path.getsize(file_path)
        size_complete = size_image + VHDFooter.size

        self.put_blob(
            container_name,
            blob_name,
            b'',
            'PageBlob',
            x_ms_blob_content_length=size_complete,
        )

        uploader = PageBlobChunkUploader(
            self,
            container_name,
            blob_name,
        )

        with open(file_path, 'rb') as stream:
            uploader(size_image, stream, progress_stream)

        footer = VHDFooter(size_image)
        uploader.upload_chunk(size_image, footer.pack())

        return 'https://{}/{}/{}'.format(self._get_host(), container_name, blob_name)
