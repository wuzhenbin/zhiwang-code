
'''
tesseract test1.png result
tesseract code.font.exp1.png result -l font


tesseract code.font.exp1.png result -l eng
.1970 7V6}! IIKYB .IXUY TLWC
HJLP J73W 461/5 SXEX HNCT
WURN P208 BVFU 08W]. 47516
6ULV JWZ 0560 KDYE N9M9

tesseract code.font.exp1.png result -l eng+font

'''

import PIL.Image as Image
import os, sys


def train_before():
    img_lis = os.listdir('imgs')

    img_ex = Image.open(os.getcwd()+'\\imgs\\'+img_lis[0])
    img_ex_width = img_ex.width
    img_ex_height = img_ex.height


    wrap_width = img_ex_width * 5
    wrap_height = img_ex_height * 4


    toImage = Image.new('RGBA', (wrap_width, wrap_height))
    for x in range(5):
        for y in range(4):
            item = img_lis.pop(0)
            fromImage = Image.open(os.getcwd()+'\\imgs\\'+item)
            toImage.paste(fromImage, (x*img_ex_width, y*img_ex_height))

    # toImage.show()
    toImage.save('code.font.exp1.tiff')
    toImage.save('code.font.exp1.png')

    os.system('tesseract code.font.exp1.png code.font.exp1 -l eng batch.nochop makebox')


def rename_file(target):
    cwd = os.getcwd()
    lis = os.listdir(cwd)
    for item in target:
        if item in lis:
            # 设置旧文件名（就是路径+文件名）
            oldname = cwd + '\\' + item
            # 设置新文件名
            newname = cwd + '\\font.' + item
            os.rename(oldname, newname)
            print(oldname, '======>', newname)

def delete_file(target):
    cwd = os.getcwd()
    lis = os.listdir(cwd)

    for item in target:
        if item in lis:
            os.unlink(cwd+'\\{}'.format(item))


def traning_after():
    # 写文件font_properties：
    with open('font_properties', 'w') as f:
        f.write('font 0 0 0 0 0')

    # 生成文件
    os.system('tesseract code.font.exp1.tiff  code.font.exp1  nobatch box.train')
    os.system('unicharset_extractor code.font.exp1.box')
    os.system('mftraining -F font_properties -U unicharset code.font.exp1.tr')
    os.system('cntraining code.font.exp1.tr')

    rename_file(['unicharset','inttemp', 'pffmtable', 'shapetable', 'normproto'])
    os.system('combine_tessdata font.')
    delete_file(['font.unicharset','font.inttemp', 'font.pffmtable', 'font.shapetable', 'font.normproto','font_properties','code.font.exp1.tr'])

def main():
    # 请按顺序执行脚本
    # 1 训练前
    # train_before()
    # 2 手动矫正tiff文件
    # 3 训练完获取font.traineddata 
    # traning_after()
    # 4 将font.traineddata 文件放入 Tesseract-OCR的tessdata文件里面 C:\Program Files (x86)\Tesseract-OCR\tessdata
    pass

    

if __name__ == '__main__':
    main()