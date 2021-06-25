# ini読み込み　Dictionaryで返却
def get_property(fileName, encode):
    propertyData = {}
    file = open(fileName, 'r', encoding=encode)
    lines = file.readlines()
    for line in lines:
        if len(line.split('=')) == 2:
            [key, value] = line.split('=')
            propertyData[key] = value.strip()
    return propertyData