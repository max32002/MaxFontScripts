#!/bin/bash
# change version.
#
# find ~/Documents/noto/convert* -maxdepth 2 -name "TtfConfig.py" -exec ~/Documents/sh/replace_string.py {} "\"2.082\"" "\"2.086\"" \;
# find ~/Documents/noto/convert* -maxdepth 2 -name "TtfConfig.py" -exec ~/Documents/sh/replace_string.py {} "\"2.114\"" "\"2.115\"" \;

# update .sh version.
# find . -maxdepth 2 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Version: 2.071" "Version: 2.101" \;

# convert script CJK TC to CJK SC
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "CJK TC" "CJK SC" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "CJK\ TC" "CJK\ SC" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "CJKtc" "CJKsc" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "/noto/" "/noto_sc/" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "/Documents/noto_sc/convert" "/Documents/noto/convert" \;
# chmod +x *.sh

# convert script CJK SC to CJK JP
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "CJK SC" "CJK JP" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "CJK\ SC" "CJK\ JP" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "CJKsc" "CJKjp" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "/noto_sc/" "/noto_jp/" \;
# chmod +x *.sh

# convert script Swei-3TSans to Swei-Leg
# make sure sans to leg, base image is different.
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "~/Documents/git/swei-sans/CJK\ TC/SweiSansCJKtc" "~/Documents/noto/base/SweiSansCJKtc" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3tsans" "3tleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-3t-sans" "-3t-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3TSans" "3TLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3T Sans" "3T Leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bmp-swei-sans" "bmp-noto-leg" \;
# chmod +x *.sh


# convert script Swei-3TSans to Swei-Del-Luna-Sans
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_3t" "convert_del" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3tsans" "delsans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-3t-sans" "-del-luna-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3TSans" "DelLunaSans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3T Sans" "Del Luna Sans" \;
# chmod +x *.sh

# convert script Swei-3TSans to Swei-Gospel-Sans
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_3t" "convert_gospel" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3tsans" "gospelsans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-3t-sans" "-gospel-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3TSans" "GospelSans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "3T Sans" "Gospel Sans" \;
# chmod +x *.sh

# convert script Swei-Del-Luna-Sans to Swei-Del-Luna-Leg
# make sure sans to leg, base image is different.
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "~/Documents/git/swei-sans/CJK\ TC/SweiSansCJKtc" "~/Documents/noto/base/SweiSansCJKtc" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "delsans" "delleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-del-luna-sans" "-del-luna-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "DelLunaSans" "DelLunaLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Del Luna Sans" "Del Luna Leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bmp-swei-sans" "bmp-noto-leg" \;
# chmod +x *.sh

# convert script Swei-Gospel-Sans to Swei-Gospel-Leg
# make sure sans to leg, base image is different.
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "~/Documents/git/swei-sans/CJK\ TC/SweiSansCJKtc" "~/Documents/noto/base/SweiSansCJKtc" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bmp-swei-sans" "bmp-noto-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "gospelsans" "gospelleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-gospel-sans" "-gospel-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "GospelSans" "GospelLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Gospel Sans" "Gospel Leg" \;
# chmod +x *.sh

# convert script Swei-Gospel-Sans to Swei-Shear-Sans
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_gospel" "convert_shear" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "gospelsans" "shearsans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-gospel-sans" "-shear-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "GospelSans" "ShearSans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Gospel Sans" "Shear Sans" \;
# chmod +x *.sh

# convert script Swei-Shear-Sans to Swei-Shear-Leg
# make sure sans to leg, base image is different.
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "~/Documents/git/swei-sans/CJK\ TC/SweiSansCJKtc" "~/Documents/noto/base/SweiSansCJKtc" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "shearsans" "shearleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-shear-sans" "-shear-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "ShearSans" "ShearLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Shear Sans" "Shear Leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bmp-swei-sans" "bmp-noto-leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Curve-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_curve" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "curveleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-curve-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "CurveLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Curve Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Sans to Swei-Curve-Sans
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_curve" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowsans" "curvesans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-sans" "-curve-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowSans" "CurveSans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Sans" "Curve Sans" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Rainbow-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_rainbow" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "rainbowleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-rainbow-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "RainbowLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Rainbow Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Gothic-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "gothicleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-gothic-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "GothicLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Gothic Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Sans to Swei-Gothic
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowsans" "gothic" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-sans" "-gothic" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowSans" "Gothic" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Sans" "Gothic" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-B2-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_b2" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "b2leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-b2-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "B2Leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "B2 Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Sans to Swei-B2-Sans
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_b2" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowsans" "b2sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-sans" "-b2-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowSans" "B2Sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Sans" "B2 Sans" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Nut-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_nut" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "nutleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-nut-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "NutLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Nut Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-3T-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_3t" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "3tleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-3t-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "3TLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "3T Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Del-Luna-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_del" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "delleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-del-luna-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "DelLunaLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Del Luna Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Shear-Leg
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_shear" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "shearleg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-shear-leg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "ShearLeg" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Shear Leg" \;
# chmod +x *.sh

# convert script Swei-Bow-Leg to Swei-Bow-Sans
# make sure sans to leg, base image is different.
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "~/Documents/noto/base/" "~/Documents/git/swei-bow-sans/CJK\ TC/"\;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bmp-noto-leg" "bmp-swei-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "new-noto-leg" "new-swei-sans" \;

# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "convert_bow" "convert_bow" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "bowleg" "bowsans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "-bow-leg" "-bow-sans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "BowLeg" "BowSans" \;
# find . -maxdepth 1 -name "*.sh" -exec ~/Documents/sh/replace_string.py {} "Bow Leg" "Bow Sans" \;
# chmod +x *.sh


rm -rf ~/Documents/noto/convert_d/util
rm -rf ~/Documents/noto/convert_xd/util
rm -rf ~/Documents/noto/convert_halfmoon/util
rm -rf ~/Documents/noto/convert_b2/util
rm -rf ~/Documents/noto/convert_rainbow/util
rm -rf ~/Documents/noto/convert_bow/util
rm -rf ~/Documents/noto/convert_nut8/util
rm -rf ~/Documents/noto/convert_3tsans/util
rm -rf ~/Documents/noto/convert_toothpaste/util
rm -rf ~/Documents/noto/convert_bat/util
rm -rf ~/Documents/noto/convert_curve/util
rm -rf ~/Documents/noto/convert_del/util
rm -rf ~/Documents/noto/convert_gospel/util
rm -rf ~/Documents/noto/convert_shear/util

cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_d/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_xd/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_halfmoon/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_b2/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_rainbow/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_bow/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_nut8/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_3tsans/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_toothpaste/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_bat/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_curve/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_del/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_gospel/
cp -r ~/Documents/noto/convert/util ~/Documents/noto/convert_shear/

~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_d/TtfConfig.py 			--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_xd/TtfConfig.py 			--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_halfmoon/TtfConfig.py 	--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_b2/TtfConfig.py 			--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_rainbow/TtfConfig.py 		--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_bow/TtfConfig.py 			--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_nut8/TtfConfig.py 		--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_3tsans/TtfConfig.py 		--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_toothpaste/TtfConfig.py 	--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_bat/TtfConfig.py 			--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_curve/TtfConfig.py 		--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_del/TtfConfig.py 			--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_gospel/TtfConfig.py 		--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"
~/Documents/sh/update_block_from_file.py --first ~/Documents/noto/convert_shear/TtfConfig.py 		--second ~/Documents/noto/convert/TtfConfig.py --begin "    STYLE_INDEX = 5"

cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_d/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_xd/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_halfmoon/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_b2/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_rainbow/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_bow/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_nut8/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_3tsans/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_toothpaste/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_bat/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_curve/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_del/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_gospel/
cp ~/Documents/noto/convert/convert_font.py ~/Documents/noto/convert_shear/

rm -rf ~/Documents/git/swei-gothic/python 
rm -rf ~/Documents/git/swei-d-lucy/python 
rm -rf ~/Documents/git/swei-xd/python 
rm -rf ~/Documents/git/swei-halfmoon/python 
rm -rf ~/Documents/git/swei-b2-sans/python 
rm -rf ~/Documents/git/swei-b2-serif/python
rm -rf ~/Documents/git/swei-rainbow-leg/python
rm -rf ~/Documents/git/swei-bow-leg/python
rm -rf ~/Documents/git/swei-nut-sans/python
rm -rf ~/Documents/git/swei-3t-sans/python
rm -rf ~/Documents/git/swei-toothpaste/python
rm -rf ~/Documents/git/swei-bat-sans/python
rm -rf ~/Documents/git/swei-curve-sans/python
rm -rf ~/Documents/git/swei-del-luna-sans/python
rm -rf ~/Documents/git/swei-gospel-sans/python
rm -rf ~/Documents/git/swei-shear-sans/python

mkdir ~/Documents/git/swei-gothic/python 
mkdir ~/Documents/git/swei-d-lucy/python 
mkdir ~/Documents/git/swei-xd/python 
mkdir ~/Documents/git/swei-halfmoon/python 
mkdir ~/Documents/git/swei-b2-sans/python 
mkdir ~/Documents/git/swei-b2-serif/python
mkdir ~/Documents/git/swei-rainbow-leg/python
mkdir ~/Documents/git/swei-bow-leg/python
mkdir ~/Documents/git/swei-nut-sans/python
mkdir ~/Documents/git/swei-3t-sans/python
mkdir ~/Documents/git/swei-toothpaste/python
mkdir ~/Documents/git/swei-bat-sans/python
mkdir ~/Documents/git/swei-curve-sans/python
mkdir ~/Documents/git/swei-del-luna-sans/python
mkdir ~/Documents/git/swei-gospel-sans/python
mkdir ~/Documents/git/swei-shear-sans/python

cp -r ~/Documents/noto/convert/* ~/Documents/git/swei-gothic/python 
cp -r ~/Documents/noto/convert_d/* ~/Documents/git/swei-d-lucy/python 
cp -r ~/Documents/noto/convert_xd/* ~/Documents/git/swei-xd/python 
cp -r ~/Documents/noto/convert_halfmoon/* ~/Documents/git/swei-halfmoon/python 
cp -r ~/Documents/noto/convert_b2/* ~/Documents/git/swei-b2-sans/python 
cp -r ~/Documents/noto/convert_b2/* ~/Documents/git/swei-b2-serif/python
cp -r ~/Documents/noto/convert_rainbow/* ~/Documents/git/swei-rainbow-leg/python
cp -r ~/Documents/noto/convert_bow/* ~/Documents/git/swei-bow-leg/python
cp -r ~/Documents/noto/convert_nut8/* ~/Documents/git/swei-nut-sans/python
cp -r ~/Documents/noto/convert_3tsans/* ~/Documents/git/swei-3t-sans/python
cp -r ~/Documents/noto/convert_toothpaste/* ~/Documents/git/swei-toothpaste/python
cp -r ~/Documents/noto/convert_bat/* ~/Documents/git/swei-bat-sans/python
cp -r ~/Documents/noto/convert_curve/* ~/Documents/git/swei-curve-sans/python
cp -r ~/Documents/noto/convert_del/* ~/Documents/git/swei-del-luna-sans/python
cp -r ~/Documents/noto/convert_gospel/* ~/Documents/git/swei-gospel-sans/python
cp -r ~/Documents/noto/convert_shear/* ~/Documents/git/swei-shear-sans/python

