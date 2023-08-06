from array import array
from types import NoneType
from bs4 import BeautifulSoup, NavigableString, Tag




class CellcubeXmlElement: 

    def __init__(self, root_tag_name=None, xml=None, features="html.parser"):
        self._root_tag_name = root_tag_name
        self._soup = self._get_soup(xml, features=features)  
        self._tag =  self._soup.find(self._root_tag_name)

    def _get_soup(self, text, features="html.parser") -> BeautifulSoup  :
        soup = BeautifulSoup(text, features=features) 
        return soup

    def root_tag_name(self):
        return self._root_tag_name     

    def set_attribute(self, attribute:str, value:str) :
        if self._tag is not None and attribute is not None:
            if value is not None:
                self._tag[attribute] = value
            else:
                if attribute in self._tag.attrs:
                    del self._tag[attribute]
        return self

    def get_attribute(self, attribute:str, default_value=None) :
        if type(attribute) is str and attribute in self._tag:
            return self._tag[attribute]
        else:
            return default_value

    

    def to_xml(self, beautify=False, indent_level=1):

        if beautify:            
            return  self._tag.prettify()
        return str(self._tag)

    def tag(self):
        return self._tag

    def remove(self):
        if self._tag is not None:           
            self._tag.extract()

    def clear(self):
        if self._tag is not None: 
            self._tag.clear()


    def __str__(self):
        return self.to_xml()



class CellcubeXmlPageLink(CellcubeXmlElement):

    def __init__(self, href=None, content=None, root_tag_name="a", key=None, attributes:dict=dict()):
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name} href="{href}">{content}</{root_tag_name}>')
        
        self.set_link_content(str(content))
        
        
        if key is not None:        
            attributes["key"]=key

        for key in attributes:
            self.set_link_attribute(key,attributes[key])
        
    def set_link_content(self, content:str):
        self._tag.clear()
        self._tag.append(NavigableString(content if content is not None else ""))
        return self


    def get_link_content(self):
        return self._tag.string
    
    def set_link_attribute(self, attribute:str, value:str) :
        self.set_attribute(attribute=attribute,value=value)
        return self



class CellcubeXmlFormEntry(CellcubeXmlElement):
    def __init__(self, prompt, variable_name, kind=None,  default_language="en", root_tag_name="entry", prompt_tag_name="prompt" ):
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name}><{prompt_tag_name}></{prompt_tag_name}></{root_tag_name}>')
        self.default_language = default_language    
        self.set_attribute("var",variable_name)
        self.set_attribute("kind",kind)
        self._prompt_tag = self._soup.find(prompt_tag_name)
        self._prompt_tag.append(NavigableString(prompt if prompt is not None else ""))

        self.prompt = prompt
        self.var = variable_name
        self.kind = kind

    def set_prompt(self, prompt:str):
        self.prompt = prompt
        if self._prompt_tag is not None:
            self._prompt_tag.clear()
            self._prompt_tag.append(NavigableString(prompt if prompt is not None else ""))
        return self


    def set_variable_name(self, variable_name:str):
        self.var = variable_name
        if self._tag is not None:
            if variable_name is not None:
                self._tag["var"] = variable_name
            else:
                if "var" in self._tag.attrs:
                    del self._tag["var"]
        return self
    
    def set_kind(self, kind:str):
        self.kind = kind
        self.var = kind
        if self._tag is not None:
            if kind is not None:
                self._tag["kind"] = kind
            else:
                if "kind" in self._tag.attrs:
                    del self._tag["kind"]
        return self

    def set_default_language(self, default_language:str):
        self.default_language = default_language   
    

    def get_prompt(self):
        return self.prompt

    def get_variable_name(self):
        return self.var

    def get_kind(self):
        return self.kind

    def get_default_language(self):
        return self.default_language
        


class CellcubeXmlPage(CellcubeXmlElement):

    def __init__(self, default_language:str="en", root_tag_name:str="page", page_tag:str=None, content:str=""):
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name}></{root_tag_name}>')
        self.default_language = default_language
        if page_tag is not None:
            self.set_page_tag(page_tag)
        content = "" if type(content) is NoneType else content
        self._content = NavigableString(content)
        self._tag.append(self._content)

    

    def parse_from_string(self, xml:str):
        return self

    def set_page_content(self, content:str):
        if content is None: content = ""        
        self._content.extract()
        if ( type(self._content) is NavigableString):
            self._content.extract()
        self._content = NavigableString(content)
        self._tag.insert(0,self._content)
        return self

    def get_page_content(self):        
        return str(self._content)

    def remove_page_content(self):
        if self._content is not None:
            self._content.extract()
        return self
    
    def set_form(self, form_entry:CellcubeXmlFormEntry, form_tag_name:str="form"):
        self._form_tag = self._get_soup(f'<{form_tag_name}></{form_tag_name}>').find(form_tag_name)
        if form_entry is not None:            
            self._form_tag.append(form_entry.tag())
        if self._content is not None:
            self._tag.insert(1, self._form_tag)
        else:
            self._tag.append(self._form_tag)
        return self

    def remove_form(self):
        if self._form_tag is not None:
            self._form_tag.extract()
        return self
        
    def set_page_attribute(self, attribute:str, value:str) :        
        self.set_attribute(attribute=attribute, value=value)
        return self

    def get_page_attribute(self, attribute:str) -> str :
        if attribute in self.tag().attrs:
            return self.tag().attrs[attribute]
        return None
    
    def set_page_tag(self, tag_name:str):
        self.set_page_attribute("tag",tag_name)
        return self

    def get_page_tag(self):
        return self.get_page_attribute("tag")

    
    def content(self):
        return self._content
        

    def add_content_translation(self, language_code:str, text:str):
        return self

    def add_link(self, link:CellcubeXmlPageLink):
        self._tag.append(link.tag())
        return self

    def remove_link(self, position:int):
        link_to_remove = self.get_link_at(position)
        if link_to_remove is not None:
            link_to_remove.tag().extract()
        return self

    def links(self) -> tuple[CellcubeXmlPageLink]:
        result_set = []
        links = self._tag.find_all("a")

        for link_tag in links:
            result_set.append(CellcubeXmlPageLink(href=link_tag.attrs['href'],content=link_tag.string))
            
        result_set = (result_set)        
        return result_set

    def get_link_at(self, position:int) -> CellcubeXmlPageLink:
        cellcube_xml_page_link = None
        links = self._tag.find_all("a")
        if position < len(links):
            cellcube_xml_page_link = CellcubeXmlPageLink(href=links[position].attrs['href'],content=links[position].string)
        return cellcube_xml_page_link
        

    def include_page(self):
        return self



class CellcubeXmlFormPage(CellcubeXmlPage):

    def __init__(self, default_language="en", root_tag_name="page", page_tag=None, content="", method="GET", action="#", form_tag_name="form"):
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=f'<{root_tag_name}></{root_tag_name}>')
        self.default_language = default_language
        self._content = NavigableString("" if content is None else content)
        self._tag.append(self._content)
        self._form_tag = self._get_soup(f'<{form_tag_name}></{form_tag_name}>').find(form_tag_name)
        self._tag.append(self._form_tag)

    def add_entry(self, entry:CellcubeXmlFormEntry):
        self._form_tag.append(entry.tag())
        return self



class CellcubeXmlDocument(CellcubeXmlElement):

    def __init__(self, root_tag_name="pages", default_language="en", document_prologue='<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE pages SYSTEM "cellflash-1.3.dtd">', include_prologue=True, xml_input:str=None):
        self.document_prologue = document_prologue
        self.include_prologue = include_prologue
        self.default_language = default_language
        xml = (
        f'{document_prologue}'
        f'<{root_tag_name}>'
        f'</{root_tag_name}>'
        )
        if xml_input is not None: xml = xml_input
        CellcubeXmlElement.__init__(self,root_tag_name=root_tag_name, xml=xml)

    


    def add_single_page(self, page:CellcubeXmlPage=None,  position=None):
        """
        Add new page element to the xml document
        """
        if isinstance(page, CellcubeXmlPage):
            if position is None:
                self._tag.append(page.tag())
            if type(position) is int:
                if position < len(self._tag.contents) and len(self._tag.contents) > 0:
                    self._tag.insert(position, page.tag())
                else:
                    raise Exception(f"Position is out of bound! Value must be below {len(self._tag.contents)}")
        return self   


    def add_multiple_pages(self, pages: list[CellcubeXmlPage]):
        if type(pages) is list:    
            for page in pages:
                self.add_single_page(page)
        return self 


    def get_page_at_position(self, position:int) -> CellcubeXmlPage:
        if type(position) is int:
            if position < len(self._tag.contents) and len(self._tag.contents) > 0:
                page_tag = self._tag.contents[position]
                cellcube_xml_page = self.parse_page_from_tag(page_tag)
                return cellcube_xml_page
            else:
                raise Exception(f"Position is out of bound! Value must be below {len(self._tag.contents)}")


    def get_pages(self) -> tuple[CellcubeXmlPage]:
        results_set = []
        all_page_tags = self._tag.find_all("page")
        for page_tag in all_page_tags:
            results_set.append(self.parse_page_from_tag(page_tag))
        return (results_set)


    def remove_page_at_position(self, position:int):
        if type(position) is int:
            if position < len(self._tag.contents):
                return self._tag.contents[position].extract()
        return self

    
    def parse_page_from_tag(self, tag:Tag):
        cellcube_xml_page = CellcubeXmlPage()
        if tag is not None:
            # Set page content (text)
            cellcube_xml_page.set_page_content(tag.contents[0])
            # Set page attributes
            for key in tag.attrs:
                cellcube_xml_page.set_attribute(key,tag.attrs[key] )
            # Set page link
            link_tags = tag.find_all("a")
            for link_tag in link_tags:
                cellcube_xml_page_link = CellcubeXmlPageLink(href=link_tag.attrs['href'],content=link_tag.string)
                cellcube_xml_page.add_link(cellcube_xml_page_link)
                
                

        return cellcube_xml_page

    
        

 
        
        
    






