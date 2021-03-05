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
                 articles: str,
                 organism_id: str,
                 organism_label: str,
                 tissue_id: str,
                 tissue_label: str,
                 technology_id: str,
                 technology_label: str):

        self.creator: str = creator
        self.token: str = token
        self.project: str = project
        self.title: str = title
        self.description: str = description
        self.date: str = date
        self.articles: str = articles
        self.organism_id: str = organism_id
        self.organism_label: str = organism_label
        self.tissue_id: str = tissue_id
        self.tissue_label: str = tissue_label
        self.technology_id: str = technology_id
        self.technology_label: str = technology_label

    @classmethod
    def create_from_dict(cls, data: Dict) -> 'MetadataXML':
        metadata = cls(data["creator"], data["token"],
                       data["project"], data["title"], data["description"],
                       data["date"], data["articles"],
                       data["organism_id"], data["organism_label"],
                       data["tissue_id"], data["tissue_label"],
                       data["technology_id"], data["technology_label"])
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

        if self.organism_label != '':
            organism = medata_xml.find("organism")
            organism.set("id", self.organism_id)
            organism.text = self.organism_label

        if self.tissue_label != '':
            tissue = medata_xml.find("tissue")
            tissue.set("id", self.tissue_id)
            tissue.text = self.tissue_label

        if self.technology_label != '':
            technology = medata_xml.find("technology")
            technology.set("id", self.technology_id)
            technology.text = self.technology_label

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
            tissue = read_tag(root, "tissue")
            technology = read_tag(root, "technology")
            organism = read_tag(root, "organism")
            data = {
                "project": root.find("project").text,
                "title": root.find("title").text,
                "description": root.find("description").text,
                "date": root.find("date").text,
                "creator": root.find("creator").text,
                "token": token,
                "articles": read_tag_list(root, "article"),
                "organism_id": organism['id'],
                "organism_label": organism['label'],
                "tissue_id": tissue['id'],
                "tissue_label": tissue['label'],
                "technology_id": technology['id'],
                "technology_label": technology['label']
            }

            return cls(data["creator"], data["token"],
                       data["project"], data["title"], data["description"],
                       data["date"], data["articles"],
                       data["organism_id"], data["organism_label"],
                       data["tissue_id"], data["tissue_label"],
                       data["technology_id"], data["technology_label"])

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


def read_tag(root, tag):
    if root.find(tag).text is not None:
        # Check if the xml tag exist and if it contains an ontology class
        if root.find(tag).get("id") is not None and ":http:" in root.find(tag).get("id"):
            return {"id": root.find(tag).get("id"), "label": root.find(tag).text}
        else:
            return {"id": "", "label": root.find(tag).text}
    else:
        return {"id": "", "label": ""}
