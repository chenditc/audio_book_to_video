#!/bin/env bash
set -e
set -x

mkdir -p ./output
for file in ./input/*.mp3
do
    filename=$(basename "$file")
    if [[ ! -f "./output/${filename}.srt" ]]
    then
        echo "Converting $filename to srt"
        python3 captioning.py --input "${file}" --format mp3 --output "./output/${filename}.srt" \
            --srt --offline --threshold 5 --delay 0 --remainTime 5000 --profanity raw \
            --maxLineLength 120 --lines 1
    fi

    if [[ ! -f "./output/${filename}-ch.srt" ]]
    then
        echo "Translating $filename to chinese"
        python3 translate.py --input_srt "./output/${filename}.srt" --output_srt "./output/${filename}-ch.srt"
    fi

    if [[ ! -f "./output/${filename}.mp4" ]]
    then
        echo "Generating $filename to video"
        python3 generate_video.py --audio_file "${file}" --subtitle_file "./output/${filename}-ch.srt" --output_file "./output/${filename}.mp4"
    fi
done