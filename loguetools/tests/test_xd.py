from loguetools import xd


def test_translate_step_data():
    data = "00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 20 30 40".replace(' ', '')
    og_step_data = bytes.fromhex(data)
    output = xd.fn_translate_step_data(og_step_data)
    match = bytes.fromhex(
        '00 01 02 03 00 00 00 00 04 05 06 07 00 00 00 00 08 09 0a 0b 00 00 00 00 0c 0d 00 00 ' + \
        '00 00 00 0e 0f 00 00 00 00 00 10 20 00 00 00 00 00 30 40 00 00 00 00 00'.replace(' ', '')
    )
    assert output == match
