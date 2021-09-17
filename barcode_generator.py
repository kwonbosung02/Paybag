from barcode import EAN13
from barcode.writer import ImageWriter
import random

def generate_number(phone):
    generate_number = phone
    generate_number += str(random.randrange(0,10)) + str(random.randrange(0,10))
    return generate_number

def generate_barcode_png(phone):
    generate_num = generate_number(phone)
    generated_code = EAN13(generate_num, writer=ImageWriter())
    generated_code.save(generate_num)
    return generate_num

def generate_barcode_svg(phone):
    generate_num = generate_number(phone)
    generate_code = EAN13(generate_num)
    generate_code.save(generate_num)
    return generate_num
