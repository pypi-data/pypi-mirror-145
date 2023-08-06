
phpp_topics = {
    'forum_id': 0, 'icon_id': 0, 'topic_attachment': False, 'topic_reported': False,
    'topic_title': '', 'topic_poster': 2, 'topic_time': 0, 'topic_time_limit': 0,
    'topic_views': 0, 'topic_status': 0, 'topic_type': 0, 'topic_first_post_id': 0,
    'topic_first_poster_name': '', 'topic_first_poster_colour': '',
    'topic_last_post_id': 0, 'topic_last_poster_id': 2, 'topic_last_poster_name': '',
    'topic_last_poster_colour': 'AA0000', 'topic_last_post_subject': '',
    'topic_last_post_time': 0, 'topic_last_view_time': 0, 'topic_moved_id': 0,
    'topic_bumped': False, 'topic_bumper': 0, 'poll_title': '', 'poll_start': 0,
    'poll_length': 0, 'poll_max_options': 0, 'poll_last_vote': 0, 'poll_vote_change': False,
    'topic_visibility': 1, 'topic_delete_time': 0, 'topic_delete_reason': '',
    'topic_delete_user': 0, 'topic_posts_approved': 1, 'topic_posts_unapproved': 0,
    'topic_posts_softdeleted': 0
}

phpbb_posts = {
    'topic_id': 0, 'forum_id': 0, 'poster_id': 2, 'icon_id': 0, 'poster_ip': '0.0.0.0',
    'post_time': 0, 'post_reported': False, 'enable_bbcode': True, 'enable_smilies': True,
    'enable_magic_url': True, 'enable_sig': True, 'post_username': '', 'post_subject': '',
    'post_text': '', 'post_checksum': '', 'post_attachment': False, 'bbcode_bitfield': '',
    'bbcode_uid': '', 'post_postcount': True, 'post_edit_time': 0, 'post_edit_reason': '',
    'post_edit_user': 0, 'post_edit_count': 0, 'post_edit_locked': False,
    'post_visibility': 1, 'post_delete_time': 0, 'post_delete_reason': '',
    'post_delete_user': 0
}

add_topics = "INSERT INTO phpbb_topics (forum_id, icon_id, topic_attachment, topic_reported, topic_title, topic_poster, topic_time, topic_time_limit, topic_views, topic_status, topic_type, topic_first_post_id, " \
             "topic_first_poster_name, topic_first_poster_colour, topic_last_post_id, topic_last_poster_id, topic_last_poster_name, " \
             "topic_last_poster_colour, topic_last_post_subject, topic_last_post_time, topic_last_view_time, topic_moved_id, topic_bumped, " \
             "topic_bumper, poll_title, poll_start, poll_length, poll_max_options, poll_last_vote, poll_vote_change, topic_visibility, " \
             "topic_delete_time, topic_delete_reason, topic_delete_user, topic_posts_approved, topic_posts_unapproved, topic_posts_softdeleted)" \
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s," \
             "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"


add_posts = "INSERT INTO phpbb_posts (topic_id, forum_id, poster_id, icon_id, poster_ip, post_time, " \
            "post_reported, enable_bbcode, enable_smilies, enable_magic_url, enable_sig, post_username, post_subject, " \
            "post_text, post_checksum, post_attachment, bbcode_bitfield, bbcode_uid, post_postcount, post_edit_time, " \
            "post_edit_reason, post_edit_user, post_edit_count, post_edit_locked, post_visibility, post_delete_time, " \
            "post_delete_reason, post_delete_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"



