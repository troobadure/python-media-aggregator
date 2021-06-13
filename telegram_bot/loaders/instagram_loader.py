from instaloader import instaloader, Instaloader, Profile, Post, StoryItem, InstaloaderException, PostChangedException, LoginRequiredException, PrivateProfileNotFollowedException
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Callable, Iterator, Optional, Set, Union
from pathlib import Path
import os, glob


def load_profile(profile_name, likes_percentage, days_period):
    for filename in glob.glob(f"files/instagram/{profile_name}_*"):
        os.remove(filename) 

    loader = Instaloader_parameters('files/instagram', '{target}_{date_utc}')
    loader.login_paremeters()
    profiles = set([Profile.from_username(loader.context, profile_name)])
    loader.download_profiles_custom_parameters(profiles, date_filter_factory(datetime.now()-timedelta(days=days_period)), post_filter_factory(likes_percentage))

def main():
    inputs = open('telegram_bot/db_proto/profiles.txt', 'r')
    names = inputs.readlines()
    names = list(map(str.strip, names))

    loader = Instaloader_parameters('_{score}_{target}_{date_utc}')
    loader.login_paremeters()
    profiles = set(map(lambda name: Profile.from_username(loader.context, name), names))
    loader.download_profiles_custom_parameters(profiles, date_filter_factory(datetime.now()-timedelta(days=1500)), post_filter_factory(15))
    
def login_paremeters(self):
    return self.login('dankmemeloader', 'loaderdankmeme')
setattr(Instaloader, 'login_paremeters', login_paremeters)

def Instaloader_parameters(dirname='files/content', filename='{target}_{date_utc:%Y-%m-%d_%H-%M}'):
    return Instaloader(sleep=False, quiet=False, user_agent=None, dirname_pattern=dirname, 
    filename_pattern=filename, download_pictures=True, download_videos=True, 
    download_video_thumbnails=False, download_geotags=False, download_comments=False, save_metadata=True, compress_json=False, 
    post_metadata_txt_pattern='{caption}\n_________\nLIKES: {likes}\nVIEWS: {video_view_count}\nCOMMENTS: {comments}', 
    storyitem_metadata_txt_pattern=None, max_connection_attempts=3, request_timeout=None) #, commit_mode=False)
    # defaults:
    # sleep=True, quiet=False, user_agent=None, dirname_pattern=None, 
    # filename_pattern=None, download_pictures=True, download_videos=True, download_video_thumbnails=True, 
    # download_geotags=True, download_comments=True, save_metadata=True, compress_json=True, post_metadata_txt_pattern=None, 
    # storyitem_metadata_txt_pattern=None, max_connection_attempts=3, request_timeout=None, commit_mode=False

def download_profiles_parameters(self, profiles, filter):
    return self.download_profiles(profiles, profile_pic=False, posts=True, tagged=False, igtv=False, highlights=False, stories=False, 
    fast_update=True, post_filter=filter, storyitem_filter=None, raise_errors=False)
    # defaults:
    # profiles, profile_pic=True, posts=True, tagged=False, igtv=False, highlights=False, stories=False, 
    # fast_update=False, post_filter=None, storyitem_filter=None, raise_errors=False
setattr(Instaloader, 'download_profiles_parameters', download_profiles_parameters)

def download_profiles_custom_parameters(self, profiles, date_filter, post_filter):
    return self.download_profiles_custom(profiles, profile_pic=False, posts=True, tagged=False, igtv=False, highlights=False, stories=False, 
    fast_update=True, date_filter=date_filter, post_filter=post_filter, storyitem_filter=None, raise_errors=False)
    # defaults:
    # profiles, profile_pic=True, posts=True, tagged=False, igtv=False, highlights=False, stories=False, 
    # fast_update=False, post_filter=None, storyitem_filter=None, raise_errors=False
setattr(Instaloader, 'download_profiles_custom_parameters', download_profiles_custom_parameters)

def post_filter_factory(likes_limit=0):
    def filter(post):
        # return post.is_video and not post.video_view_count == 0 and post.likes/post.video_view_count >= likes_limit/100
        return True
    return filter

def date_filter_factory(date_limit=datetime(2020, 5, 1)):
    def filter(post):
        return post.date_utc >= date_limit
    return filter    


def download_profiles_custom(self, profiles: Set[Profile],
                        profile_pic: bool = True, posts: bool = True,
                        tagged: bool = False,
                        igtv: bool = False,
                        highlights: bool = False,
                        stories: bool = False,
                        fast_update: bool = False,
                        date_filter: Optional[Callable[[Post], bool]] = None,
                        post_filter: Optional[Callable[[Post], bool]] = None,
                        storyitem_filter: Optional[Callable[[Post], bool]] = None,
                        raise_errors: bool = False):
    """High-level method to download set of profiles.
    :param profiles: Set of profiles to download.
    :param profile_pic: not :option:`--no-profile-pic`.
    :param posts: not :option:`--no-posts`.
    :param tagged: :option:`--tagged`.
    :param igtv: :option:`--igtv`.
    :param highlights: :option:`--highlights`.
    :param stories: :option:`--stories`.
    :param fast_update: :option:`--fast-update`.
    :param post_filter: :option:`--post-filter`.
    :param storyitem_filter: :option:`--post-filter`.
    :param raise_errors:
        Whether :exc:`LoginRequiredException` and :exc:`PrivateProfileNotFollowedException` should be raised or
        catched and printed with :meth:`InstaloaderContext.error_catcher`.
    .. versionadded:: 4.1
    .. versionchanged:: 4.3
        Add `igtv` parameter.
    """

    @contextmanager
    def _error_raiser(_str):
        yield

    # error_handler type is Callable[[Optional[str]], ContextManager[None]] (not supported with Python 3.5)
    error_handler = _error_raiser if raise_errors else self.context.error_catcher

    for profile in profiles:
        with error_handler(profile.username):  # type: ignore
            profile_name = profile.username

            # Download profile picture
            if profile_pic:
                with self.context.error_catcher('Download profile picture of {}'.format(profile_name)):
                    self.download_profilepic(profile)

            # Save metadata as JSON if desired.
            if self.save_metadata:
                json_filename = '{0}/{1}_{2}'.format(self.dirname_pattern.format(profile=profile_name,
                                                                                    target=profile_name),
                                                        profile_name, profile.userid)
                self.save_metadata_json(json_filename, profile)

            # Catch some errors
            if profile.is_private and (tagged or igtv or highlights or posts):
                if not self.context.is_logged_in:
                    raise LoginRequiredException("--login=USERNAME required.")
                if not profile.followed_by_viewer and self.context.username != profile.username:
                    raise PrivateProfileNotFollowedException("Private but not followed.")

            # Download tagged, if requested
            if tagged:
                with self.context.error_catcher('Download tagged of {}'.format(profile_name)):
                    self.download_tagged(profile, fast_update=fast_update, post_filter=post_filter)

            # Download IGTV, if requested
            if igtv:
                with self.context.error_catcher('Download IGTV of {}'.format(profile_name)):
                    self.download_igtv(profile, fast_update=fast_update, post_filter=post_filter)

            # Download highlights, if requested
            if highlights:
                with self.context.error_catcher('Download highlights of {}'.format(profile_name)):
                    self.download_highlights(profile, fast_update=fast_update, storyitem_filter=storyitem_filter)

            # Iterate over pictures and download them
            if posts:
                self.context.log("Retrieving posts from profile {}.".format(profile_name))
                self.posts_download_loop_custom(profile.get_posts(), profile_name, fast_update, date_filter, post_filter,
                                            total_count=profile.mediacount)

    if stories and profiles:
        with self.context.error_catcher("Download stories"):
            self.context.log("Downloading stories")
            self.download_stories(userids=list(profiles), fast_update=fast_update, filename_target=None,
                                    storyitem_filter=storyitem_filter)
setattr(Instaloader, 'download_profiles_custom', download_profiles_custom)


def posts_download_loop_custom(self,
                            posts: Iterator[Post],
                            target: Union[str, Path],
                            fast_update: bool = False,
                            date_filter: Optional[Callable[[Post], bool]] = None,
                            post_filter: Optional[Callable[[Post], bool]] = None,
                            max_count: Optional[int] = None,
                            total_count: Optional[int] = None) -> None:
    """
    Download the Posts returned by given Post Iterator.
    ..versionadded:: 4.4
    :param posts: Post Iterator to loop through.
    :param target: Target name
    :param fast_update: :option:`--fast-update`
    :param post_filter: :option:`--post-filter`
    :param max_count: Maximum count of Posts to download (:option:`--count`)
    :param total_count: Total number of posts returned by given iterator
    """
    for number, post in enumerate(posts):
        if max_count is not None and number >= max_count:
            break
        if total_count is not None:
            self.context.log("[{0:{w}d}/{1:{w}d}] ".format(number + 1, total_count,
                                                            w=len(str(total_count))),
                                end="", flush=True)
        else:
            if max_count is not None:
                self.context.log("[{0:{w}d}/{1:{w}d}] ".format(number + 1, max_count,
                                                                w=len(str(max_count))),
                                    end="", flush=True)
            else:
                self.context.log("[{:3d}] ".format(number + 1), end="", flush=True)
        if date_filter is not None:
            try:
                if not date_filter(post):
                    self.context.log("{} date filter negative reached".format(post))
                    break
            except (InstaloaderException, KeyError, TypeError) as err:
                self.context.error("{} skipped. Date filter evaluation failed: {}".format(post, err))
                break
        if post_filter is not None:
            try:
                if not post_filter(post):
                    self.context.log("{} skipped".format(post))
                    continue
            except (InstaloaderException, KeyError, TypeError) as err:
                self.context.error("{} skipped. Filter evaluation failed: {}".format(post, err))
                continue
        with self.context.error_catcher("Download {} of {}".format(post, target)):
            # The PostChangedException gets raised if the Post's id/shortcode changed while obtaining
            # additional metadata. This is most likely the case if a HTTP redirect takes place while
            # resolving the shortcode URL.
            # The `post_changed` variable keeps the fast-update functionality alive: A Post which is
            # obained after a redirect has probably already been downloaded as a previous Post of the
            # same Profile.
            # Observed in issue #225: https://github.com/instaloader/instaloader/issues/225
            post_changed = False
            while True:
                try:
                    downloaded = self.download_post_custom(post, target=target)
                    break
                except PostChangedException:
                    post_changed = True
                    continue
            if fast_update and not downloaded and not post_changed:
                break
setattr(Instaloader, 'posts_download_loop_custom', posts_download_loop_custom)

def download_post_custom(self, post: Post, target: Union[str, Path]) -> bool:
    """
    Download everything associated with one instagram post node, i.e. picture, caption and video.
    :param post: Post to download.
    :param target: Target name, i.e. profile name, #hashtag, :feed; for filename.
    :return: True if something was downloaded, False otherwise, i.e. file was already there
    """

    # score = int(post.likes/post.video_view_count*20) + 1 if post.is_video else 0
    # score_str = str(score) + '_' + str(int(post.likes/post.video_view_count*100))
    score_str = 'score'
    dirname = instaloader._PostPathFormatter(post).format(self.dirname_pattern, target=target, score=score_str)
    filename = dirname + '/' + self.format_filename_custom(post, target=target, score=score_str)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # db_manager.insert_post(filename) need to make database writing here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # Download the image(s) / video thumbnail and videos within sidecars if desired
    downloaded = True
    # self._committed = self.check_if_committed(filename)
    if self.download_pictures:
        if post.typename == 'GraphSidecar':
            edge_number = 1
            for sidecar_node in post.get_sidecar_nodes():
                # Download picture or video thumbnail
                if not sidecar_node.is_video or self.download_video_thumbnails is True:
                    downloaded &= self.download_pic(filename=filename, url=sidecar_node.display_url,
                                                    mtime=post.date_local, filename_suffix=str(edge_number))
                # Additionally download video if available and desired
                if sidecar_node.is_video and self.download_videos is True:
                    downloaded &= self.download_pic(filename=filename, url=sidecar_node.video_url,
                                                    mtime=post.date_local, filename_suffix=str(edge_number))
                edge_number += 1
        elif post.typename == 'GraphImage':
            downloaded = self.download_pic(filename=filename, url=post.url, mtime=post.date_local)
        elif post.typename == 'GraphVideo':
            if self.download_video_thumbnails is True:
                downloaded = self.download_pic(filename=filename, url=post.url, mtime=post.date_local)
        else:
            self.context.error("Warning: {0} has unknown typename: {1}".format(post, post.typename))

    # Download video if desired
    if post.is_video and self.download_videos is True:
        downloaded &= self.download_pic(filename=filename, url=post.video_url, mtime=post.date_local)

    if downloaded:
        # Save caption if desired
        metadata_string = instaloader._ArbitraryItemFormatter(post).format(self.post_metadata_txt_pattern).strip()
        if metadata_string:
            self.save_caption(filename=filename, mtime=post.date_local, caption=metadata_string)

        # Download geotags if desired
        if self.download_geotags and post.location:
            self.save_location(filename, post.location, post.date_local)

        # Update comments if desired
        # if self.download_comments is True:
        #     #self.update_comments(filename=filename, post=post)
        #     self.save_metadata_json(filename, post)
        #     with open(filename+'.json') as filename_json:
        #         with open(filename+'.txt', 'a', encoding='utf-8') as filename_txt:
        #             data = json.load(filename_json)
        #             for comment_data in data['node']['edge_media_to_parent_comment']['edges']:
        #                 comment_text = comment_data['node']['text']
        #                 filename_txt.write('\n'+comment_text+'\n')
        #     os.remove(filename+'.json')
                    
        # Save metadata as JSON if desired.
        if self.save_metadata is not False:
            self.save_metadata_json(filename, post)


    self.context.log()
    return downloaded
setattr(Instaloader, 'download_post_custom', download_post_custom)

def format_filename_custom(self, item: Union[Post, StoryItem], target: Optional[Union[str, Path]] = None, score: int = 0):
        """Format filename of a :class:`Post` or :class:`StoryItem` according to ``filename-pattern`` parameter.
        .. versionadded:: 4.1"""
        return instaloader._PostPathFormatter(item).format(self.filename_pattern, target=target, score=score)
setattr(Instaloader, 'format_filename_custom', format_filename_custom)


if __name__ == '__main__':
    main()