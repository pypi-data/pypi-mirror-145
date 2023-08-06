# -*- coding: utf-8 -*-

"""Termbase processor module.

This module contains the termbase processor classes for nafigator

"""

from .nafdocument import NafDocument
from .utils import sublist_indices
from .const import EntityElement
from lxml import etree

NAMESPACES = {
    None: "urn:iso:std:iso:30042:ed-2",
}

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

def QName(prefix: str = None, name: str = None):
    """ """
    if prefix is None:
        qname = etree.QName("{urn:iso:std:iso:30042:ed-2}" + name, name)
    else:
        qname = etree.QName("{" + namespaces[prefix] + "}" + name, name)
    return qname


def process_termbase(doc: NafDocument = None, 
                     termbase: etree._ElementTree = None, 
                     remove_all_existing_terms: bool = True,
                     params: dict = {}):

    # delete existing term entities?

    if doc is None:
        logging.info("No naf document to process termbase.")
        return None

    if termbase is None:
        logging.info("No termbase to process.")
        return None

    if remove_all_existing_terms:
        for term in termbase.xpath("//entity[@type=\'Term\']"):
            term.getparent().remove(term)

    doc_word_id = {word['id']: word for word in doc.text}
    doc_terms = doc.terms
    for term in doc_terms:
        term['text'] = " ".join([doc_word_id[s['id']]['text'] for s in term['span']])
    term_ids = [term['id'] for term in doc_terms]

    num_entities = len(doc.entities)
    
    for concept in termbase.findall("text/body/conceptEntry", namespaces=NAMESPACES):
        concept_id = concept.attrib["id"]
        for langSec in concept:
            if langSec.tag == QName(name="langSec"):
                language = langSec.attrib[XML_LANG]
                if language == doc.language:
                    for termSec in langSec:
                        term_text = ""
                        term_type = ""
                        term_lemma = ""
                        for item in termSec:
                            if item.tag == QName(name="term"):
                                term_text = item.text
                            if item.tag == QName(name="termNote") and item.attrib['type']=='termType':
                                term_type = item.text
                            if item.tag == QName(name="termNote") and item.attrib['type']=='termLemma':
                                term_lemma = item.text
                        if term_text != "" and term_type != "":
                            if term_lemma != "":
                                # if the lowercase lemma is available then it is used
                                sub = term_lemma.lower().split(" ")
                                full = [term['lemma'].lower() for term in doc_terms]
                            else:
                                # otherwise the lowercase plain text is used
                                sub = term_text.lower().split(" ")
                                full = [term['text'].lower() for term in doc_terms]
                            spans = [[term_ids[i] for i in item] for item in sublist_indices(sub, full)]
                            ext_refs = [{"reference": concept_id+":"+term_type}]
                            comment = [term_text]
                            for span in spans:
                                entity_data = EntityElement(
                                    id="e"+str(num_entities+1),
                                    type="Term", # for now we introduce a new type
                                    status=None,
                                    source=None,
                                    span=span,
                                    ext_refs=ext_refs,
                                    comment=comment,
                                )
                                num_entities += 1
                                doc.add_entity_element(data = entity_data,
                                                       naf_version = doc.version,
                                                       comments = term_text)

    return None
