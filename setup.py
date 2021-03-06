import json
import os

import mysql.connector

# Load config file
from ags_experiments.settings.config import config

discordpy_command = "python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py"
requirements = "python3 -m pip install -r requirements.txt"

# Setup discord.py + requirements
print("Installing discord.py...")
os.system(discordpy_command)
print("\nInstalling other requirements...")
os.system(requirements)

# Database
print("\nSetting up database")

print("Connecting to DB...")
cnx = mysql.connector.connect(**config['mysql'])
print("Connected.")
cursor = cnx.cursor()

users = """
CREATE TABLE `users` (
  `user_id` varchar(64) CHARACTER SET utf8 NOT NULL,
  `username` varchar(64) CHARACTER SET utf8 NOT NULL,
  `opted_in` bit(1) NOT NULL DEFAULT b'0',
  `automate_opted_in` bit(1) NOT NULL DEFAULT b'0',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci
"""

messages = """
CREATE TABLE `messages` (
  `id` varchar(64) NOT NULL,
  `channel` varchar(64) NOT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

messages_detailed = """
CREATE TABLE `messages_detailed` (
  `id` varchar(64) NOT NULL,
  `user_id` varchar(64) CHARACTER SET utf8 NOT NULL,
  `channel_id` varchar(64) DEFAULT NULL,
  `time` timestamp NULL DEFAULT NULL,
  `contents` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4"""
markovs = """
CREATE TABLE `markovs` (
  `user` varchar(64) NOT NULL,
  `markov_json` longtext,
  PRIMARY KEY (`user`),
  CONSTRAINT `FK_markovs_users` FOREIGN KEY (`user`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

blocklist = """
CREATE TABLE `blocklists` (
  `user_id` varchar(64) NOT NULL,
  `blocklist` longtext NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
"""

apikeys = """
CREATE TABLE `apikeys` (
  `key_id` int(32) NOT NULL AUTO_INCREMENT,
  `key` varchar(33) NOT NULL,
  PRIMARY KEY (`key_id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8
"""


def make_table(query):
  try:
    cursor.execute(query)
  except mysql.connector.errors.ProgrammingError:
    print("Already exists")


print("\nCreating users table")
make_table(users)
print("\nCreating messages table")
make_table(messages)
print("\nCreating detailed messages table")
make_table(messages_detailed)
print("\nCreating markovs table")
make_table(markovs)
print("\nCreating blocklist table")
make_table(blocklist)
print("\nCreating apikeys table")
make_table(apikeys)
print("\nDone!")
