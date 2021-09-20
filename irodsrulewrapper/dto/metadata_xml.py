from typing import List, Dict
import os
from irods import exception
import xml.etree.cElementTree as ET
import json


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
                 technology_label: str,
                 factors: str,
                 contacts: str):

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
        self.factors: str = factors
        self.contacts: str = contacts

    @classmethod
    def create_from_dict(cls, data: Dict) -> 'MetadataXML':
        metadata = cls(data["creator"], data["token"],
                       data["project"], data["title"], data["description"],
                       data["date"], data["articles"],
                       data["organism_id"], data["organism_label"],
                       data["tissue_id"], data["tissue_label"],
                       data["technology_id"], data["technology_label"], data["factors"], data['contacts'])
        return metadata

    def write_metadata_xml(self, session):
        xml = self.build_metadata()
        xml.write("./metadata.xml", encoding='UTF-8', xml_declaration=True)
        ingest_zone = "/nlmumc/ingest/zones/" + self.token + "/" + "metadata.xml"
        session.data_objects.put("./metadata.xml", ingest_zone)
        os.remove("./metadata.xml")

    @classmethod
    def read_metadata_xml(cls, session, xml_path, token=''):
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
                "project": read_text(root, 'project'),
                "title": read_text(root, 'title'),
                "description": read_text(root, 'description'),
                "date": read_text(root, "date"),
                "creator": read_text(root, "creator"),
                "token": token,
                "articles": read_tag_list(root, "article"),
                "organism_id": organism['id'],
                "organism_label": organism['label'],
                "tissue_id": tissue['id'],
                "tissue_label": tissue['label'],
                "technology_id": technology['id'],
                "technology_label": technology['label'],
                "factors": read_tag_node(root, "factors"),
                "contacts": read_contacts(root)
            }

            return cls(data["creator"], data["token"],
                       data["project"], data["title"], data["description"],
                       data["date"], data["articles"],
                       data["organism_id"], data["organism_label"],
                       data["tissue_id"], data["tissue_label"],
                       data["technology_id"], data["technology_label"], data["factors"], data["contacts"])

        except ET.ParseError:
            # logger.warning("ProjectCollection %s/%s has invalid metadata.xml" % (project, collection))
            return

    def build_metadata(self):
        root = ET.Element("metadata")
        ET.SubElement(root, "project").text = self.project
        ET.SubElement(root, "title").text = self.title
        ET.SubElement(root, "description").text = self.description
        ET.SubElement(root, "date").text = self.date
        ET.SubElement(root, "creator").text = self.creator

        if self.organism_label != '':
            ET.SubElement(root, "organism", id=self.organism_id).text = self.organism_label
        else:
            ET.SubElement(root, "organism", id="")
        if self.tissue_label != '':
            ET.SubElement(root, "tissue", id=self.tissue_id).text = self.tissue_label
        else:
            ET.SubElement(root, "tissue", id="")
        if self.technology_label != '':
            ET.SubElement(root, "technology", id=self.technology_id).text = self.technology_label
        else:
            ET.SubElement(root, "technology", id="")

        for article in self.articles.split(","):
            if article != '':
                url = "https://doi.org/" + article
                ET.SubElement(root, "article").text = url
            else:
                ET.SubElement(root, "article")

        factors = ET.SubElement(root, "factors")
        if any(self.factors):
            for factor in self.factors:
                ET.SubElement(factors, "factor").text = factor
        else:
            ET.SubElement(factors, "factor")

        contacts = json.loads(self.contacts)
        for contact in contacts:
            if not is_invalid_contact(contact) or len(contacts) == 1:
                contact_element = ET.SubElement(root, "contact")
                ET.SubElement(contact_element, "lastName").text = contact["LastName"]
                ET.SubElement(contact_element, "firstName").text = contact["FirstName"]
                ET.SubElement(contact_element, "midInitials").text = contact["MidInitials"]
                ET.SubElement(contact_element, "email").text = contact["Email"]
                ET.SubElement(contact_element, "phone").text = contact["Phone"]
                ET.SubElement(contact_element, "address").text = contact["Address"]
                ET.SubElement(contact_element, "affiliation").text = contact["Affiliation"]
                ET.SubElement(contact_element, "role").text = contact["Role"]

        return ET.ElementTree(root)


def read_tag_list(root, tag):
    concatenation = ''
    for k in root.findall(tag):
        for i in k.iter():
            if i.text is not None:
                concatenation += ',' + i.text.replace("https://doi.org/", "")
    return concatenation[1:]


def read_text(root, tag):
    text = root.find(tag).text
    if text is None:
        return ''
    else:
        return text


def read_contacts(root):
    contacts = []
    for contact in root.findall("contact"):
        contact_object = {"LastName": contact.find('lastName').text,
                          "FirstName": contact.find('firstName').text,
                          "MidInitials": contact.find('midInitials').text,
                          "Email": contact.find('email').text,
                          "Phone": contact.find('phone').text,
                          "Address": contact.find('address').text,
                          "Affiliation": contact.find('affiliation').text,
                          "Role": contact.find('role').text}
        contacts.append(contact_object)

    return json.dumps(contacts)


def read_tag(root, tag):
    if root.find(tag).text is not None:
        # Check if the xml tag exist and if it contains an ontology class
        if root.find(tag).get("id") is not None and ":http:" in root.find(tag).get("id"):
            return {"id": root.find(tag).get("id"), "label": root.find(tag).text}
        else:
            return {"id": "", "label": root.find(tag).text}
    else:
        return {"id": "", "label": ""}


def read_tag_node(root, tag):
    node_list = []
    for i in root.iterfind(tag):
        for k in i:
            if k.text is not None:
                node_list.append(k.text)
    return node_list


def is_invalid_contact(contact):
    return contact["LastName"] is None and contact["FirstName"] is None and contact["MidInitials"] is None and contact[
        "Email"] is None and contact["Phone"] is None and contact["Address"] is None and contact[
               "Affiliation"] is None and contact["Role"] is None
