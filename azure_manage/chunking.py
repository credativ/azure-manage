from .progress import ProgressMeter


class BlobChunkUploader(object):
    chunk_size = 4 * 1024 * 1024

    def __init__(self, blob_service, container_name, blob_name,
                 max_retries=5, retry_wait=1):
        self.blob_service = blob_service
        self.container_name = container_name
        self.blob_name = blob_name
        self.max_retries = max_retries
        self.retry_wait = retry_wait

    def __call__(self, size, stream, progress_stream):
        with ProgressMeter(progress_stream, size // (1024 * 1024)) as progress:
            index = 0
            while index < size:
                self.process_chunk(index, size, stream)
                index += self.chunk_size
                progress.set(index // (1024 * 1024))

    def process_chunk(self, chunk_offset, size, stream):
        s = min(self.chunk_size, size - chunk_offset)
        chunk_data = stream.read(s)
        if chunk_data.strip(b'\0'):
            self.upload_chunk_with_retries(chunk_offset, chunk_data)

    def upload_chunk_with_retries(self, chunk_offset, chunk_data):
        retries = self.max_retries
        while True:
            try:
                return self.upload_chunk(chunk_offset, chunk_data)
            except AzureHttpException:
                if retries == 0:
                    raise
                retries -= 1
                sleep(self.retry_wait)


class PageBlobChunkUploader(BlobChunkUploader):
    def upload_chunk(self, chunk_offset, chunk_data):
        range_id = 'bytes={0}-{1}'.format(chunk_offset, chunk_offset + len(chunk_data) - 1)
        self.blob_service.put_page(
            self.container_name,
            self.blob_name,
            chunk_data,
            range_id,
            'update',
        )
