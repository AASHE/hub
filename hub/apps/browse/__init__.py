import logging
from sorl.thumbnail.log import ThumbnailLogHandler


handler = ThumbnailLogHandler()
handler.setLevel(logging.INFO)
logging.getLogger('sorl.thumbnail').addHandler(handler)
