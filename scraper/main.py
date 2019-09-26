import csv
from datetime import datetime

import instaloader
from instaloader import Profile

loader = instaloader.Instaloader()

account = "instablog9ja"
profile = Profile.from_username(loader.context, account)
no_of_followers = profile.followers
posts = profile.get_posts()

"""
Explanatory Variables:

    Days Posted
    Time Posted
    isAd
    Number of mentions
    Number of hashtags
    Caption length
    If the caption was edited from its origin
    Media type
    Video view ratio/number of days since it was posted
    Like ratio/number of days since it was posted
    Comment ratio/number of days since it was posted
"""

count = 0

with open("{}.csv".format(account), "w", newline="") as csv_file:
    fieldnames = [
        "HoursPosted",
        "timePosted 24hr",
        "mediatype",
        "likes",
        "isAd",
        "comments",
        "views",
        "ratioLikesToHoursPosted",
        "ratioVideoViewToHoursPosted",
        "ratioCommentsToHoursPosted",
        "noOfHashtags",
        "noOfMentions",
        "noOfFollowers",
    ]

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for post in posts:
        try:
            mediatype = post.typename
            time_posted = post.date_local.strftime("%-H").strip()

            now = datetime.now()
            post_date = post.date_local
            difference = now - post_date
            no_of_hours_posted = round(difference.total_seconds() / 3600)

            if no_of_hours_posted == 0:
                # Avoid any division by 0
                no_of_hours_posted = 1

            no_of_mentions = len(post.caption_mentions)
            no_of_hashtags = len(post.caption_hashtags)

            if post.is_video:
                video_view_count = post.video_view_count
                ratio_video_views_to_hours_posted = (
                    video_view_count / no_of_hours_posted
                )
            else:
                video_view_count = 0
                ratio_video_views_to_hours_posted = 0

            likes = post.likes
            comments = post.comments

            ratio_likes_to_hours_posted = likes / no_of_hours_posted
            ratio_comments_to_hours_posted = comments / no_of_hours_posted

            # Check for ads
            ad = False
            if "link" in post.caption:
                ad = True
            if "Link" in post.caption:
                ad = True
            if "contact us" in post.caption:
                ad = True
            if "Contact Us" in post.caption:
                ad = True
            if "Contact us" in post.caption:
                ad = True
            if "call" in post.caption:
                ad = True
            if "Call" in post.caption:
                ad = True
            if "+234" in post.caption:
                ad = True
            if "Follow IG" in post.caption:
                ad = True
            if "follow" in post.caption:
                ad = True
            if "Visit" in post.caption:
                ad = True
            if "visit" in post.caption:
                ad = True
            if "SHOP" in post.caption:
                ad = True
            if "shop" in post.caption:
                ad = True

            if likes > 5000:
                ad = False  # Large likes usually suggest not ads

            if "Kindly follow" in post.caption:
                ad = True
            if "kindly follow" in post.caption:
                ad = True

            count += 1
            print("{}\t: Write this : {}".format(count, post.shortcode))

            writer.writerow(
                {
                    "isAd": ad,
                    "HoursPosted": no_of_hours_posted,
                    "timePosted 24hr": time_posted,
                    "mediatype": mediatype,
                    "likes": post.likes,
                    "comments": post.comments,
                    "views": video_view_count,
                    "ratioLikesToHoursPosted": ratio_likes_to_hours_posted,
                    "ratioVideoViewToHoursPosted": ratio_video_views_to_hours_posted,
                    "ratioCommentsToHoursPosted": ratio_comments_to_hours_posted,
                    "noOfHashtags": no_of_hashtags,
                    "noOfMentions": no_of_mentions,
                    "noOfFollowers": no_of_followers,
                }
            )

        except TypeError as e:
            print("An error here: ", e)
        except:
            print("Breaking for a reason unknown")
