#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import base64

import requests
from requests.exceptions import RequestException

from datarobot.enums import FileLocationType
from datarobot.errors import ContentRetrievalTerminatedError
from datarobot.helpers.image_utls import format_image_bytes, ImageOptions


def get_bytes_for_path(location, continue_on_error=False, **kwargs):
    """Return file content for path as bytes"""
    try:
        with open(location, mode="rb") as f:
            buffer = f.read()
    except OSError:
        buffer = None
        # exception encountered during processing of single row should stop processing
        if not continue_on_error:
            msg = "Process terminated. Could not retrieve resource: {}".format(location)
            raise ContentRetrievalTerminatedError(msg)
    return buffer


def get_bytes_for_url(location, continue_on_error=False, headers=None, **kwargs):
    """Return file content for url as bytes"""
    try:
        response = requests.get(url=location, headers=headers or {})
        response.raise_for_status()
        return response.content
    except RequestException:
        # exception encountered during processing of single row should stop processing
        if not continue_on_error:
            msg = "Process terminated. Could not retrieve resource: {}".format(location)
            raise ContentRetrievalTerminatedError(msg)


get_bytes_switcher = {
    FileLocationType.PATH: get_bytes_for_path,
    FileLocationType.URL: get_bytes_for_url,
}


def _get_base64_encoded_string_for_location(
    locations, location_type, continue_on_error, image_options=None, **kwargs
):
    """Retrieve contents from specified locations and convert it to base64 strings."""
    result = []
    for row in locations:
        get_bytes_method = get_bytes_switcher[location_type]
        content_bytes = get_bytes_method(row, continue_on_error, **kwargs)
        if content_bytes:
            if image_options:
                content_bytes = format_image_bytes(content_bytes, image_options)
            image_base64 = base64.b64encode(content_bytes).decode("utf-8")
            result.append(image_base64)
        else:
            if not continue_on_error:
                msg = "Process terminated. Could not retrieve resource: {}".format(row)
                raise ContentRetrievalTerminatedError(msg)
            result.append(content_bytes)
    return result


def get_encoded_image_contents_from_urls(
    urls, url_download_headers=None, image_options=None, continue_on_error=False
):
    """
    Returns base64 encoded string of images located in addresses passed in input collection.
    Input collection should hold data of valid image url addresses reachable from
    location where code is being executed. Method will retrieve image, apply specified
    reformatting before converting contents to base64 string. Results will in same
    order as specified in input collection.

    Parameters
    ----------
    urls: Iterable
        Iterable with url addresses to download images from
    url_download_headers: dict
        Dictionary with headers to use when downloading files using url. Detailed data
        related to supported Headers in HTTP  can be found in RFC specification for
        headers in rfc spec: https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
    image_options: ImageOptions class
        Class holding parameters for image transformation and formatting
    continue_on_error: bool
        If one of rows encounters error while retrieving content (i.e. file does not exist) should
        this error terminate process of downloading consecutive files or should process continue
        skipping this file.

    Returns
    -------
    List of base64 encoded strings representing reformatted images.
    """
    return _get_base64_encoded_string_for_location(
        locations=urls,
        location_type=FileLocationType.URL,
        image_options=image_options or ImageOptions(),
        headers=url_download_headers or {},
        continue_on_error=continue_on_error,
    )


def get_encoded_image_contents_from_paths(paths, image_options=None, continue_on_error=False):
    """
    Returns base64 encoded string of images located in paths passed in input collection.
    Input collection should hold data of valid image paths reachable from location
    where code is being executed. Method will retrieve image, apply specified
    reformatting before converting contents to base64 string. Results will in same
    order as specified in input collection.

    Parameters
    ----------
    paths: Iterable
        Iterable with path locations to open images from
    image_options: ImageOptions class
        Class holding parameters for image transformation and formatting
    continue_on_error: bool
        If one of rows encounters error while retrieving content (i.e. file does not exist) should
        this error terminate process of downloading consecutive files or should process continue
        skipping this file.

    Returns
    -------
    List of base64 encoded strings representing reformatted images.
    """
    return _get_base64_encoded_string_for_location(
        locations=paths,
        location_type=FileLocationType.PATH,
        image_options=image_options or ImageOptions(),
        continue_on_error=continue_on_error,
    )


def get_encoded_file_contents_from_paths(paths, continue_on_error=False):
    """
    Returns base64 encoded string for files located under paths passed in input collection.
    Input collection should hold data of valid file paths locations reachable from
    location where code is being executed. Method will retrieve file and convert its contents
    to base64 string. Results will be returned in same order as specified in input collection.

    Parameters
    ----------
    paths: Iterable
        Iterable with path locations to open images from
    continue_on_error: bool
        If one of rows encounters error while retrieving content (i.e. file does not exist) should
        this error terminate process of downloading consecutive files or should process continue
        skipping this file.

    Returns
    -------
    List of base64 encoded strings representing files.
    """
    return _get_base64_encoded_string_for_location(
        locations=paths, location_type=FileLocationType.PATH, continue_on_error=continue_on_error
    )


def get_encoded_file_contents_from_urls(urls, url_download_headers=None, continue_on_error=False):
    """
    Returns base64 encoded string for files located in under url addresses passed in input
    collection. Input collection should hold data of valid file url addresses reachable from
    location where code is being executed. Method will retrieve file and convert its contents
    to base64 string. Results will be returned in same order as specified in input collection.

    Parameters
    ----------
    urls: Iterable
        Iterable with url addresses to download images from
    url_download_headers: dict
        Dictionary with headers to use when downloading files using url. Detailed data
        related to supported Headers in HTTP  can be found in RFC specification for
        headers in rfc spec: https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
    continue_on_error: bool
        If one of rows encounters error while retrieving content (i.e. file does not exist) should
        this error terminate process of downloading consecutive files or should process continue
        skipping this file.

    Returns
    -------
    List of base64 encoded strings representing files.
    """
    return _get_base64_encoded_string_for_location(
        locations=urls,
        location_type=FileLocationType.URL,
        headers=url_download_headers or {},
        continue_on_error=continue_on_error,
    )
