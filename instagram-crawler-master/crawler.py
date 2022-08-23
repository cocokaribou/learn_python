# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
import sys
from io import open

from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings


def usage():
    return """
        python crawler.py image -u cal_foodie -o ./output -i 0
        python crawler.py following -u cal_foodie  -o ./output -i 0
    """

def get_image(username, index):
    ins_crawler = InsCrawler(index)
    return ins_crawler.get_user_image(username)

def get_following(username, index):
    ins_crawler = InsCrawler(index)
    return ''#ins_crawler.get_user_following(username)

# def get_posts_by_user(username, number, detail, debug):
#     ins_crawler = InsCrawler(has_screen=debug)
#     return ins_crawler.get_user_posts(username, number, detail)
#
#
# def get_profile(username):
#     ins_crawler = InsCrawler()
#     return ins_crawler.get_user_profile(username)
# def get_profile_from_script(username):
#     ins_cralwer = InsCrawler()
#     return ins_cralwer.get_user_profile_from_script_shared_data(username)
#
#
# def get_posts_by_hashtag(tag, number, debug):
#     ins_crawler = InsCrawler(has_screen=debug)
#     return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def output(data, filepath):
    out = json.dumps(data, ensure_ascii=False)
    if filepath:
        with open(filepath, "w", encoding="utf8") as f:
            f.write(out)
    else:
        print(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
    parser.add_argument(
        "mode", help="options: [image, following]"
    )
    # parser.add_argument("-n", "--number", type=int, help="number of returned posts")
    parser.add_argument("-u", "--username", help="instagram's username")
    # parser.add_argument("-t", "--tag", help="instagram's tag name")
    parser.add_argument("-o", "--output", help="output file name(json format)")
    parser.add_argument("-i", "--index", help="login ID Index")
    parser.add_argument("--debug", action="store_true")

    prepare_override_settings(parser)

    args = parser.parse_args()

    override_settings(args)

    if args.mode == "image":
        arg_required("username")
        output(get_image(args.username, args.index), args.output)
    elif args.mode == "following":
        arg_required("username")
        output(get_following(args.username, args.index), args.output)
    # elif args.mode in ["posts", "posts_full"]:
    #     arg_required("username")
    #     output(
    #         get_posts_by_user(
    #             args.username, args.number, args.mode == "posts_full", args.debug
    #         ),
    #         args.output,
    #     )
    # elif args.mode == "profile":
    #     arg_required("username")
    #     output(get_profile(args.username), args.output)
    # elif args.mode == "profile_script":
    #     arg_required("username")
    #     output(get_profile_from_script(args.username), args.output)
    # elif args.mode == "hashtag":
    #     arg_required("tag")
    #     output(
    #         get_posts_by_hashtag(args.tag, args.number or 100, args.debug), args.output
    #     )
    else:
        usage()
