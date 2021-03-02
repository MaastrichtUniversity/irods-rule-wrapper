from typing import List, Dict
import os
from irods import exception
import xml.etree.cElementTree as ET


class MetadataXML:
    def __init__(self, creator: str, token: str, project: str, title: str, date: str):
        self.creator = creator
        self.token = token
        self.project = project
        self.title = title
        self.date = date

    @classmethod
    def create_from_dict(cls, data: Dict) -> 'MetadataXML':
        metadata = cls(data["creator"], data["token"], data["project"], data["title"], data["date"])
        return metadata

    def write_metadata_xml(self, session):
        xml = """<?xml version="1.0"?>
<metadata>
  <project>*project</project>
  <title>*title</title>
  <description></description>
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
        xml = xml.replace('*date', self.date)
        xml = xml.replace('*creator', self.creator)

        with open("./metadata.xml", "w+") as f:
            f.write(xml)

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
                "token": token
            }

            return cls(data["creator"], data["token"], data["project"], data["title"], data["date"])

        except ET.ParseError:
            # logger.warning("ProjectCollection %s/%s has invalid metadata.xml" % (project, collection))
            return
