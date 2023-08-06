
from cellcube_xml_elements import CellcubeXmlDocument, CellcubeXmlPage, CellcubeXmlPageLink, CellcubeXmlFormEntry, CellcubeXmlFormPage
from cellcube_xml_builder import CellcubeXmlPageBuilder, Page, Link, Document
import os





os.system("clear")
print()
print()
print()


"""
document = CellcubeXmlDocument()

link = CellcubeXmlPageLink(href="http://www.google.ci", content="Google search engine", key="1")
entry = CellcubeXmlFormEntry(prompt="Quel est votre nom ?", variable_name="name", kind="digits")
print(entry.to_xml())
print()
entry.set_kind(None)
entry.set_prompt("Votre nom")
entry.set_variable_name("your_name")
print(entry.to_xml())
print()

page1 = CellcubeXmlPage(content="Belle vue")
page1.set_page_tag("item1")

page1.add_link(link)
page1.set_page_content("Ca marche comme je veux")

page2 = CellcubeXmlPage(page_tag="item2")
page2.set_page_content("pas mal")


form_page = CellcubeXmlFormPage(content="Weather service",action="/cgi/weather")
form_page.add_entry(entry=entry)
print(form_page.to_xml())
print()



document.add_page(page1)
document.add_page(page2)

page2.set_form(entry)
page2.remove_form()
#document.add_page(pages=[Page(),Page()], page=basic_page)


print(page1._tag)
print(document.to_xml(True))
print()
"""





print("========= BUILDER =========")

xml = ('<?xml version="1.0" encoding="UTF-8"?>'
        '<!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">'
        '<pages><page tag="page1">it\'s ok<a href="#1">line 1</a><a href="#2">line 2</a></page><page>Nouvelle page ajoutée.</page><page>New page at the specified index</page></pages>'
        )

#print(xml)
#print()

cellcube_xml_builder = CellcubeXmlPageBuilder()


"""
print()
print(":::::::::::")
xml_doc = Document(xml_input=xml) # OK
xml_doc = cellcube_xml_builder.parse_xml_document(xml) # OK
print(xml_doc.xml(True)) # OK
print(":::::::::::")
print()
"""




"""
# Simple page as xml
simple_page_xml = cellcube_xml_builder.build_xml_page(content="Bienvenue sur le service")
print(simple_page_xml) # OK
"""



doc = cellcube_xml_builder.new_cellecube_xml_document()



"""
doc.add_page(page=Page(content="it's ok", tag="page1", links=[Link(href="#1", text="line 1"), Link(href="#2", text="line 2")])) # OK
# print(doc.xml(True)) # OK
doc.add_page("Nouvelle page ajoutée.")
doc.add_page("New page at the specified index") # OK
"""




#the_page = doc.get_page_at_index(0) # OK

"""
the_page = doc.get_page_at_index(0) # OK
links = the_page.links() # OK
print(f"======> {len(links)}") # OK
"""


"""
print(".......")
print(the_page.get_page_text()) # OK
print(the_page.text) # OK
print(".......")
"""


"""
pages = doc.pages() # OK
print(len(pages))
"""

#doc.remove_page_at_index(2) # OK

#doc.add_pages("toto","hello",Page(content="it's ok 2"))
print(doc.xml(True)) # OK
print()

"""
print(cellcube_xml_builder.build_xml_page("c'est la foire")) # OK
"""





"""
#doc.add_page(sample_page)
print("----get_page_at_index---")
#p = doc.get_page_at_index(0)
#print(p.xml(True))
print("B")
print("-----")
"""
