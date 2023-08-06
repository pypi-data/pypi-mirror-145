from nautilus_librarian.mods.namecodes.domain.filename_filters import (
    filter_base_images,
    filter_gold_images,
    filter_media_library_files,
)


def test_filter_media_files_from_file_list():

    original_file_list = ["data/000001/32/000001-32.600.2.tif"]

    filtered_file_list = filter_media_library_files(original_file_list)

    expected_file_list = ["data/000001/32/000001-32.600.2.tif"]

    assert filtered_file_list == expected_file_list


def test_filter_media_files_from_file_list_with_other_non_library_files():

    original_file_list = [
        "data/000001/32/000001-32.600.2.tif",
        "other.txt",
    ]

    filtered_file_list = filter_media_library_files(original_file_list)

    expected_file_list = ["data/000001/32/000001-32.600.2.tif"]

    assert filtered_file_list == expected_file_list


def test_filter_media_files_from_file_list_with_other_valid_library_files():

    original_file_list = [
        "data/000001/32/000001-32.600.2.tif",
        "data/000001/32/000001-32.600.1.json",
    ]

    filtered_file_list = filter_media_library_files(original_file_list)

    expected_file_list = ["data/000001/32/000001-32.600.2.tif"]

    assert filtered_file_list == expected_file_list


def test_filter_media_files_from_file_list_with_other_invalid_library_files():

    original_file_list = [
        "data/000001/32/000001-32.600.2.tif",
        "data/000001/32/000001-32.600.2.json",  # json file should have type 1 instead fo 2.
    ]

    filtered_file_list = filter_media_library_files(original_file_list)

    expected_file_list = ["data/000001/32/000001-32.600.2.tif"]

    assert filtered_file_list == expected_file_list


def test_filter_gold_images_from_file_list():

    original_file_list = [
        "data/000001/32/000001-32.600.2.tif",
        "data/000001/52/000001-52.600.2.tif",
    ]

    filtered_file_list = filter_gold_images(original_file_list)

    expected_file_list = ["data/000001/32/000001-32.600.2.tif"]

    assert filtered_file_list == expected_file_list


def test_filter_base_images_from_file_list():

    original_file_list = [
        "data/000001/32/000001-32.600.2.tif",
        "data/000001/52/000001-52.600.2.tif",
    ]

    filtered_file_list = filter_base_images(original_file_list)

    expected_file_list = ["data/000001/52/000001-52.600.2.tif"]

    assert filtered_file_list == expected_file_list
