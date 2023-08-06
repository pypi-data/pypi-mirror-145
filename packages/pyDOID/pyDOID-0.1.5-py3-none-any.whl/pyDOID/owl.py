"""RDF/OWL file utilities."""

from rdflib import Graph
from os.path import exists
import pandas as pd
import re

from . import util


class functional:
    """OWL functional format class"""
    def __init__(self, path):
        self._path = util.ensure_file(path)

    def extract_class_axioms(self):
        axiom = []
        id_label = {}
        with open(self._path, "r") as file:
            for line in file:
                eq = re.search("EquivalentClasses\(([^ ]+) (.+)", line)
                if eq:
                    axiom.append({
                        "id": eq.group(1),
                        "type": "equivalentClass",
                        "axiom": eq.group(2)
                    })

                sc = re.search("SubClassOf\(([^ ]+) (Object.+)", line)
                if sc:
                    axiom.append({
                        "id": sc.group(1),
                        "type": "subClassOf",
                        "axiom": sc.group(2)
                    })

                il = re.search(
                    'AnnotationAssertion\(rdfs:label ([^ ]+) [\'"]([^\'"]+)',
                    line
                )
                if il: id_label[il.group(1)] = il.group(2)

        for a in axiom:
            if a["id"] in id_label.keys(): a["label"] = id_label[a["id"]]

        col_order = [ "id", "label", "type", "axiom" ]
        df = pd.DataFrame.from_dict(axiom).reindex(columns=col_order)

        return df


class xml:
    """OWL XML format class"""
    def __init__(self, path):
        self.path = util.ensure_file(path)

    def load(self, **kwargs):
        """
        Read RDF/OWL files into Python for querying/manipulation.

        Keyword arguments:
        path -- the path to the RDF/OWL file
        """
        self.graph = Graph().parse(
            source=self.path,
            format="application/rdf+xml",
            **kwargs
        )
        return self

    def query(self, query, reload=False):
        """
        Query a loaded RDF graph with SPARQL.

        Keyword arguments:
        query -- The SPARQL query to execute, as a string or the path to a
            .sparql/.rq file.
        reload -- Whether the owl.xml file should be (re)loaded prior to query
            execution (default: False). When set to True, previously loaded
            information is overwritten. This was created to make iterative
            execution across multiple versions of an owl file more
            straightforrward (eg. iterate through ontology releases).

        :returntype: pandas.DataFrame
        """
        if not isinstance(query, str):
            raise TypeError('query must be a string/path.')

        if exists(query):
            with open(query) as f:
                q = f.read()
        else:
            q = query

        if reload or not hasattr(self, "graph"):
            # instantiate new graph to avoid adding to already loaded Graph
            self.load()

        res = self.graph.query(query_object=q)

        # SPARQLResult to DataFrame solution from Daniel Himmelstein:
        #   https://github.com/RDFLib/sparqlwrapper/issues/125#issuecomment-704291308
        # see also https://github.com/RDFLib/rdflib/issues/1179
        df = pd.DataFrame(
            data=([None if x is None else x.toPython() for x in row] for row in res),
            columns=[str(x) for x in res.vars],
        )

        return df
