import glob
import logging
import os

import coloredlogs

from elbo.utils.misc_utils import remove_prefix

logger = logging.getLogger("elbo.ai.client")
coloredlogs.install(level='DEBUG',
                    logger=logger,
                    fmt='%(name)s %(message)s')


def cp_file_to_elbo(elbo_connector, filename, source_object, destination_dir):
    if not os.path.exists(filename):
        logger.error(f"{filename} does not exist, please check path.")
        exit(0)
        return
    file_size = os.path.getsize(filename)

    destination_file_path = os.path.join(destination_dir, os.path.basename(filename))

    url_response = elbo_connector.get_upload_url(file_size, destination_file_path, is_training_task=False)
    if url_response is None:
        logger.error(f"is unable to authenticate with server..")
        exit(-6)

    upload_url, user_id, authorization_token, session_id, show_low_balance_alert, user_first_name = url_response
    if upload_url is not None and user_id is not None and authorization_token is not None:
        destination_dir = remove_prefix(destination_dir, '/')
        rel_path = os.path.relpath(filename, start=source_object)
        if rel_path == ".":
            bucket_key = os.path.join(user_id, destination_dir, os.path.basename(source_object))
        else:
            bucket_key = os.path.join(user_id, destination_dir, os.path.basename(source_object), rel_path)

        if not bucket_key.startswith(user_id):
            logger.error(f"something is wrong with the destination {bucket_key}, "
                         f"please email this bug report to hi@elbo.ai")
            exit(0)

        logger.info(f"uploading {filename} -> elbo://{bucket_key} ...")
        _ = elbo_connector.upload_file(filename, upload_url, user_id, authorization_token, bucket_key=bucket_key)


def cp_to_elbo(elbo_connector, file_path, destination_dir):
    """
    Copy the local file path to elbo storage
    :param elbo_connector: The elbo connector
    :param file_path: The local file path
    :param destination_dir: The elbo path
    :return:
    """
    if os.path.isabs(file_path):
        source_object = file_path
    else:
        source_object = os.path.join(os.getcwd(), file_path)

    if not os.path.exists(file_path):
        logger.error(f"Unable to find {file_path}, does it exist?")
        return 0

    if destination_dir == "." or destination_dir == "/":
        # User intends to copy to root
        destination_dir = ""

    if os.path.isdir(source_object):
        for filename in glob.iglob(os.path.join(source_object, '**/**'), recursive=True):
            if os.path.isdir(filename):
                continue
            cp_file_to_elbo(elbo_connector, filename, source_object, destination_dir)
    else:
        cp_file_to_elbo(elbo_connector, file_path, source_object, destination_dir)
