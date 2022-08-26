# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import sys

import pymysql

from inscrawler import InsCrawler
from inscrawler.settings import override_settings
from inscrawler.settings import prepare_override_settings


def usage():
    return """
        python crawler.py image -u cal_foodie -o ./output.txt -i 0
        python crawler.py following -u cal_foodie  -o ./output.txt -i 0
    """


def get_image(username, index):
    ins_crawler = InsCrawler(index)
    return ins_crawler.get_user_image(username)


def get_following(username, index):
    ins_crawler = InsCrawler(index)
    return ins_crawler.get_user_following(username)


# def get_posts_by_user(username, number, detail, debug):
#     ins_crawler = InsCrawler(has_screen=debug)
#     return ins_crawler.get_user_posts(username, number, detail)
#
#
# def get_profile(username):
#     ins_crawler = InsCrawler(0)
#     return ins_crawler.get_user_profile(username)
#
#
# def get_profile_from_script(username):
#     ins_cralwer = InsCrawler(0)
#     return ins_cralwer.get_user_profile_from_script_shared_data(username)
#
#
# def get_posts_by_hashtag(tag, number, debug):
#     ins_crawler = InsCrawler(0, has_screen=debug)
#     return ins_crawler.get_latest_posts_by_tag(tag, number)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


# def output(data, filepath):
#     out = json.dumps(data, ensure_ascii=False)
#     if filepath:
#         with open(filepath, "w", encoding="utf8") as f:
#             f.write(out)
#     else:
#         # print(out)


if __name__ == "__main__":
    # db 접속 코드
    db = pymysql.connect(host='',
                         port=0,
                         user='',
                         password='',
                         db='insta_crawler',
                         charset='utf8')
    cur = db.cursor()

    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
    parser.add_argument(
        "mode", help="options: [image, following]"
    )
    # parser.add_argument("-n", "--number", type=int, help="number of returned posts")
    parser.add_argument("-u", "--username", help="instagram's username")
    # parser.add_argument("-t", "--tag", help="instagram's tag name")
    parser.add_argument("-o", "--output", help="output.txt file name(json format)")
    parser.add_argument("-i", "--index", help="login ID Index")
    parser.add_argument("--debug", action="store_true")

    prepare_override_settings(parser)

    args = parser.parse_args()

    override_settings(args)

    if args.mode == "image":
        arg_required("username")
        result_dict = get_image(args.username, args.index)
        userId = result_dict["userid"][0]
        paths = result_dict["images"]

        # insert image path data
        for path in paths:
            insert_dict = {'crawIdx': 0, 'insertUser': userId, 'imgPath': path}
            sql = """INSERT INTO m_img_list(crawIdx, insertUser, imgPath)
                    VALUES (%(crawIdx)s, %(insertUser)s, %(imgPath)s)"""
            cur.execute(sql, insert_dict)

        db.commit()

    elif args.mode == "following":
        arg_required("username")
        result_dict = get_following(args.username, args.index)
        followings = result_dict["following"]

        # insert following list data
        for following in followings:
            insert_dict = {}

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

    db.close()
