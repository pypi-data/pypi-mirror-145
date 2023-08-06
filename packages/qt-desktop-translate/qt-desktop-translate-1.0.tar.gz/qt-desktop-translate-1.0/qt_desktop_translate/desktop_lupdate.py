from typing import List, Dict
from lxml import etree
import argparse
import re
import os


def parse_desktop_file(path: str, keys: List[str]) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    results = {}
    for i in keys:
        try:
            results[i] = re.search(f"(?<={i}=).*", text).group()
        except AttributeError:
            pass
    return results


def update_ts_file(path: str, context: str, elements: Dict[str, str]):
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse(path, parser)

    ts_tag = root.xpath("//TS")[0]

    context_list = ts_tag.xpath(f"context//name[text()='{context}']")
    if len(context_list) == 0:
        context_tag = etree.SubElement(ts_tag, "context")
        name_tag = etree.SubElement(context_tag, "name")
        name_tag.text = context
    else:
        context_tag = context_list[0].getparent()

    for text in elements.values():
        source_list = context_tag.xpath(f"message//source[text()='{text}']")

        if len(source_list) == 0:
            message_tag = etree.SubElement(context_tag, "message")

            source_tag = etree.SubElement(message_tag, "source")
            source_tag.text = text

            translation_tag = etree.SubElement(message_tag, "translation")
            translation_tag.set("type", "unfinished")
        else:
            translation_tag = source_list[0].getparent().find("translation")

            if translation_tag.get("type") == "vanished":
                translation_tag.attrib.pop("type")

    root.write(path, pretty_print=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("desktop", type=str)
    parser.add_argument("ts", type=str)
    parser.add_argument('--keys', type=str, default="Comment Description")
    parser.add_argument('--context', type=str, default="DesktopFile")
    args = parser.parse_args()

    entries = parse_desktop_file(args.desktop, args.keys.split(" "))

    if os.path.isdir(args.ts):
        for i in os.listdir(args.ts):
            update_ts_file(os.path.join(args.ts, i), args.context, entries)
    else:
        update_ts_file(os.path.join(args.ts, i), args.context, entries)


if __name__ == "__main__":
    main()

