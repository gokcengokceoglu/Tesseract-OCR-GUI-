import json

def parse_json(input_file, text_output):
    text_output_file = open(text_output, "w+")
    f = open(input_file)
    content =  json.load(f)
    for page_id in range(len(content['responses'])):
        text_output_file.write(content['responses'][page_id]['fullTextAnnotation']['text'])
    text_output_file.close()
