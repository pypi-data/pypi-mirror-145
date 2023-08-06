
class website():
    head= []
    body=[] 
    style=[]   
    def generate(self):
        index = ['<!DOCTYPE html>','<html>','<head>','<meta charset="UTF-8">','\n'.join(self.head),'<style>','\n'.join(self.style),'</style>','</head>', '<body>', '\n'.join(self.body), '</body>', '</html>']
        site = '\n'.join(index)
        return site

#head
    def set_title(self, name:str):
        self.head.insert(len(self.head), f"<title>{name}</title>")
        return name
    
    def set_keywords(self,content:list):
        self.head.insert(len(self.head), f"""<meta name="keywords" content="{', '.join(content)}">""")
        return content

    def set_description(self, desc:str):
        self.head.insert(len(self.head), f'<meta name="description" content="{desc}">')
        return desc

    def set_author(self, name:str):
        self.head.insert(len(self.head), f'<meta name="author" content="{name}">')
        return name

    def set_refresh(self, seconds:int):
        self.head.insert(len(self.head), f'<meta http-equiv="refresh" content="{seconds}">')
        return seconds

        



#body
    def paragraph(self, text:str,types:str=None,name:str=None):
        if (types == "id"or types =="class") and name!=None:
            self.body.insert(len(self.body), f'<p {types}="{name}">{text}</p>')
            if types=="id":
                return f"#{name}"
            else:
                return f".{name}"
        else:
            self.body.insert(len(self.body), f'<p>{text}</p>')
            return "p"
    
    def heading(self, text:str,size:int=1,types:str=None,name:str=None):
        if size >6 or size<1:
            size = 1
        if (types == "id"or types =="class") and name!=None:
            self.body.insert(len(self.body), f'<h{size} {types}="{name}">{text}</h{size}>')
            if types=="id":
                return f"#{name}"
            else:
                return f".{name}"
        else:
            self.body.insert(len(self.body), f'<h{size}>{text}</h{size}>')
            return f"h{size}"

