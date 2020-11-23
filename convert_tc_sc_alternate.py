#!/usr/bin/env python3
#encoding=utf-8

import LibGlyph

from os import listdir, remove, rename
from os.path import join, exists, splitext

import json

# to copy/move file.
import shutil

# for convert TC/SC
from hanziconv import HanziConv

def open_db(dictionary_filename):
    dict_data = None
    with open(dictionary_filename, 'r') as read_file:
        dict_data = json.load(read_file)
        read_file.close()

    return dict_data

def add_converted_char_to_write_alt_code_list(mycode, converted_char, write_alt_code_list, ff_folder, ff_unicode_set, ff_dict, alt_dict):
    show_debug = False  #online
    #show_debug = True   #debug

    do_convert_process_flag = False
    converted_alt_code = 0

    #print("converted_char:", converted_char)
    if len(converted_char) > 0:
        converted_alt_code = ord(converted_char)
        if converted_alt_code > 0:
            if converted_alt_code != mycode:
                if not converted_alt_code in write_alt_code_list:
                    do_convert_process_flag = True
                    if show_debug:
                        print("converted_code:", converted_alt_code)
                        print("do_convert_process_flag:", do_convert_process_flag)
                else:
                    if show_debug:
                        print("this alt code exist in mapping list.")

    # make sure target empty.
    # purpose: add converted_alt_code to write_alt_code_list
    if do_convert_process_flag:
        if converted_alt_code in ff_unicode_set:
            filename=ff_dict[converted_alt_code]
            glyth_path = join(ff_folder,filename)
            if show_debug:
                print("start to delete the real path:",glyth_path)
            
            if exists(glyth_path):
                remove(glyth_path)

        if converted_alt_code not in write_alt_code_list:
            write_alt_code_list.append(converted_alt_code)

        # purpose: check converted_alt_code in alt_dict.
        # make sure target with altnuit empty, delete reference glyph file.
        # scan full alt_dict mapping.
        alt_unicode_string = "000000" + str(hex(converted_alt_code)).lower()[2:]
        alt_unicode_string = alt_unicode_string[-6:]
        if show_debug:
            print("alt_unicode_string:", alt_unicode_string)

        for key in alt_dict:
            if alt_unicode_string in alt_dict[key]:
                # add key to write alt list.
                if key not in write_alt_code_list:
                    write_alt_code_list.append(key)

                filename=ff_dict[key]
                glyth_path = join(ff_folder,filename)
                if show_debug:
                    print("alt key:", key)
                    print("start to delete the real alt path:",glyth_path)
                if exists(glyth_path):
                    remove(glyth_path)

    return write_alt_code_list


def append_config_encoding(ff_folder, file_path, unicode_field, alt_dict, ff_unicode_set, ff_dict, sc_ignore_case):
    show_debug = False  #online
    #show_debug = True   #debug

    mycode = 0
    is_mycode_in_alt_dict = False

    output_filepath = file_path + ".tmp"
    input_file = open(file_path, 'r')
    output_file = open(output_filepath, 'w')

    left_part = 'Encoding: '
    left_part_length = len(left_part)

    left_part_alt = 'AltUni2: '
    left_part_alt_length = len(left_part_alt)

    x_line = input_file.readline()
    alt_line = ""

    if show_debug:
        print("checking file:", file_path)

    #scan #1 for get info.
    while x_line:
        #print(x_line)
        new_line = x_line

        if left_part == x_line[:left_part_length]:
            right_part = x_line[left_part_length:]
            if ' ' in right_part:
                mychar_array = right_part.split(' ')
                if len(mychar_array) > 0:
                    mycode = int(mychar_array[unicode_field-1])

                    if mycode > 0:
                        if mycode in alt_dict:
                            is_mycode_in_alt_dict = True

        if is_mycode_in_alt_dict:
            if left_part_alt == x_line[:left_part_alt_length]:
                # PS: should only one line.
                alt_line = x_line

        x_line = input_file.readline()

    # after scan , get code list.
    write_alt_code_list = []
    travl_alt_code_list = []

    if mycode > 0:
        travl_alt_code_list.append(mycode)

        # PS: should only add one line.
        if ' ' in alt_line:
            alt_item_array = alt_line.split(' ')
            for right_part in alt_item_array:
                #print("right_part:", right_part)
                if '.' in right_part:
                    right_part_array = right_part.split('.')
                    alt_unicode_string = right_part_array[0].strip()
                    #print("alt_unicode_string:", alt_unicode_string)
                    if len(alt_unicode_string) > 0:
                        alt_unicode_int = int(alt_unicode_string,16)
                        if alt_unicode_int > 0:
                            if alt_unicode_int not in travl_alt_code_list:
                                travl_alt_code_list.append(alt_unicode_int)
                            if alt_unicode_int not in write_alt_code_list:
                                write_alt_code_list.append(alt_unicode_int)


    # find converted target code glyth file to delete.
    # PS: should one or two item.
    #print("travl_alt_code_list:", travl_alt_code_list)

    # PS: SC(1) mapping to TC(N), 
    #     so travel TC to find SC, maybe one SC file be deleted many times.
    for alt_code in travl_alt_code_list:
        if show_debug:
            print("current alt_code:", alt_code, chr(alt_code))
            pass

        converted_char = ""
        if to_lang == "TC":
            converted_char = HanziConv.toSimplified(chr(alt_code))

            # "TC" mode to ignore char.
            if converted_char in sc_ignore_case:
                if show_debug:
                    print('match ignore_case:', converted_char)
            else:
                write_alt_code_list = add_converted_char_to_write_alt_code_list(mycode, converted_char, write_alt_code_list, ff_folder, ff_unicode_set, ff_dict, alt_dict)

        if to_lang == "SC":
            orig_char = chr(alt_code)

            if False:
                directly_sc_char = HanziConv.toSimplified(orig_char)
                is_able_to_sc = True
                if orig_char == directly_sc_char:
                    is_able_to_sc = False

            # get normolize char.
            directly_tc_char = HanziConv.toTraditional(orig_char)
            is_able_to_tc = True
            if orig_char == directly_tc_char:
                is_able_to_tc = False

            if show_debug:
                #print('is_able_to_sc:', is_able_to_sc, directly_sc_char, ord(directly_sc_char))
                print('is_able_to_tc:', is_able_to_tc, directly_tc_char, ord(directly_tc_char))

            # check Traditional alt.
            if is_able_to_tc:

                # travel each real glyph file.
                for each_code in ff_unicode_set:
                    if each_code == mycode:
                        continue
                    if each_code == alt_code:
                        continue

                    sc_char = HanziConv.toSimplified(chr(each_code))
                    is_able_to_sc = True
                    if each_code == ord(sc_char):
                        is_able_to_sc = False

                    if is_able_to_sc and sc_char == orig_char:
                        # bingo, we found match char.
                        filename=ff_dict[each_code]
                        glyth_path = join(ff_folder,filename)
                        if show_debug:
                            print("start to delete the real path:",glyth_path)
                        if exists(glyth_path):
                            if file_path != file_path:
                                remove(glyth_path)

                        if each_code not in write_alt_code_list:
                            write_alt_code_list.append(each_code)

                # travel each alt_dict mapping.
                for key in alt_dict:
                    alt_unicode_string = alt_dict[key]
                    alt_unicode_int = 0
                    if len(alt_unicode_string) > 0:
                        alt_unicode_int = int(alt_unicode_string,16)
                    if alt_unicode_int > 0:
                        if alt_unicode_int == mycode:
                            continue
                        if alt_unicode_int == alt_code:
                            continue

                        sc_char = HanziConv.toSimplified(chr(alt_unicode_int))
                        is_able_to_sc = True
                        if alt_unicode_int == ord(sc_char):
                            is_able_to_sc = False

                        if is_able_to_sc and sc_char == orig_char:
                            # bingo, we found match char.

                            # add key to write alt list.
                            if key not in write_alt_code_list:
                                write_alt_code_list.append(key)

                            if key in ff_unicode_set:
                                #PS: all alt_dict key may not all in ff_dict (SC).
                                filename=ff_dict[key]
                                glyth_path = join(ff_folder,filename)
                                if show_debug:
                                    print("alt key:", key)
                                    print("start to delete the real alt path:",glyth_path)
                                if exists(glyth_path):
                                    if file_path != file_path:
                                        remove(glyth_path)

                            # there are no 'real' file in all_dict mapping table.
                            if alt_unicode_int not in write_alt_code_list:
                                write_alt_code_list.append(alt_unicode_int)



    if show_debug:
        print("mycode:", mycode)
        print("is_mycode_in_alt_dict:", is_mycode_in_alt_dict)
        print("write_alt_code_list:", write_alt_code_list)

    # open again to re-scan.
    input_file = open(file_path, 'r')

    x_line = input_file.readline()

    #scan #2 for output.
    while x_line:
        #print(x_line)
        new_line = x_line

        if left_part == x_line[:left_part_length]:
            right_part = x_line[left_part_length:]
            if ' ' in right_part:
                mychar_array = right_part.split(' ')
                if len(mychar_array) > 0:
                    mycode = int(mychar_array[unicode_field-1])
                    if mycode > 0:
                        # flush buffer.
                        output_file.write(new_line)
                        new_line = None

                        # compose altunit
                        if len(write_alt_code_list) > 0:
                            insert_line = "AltUni2:"
                            for converted_alt_code in write_alt_code_list:
                                alt_unicode_string = "000000" + str(hex(converted_alt_code)).lower()[2:]
                                alt_unicode_string = alt_unicode_string[-6:]
                                insert_line += " %s.ffffffff.0" % (alt_unicode_string)
                            insert_line += "\n"
                            output_file.write(insert_line)

        # ignore all altpart.
        if left_part_alt == x_line[:left_part_alt_length]:
            new_line = None

        if not new_line is None:
            output_file.write(new_line)

        x_line = input_file.readline()

    input_file.close()
    output_file.close()

    if exists(file_path):
        remove(file_path)
        pass
    rename(output_filepath, file_path)

def scan_files(ff_folder, unicode_field, alt_dict, ff_unicode_set, ff_dict, sc_ignore_case, to_lang):
    my_set = set()
    my_dict = {}

    files = listdir(ff_folder)
    file_count = 0
    for f in files:
        file_count += 1

        # must match extension only, exclude ".extension.tmp" file.
        extension = splitext(f)
        #print("extension:", extension[1])
        #break

        if extension[1] == '.glyph':
            # skip hidden files.
            if f[:1] == ".":
                continue

            if f == "nonmarkingreturn.glyph":
                continue
                
            source_path = join(ff_folder,f)

            # allow joined filepath deleted in process.
            if exists(source_path):
                append_config_encoding(ff_folder, source_path, unicode_field, alt_dict, ff_unicode_set, ff_dict, sc_ignore_case)
    return my_set, my_dict



if __name__ == '__main__':
    # 說明： key 是有值的。 value 的假的分身.
    alt_dict={64073: '002ea4', 36710: '002ecb', 35744: '002ec8', 63937: '007642', 149737: '002ea9', 63967: '005c65', 63763: '00908f', 63830: '007a1c', 8209: '00002d', 63961: '006144', 63853: '007701', 63786: '006d6a', 32595: '002eb1', 64012: '005140', 64079: '007950', 64049: '0050e7', 20059: '002e82', 194594: '005272', 63758: '007669', 63928: '0096b8', 63799: '008def', 63858: '006c88', 194604: '020984', 64080: '007956', 64021: '0051de', 36125: '002ec9', 26422: '006735', 40399: '009dc6', 65344: '002035', 63995: '007099', 31035: '002ead', 63909: '006bae', 12296: '002329', 63968: '006613', 36672: '008f3c', 63911: '007375', 38021: '002ed0', 63970: '0068a8', 63883: '0066c6', 63752: '00f907', 63934: '006599', 63797: '008606', 63856: '006bba', 24020: '005dd3', 163767: '002eca', 63819: '005c62', 64046: '0090de', 33073: '00812b', 64082: '00798d', 64023: '0076ca', 40863: '002ef3', 25993: '002eeb', 63761: '0087ba', 63828: '0051dc', 32277: '007dfc', 64051: '0052c9', 64010: '00898b', 64077: '007949', 34111: '00848d', 35265: '002ec5', 40857: '002ef0', 63965: '005229', 63849: '006578', 63939: '00907c', 63892: '007489', 38322: '0095b1', 64055: '005606', 38264: '002ed2', 63765: '006d1b', 63824: '007e37', 39136: '002edf', 25909: '002e99', 63851: '0053c3', 63943: '005289', 40479: '002ee6', 20842: '004fde', 63888: '006200', 63784: '005eca', 28520: '006f40', 194848: '007228', 40831: '002eee', 63817: '0096f7', 63997: '004ec0', 63930: '004e86', 167439: '002ed5', 63907: '005ff5', 63974: '007f79', 64086: '007bc0', 64042: '0098ef', 36530: '008eb1', 63881: '009ece', 63823: '007d2f', 39135: '002edd', 63756: '005948', 63793: '006ad3', 63860: '0082e5', 29061: '007174', 64044: '009928', 25437: '006329', 64084: '007a40', 63795: '0076e7', 63862: '007565', 63821: '006dda', 63993: '007c92', 63754: '0091d1', 63905: '00f96f', 63972: '007406', 63999: '00523a', 63932: '005bee', 63885: '008f62', 64105: '0097ff', 20096: '002ef2', 20702: '00507d', 20817: '00514c', 63963: '00f961', 63890: '006f23', 63941: '006688', 38376: '002ed4', 64008: '00884c', 22428: '00579b', 64053: '005351', 64075: '007891', 63790: '0051b7', 40912: '004ca4', 63767: '0073de', 63826: '0052d2', 13630: '002e8b', 64106: '00983b', 64022: '00732a', 64083: '00798e', 29357: '002ea8', 36790: '002ece', 63857: '008fb0', 63796: '008001', 27014: '006961', 39532: '002ee2', 194586: '0051ac', 63759: '007f85', 63820: '006a13', 63971: '006ce5', 63910: '007c3e', 63884: '006b77', 63753: '005951', 63933: '005c3f', 63994: '0072c0', 63966: '00540f', 63848: '006ccc', 63938: '0084fc', 63893: '0079ca', 24271: '005ec4', 65374: '00301c', 20058: '002e83', 64078: '007948', 63787: '0072fc', 63829: '0051cc', 63760: '00863f', 194732: '0061b2', 32594: '002eb2', 64011: '005ed3', 64048: '004fae', 195024: '008aed', 63831: '007dbe', 24051: '002e92', 63762: '0088f8', 63960: '005f8b', 63854: '008449', 63895: '00806f', 39029: '002eda', 63936: '0071ce', 64072: '00716e', 27514: '002e9e', 63935: '00f95c', 63996: '008b58', 63882: '00529b', 63969: '00674e', 63908: '00637b', 12297: '00232a', 64081: '00795d', 64047: '0096b7', 63757: '0061f6', 63929: '0060e1', 63818: '0058d8', 63859: '0062fe', 63798: '00865c', 64104: '0096e3', 38429: '002ed6', 63973: '0075e2', 63904: '0088c2', 63931: '0050da', 63886: '005e74', 154327: '002eae', 63863: '004eae', 63794: '007210', 194658: '0059ec', 39134: '002edc', 63822: '006f0f', 63992: '007b20', 64043: '0098fc', 64085: '007a81', 63789: '004f86', 63850: '007d22', 63827: '00808b', 63766: '0070d9', 158033: '002ebd', 64052: '0052e4', 64076: '00793e', 22669: '005848', 64009: '00964d', 63964: '009686', 63891: '007149', 26081: '002e9b', 63940: '009f8d', 38271: '002ed3', 63942: '00962e', 63889: '00649a', 63785: '006717', 63962: '006817', 63825: '00964b', 63791: '0052de', 63852: '00585e', 64074: '007422', 64013: '0055c0', 64054: '00559d', 23228: '005aaa', 63880: '009e97', 63755: '005587', 63861: '0063a0', 63792: '0064c4', 27597: '002e9f', 64018: '006674', 64087: '00f996', 24186: '002e93', 22635: '005861', 63816: '008cc2', 63998: '008336', 63975: '0088cf', 63906: '005ec9', 64026: '007965', 64093: '002ec0', 28165: '006df8', 64102: '002ecc', 63745: '0066f4', 63812: '007c60', 40702: '002eea', 27701: '002ea1', 63871: '0052f5', 63804: '00797f', 63923: '009748', 63990: '0081e8', 63876: '006ffe', 63865: '0051c9', 63981: '00541d', 63914: '00f95f', 194794: '0069ea', 63899: '00934a', 63950: '00786b', 63768: '00843d', 40784: '002eec', 63954: '00622e', 171991: '029fce', 36346: '008de5', 32415: '002eb0', 24742: '006085', 30495: '00771e', 194965: '0082bd', 14771: '00363d', 64007: '008f3b', 23587: '002e8f', 63835: '0062cf', 8231: '002022', 23578: '005c19', 27665: '002ea0', 63781: '0062c9', 63840: '006012', 20012: '002ea6', 64005: '006d1e', 173037: '003d1d', 63783: '00881f', 63842: '007570', 39154: '0098ee', 63944: '00677b', 63774: '00721b', 194679: '005c60', 40644: '002ee9', 63952: '00985e', 194789: '00681f', 64056: '005668', 34314: '0085f4', 38263: '002ed1', 24910: '00613c', 63983: '007498', 63916: '00601c', 63878: '0095ad', 63921: '009234', 63988: '006797', 34916: '002ec2', 169599: '002ede', 64089: '007e41', 64100: '008cd3', 35199: '002ec4', 31452: '002eef', 21348: '002ee7', 64028: '009756', 64095: '008457', 63869: '008ad2', 63977: '0091cc', 63802: '009dfa', 63747: '008cc8', 63814: '007262', 35200: '002ec3', 17307: '003588', 63874: '005eec', 63925: '004f8b', 63984: '0085fa', 39003: '00985a', 63979: '00533f', 27699: '006c32', 63810: '0058df', 31993: '002eaf', 63806: '0083c9', 63912: '004ee4', 39118: '002edb', 64091: '008005', 64096: '008910', 170000: '002ee1', 63837: '008afe', 63770: '0099f1', 38738: '009751', 194780: '006753', 63779: '0085cd', 63846: '005fa9', 64068: '006885', 24401: '002e94', 64001: '005ea6', 20600: '005077', 63948: '007409', 63901: '0052a3', 63956: '00502b', 145393: '006af8', 24516: '002e96', 63958: '006dea', 63903: '0070c8', 63833: '009675', 63946: '006d41', 32896: '002eba', 63777: '005d50', 63844: '0078fb', 63897: '0084ee', 34581: '0086fb', 63772: '005375', 64058: '0058a8', 64070: '006e1a', 64003: '007cd6', 63867: '007ce7', 32214: '007dd2', 40614: '002ee8', 63749: '004e32', 63808: '009e7f', 64098: '008b01', 28780: '002ea3', 64030: '007fbd', 40060: '002ee5', 27503: '002eed', 63800: '009732', 63918: '007469', 38886: '002ed9', 63927: '0091b4', 63872: '005442', 64057: '005840', 23296: '005aaf', 37278: '009196', 63953: '00516d', 194924: '007d63', 32770: '002eb9', 63951: '007d10', 63898: '009023', 63843: '005317', 195039: '008f38', 63782: '0081d8', 63945: '0067f3', 63773: '006b04', 64063: '00618e', 64004: '005b85', 64065: '00654f', 12288: '002003', 63870: '0091cf', 63976: '0088e1', 28058: '006d97', 63815: '0078ca', 63746: '008eca', 64101: '008d08', 64027: '00798f', 194812: '006cbf', 33155: '00817d', 29234: '0070ba', 24909: '006120', 63915: '005dba', 63879: '009a6a', 63989: '006dcb', 63920: '008046', 160: '000020', 63991: '007acb', 63922: '0096f6', 63877: '00792a', 20994: '002e89', 63864: '005169', 63813: '00807e', 63744: '008c48', 63803: '00788c', 65440: '002002', 64034: '008af8', 64103: '009038', 23586: '002e90', 63775: '00862d', 63780: '008964', 64006: '0066b4', 64067: '006691', 64061: '006094', 39267: '002ee0', 28505: '006e88', 27097: '0069c7', 63900: '005217', 63949: '007559', 63769: '00916a', 63955: '009678', 8943: '002026', 64002: '0062d3', 8211: '002012', 64071: '006f22', 37806: '0093ad', 63845: '004fbf', 63776: '009e1e', 132648: '002e87', 63896: '008f26', 63771: '004e82', 63959: '008f2a', 21947: '0055a9', 63832: '0083f1', 63801: '009b6f', 63917: '0073b2', 63978: '0096e2', 63926: '0079ae', 63873: '005973', 25164: '002e98', 20155: '002e85', 65293: '002212', 33401: '002ebf', 194797: '006adb', 37613: '0092b3', 26817: '0068b2', 64038: '0090fd', 64099: '008b39', 64090: '007f72', 64029: '007cbe', 63807: '009304', 63868: '00826f', 63809: '008ad6', 63748: '006ed1', 64092: '0081ed', 64097: '008996', 63811: '005f04', 63750: '0053e5', 63805: '007da0', 63913: '0056f9', 63866: '006881', 63875: '0065c5', 21057: '005234', 63924: '009818', 63919: '007f9a', 63980: '006eba', 64025: '00795e', 65295: '002215', 63947: '006e9c', 63902: '0054bd', 63957: '005d19', 31246: '007a05', 64000: '005207', 64069: '006d77', 23214: '005a7e', 64059: '005c64', 20540: '005024', 63838: '004e39', 161970: '002ec7', 194779: '0233cc', 63847: '004e0d', 63778: '006feb', 21855: '005553', 21373: '005373', 37065: '0090a2', 29227: '002ea4', 25944: '00654d', 194831: '006f6e', 23643: '005c4f', 30799: '007814', 13505: '002eb3', 33089: '0080fc', 21578: '00543f', 63788: '0090de', 24400: '002e95', 24114: '005e21', 24183: '005e76', 39200: '009905', 36908: '008ff8', 33289: '0064e7', 39432: '0099e2', 36647: '008eff', 25946: '006553', 35939: '008c5c', 185668: '002e8d', 23032: '00598d', 11157: '0027a1', 37522: '009203', 35500:'008aaa', 23567:'002f29', 22805:'002f23', 21475:'002f1d',21340:'002f18',26408:'002f4a',27611:'002f51',32780:'002f7d',32819:'002f7f',35282:'002f93',36208:'002f9b',38428:'002fa9',39592:'002fbb',40860:'002fd4',194742:'0062d4'}
    sc_ignore_case=[
        '干','了','卜','乃','才','亏','于','千','','么','巨','丑','仇','云','扎','夭','凶','夫','斗','只','布','出','冬','发','它','他','占','扑','扣','托','奶','札','汇','吊','奸','夸','回','同','团','曲','伙','仿','后','朱','合','吃','匡','庄','村','志','里','别','谷','克','困','沈','佛','余','折','助','沄','芸','肖','坛','杆','表','杯','板','松','范','苧','刮','卷','弥','弦','舍','昆','岳','征','制','虮','杰','面','厘','咸','须','茧','药','荡','挂','挑','尝','秋','洒','适','洁','洼','荐','咱','炫','鸩','恹','钥','剃','咽','咯','背','炼','姜','拐','咨','恤','荫','昵','垒','党','获','借','脏','致','蚕','赶','家','晒','症','离','恶','娘','殷','栖','盏','绦','','唉','席','捂','挽','效','核','栗','疱','瓶','疴','莼','浩','浚','涌','涂','凌','凄','准','烟','挨','焊','蝎','象','雇','游','剩','棹','搜','逾','愧','踊','演','历','升','划','向','冲','并','苏','系','你','刨','弄','泛','抵','呼','周','胡','炮','迹','宴','捆','崎','麻','棱','毁','暗','橹','台','局','采','复','蒙','雕'
    ]

    # from 1 to 3.
    unicode_field = 1       # default
    unicode_field = 2       # for Noto Sans

    import sys
    argument_count = 3

    clean_max_count = 99999
    if len(sys.argv)==argument_count:
        source_ff = sys.argv[2]
        to_lang = sys.argv[1]

        if len(source_ff) > 0 and len(to_lang) > 0:
            to_lang = to_lang.strip().upper()

            if not exists(source_ff):
                if not ".sfdir" in source_ff:
                    source_ff += ".sfdir"
            if exists(source_ff):
                print("converting sfdir:", source_ff)
                ff_unicode_set, ff_dict = LibGlyph.load_files_to_set_dict(source_ff, unicode_field)
                scan_files(source_ff, unicode_field, alt_dict, ff_unicode_set, ff_dict, sc_ignore_case, to_lang)
    else:
        print("Argument must be: %d" % (argument_count -1))
        print("Ex:%s folder_name" % (sys.argv[0]))
