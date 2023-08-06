def convert(word):
    VOWELS = 'aeiouy'

    while True:
        word = input("Type a word and get its pig Latin translation: ")

        if word[0] in VOWELS:
            pig_Latin = word + 'way'
        else:
            pig_Latin = word[1:] + word[0] + 'ay'

        return pig_Latin

