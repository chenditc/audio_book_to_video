import pysrt
import requests, uuid, json
import os
import fire
import copy

stop_charactors = [" ", ".", "，", "(", ")", "。", ",", "、"]

def translate(input_text_list):
# Add your key and endpoint
    key = os.environ["TRANSLATOR_KEY"]
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = os.environ["TRANSLATOR_REGION"]

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ['zh-Hans']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    # You can pass more than one object in body.
    body = [{"text": x} for x in input_text_list]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    trans_text_list = [x["translations"][0]["text"] for x in response]
    return trans_text_list

def find_split_point(input_line, max_index, split_by=stop_charactors):
    split_points = [index for index, char in enumerate(input_line) if char in split_by and index < max_index]
    if len(split_points) == 0:
        return int(max_index - 1)
    return max(split_points)

def translate_srt(input_srt, output_srt):
    filename = os.path.basename(input_srt).split(".")[0]

    subs = pysrt.open(input_srt)

    #subs[0].start = "00:00:00"

    en_sub_list = [ sub.text.replace("\n", " ")  for sub in subs]
    ch_sub_list = []
    for i in range(int(len(en_sub_list)/100 + 1)):
        ch_sub_list += translate(en_sub_list[ i*100 : (i+1)*100 ])

    # Font = 30, width = 1280
    max_en_charactor = 60
    max_ch_charactor = max_en_charactor / 2

    for sub, trans_text in zip(subs, ch_sub_list):
        # One line might contains two sentence
        multiline_en = sub.text.split(".")
        multiline_ch = trans_text.split("。")
        final_line = ""
        for en_line, ch_line in zip(multiline_en, multiline_ch):
            if en_line == "":
                continue
            # Split line into max width
            while len(en_line) > max_en_charactor:
                split_point = find_split_point(en_line, max_en_charactor) + 1
                final_line += en_line[:split_point] + "\n"
                en_line = en_line[split_point:]
            final_line += en_line
            if final_line[-1] not in stop_charactors:
                final_line += "."
            final_line += "\n"

            while len(ch_line) > max_ch_charactor:
                split_point = find_split_point(ch_line, max_ch_charactor) + 1
                final_line += ch_line[:split_point] + "\n"
                ch_line = ch_line[split_point:]
            final_line += ch_line
            if final_line[-1] not in stop_charactors:
                final_line += "。"
            final_line += "\n"
        sub.text = final_line

    # first_sub = copy.copy(subs[0])
    # first_sub.start = "00:00:00"
    # first_sub.end = subs[0].start
    # first_sub.text = filename
    # subs.insert(0, first_sub)

    subs[0].start = "00:00:00,000"
    subs[0].text = filename + "\n" + subs[0].text

    subs.save(output_srt)

if __name__ == "__main__":
    fire.Fire(translate_srt)