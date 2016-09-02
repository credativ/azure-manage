# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os

from azure.storage.blob.pageblobservice import PageBlobService

from .chunking import PageBlobChunkUploader


class BlobService(PageBlobService):
    def put_image_from_file(self, container_name, blob_name, size, stream, progress_stream):
        self.create_blob(
            container_name,
            blob_name,
            size,
        )

        uploader = PageBlobChunkUploader(
            self,
            container_name,
            blob_name,
        )

        uploader(size, stream, progress_stream)
