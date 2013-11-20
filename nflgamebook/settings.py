# Scrapy settings for nflgamebook project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nflgamebook'

SPIDER_MODULES = ['nflgamebook.spiders']
NEWSPIDER_MODULE = 'nflgamebook.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nflgamebook (+http://www.yourdomain.com)'

# Be a good citizen to the NFL and do not attempt to overload their servers.
DOWNLOAD_DELAY = 0.5  # seconds