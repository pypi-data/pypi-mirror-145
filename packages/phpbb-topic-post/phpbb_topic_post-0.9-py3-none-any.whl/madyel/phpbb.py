import pymysql
import sshtunnel
from sshtunnel import SSHTunnelForwarder
import time
import calendar
import hashlib
import logging
from madyel.config import configure as conf


__author__ = "madyel"


class PhpBB(object):

    def __init__(self, config, enable_ssh=True, verbose=False):
        self.conf = conf
        self.ts = None
        self.body = None
        self.title = None
        self.username = None
        self.category_id = None
        self.tunnel = None
        self.connection = None
        self.verbose = verbose
        self.enable_ssh = enable_ssh
        self.config = config
        if self.enable_ssh:
            self.__open_ssh_tunnel()
        self.__mysql_connect()

    def __get_user_detail(self):
        sql = "SELECT user_id, user_colour  FROM phpbb_users where username=%s;"
        cursor = self.connection.cursor()
        cursor.execute(sql, self.username)
        details = cursor.fetchone()
        self.conf.phpp_topics['topic_last_poster_colour'] = details[1]
        self.conf.phpp_topics['topic_first_poster_colour'] = details[1]
        self.conf.phpp_topics['topic_last_poster_id'] = details[0]
        self.conf.phpp_topics['topic_poster'] = details[0]
        self.conf.phpbb_posts['poster_id'] = details[0]

    def insert_topic_post(self, category_id, username_phpbb, title, body):
        self.category_id = category_id
        self.username = username_phpbb
        self.title = title
        self.body = body
        gmt = time.gmtime()
        self.ts = calendar.timegm(gmt)
        self.__get_user_detail()
        self.__add_topic()
        return "Complete"

    def __add_post(self, last_topic_id):
        self.conf.phpbb_posts['topic_id'] = last_topic_id[0]
        self.conf.phpbb_posts['forum_id'] = self.category_id
        self.conf.phpbb_posts['post_subject'] = self.title
        self.conf.phpbb_posts['post_time'] = self.ts
        self.conf.phpbb_posts['post_text'] = self.body
        self.conf.phpbb_posts['post_checksum'] = hashlib.md5(self.body.encode()).hexdigest()
        self.conf.phpbb_posts['post_username'] = self.username
        value_p = tuple(self.conf.phpbb_posts.values())
        cursor = self.connection.cursor()
        cursor.execute(self.conf.add_posts, value_p)
        self.connection.commit()
        cursor.execute('select last_insert_id() from phpbb_posts')
        last_post_id = cursor.fetchone()
        return last_post_id

    def __update_forum(self, last_post_id):
        sql = "SELECT count(*) FROM phpbb_topics where forum_id=%s;"
        cursor = self.connection.cursor()
        cursor.execute(sql, self.category_id)
        tot = cursor.fetchone()
        update_sql = f"UPDATE phpbb_forums set forum_last_post_id=%s, forum_last_post_subject=%s, forum_last_post_time=%s, " \
                     f"forum_posts_approved=%s, forum_topics_approved=%s, forum_last_poster_name='{self.username}', forum_last_poster_colour='{self.conf.phpp_topics['topic_last_poster_colour']}' where forum_id=%s;"
        cursor.execute(update_sql, (last_post_id[0], self.title, self.ts, tot[0], tot[0], self.category_id))
        self.connection.commit()
        self.__update_posts_user()

    def __update_posts_user(self):
        sql = "SELECT count(*) FROM phpbb_topics where topic_first_poster_name=%s;"
        cursor = self.connection.cursor()
        cursor.execute(sql, self.username)
        tot = cursor.fetchone()
        update_sql = "UPDATE phpbb_users set user_posts=%s where username=%s;"
        cursor.execute(update_sql, (tot[0], self.username))
        self.connection.commit()

    def __check_sql_string(self, sql, values):
        unique = "%PARAMETER%"
        sql = sql.replace("%s", unique)
        for v in values: sql = sql.replace(unique, repr(v), 1)
        return sql

    def __add_topic(self):
        self.conf.phpp_topics['forum_id'] = self.category_id
        self.conf.phpp_topics['topic_title'] = self.title
        self.conf.phpp_topics['topic_time'] = self.ts
        self.conf.phpp_topics['topic_last_post_time'] = self.ts
        self.conf.phpp_topics['topic_last_post_subject'] = self.title
        self.conf.phpp_topics['topic_first_poster_name'] = self.username
        self.conf.phpp_topics['topic_last_poster_name'] = self.username
        value = tuple(self.conf.phpp_topics.values())
        cursor = self.connection.cursor()
        cursor.execute(self.conf.add_topics, value)
        self.connection.commit()
        cursor.execute('select last_insert_id() from phpbb_topics')
        last_topic_id = cursor.fetchone()

        update_sql = "UPDATE phpbb_topics set topic_first_post_id=%s,topic_last_post_id=%s where topic_id=%s;"
        cursor.execute(update_sql, (last_topic_id[0], last_topic_id[0], last_topic_id[0]))
        self.connection.commit()

        last_post_id = self.__add_post(last_topic_id)
        self.__update_forum(last_post_id)

    def close(self):
        self.__mysql_connect()
        self.__close_ssh_tunnel()

    def __open_ssh_tunnel(self):
        if self.verbose:
            sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
        self.tunnel = SSHTunnelForwarder(
            (self.config['ssh_host'], self.config['ssh_port']),
            ssh_username=self.config['ssh_username'],
            ssh_password=self.config['ssh_password'],
            remote_bind_address=(self.config['localhost'], self.config['port_db']))
        self.tunnel.start()

    def __mysql_connect(self):
        port = self.config['port_db']
        if self.enable_ssh:
            port = self.tunnel.local_bind_port
        self.connection = pymysql.connect(
            host=self.config['localhost'],
            user=self.config['database_username'],
            passwd=self.config['database_password'],
            db=self.config['database_name'],
            port=port)

    def __mysql_disconnect(self):
        self.connection.close()

    def __close_ssh_tunnel(self):
        self.tunnel.close()
