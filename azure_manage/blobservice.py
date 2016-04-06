# -*- coding: utf-8 -*-
# Copyright: 2015 Bastian Blank
# License: MIT, see LICENSE.txt for details.

import os

from azure.storage.blob.blobservice import BlobService as BlobServiceBase

from .chunking import PageBlobChunkUploader


class BlobService(BlobServiceBase):
    def put_image_from_file(self, container_name, blob_name, size, stream, progress_stream):
        self.put_blob(
            container_name,
            blob_name,
            b'',
            'PageBlob',
            x_ms_blob_content_length=size,
        )

        uploader = PageBlobChunkUploader(
            self,
            container_name,
            blob_name,
        )

        uploader(size, stream, progress_stream)
