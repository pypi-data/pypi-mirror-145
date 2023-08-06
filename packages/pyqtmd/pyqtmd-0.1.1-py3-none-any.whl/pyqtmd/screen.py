
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.Qt import QThreadPool
from pyqtmd import helpers
import re
import webbrowser

class ArticlePage(QtWidgets.QMainWindow):

    def __init__(self, uri):
        super(ArticlePage, self).__init__()
        uic.loadUi(helpers.relative_path('designer/article.ui'), self)
        self.uri = uri
        self.load_thread = QThread()
        self.thread_pool = QThreadPool()

    def show(self):
        self.load()
        super(ArticlePage, self).show()

    def load(self):
        self.opener = helpers.Opener(self.uri)
        self.opener.moveToThread(self.load_thread)
        self.load_thread.started.connect(self.opener.run)
        self.opener.error.connect(self.close)
        self.opener.finished.connect(self.add_markdown_article)
        self.opener.finished.connect(self.opener.deleteLater)
        self.opener.finished.connect(self.load_thread.quit)
        self.load_thread.start()

    def add_markdown_article(self, article):
        self.loading_label.deleteLater()

        # markdown images look like: ![alt text](image link)
        # they may be encased in a hyperlink: [image](hyperlink)

        # this regex must not have capturing groups, or it makes extra splits.
        splitter = re.compile(r'(?:\[)?\!\[[^\]]*\]\([^\)]*\)(?:\]\([^\)]*\))?')
        text_parts = splitter.split(article)

        # this regex uses capturing groups to get the image metadata
        finder = re.compile(r'\[?\!\[([^\]]*)\]\(([^)]+)\)(?:\]\(([^)]*)\))?')
        img_groups = finder.findall(article)

        # there will always be one more text part than image:
        # text ![](image) text
        # so pop off the last piece of text and add the rest in pairs.
        final_text = text_parts.pop()
        for text_part, img_group in zip(text_parts, img_groups):
            self.add_label(text_part)
            [alt_text, img_link, ext_link] = img_group
            self.add_img(alt_text, img_link, ext_link)
        self.add_label(final_text)

    def add_label(self, text: str):
        label = QLabel()
        label.setText(text)
        label.setTextFormat(Qt.MarkdownText)
        label.linkActivated.connect(webbrowser.open)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)
        font = QFont()
        font.setPointSize(14)
        label.setFont(font)
        self.article_layout.addWidget(label)

    def img_url_to_label(self, url, label):
        label.setText('Loading image')
        worker = helpers.ImageWorker(url, label)
        self.thread_pool.start(worker)

    def add_img(self, alt_text: str, img_link: str, ext_link: str):
        img_label = Image(img_link, ext_link)
        img_label.change_url.connect(webbrowser.open)
        self.img_url_to_label(img_link, img_label)
        img_label.setText(alt_text)
        self.article_layout.addWidget(img_label)

    def add_html_article(self, article: str):
        # may as well reuse this label
        self.loading_label.setText(article)
        self.loading_label.setTextFormat(Qt.RichText)

class Image(QLabel):
    change_url = pyqtSignal(str)
    def __init__(self, img_url, link_url):
        super(Image, self).__init__()
        self.setToolTip(link_url)
        self.mousePressEvent = lambda _: self.change_url.emit(link_url)
        self.setCursor(Qt.PointingHandCursor)

