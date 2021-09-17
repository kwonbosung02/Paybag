from barcode import EAN13
from barcode.writer import ImageWriter
import random
import shutil

#main location, user barcode directory, ecobag barcode directory
src = './'
dir_u = './barcode_user/'
dir_e = './barcode_ecobag/'

#GET Unique Barcode Number for User
def generate_number_user(phone) -> str:
    generate_number = phone
    generate_number += str(random.randrange(0,10)) + str(random.randrange(0,10))
    return generate_number

#GET Unique Barcode Number for Ecobag
def generate_number_market() -> str:
    number = ''
    for i in range(1,14):
        number = number + str(random.randrange(0,10))
    return number
    #If number already exists in database, then recall this function



#Move User barcode
def locate_user_barcode(generate_code,type):
    filename = str(generate_code) + type
    shutil.move(src+filename,dir_u+filename)

#Move Ecobag barcode
def locate_ecobag_barcode(generate_code,type):
    filename = str(generate_code) + type
    shutil.move(src+filename,dir_e+filename)



#Generate barcode for User
def generate_barcode_user_png(phone) -> str:
    generate_num = generate_number_user(phone)
    generate_code = EAN13(generate_num, writer=ImageWriter())
    generate_code.save(generate_code)
    locate_user_barcode(generate_code,'.png')
    return str(generate_code)

#Generate barcode for User
def generate_barcode_user_svg(phone) -> str:
    generate_num = generate_number_user(phone)
    generate_code = EAN13(generate_num)
    generate_code.save(generate_code)
    locate_user_barcode(generate_code,'.svg')
    return str(generate_code)



#Generate barcode for Ecobag
def generate_barcode_ecobag_svg() -> str:
    generate_num = generate_number_market()
    generate_code = EAN13(generate_num)
    generate_code.save(generate_code)
    locate_ecobag_barcode(generate_code,'.svg')
    return str(generate_code)

#Generate barcode for Ecobag
def generate_barcode_ecobag_png() -> str:
    generate_num = generate_number_market()
    generate_code = EAN13(generate_num,writer=ImageWriter())
    generate_code.save(generate_code)
    locate_ecobag_barcode(generate_code,'.png')
    return str(generate_code)
