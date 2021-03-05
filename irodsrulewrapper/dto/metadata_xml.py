from typing import List, Dict
import os
from irods import exception
import xml.etree.cElementTree as ET


class MetadataXML:
    def __init__(self,
                 creator: str,
                 token: str,
                 project: str,
                 title: str,
                 description: str,
                 date: str,
                 articles: str):
        self.creator: str = creator
        self.token: str = token
        self.project: str = project
        self.title: str = title
        self.description: str = description
        self.date: str = date
        self.articles: str = articles

    @classmethod
    def create_from_dict(cls, data: Dict) -> 'MetadataXML':
        metadata = cls(data["creator"], data["token"], data["project"],
                       data["title"], data["description"], data["date"], data["articles"])
        return metadata

    def write_metadata_xml(self, session):
        xml = """<?xml version="1.0"?>
<metadata>
  <project>*project</project>
  <title>*title</title>
  <description>*description</description>
  <date>*date</date>
  <factors>
    <factor></factor>
  </factors>
  <organism id=""></organism>
  <tissue id=""></tissue>
  <technology id=""></technology>
  <article></article>
  <creator>*creator</creator>
  <contact>
    <lastName></lastName>
    <firstName></firstName>
    <midInitials></midInitials>
    <email></email>
    <phone></phone>
    <address></address>
    <affiliation></affiliation>
    <role></role>
  </contact>
  <protocol>
    <name></name>
    <filename></filename>
  </protocol>
</metadata>"""

        xml = xml.replace('*project', self.project)
        xml = xml.replace('*title', self.title)
        xml = xml.replace('*description', self.description)
        xml = xml.replace('*date', self.date)
        xml = xml.replace('*creator', self.creator)

        medata_xml = ET.fromstring(xml)

        for article in self.articles.split(","):
            url = "https://doi.org/" + article
            medata_xml.append(ET.fromstring("<article>" + url + "</article>"))

        ET.ElementTree(medata_xml).write("./metadata.xml", encoding='UTF-8', xml_declaration=True)

        ingest_zone = "/nlmumc/ingest/zones/" + self.token + "/" + "metadata.xml"
        session.data_objects.put("./metadata.xml", ingest_zone)

        os.remove("./metadata.xml")

    @classmethod
    def read_metadata_xml(cls, session, token):
        xml_path = "/nlmumc/ingest/zones/" + token + "/" + "metadata.xml"
        # Get metadata.xml
        try:
            with session.data_objects.open(xml_path, 'r') as f:
                metadata_xml = f.read()
        except exception.DataObjectDoesNotExist as e:
            metadata_xml = ""
            # logger.warning("ProjectCollection %s/%s is missing metadata.xml" % (project, collection))

        if metadata_xml == "":
            return

        try:
            root = ET.fromstring(metadata_xml)
            data = {
                "project": root.find("project").text,
                "title": root.find("title").text,
                "description": root.find("description").text,
                "date": root.find("date").text,
                "creator": root.find("creator").text,
                "token": token,
                "articles": read_tag_list(root, "article"),
            }

            return cls(data["creator"], data["token"], data["project"],
                       data["title"], data["description"], data["date"], data["articles"])

        except ET.ParseError:
            # logger.warning("ProjectCollection %s/%s has invalid metadata.xml" % (project, collection))
            return


def read_tag_list(root, tag):
    concatenation = ''
    for k in root.findall(tag):
        for i in k.iter():
            if i.text is not None:
                concatenation += ',' + i.text.replace("https://doi.org/", "")
    return concatenation[1:]


