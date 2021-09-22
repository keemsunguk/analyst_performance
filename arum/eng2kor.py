from googletrans import Translator

translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
ex1 = translator.translate('안녕하세요.', src="ko", dest="en")
print(ex1.text)
print(ex1.extra_data)


