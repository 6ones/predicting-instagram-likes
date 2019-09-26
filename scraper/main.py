import csv
from datetime import datetime

import instaloader
from instaloader import Profile

from scraper.text_processing import analyze_sentiment

loader = instaloader.Instaloader()

account = "instablog9ja"
profile = Profile.from_username(loader.context, account)
no_of_followers = profile.followers
no_of_followees = profile.followees
posts = profile.get_posts()

"""
Explanatory Variables:

    Hours Since Posted
    Time Posted
    Day Posted
    isAd
    Number of mentions
    Number of hashtags
    Caption length
    If the caption was edited from its origin
    Media type
    Video view ratio/number of days since it was posted
    Like ratio/number of days since it was posted
    Comment ratio/number of days since it was posted
    noOfFollowees
    noOfFollowers
"""

count = 0

with open("{}.csv".format(account), "w", newline="") as csv_file:
    fieldnames = [
        "HoursPosted",
        "timePosted 24hr",
        "day posted",
        "mediatype",
        "sentiment",
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
        "noOfFollowees",
    ]

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for post in posts:
        try:
            mediatype = post.typename
            time_posted = post.date_local.strftime("%-H").strip()
            day_posted = post.date_local.strftime("%A").strip()

            # This is to be consumed by Google Cloud NLP
            caption = post.caption

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
            if "link" in caption:
                ad = True
            if "Link" in caption:
                ad = True
            if "contact us" in caption:
                ad = True
            if "Contact Us" in caption:
                ad = True
            if "Contact us" in caption:
                ad = True
            if "call" in caption:
                ad = True
            if "Call" in caption:
                ad = True
            if "+234" in caption:
                ad = True
            if "Follow IG" in caption:
                ad = True
            if "follow" in caption:
                ad = True
            if "Visit" in caption:
                ad = True
            if "visit" in caption:
                ad = True
            if "SHOP" in caption:
                ad = True
            if "shop" in caption:
                ad = True
            if "wat" in caption:
                ad = True
            if "on Android" in caption:
                ad = True
            if "Exclusive" in caption:
                ad = True
            if "exclusive" in caption:
                ad = True
            if "coming soon" in caption:
                ad = True
            if "Coming soon" in caption:
                ad = True
            if "Catch us" in caption:
                ad = True
            if "Download" in caption:
                ad = True
            if "download" in caption:
                ad = True

            # Large likes usually suggest not ads, set threshold at 5000
            if likes > 5000:
                ad = False

            if "Kindly follow" in caption:
                ad = True
            if "kindly follow" in caption:
                ad = True
            if "Follow us" in caption:
                ad = True
            if "follow us" in caption:
                ad = True

            # sentiment analysis
            sentiment = analyze_sentiment(caption)
            print(caption)
            print("\n\tSentiment: ", sentiment, "\n")

            count += 1
            print("{}\t: Write this : {}".format(count, post.shortcode))

            writer.writerow(
                {
                    "isAd": ad,
                    "HoursPosted": no_of_hours_posted,
                    "timePosted 24hr": time_posted,
                    "day posted": day_posted,
                    "mediatype": mediatype,
                    "sentiment": sentiment,
                    "likes": post.likes,
                    "comments": post.comments,
                    "views": video_view_count,
                    "ratioLikesToHoursPosted": ratio_likes_to_hours_posted,
                    "ratioVideoViewToHoursPosted": ratio_video_views_to_hours_posted,
                    "ratioCommentsToHoursPosted": ratio_comments_to_hours_posted,
                    "noOfHashtags": no_of_hashtags,
                    "noOfMentions": no_of_mentions,
                    "noOfFollowers": no_of_followers,
                    "noOfFollowees": no_of_followees,
                }
            )

        except TypeError as e:
            print("An error here: ", e)
        except KeyboardInterrupt:
            print("Script ended by keyboard")
            break
        except:
            print("Breaking for a reason unknown")
