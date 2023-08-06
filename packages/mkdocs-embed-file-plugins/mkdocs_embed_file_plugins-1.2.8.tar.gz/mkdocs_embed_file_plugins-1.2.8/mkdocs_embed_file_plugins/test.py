import markdown
from mdx_wikilink_plus.mdx_wikilink_plus import WikiLinkPlusExtension
from bs4 import BeautifulSoup

quote = ''''# heading 1
Link to [[private]]
Link to [[index]]
![[metacopy2.png]]'''

html = markdown.markdown(
            quote,
            extensions=[
                "nl2br",
                "footnotes",
                "attr_list",
                "mdx_breakless_lists",
                "smarty",
                "sane_lists",
                "tables",
                "admonition",
                WikiLinkPlusExtension(),
            ],
        )
link_soup = BeautifulSoup(html, "html.parser")
tooltip_template = (
    "<a href='"
    + str('')
    + "' class='link_citation'><i class='fas fa-link'></i> </a> <div"
    " class='citation'>"
    + str(link_soup).replace('!<img class="wikilink-image', '<img class="wikilink-image')
    + "</div>"
)

print(tooltip_template)
