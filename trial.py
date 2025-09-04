def find_SSD_val(text):
    text=text.strip()
    if 'TB' in text:
        if '.0TB' in text:
            text = text.replace('.0TB' , '000')
        else:
            text = text.replace('TB' , '000')
    if 'GB' in text:
        text = text.replace('GB' , '')
    if '+' in text:
        text = text.replace('Hybrid' , 'HDD')

    ssd = 0
    if 'SSD' in text and '+' in text:
        spl = text.split('+')
        for word in spl :
            if 'SSD' in word:
                word = word.replace("GB" , "")
                word = word.replace("SSD" , "")
                word = int(word.strip())
                print(word)
    if 'SSD' in text and '+' not in text:
        print(int(text.replace("GB" , "").replace('SSD','').strip()))
    
    hdd=0
    if 'HDD' in text and '+' in text:
        spl = text.split('+')
        for word in spl :
            if 'HDD' in word:
                word = word.replace("GB" , "")
                word = word.replace("HDD" , "")
                word = int(word.strip())
                print("HDD :- " ,word)
    if 'HDD' in text and '+' not in text:
        print("HDD :- ",int(text.replace("GB" , "").replace('HDD','').strip()))

find_SSD_val('500GB HDD ')