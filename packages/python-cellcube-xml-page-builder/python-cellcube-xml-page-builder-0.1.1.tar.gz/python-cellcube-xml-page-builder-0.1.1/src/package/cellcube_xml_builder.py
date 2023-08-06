

from cellcube_xml_elements import CellcubeXmlDocument, CellcubeXmlElement, CellcubeXmlPage, CellcubeXmlPageLink

class Part():

    def __init__(self, attributes:dict=dict(), root_tag_name:str="element", features="html.parser"):
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlElement(root_tag_name=root_tag_name, features=features)
        for key in attributes:
            self._cellcube_xml_element.set_attribute(attribute=key, value=attributes[key])

    def _set_attribute(self, name:str, value):
        self._cellcube_xml_element.set_attribute(attribute=name,value=value)
        return self

    def _get_attribute(self, name:str, default=None):
        return self._cellcube_xml_element.get_attribute(name,default_value=default)        

    def xml(self, beautify:bool=False, indent_level=1):
        result =  self._cellcube_xml_element.to_xml(beautify=beautify, indent_level=indent_level) if self._cellcube_xml_element is not None else f"<{self._root_tag_name}></{self._root_tag_name}>"
        return result

    def cellcube_xml_element(self):
        return self._cellcube_xml_element 

    def cellcube_xml_element_tag(self):
        return self._cellcube_xml_element.tag() if self._cellcube_xml_element is not None else None

    def __str__(self):
        return self.xml()

    

    
class Link(Part):
    def __init__(self, href:str=None, text=str, key:str=None, attributes:dict=dict(), root_tag_name="a", cellcube_xml_page_link=None):
        self._attributes = attributes
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlPageLink(href=href, key=key, content=text, root_tag_name=self._root_tag_name, attributes=attributes)
        self.text = text
        self.key = key
        self.href = href  
        self.set_cellcube_xml_page_link(cellcube_xml_page_link)

    def set_link_text(self, text:str):
        self.text = text
        self._cellcube_xml_element.set
        return self

    def get_link_text(self) -> str:
        return self._cellcube_xml_element.get_link_content()

    def set_link_attribute(self, attribute_name:str, attribute_value): 
        if (str(attribute_name).lower() == "href"):
            self.href = attribute_value      
        if (str(attribute_name).lower() == "key"):
            self.key = attribute_value         
        self._set_attribute(name=attribute_name,value=attribute_value)
        return self

    def get_link_attribute(self, attribute_name:str, default:None):        
        self._get_attribute(attribute_name=attribute_name,default=default)
        return self

    def set_cellcube_xml_page_link(self, cellcube_xml_page_link:CellcubeXmlPageLink):
        if cellcube_xml_page_link is not None:
            self._cellcube_xml_element = cellcube_xml_page_link
        return self
        
    

class Form:
    pass

class Page(Part):

    def __init__(self, content:str=None, tag:str=None, form:Form=None, links:list[Link]=(), attributes:dict=dict(), default_language="en", root_tag_name="page", cellcube_xml_page:CellcubeXmlPage=None):
        
        self._attributes = attributes
        
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlPage(default_language=default_language, page_tag=tag, content=content, root_tag_name=self._root_tag_name)
        self.content = content
        
        self.set_page_text(content)
        #self.links_ = links
        self.form = form
        self.tag = tag
        
        # Set page attributes
        for key in attributes:
            self._attributes[key]=attributes[key]

        # Set page links
        for link in links:
            self.add_link(link=link)

        self.set_cellcube_xml_page(cellcube_xml_page)

    @property
    def text(self):
        return self.get_page_text()

    @text.setter
    def temperature(self, value):
        self.set_page_text(value)

    def set_cellcube_xml_page(self, cellcube_xml_page:CellcubeXmlPage):
        if cellcube_xml_page is not None:
            self._cellcube_xml_element = cellcube_xml_page
        return self

    def set_page_attribute(self, attribute_name:str, attribute_value):        
        self._set_attribute(name=attribute_name,value=attribute_value)
        return self

    def get_page_attribute(self, attribute_name:str, default:None):
        self._get_attribute(attribute_name=attribute_name,default=default)
        return self

    def set_tag(self, tag:str):
        self.set_page_attribute(name="tag",value=tag)
        return self

    def get_tag(self):
        return self.get_page_attribute("tag")

    def set_descr(self, descr:str):
        self._set_attribute(name="descr",value=descr)
        return self

    def get_descr(self):
        return self._get_attribute("descr")

    def set_page_text(self, text:str):
        self._cellcube_xml_element.set_page_content(content=text)
        self.content=text
        return self

    def get_page_text(self) -> str:   
        return self._cellcube_xml_element.get_page_content() 

    def clear_page_text(self):
        self._cellcube_xml_element.remove_page_content()
        self.content=None
        return self

    def set_form(self, form:Form):
        return self

    def get_form(self):
        return self.form


    def add_link(self, link:Link):
        self._cellcube_xml_element.add_link(link.cellcube_xml_element())
        return self
        
    def get_link_at_index(self, index:int):
        # A implémenter
        try:
            return self.links_[index]
        except:
            pass
        return self

    def remove_link_at_index(self, index:int):
        self._cellcube_xml_element.remove_link(index)
        return self


    def links(self) -> tuple[Link]:        
        """Return links"""
        # Get all page tags
        links = []
        cellcube_xml_page_links = self._cellcube_xml_element.links()
        for cellcube_xml_page_link in cellcube_xml_page_links:
            links.append(Link(cellcube_xml_page_link=cellcube_xml_page_link))
        return (links)




    def __str__(self) -> str:
        return super().__str__()


class Document(Part):
    
    def __init__(self, page:Page=Page(), pages:list[Page]=[], attributes:dict=dict(), default_language="en", root_tag_name="pages", document_prologue='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">', include_prologue=True, xml_input=None, include_default_page=True):
        self._attributes = attributes
        self._root_tag_name=root_tag_name
        self._cellcube_xml_element = CellcubeXmlDocument(root_tag_name=self._root_tag_name, default_language=default_language, document_prologue=document_prologue, include_prologue=include_prologue, xml_input=xml_input)
        
        #self.pages_ = pages
        
        if xml_input is not None:
            for key in attributes:
                self._set_attribute(key, attributes[key])

            if page is not None:
                self.add_page(page=page)

        

    def add_pages(self, *args):
        for arg in args: 
            if type(arg) is str:
                self.add_page(content=arg)
            if (type(arg) is Page):
                self.add_page(page=arg)
        return self


    def add_page(self, content:str=None, page:Page=None, position=None):
        if content is not None and page is None:
            page = Page(content=content)
        self._cellcube_xml_element.add_single_page(page.cellcube_xml_element(),position=position)       
        return self

    def get_page_at_index(self, index:int) -> Page:  
        cellcube_xml_page = self._cellcube_xml_element.get_page_at_position(index)  
        page = Page(cellcube_xml_page=cellcube_xml_page)
        return page
        

    def remove_page_at_index(self, index:int):
        self._cellcube_xml_element.remove_page_at_position(position=index)    
        return self

    def pages(self) -> tuple[Page]:        
        """Return pages"""
        # Get all page tags
        pages = []
        cellcube_xml_pages = self._cellcube_xml_element.get_pages()
        for cellcube_xml_page in cellcube_xml_pages:
            pages.append(Page(cellcube_xml_page=cellcube_xml_page))
        return (pages)

    def xml(self, beautify=False, indent_level=1) -> str:
        xml = Part.xml(self,beautify=beautify,indent_level=indent_level)
        #xml = self._cellcube_xml_element.tag() if self._cellcube_xml_element is not None else ""
        if self._cellcube_xml_element.include_prologue:
            if beautify is True:
                xml = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">\n' + xml
            else:
                xml = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">' + xml
        
        return xml
        #return self._cellcube_xml_element.tag() if self._cellcube_xml_element is not None else None


class CellcubeXmlPageBuilder:

    def __init__(self):
        pass

    
    def build_xml_page(self, content:str="", page_tag:str=None, root_tag_name:str="page", default_language:str="en", links:list[Link]=[], attributes:dict=dict(), as_document:bool=False, beautify=False) -> str:
        
        xml_document = Document(page=Page(
            content=content
            , tag=page_tag
            , default_language=default_language
            , root_tag_name=root_tag_name
            , links=links
            , attributes=attributes
        ))

        
        return xml_document.xml(beautify=beautify) if not as_document  else xml_document

    def build_xml_form_page(self):
        pass

    def new_cellecube_xml_document(self, page:Page=None, pages:list[Page]=[], attributes:dict=dict(), default_language="en", root_tag_name="pages", document_prologue='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">', include_prologue=True):
        return Document(page=page, pages=pages, attributes=attributes, default_language=default_language, root_tag_name=root_tag_name, document_prologue=document_prologue, include_prologue=include_prologue)

    def parse_xml_document(self, string:str) -> Document:
        return Document(xml_input=string)

