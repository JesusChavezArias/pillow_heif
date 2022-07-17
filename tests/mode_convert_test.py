import os
from io import BytesIO
from pathlib import Path

import pytest
from helpers import compare_hashes, gradient_rgb, gradient_rgba

from pillow_heif import from_pillow, open_heif, options, register_heif_opener

os.chdir(os.path.dirname(os.path.abspath(__file__)))
register_heif_opener()

pytest.importorskip("numpy", reason="NumPy not installed")
if not options().hevc_enc:
    pytest.skip("No HEVC encoder.", allow_module_level=True)


@pytest.mark.parametrize("enc_bits", (10, 12))
@pytest.mark.parametrize("mode", ("RGB;16", "BGR;16"))
def test_rgb8_to_16_bit_color_mode(mode, enc_bits):
    try:
        options().save_to_12bit = True if enc_bits == 12 else False
        png_pillow = gradient_rgb()
        heif_file = from_pillow(png_pillow)
        assert heif_file.bit_depth == 8
        heif_file[0].convert_to(mode)
        out_heic = BytesIO()
        heif_file.save(out_heic, quality=-1)
        assert heif_file.bit_depth == 16
        assert not heif_file.has_alpha
        heif_file = open_heif(out_heic, convert_hdr_to_8bit=False)
        assert heif_file.bit_depth == enc_bits
        assert not heif_file.has_alpha
        compare_hashes([png_pillow, out_heic], hash_size=8)
    finally:
        options().reset()


@pytest.mark.parametrize("enc_bits", (10, 12))
@pytest.mark.parametrize("mode", ("RGBA;16", "BGRA;16"))
def test_rgba8_to_16_bit_color_mode(mode, enc_bits):
    try:
        options().save_to_12bit = True if enc_bits == 12 else False
        png_pillow = gradient_rgba()
        heif_file = from_pillow(png_pillow)
        assert heif_file.bit_depth == 8
        heif_file[0].convert_to(mode)
        out_heic = BytesIO()
        heif_file.save(out_heic, quality=-1)
        assert heif_file.bit_depth == 16
        assert heif_file.has_alpha
        heif_file = open_heif(out_heic, convert_hdr_to_8bit=False)
        assert heif_file.bit_depth == enc_bits
        assert heif_file.has_alpha
        compare_hashes([png_pillow, out_heic], hash_size=8)
    finally:
        options().reset()


@pytest.mark.parametrize("img, bit", (("images/rgb10.heif", 10), ("images/rgb12.heif", 12)))
@pytest.mark.parametrize("mode", ("RGB;16", "BGR;16"))
def test_rgb10_to_16bit_color_mode(img, mode, bit):
    heif_file = open_heif(Path(img), convert_hdr_to_8bit=False)
    assert heif_file.bit_depth == bit
    heif_file[0].convert_to(mode)
    out_heic = BytesIO()
    heif_file.save(out_heic, quality=-1)
    assert heif_file.bit_depth == 16
    assert not heif_file.has_alpha
    heif_file = open_heif(out_heic, convert_hdr_to_8bit=False)
    assert heif_file.bit_depth == 10
    assert not heif_file.has_alpha
    compare_hashes([Path(img), out_heic], hash_size=8)


@pytest.mark.parametrize("img, bit", (("images/rgba10.heif", 10), ("images/rgba12.heif", 12)))
@pytest.mark.parametrize("mode", ("RGBA;16", "BGRA;16"))
def test_rgba10_to_16bit_color_mode(img, mode, bit):
    heif_file = open_heif(Path(img), convert_hdr_to_8bit=False)
    assert heif_file.bit_depth == bit
    heif_file[0].convert_to(mode)
    out_heic = BytesIO()
    heif_file.save(out_heic, quality=-1)
    assert heif_file.bit_depth == 16
    assert heif_file.has_alpha
    heif_file = open_heif(out_heic, convert_hdr_to_8bit=False)
    assert heif_file.bit_depth == 10
    assert heif_file.has_alpha
    compare_hashes([Path(img), out_heic], hash_size=8)