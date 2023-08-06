"""Main module."""
import datetime
import os

from loguru import logger
from mdutils.mdutils import MdUtils

from typing import List


def get_file_names(start_date: datetime, end_date: datetime) -> List[str]:
    """

    :param start_date:
    :type start_date:
    :param end_date:
    :type end_date:
    :return:
    :rtype:
    """
    delta = end_date - start_date

    file_names = []

    for i in range(delta.days + 1):
        day = start_date + datetime.timedelta(days=i)
        weekday_number = day.weekday()
        # Exclude saturday and Sunday
        if weekday_number < 5:
            file_name = (
                os.path.join(
                    day.strftime("%Y"), day.strftime("%B"), day.strftime("%Y-%m-%d")
                )
                + ".md"
            )
            file_names.append(file_name)
    return file_names


def create_dir(directory: str) -> None:
    """

    :param directory:
    :type directory:
    """
    # Create target Directory if don't exist
    if not os.path.exists(directory):
        os.mkdir(directory)
        logger.info(f"Directory {directory} created ")
    else:
        logger.info(f"Directory {directory} already exists")


def create_md_file(file_name: str) -> None:
    """

    :param file_name:
    :type file_name:
    """
    create_dir(os.path.dirname(file_name))
    logger.info(file_name)
    if not (os.path.exists(file_name)):
        file_name_without_extension = os.path.splitext(file_name)[0]

        file_header = datetime.datetime.strptime(
            os.path.basename(file_name_without_extension), "%Y-%m-%d"
        ).strftime("%A %d %B")

        markdown_file = MdUtils(
            file_name=file_name_without_extension, title=file_header
        )
        markdown_file.new_paragraph("Done:")
        markdown_file.new_line()
        markdown_file.create_md_file()
    else:
        logger.info(f"{file_name} exists")


def create_files(base_path: str, days_to_create: int = 30) -> None:
    """

    :param base_path:
    :type base_path:
    :param days_to_create:
    :type days_to_create:
    """
    if not (os.path.exists(base_path)):
        logger.info(f"{base_path} does not exist, creating")
        create_dir(base_path)

    file_names = get_file_names(
        datetime.date.today(),
        datetime.date.today() + datetime.timedelta(days=days_to_create),
    )

    for file_name in file_names:
        create_md_file(os.path.join(base_path, file_name))


def copy_after_phrase(
    copy_from_file_name: str, copy_to_file_name: str, phrase: str
) -> None:
    """

    :param copy_from_file_name:
    :type copy_from_file_name:
    :param copy_to_file_name:
    :type copy_to_file_name:
    :param phrase:
    :type phrase:
    :return: None
    """
    file_from = open(copy_from_file_name)
    file_to = open(copy_to_file_name)

    if os.path.exists(copy_to_file_name):
        for line in file_to.readlines():
            if phrase in line:
                logger.info(
                    f"{phrase} already exists in {copy_to_file_name}, I won't do anything"
                )
                return
        # if phrase isn't found but the file exists,
        # set the file to append rather than create
        file_to.close()
        file_to = open(copy_to_file_name, "a")

    phrase_exists_in_file = False

    for line in file_from.readlines():

        if phrase in line:
            phrase_exists_in_file = True

        if phrase_exists_in_file:
            file_to.write(line)

    if phrase_exists_in_file is False:
        logger.info(f"{phrase} not found")

    file_to.close()
    file_from.close()


def move_to_dos(base_path: str) -> None:
    """

    :param base_path:
    :type base_path:
    """
    current_date = datetime.date.today()
    # if its a Monday "yesterday" is Friday
    if current_date.weekday() == 0:
        yesterdays_date = current_date - datetime.timedelta(days=3)
    else:
        yesterdays_date = current_date - datetime.timedelta(days=1)

    current_date_file_name = (
        os.path.join(
            base_path,
            current_date.strftime("%Y"),
            current_date.strftime("%B"),
            current_date.strftime("%Y-%m-%d"),
        )
        + ".md"
    )

    yesterdays_date_file_name = (
        os.path.join(
            base_path,
            yesterdays_date.strftime("%Y"),
            yesterdays_date.strftime("%B"),
            yesterdays_date.strftime("%Y-%m-%d"),
        )
        + ".md"
    )

    if not os.path.exists(current_date_file_name):
        create_files(base_path)

    logger.info(
        f"Moving todos from {yesterdays_date_file_name} to {current_date_file_name}"
    )

    copy_after_phrase(yesterdays_date_file_name, current_date_file_name, phrase="ToDO")
