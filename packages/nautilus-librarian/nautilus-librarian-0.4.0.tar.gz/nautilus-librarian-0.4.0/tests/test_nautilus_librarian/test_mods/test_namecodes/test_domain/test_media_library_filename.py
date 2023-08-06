from nautilus_librarian.mods.namecodes.domain.media_library_filename import (
    MediaLibraryFilename,
)


def test_instantiation_from_string():
    gold_image_filename = MediaLibraryFilename("000001-32.600.2.tif")

    assert gold_image_filename.artwork_id == "000001"
    assert gold_image_filename.is_gold_image()
    assert gold_image_filename.transformation_code == "600"
    assert gold_image_filename.type_code == "2"
    assert gold_image_filename.extension == "tif"


def test_instantiation_with_absolute_path():
    gold_image_filename = MediaLibraryFilename("/home/user/000001-32.600.2.tif")

    assert gold_image_filename.artwork_id == "000001"
    assert gold_image_filename.is_gold_image()
    assert gold_image_filename.transformation_code == "600"
    assert gold_image_filename.type_code == "2"
    assert gold_image_filename.extension == "tif"


def test_base_image_instantiation_from_gold_image():
    gold_image_filename = MediaLibraryFilename("000001-32.600.2.tif")

    base_image = gold_image_filename.generate_base_image_filename()

    assert str(base_image) == str(MediaLibraryFilename("000001-52.600.2.tif"))


def test_invalid_filename():
    MediaLibraryFilename("invalid filename")
