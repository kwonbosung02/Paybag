from barcode import EAN13
from barcode.writer import ImageWriter

generate_number = '2021001110023' #year[4] location code[5] count[4]

generated_code = EAN13(generate_number, writer=ImageWriter())

generated_code.save('code')