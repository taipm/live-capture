from ebooklib import epub
from DateHelper import TODAY

class Ebook:
    class Chapter:
        def __init__(self) -> None:
            self._title:str

        @property
        def title(self):
            return self._title
        
        @title.setter
        def title(self, title):
            # if(a < 18):
            #     raise ValueError("Sorry you age is below eligibility criteria")        
            self._title = title

    def __init__(self) -> None:
        self.createdDate = TODAY
        self._title:str

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        # if(a < 18):
        #     raise ValueError("Sorry you age is below eligibility criteria")
        print("setter method called")
        self._title = title

    def createBook(self):
        pass

    def addChapter(self):
        pass

    def addPage(self, chapter)

book = epub.EpubBook()

# set metadata
book.set_identifier("id123456")
book.set_title("Sample book")
book.set_language("en")

book.add_author("Author Authorowski")
book.add_author(
    "Danko Bananko",
    file_as="Gospodin Danko Bananko",
    role="ill",
    uid="coauthor",
)

# create chapter
c1 = epub.EpubHtml(title="Intro", file_name="chap_01.xhtml", lang="hr")
c1.content = (
    "<h1>Intro heading</h1>"
    "<p>Zaba je skocila u baru.</p>"
    '<p><img alt="[ebook logo]" src="static/ebooklib.gif"/><br/></p>'
)

# create image from the local image
image_content = open("ebooklib.gif", "rb").read()
img = epub.EpubImage(
    uid="image_1",
    file_name="static/ebooklib.gif",
    media_type="image/gif",
    content=image_content,
)

# add chapter
book.add_item(c1)
# add image
book.add_item(img)

# define Table Of Contents
book.toc = (
    epub.Link("chap_01.xhtml", "Introduction", "intro"),
    (epub.Section("Simple book"), (c1,)),
)

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = "BODY {color: white;}"
nav_css = epub.EpubItem(
    uid="style_nav",
    file_name="style/nav.css",
    media_type="text/css",
    content=style,
)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ["nav", c1]

# write to the file
epub.write_epub("test.epub", book, {})