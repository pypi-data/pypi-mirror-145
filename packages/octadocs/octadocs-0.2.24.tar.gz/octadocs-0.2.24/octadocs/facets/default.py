from dominate.tags import a, span  # noqa: WPS347
from iolanta.facet import Facet
from more_itertools import first
from rdflib.term import Literal


class Default(Facet):
    """Default facet for rendering an unknown node."""

    def render(self):   # noqa: C901
        """Render HTML."""
        if isinstance(self.iri, Literal):
            return str(self.iri.value)

        descriptions = self.query(
            query_text='''
            SELECT * WHERE {
                OPTIONAL {
                    ?page rdfs:label ?label .
                }

                OPTIONAL {
                    ?page octa:symbol ?symbol .
                }

                OPTIONAL {
                    ?page octa:url ?url .
                }

                OPTIONAL {
                    ?page rdfs:comment ?comment .
                }

                OPTIONAL {
                    ?page a octa:Page .
                    BIND(true AS ?is_page)
                }
            } ORDER BY ?label LIMIT 1
            ''',
            page=self.iri,
        )

        try:
            description = first(descriptions)
        except ValueError:
            return str(self.iri)

        label = description.get('label', str(self.iri))
        url = description.get('url')

        symbol = description.get('symbol')
        if not symbol:
            symbol = ''

        comment = description.get('comment')

        if url:
            return a(
                symbol,
                label,
                href=url,
                title=comment,
            )

        if comment:
            return span(label, title=comment)

        return label
