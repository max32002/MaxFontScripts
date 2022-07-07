#!/usr/bin/env python3
#encoding=utf-8

hex_list=['F8FED'
,'35C1'
,'373A'
,'39E9'
,'488D'
,'4D5F'
,'8EF7'
,'9B81'
]

new_char=""
for item in hex_list:
	new_char += chr(int(item,16))

print("new chars:", new_char)
