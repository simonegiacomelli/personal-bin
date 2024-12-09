file_content = r"Your file content with escape sequences like \n and \t"
interpreted_string = file_content.encode('utf-8').decode('unicode_escape')

print(interpreted_string)
