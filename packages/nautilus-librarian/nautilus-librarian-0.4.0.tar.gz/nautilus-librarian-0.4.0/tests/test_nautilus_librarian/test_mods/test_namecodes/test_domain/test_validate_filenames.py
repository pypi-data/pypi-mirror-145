import pytest

from nautilus_librarian.mods.namecodes.domain.validate_filenames import (
    FilenameException,
    validate_filename,
)


@pytest.mark.parametrize("filename", [("000001-32.600.2.tif"), ("099999-32.600.2.tif")])
def test_valid_artwork_id(filename):
    validate_filename(filename)


def test_missing_artwork_id():
    with pytest.raises(FilenameException):
        validate_filename("-32.600.2.tif")


@pytest.mark.parametrize("filename", [("100000-32.600.2.tif"), ("100001-32.600.2.tif")])
def test_invalid_artwork_id(filename):
    with pytest.raises(FilenameException):
        validate_filename(filename)


@pytest.mark.parametrize("filename", [("000001-32.600.2.tif"), ("000001-52.600.2.tif")])
def test_valid_purpose_code(filename):
    validate_filename(filename)


def test_missing_purpose_code():
    with pytest.raises(FilenameException):
        validate_filename("000001-.600.2.tif")


@pytest.mark.parametrize(
    "filename",
    [("000001-32.600.0.tif"), ("000001-32.600.1.tif"), ("000001-32.600.3.tif")],
)
def test_invalid_purpose_code(filename):
    with pytest.raises(FilenameException):
        validate_filename(filename)


def test_valid_transformation_code():
    validate_filename("000001-32.600.2.tif")


def test_missing_transformation_code():
    with pytest.raises(FilenameException):
        validate_filename("000001-32..2.tif")


@pytest.mark.parametrize("filename", [("000001-32.599.2.tif"), ("000001-32.601.2.tif")])
def test_invalid_transformation_code(filename):
    with pytest.raises(FilenameException):
        validate_filename(filename)


def test_valid_type_code():
    validate_filename("000001-32.600.2.tif")


def test_missing_type_code():
    with pytest.raises(FilenameException):
        validate_filename("000001-32.600..tif")


@pytest.mark.parametrize(
    "filename",
    [("000001-32.600.0.tif"), ("000001-32.600.1.tif"), ("000001-32.600.3.tif")],
)
def test_invalid_type_code(filename):
    with pytest.raises(FilenameException):
        validate_filename(filename)


@pytest.mark.parametrize("filename", [("000001-32.600.2.tif")])
def test_valid_extension(filename):
    validate_filename(filename)


def test_missing_extension():
    with pytest.raises(FilenameException):
        validate_filename("000002-32.600.2")


def test_invalid_extension():
    with pytest.raises(FilenameException):
        validate_filename("000003-32.600.2.tiff")
