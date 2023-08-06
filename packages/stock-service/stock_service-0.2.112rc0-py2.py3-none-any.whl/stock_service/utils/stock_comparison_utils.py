from retry import retry

from s4f_clients.file_service import FileServiceClient
from s4f_clients.service_health_status import HealthStatusClient
from stock_service.config import OldConfig

config = OldConfig()
config.configure()

file_service_host = config.find_service("s4f-file-service")
logger = config.logger


@retry(tries=2, delay=20, logger=logger)
def upload_file(file_stream, filename):
    """
    This function uploads the file to the file service and returns the file_id of the
    uploaded file.
    """
    file_service_client = FileServiceClient(endpoints=file_service_host)
    reponse = file_service_client.put(filename)
    file_id = reponse.file.id
    file_service_client.upload(file_id, file_stream, "text/csv")
    return file_id


def download_file(file_id):
    if file_id is None:
        raise TypeError("file_id cannot be None. Please enter a valid file_id.")

    file_service_client = FileServiceClient(endpoints=file_service_host)
    _, file_stream = file_service_client.download(file_id)

    return file_id, file_stream


def file_service_is_available():
    """
    This functions determines if the file service is available, and returns the appropriate
    response.
    """
    health_status_client = HealthStatusClient(endpoints=file_service_host)
    service_status = health_status_client.get_service_status().ok
    return service_status


def upload_csv_to_file_service(filename, file_path):
    """
    This function uploads a file to the file service, only if the file service is available.
    If it is not available, the appropriate error message is logged.
    """
    if file_service_is_available():
        with open(file_path, "r") as snapshot_csv_file:
            csv_contents = snapshot_csv_file.read()
            file_id = upload_file(csv_contents.encode("utf-8"), filename)
        logger.info(
            "File has been uploaded to file service: file_id=%s, filename=%s",
            file_id,
            filename,
        )
    else:
        logger.error(
            "File service is not connected. File was not uploaded: filename=%s",
            filename,
        )
