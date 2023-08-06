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
from io import BytesIO

from PIL import Image
import mock
import numpy as np
import pandas as pd
import pytest
import responses
import six

from datarobot.enums import ImageFormat
from datarobot.errors import ContentRetrievalTerminatedError
from datarobot.helpers.binary_data_utils import (
    get_bytes_for_path,
    get_bytes_for_url,
    get_encoded_file_contents_from_paths,
    get_encoded_file_contents_from_urls,
    get_encoded_image_contents_from_paths,
    get_encoded_image_contents_from_urls,
)
from datarobot.helpers.image_utls import format_image_bytes, ImageOptions

COLLECTION_TYPES_TEST_CASES = [
    pytest.param("images_urls_list", id="list"),
    pytest.param("images_urls_numpy_1d_arr", id="numpy_array"),
    pytest.param("images_urls_pandas_dataframe_column", id="dataframe_column"),
    pytest.param("images_urls_pandas_series", id="pandas_series"),
]

IMAGE_FORMAT_TEST_CASES = ImageFormat.ALL

FILE_CONTENT_METHODS = [
    get_encoded_file_contents_from_urls,
    get_encoded_file_contents_from_paths,
]

IMAGE_CONTENT_METHODS = [
    get_encoded_image_contents_from_urls,
    get_encoded_image_contents_from_paths,
]

GET_CONTENTS_ALL_METHODS = FILE_CONTENT_METHODS + IMAGE_CONTENT_METHODS


@pytest.fixture(scope="session", params=COLLECTION_TYPES_TEST_CASES)
def all_collection_types(request):
    fixture = request.param
    return request.getfixturevalue(fixture)


@pytest.fixture(scope="session")
def images_urls_list():
    return [
        "http://datarobot.com/foo.jpg",
        "https://datarobot.com/bar.png",
        "http://datarobot.com/baz.jpeg",
    ]


@pytest.fixture(scope="session")
def images_urls_numpy_1d_arr(images_urls_list):
    return np.array(images_urls_list, dtype=str)


@pytest.fixture(scope="session")
def images_urls_pandas_dataframe_column(images_urls_list):
    df = pd.DataFrame(
        [[url, None] for url in images_urls_list], columns=["image_urls", "other_col"]
    )
    return df["image_urls"]


@pytest.fixture(scope="session")
def images_urls_pandas_series(images_urls_list):
    return pd.Series(images_urls_list)


def get_image_bytes_helper(im_size, format="PNG", mode="RGB"):
    byte_arr = BytesIO()
    image = Image.new(mode=mode, size=im_size)
    image.format = format
    image.save(byte_arr, format=format)
    return byte_arr.getvalue()


def get_random_image(*args, **kwargs):
    width, height = np.random.randint(10, 20, 2)
    return get_image_bytes_helper((width, height))


@pytest.fixture
def open_mock_path():
    return "{}.open".format("__builtin__" if six.PY2 else "builtins")


@pytest.mark.parametrize("method", FILE_CONTENT_METHODS)
def test__base64_conversion_for_file_methods__no_transformations(method, all_collection_types):
    # prepare expected results to validate content retrieved using function under test
    np.random.seed(1234)
    expected_results = [
        base64.b64encode(get_random_image()).decode("utf-8")
        for _ in range(len(all_collection_types))
    ]
    with mock.patch("datarobot.helpers.binary_data_utils.get_bytes_switcher") as m:
        # mock content retriever to make sure we don't download data or try to open files
        m.__getitem__.return_value = get_random_image
        # reset seed to make sure random image generator will yield same results
        np.random.seed(1234)
        actual_results = method(all_collection_types)
        assert len(actual_results) == len(all_collection_types)
        for actual_b64, expected_b64 in zip(actual_results, expected_results):
            assert actual_b64 == expected_b64


@pytest.mark.parametrize("method", IMAGE_CONTENT_METHODS)
def test__base64_conversion_for_image_methods__no_transformations(method, all_collection_types):
    # prepare expected results to validate content retrieved using function under test
    np.random.seed(1234)
    expected_results = [
        base64.b64encode(get_random_image()).decode("utf-8")
        for _ in range(len(all_collection_types))
    ]
    with mock.patch("datarobot.helpers.binary_data_utils.get_bytes_switcher") as m:
        # mock content retriever to make sure we don't download data or try to open files
        m.__getitem__.return_value = get_random_image
        # reset seed to make sure random image generator will yield same results
        np.random.seed(1234)
        # prepare image options that will make no transformations to original images
        # this way we should receive base64 values that should match these for org images
        image_options = ImageOptions(should_resize=False, image_format="PNG")
        actual_results = method(all_collection_types, image_options=image_options)

        assert len(actual_results) == len(all_collection_types)
        assert actual_results == expected_results


@pytest.mark.parametrize("method", GET_CONTENTS_ALL_METHODS)
def test__get_encoded_image__does_methods_keep_order(method, images_urls_list):
    with mock.patch("datarobot.helpers.binary_data_utils.get_bytes_switcher") as m:
        image_results = [get_random_image() for _ in range(len(images_urls_list))]

        m.__getitem__.return_value = mock.MagicMock(side_effect=image_results)
        results_ordered = method(images_urls_list)

        m.__getitem__.return_value = mock.MagicMock(side_effect=reversed(image_results))
        results_reversed = method(images_urls_list)

        for a, b in zip(results_ordered, reversed(results_reversed)):
            assert a == b


@pytest.mark.parametrize(
    ["im_size_original", "im_size_requested"], [[(50, 50), (40, 40)], [(40, 60), (20, 30)]]
)
@pytest.mark.parametrize("should_resize", [True, False])
@pytest.mark.parametrize("image_format", IMAGE_FORMAT_TEST_CASES)
def test_format_image_bytes__triggered_by_should_resize(
    im_size_original, im_size_requested, should_resize, image_format
):
    original_image = get_image_bytes_helper(im_size_original)
    output_image_bytes = format_image_bytes(
        image_bytes=original_image,
        image_options=ImageOptions(
            should_resize=should_resize, image_size=im_size_requested, image_format=image_format
        ),
    )

    # inspect output image dimensions
    output_image = Image.open(BytesIO(output_image_bytes))
    actual_size = (output_image.width, output_image.height)

    if should_resize:
        # when resize takes place dimensions should match requested
        actual_size == im_size_requested
    else:
        # when no resize takes place dimensions should remain unchanged
        actual_size == im_size_original


@pytest.mark.parametrize(
    ["im_size_original", "im_size_requested", "im_size_expected"],
    [
        [(50, 50), (40, 40), (40, 40)],  # width = height
        [(30, 60), (35, 35), (35, 35)],  # width < height
        [(60, 30), (25, 25), (25, 25)],  # width > height
    ],
)
@pytest.mark.parametrize("image_format", IMAGE_FORMAT_TEST_CASES)
def test_format_image_bytes__no__keep_aspect_ratio(
    im_size_original, im_size_expected, im_size_requested, image_format
):
    original_image = get_image_bytes_helper(im_size_original, format=image_format)
    resized_image_bytes = format_image_bytes(
        image_bytes=original_image,
        image_options=ImageOptions(
            should_resize=True, image_size=im_size_requested, image_format=image_format
        ),
    )

    # inspect output image dimensions
    resized_image = Image.open(BytesIO(resized_image_bytes))
    actual_size = (resized_image.width, resized_image.height)
    assert im_size_requested == actual_size


@pytest.mark.parametrize(
    "image_format",
    [
        ImageFormat.JPEG,
        ImageFormat.TIFF,
        ImageFormat.GIF,
        ImageFormat.PPM,
        ImageFormat.BMP,
        ImageFormat.PNG,
    ],
)
def test_format_image_bytes__input_matches_output__when_no_transformation_needed(image_format):
    input_image_bytes = get_image_bytes_helper(im_size=(16, 16), format=image_format)
    output_image_bytes = format_image_bytes(
        image_bytes=input_image_bytes,
        image_options=ImageOptions(
            should_resize=True, image_size=(16, 16), image_format=image_format
        ),
    )
    assert bytearray(input_image_bytes) == bytearray(output_image_bytes)


@pytest.mark.parametrize(
    ["im_size_original", "im_size_requested", "im_size_expected"],
    [
        # width = height
        [(50, 50), (None, 40), (40, 40)],
        [(50, 50), (-1, 40), (40, 40)],
        [(50, 50), (40, None), (40, 40)],
        [(50, 50), (40, -1), (40, 40)],
        # width < height
        [(40, 60), (None, 30), (20, 30)],
        [(40, 60), (-1, 30), (20, 30)],
        [(40, 60), (30, None), (30, 45)],
        [(40, 60), (30, -1), (30, 45)],
        # width > height
        [(60, 40), (None, 30), (45, 30)],
        [(60, 40), (-1, 30), (45, 30)],
        [(60, 40), (30, None), (30, 20)],
        [(60, 40), (30, -1), (30, 20)],
    ],
)
@pytest.mark.parametrize("image_format", IMAGE_FORMAT_TEST_CASES)
def test_format_image_bytes__keep_aspect_ratio(
    im_size_original, im_size_expected, im_size_requested, image_format
):
    original_image = get_image_bytes_helper(im_size_original, format=image_format)
    resized_image_bytes = format_image_bytes(
        image_bytes=original_image,
        image_options=ImageOptions(
            should_resize=True, image_size=im_size_requested, image_format=image_format
        ),
    )

    # inspect output image dimensions
    resized_image = Image.open(BytesIO(resized_image_bytes))
    actual_size = (resized_image.width, resized_image.height)
    assert im_size_expected == actual_size


@responses.activate
def test_get_file_contents_from_path__expected_data_valid():
    test_image_url = "https://datarobot.com/foo.png"
    test_image_data = get_random_image()

    responses.add(
        responses.GET,
        url=test_image_url,
        status=200,
        content_type="image/png",
        body=test_image_data,
    )
    result = get_bytes_for_url(location=test_image_url)

    # check if expected image contents is equal to BytesIO buffer value
    assert bytearray(test_image_data) == bytearray(result)


@responses.activate
def test_get_file_contents_from_path__data_and_expected_headers_valid():
    test_image_url = "https://datarobot.com/bar.png"

    responses.add(responses.GET, url=test_image_url, status=200, content_type="image/png")

    test_header_user_agent = "TestUserAgent"
    test_header_accepts = "TestAccepts"
    test_headers = {"User-Agent": test_header_user_agent, "Accept": test_header_accepts}

    get_bytes_for_url(location=test_image_url, headers=test_headers)

    # check if headers passed to method were forwarded to http call
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == test_image_url
    assert responses.calls[0].request.headers["User-Agent"] == test_header_user_agent
    assert responses.calls[0].request.headers["Accept"] == test_header_accepts


@pytest.mark.parametrize("status_code", [403, 404, 500])
def test_get_file_contents_from_path__throws_ex__when_no_continue_on_error(status_code):
    test_image_url = "https://datarobot.com/baz.png"
    test_image_data = get_random_image()
    responses.add(
        responses.GET,
        url=test_image_url,
        status=status_code,
        content_type="image/png",
        body=test_image_data,
    )
    with pytest.raises(ContentRetrievalTerminatedError):
        get_bytes_for_url(location=test_image_url)


@pytest.mark.parametrize("status_code", [403, 404, 500])
def test_get_file_contents_from_path__dont_throw_ex__when_is_continue_on_error(status_code):
    test_image_url = "https://datarobot.com/boo.png"
    test_image_data = get_random_image()
    responses.add(
        responses.GET,
        url=test_image_url,
        status=status_code,
        content_type="image/png",
        body=test_image_data,
    )
    content_bytes = get_bytes_for_url(location=test_image_url, continue_on_error=True)
    assert content_bytes is None


def test_get_file_contents_from_url(open_mock_path):
    test_image_data = get_random_image()
    test_image_path = "/some/path/foo.png"

    mock_open_func = mock.mock_open(read_data=test_image_data)
    with mock.patch(open_mock_path, mock_open_func):
        result = get_bytes_for_path(test_image_path)

    assert bytearray(test_image_data) == bytearray(result)


def test_get_file_contents_from_url__raises_ex__when_no_continue_on_error(open_mock_path):
    test_image_data = get_random_image()
    test_image_path = "/some/path/foo.png"

    mock_open_func = mock.mock_open(read_data=test_image_data)
    mock_open_func.side_effect = OSError
    with mock.patch(open_mock_path, mock_open_func):
        with pytest.raises(ContentRetrievalTerminatedError):
            get_bytes_for_path(test_image_path)


def test_get_file_contents_from_url__dont_throw_ex__when_is_continue_on_error(open_mock_path):
    test_image_data = get_random_image()
    test_image_path = "/some/path/foo.png"

    mock_open_func = mock.mock_open(read_data=test_image_data)
    mock_open_func.side_effect = OSError
    with mock.patch(open_mock_path, mock_open_func):
        content_bytes = get_bytes_for_path(test_image_path, continue_on_error=True)
        assert content_bytes is None
