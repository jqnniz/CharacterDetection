#pip install paddleocr
#pip install paddlepaddle


from paddleocr import PaddleOCR
#ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to load model into memory
ocr = PaddleOCR(lang='de') # need to run only once to load model into memory

#img_path = 'PaddleOCR/doc/imgs_words_en/word_10.png'

img_path = 'C://projects//CharacterDetection//images//date02.jpeg'
#result = ocr.ocr(img_path, det=False, cls=True)
result = ocr.ocr(img_path)
result = [result[1][0] for result in result[0]]


for line in result:
    print(line)