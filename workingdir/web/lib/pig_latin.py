def pig_latin(string): 
    sentence = []
    for item in string.split():
        word = ""
        for char in item: 
            if char.isalpha():
                word = word.lower() + char
        
        if len(word) > 1 and word[0] not in "aeiou":
            word = word.lower()
            pig = (word[1] + word[2:]) + (word[0] + "ay")  
            sentence.append(pig)
        elif len(word) > 1 and word[0] in "aeiou":
            word = word.lower()
            pig = word + word[0] + "ay"
            sentence.append(pig)
        else: 
            sentence.append(word)
    result = " ".join(sentence)
    return result

