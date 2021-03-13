from german_tools.detect_text import get_image_filename


def test_get_image_filename():
    assert "Photo%252009.02.21%252C%252012%252020%252014.jpg" == get_image_filename(
        "https://dl.dropboxusercontent.com:443/s/aklsjflsakjflkasj/Photo%252009.02.21%252C%252012%252020%252014.jpg"
    )
