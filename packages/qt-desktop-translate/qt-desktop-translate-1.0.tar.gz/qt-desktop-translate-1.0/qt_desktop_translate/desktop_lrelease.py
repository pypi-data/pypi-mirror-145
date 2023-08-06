from typing import List, Dict
from lxml import etree
import argparse
import re
import os


def parse_ts_file(path: str, context: str, translations: Dict[str, Dict[str, str]]):
    root = etree.parse(path)

    ts_tag = root.xpath("//TS")[0]

    context_tag = ts_tag.xpath(f"context//name[text()='{context}']")[0].getparent()

    lang = ts_tag.get("language")
    translations[lang] = {}

    for i in context_tag.findall("message"):
        translations[lang][i.find("source").text] = i.find("translation").text


def update_desktop_text(in_path: str, out_path: str, keys: List[str], translations: Dict[str, Dict[str, str]]):
    with open(in_path, "r", encoding="utf-8") as f:
        text = f.read()
    for i in keys:
        try:
            key_text = re.search(f"(?<={i}=).*", text).group()
        except AttributeError:
            continue

        current_text = f"{i}={key_text}\n"

        for key, value in translations.items():
            try:
                if value[key_text] is None:
                    continue

                current_text += f"{i}[{key}]={value[key_text]}\n"
            except Exception:
                pass

        text = re.sub(f"(?<={i}=).*", current_text[:-1], text)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("desktop_in", type=str)
    parser.add_argument("desktop_out", type=str)
    parser.add_argument("ts", type=str)
    parser.add_argument('--keys', type=str, default="Comment Description")
    parser.add_argument('--context', type=str, default="DesktopFile")
    args = parser.parse_args()

    translations = {}
    if os.path.isdir(args.ts):
        for i in os.listdir(args.ts):
            parse_ts_file(os.path.join(args.ts, i), args.context, translations)
    else:
        parse_ts_file(args.ts, args.context, translations)

    update_desktop_text(args.desktop_in, args.desktop_out, args.keys.split(" "), translations)


if __name__ == "__main__":
    main()
