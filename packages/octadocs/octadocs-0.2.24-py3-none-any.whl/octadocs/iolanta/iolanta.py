"""
Iolanta facet management.

This module contains a few functions which later will be refactored into
Iolanta - the generic metaverse/cyberspace browser.
"""
import operator
import pydoc
from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Union

from iolanta.facet import Facet
from iolanta.facets.base import FacetSearchAttempt
from iolanta.facets.by_environment import FindFacetByEnvironment
from iolanta.facets.by_instance import FindFacetByInstance
from iolanta.facets.by_literal_datatype import FindFacetByLiteralDatatype
from iolanta.facets.by_type import FindFacetByType
from ldflex import LDFlex
from octadocs.iolanta.errors import FacetError, FacetNotCallable, FacetNotFound
from octadocs.octiron import Octiron
from rdflib import RDFS
from rdflib.term import Literal, Node, URIRef

HTML = URIRef('https://html.spec.whatwg.org/')


def resolve_facet(iri: URIRef) -> Callable[[Octiron, Node], str]:
    """Resolve a path to a Python object to that object."""
    url = str(iri)

    if not url.startswith('python://'):
        raise Exception(
            'Octadocs only supports facets which are importable Python '
            'callables. The URLs of such facets must start with `python://`, '
            'which {url} does not comply to.'.format(
                url=url,
            )
        )

    # It is impossible to use `urlpath` for this operation because it (or,
    # rather, one of upper classes from `urllib` that `urlpath` depends upon)
    # will lowercase the URL when parsing it - which means, irreversibly. We
    # have to resort to plain string manipulation.
    import_path = url.replace('python://', '').strip('/')

    facet = pydoc.locate(import_path)

    if not callable(facet):
        raise FacetNotCallable(
            path=import_path,
            facet=facet,
        )

    return facet


def render(
    node: Union[str, Node],
    octiron: Octiron,
    environments: Optional[List[URIRef]] = None,
) -> str:
    """Find an Iolanta facet for a node and render it."""
    if not environments:
        environments = [HTML]

    facet_search_attempt = Render(
        ldflex=octiron.ldflex,
    ).search_for_facet(
        node=node,
        environments=environments,
    )

    facet = resolve_facet(
        iri=facet_search_attempt.facet,
    )

    facet = facet(
        iri=node,
        octiron=octiron,
        environment=facet_search_attempt.environment,
    )

    if isinstance(facet, Facet):
        try:
            return facet.render()

        except (FacetError, FacetNotFound):   # noqa: WPS329
            # Prevent nested `FacetError` exceptions.
            raise

        except Exception as err:
            raise FacetError(
                node=node,
                facet_iri=facet_search_attempt.facet,
                facet_search_attempt=facet_search_attempt,
                error=err,
            ) from err

    return facet


@dataclass
class Render:
    """Facet renderer."""

    ldflex: LDFlex

    def search_for_facet(
        self,
        node: Node,
        environments: List[URIRef],
    ) -> FacetSearchAttempt:
        """Find facet IRI for given node for all environments given."""
        facet_search_attempts = list(
            self.attempt_search_for_facet(
                node=node,
                environments=environments,
            ),
        )

        *failures, success = facet_search_attempts

        if success:
            return success

        raise FacetNotFound(
            node=node,
            environments=environments,
            facet_search_attempts=facet_search_attempts,
        )

    def find_facet_iri(
        self,
        node: Node,
        environments: List[URIRef],
    ) -> URIRef:
        """Find facet IRI for given node for all environments given."""
        return self.search_for_facet(
            node=node,
            environments=environments,
        ).facet

    def attempt_search_for_facet(
        self,
        node: Node,
        environments: List[URIRef],
    ) -> Iterable[FacetSearchAttempt]:
        """
        Stream of attempts to find a facet.

        If this function yields a sequence of N elements, first (N - 1) of those
        are guaranteed to be failures. The remaining one element can be both
        a failure (if nothing was found) or a success (if a facet was found).
        """
        for environment in environments:
            facet_searches = self.find_facet_iri_per_environment(
                node=node,
                environment=environment,
            )

            for facet_search in facet_searches:
                yield facet_search

                if facet_search:
                    return

    def find_facet_iri_per_environment(
        self,
        node: Node,
        environment: URIRef,
    ):
        """Find facet IRI for given node in given env."""
        if isinstance(node, Literal):
            yield from self.find_facet_iri_for_literal(
                literal=node,
                environment=environment,
            )

        yield FindFacetByInstance(
            ldflex=self.ldflex,
            node=node,
            environment=environment,
        )

        instance_types = self.find_instance_types(node)
        for instance_type in instance_types:
            yield FindFacetByType(
                ldflex=self.ldflex,
                node=node,
                environment=environment,
                instance_type=instance_type,
            )

        yield FindFacetByEnvironment(
            ldflex=self.ldflex,
            node=node,
            environment=environment,
        )

    def __call__(
        self,
        node: Node,
        environment: URIRef,
    ) -> str:
        ...

    def find_facet_iri_for_literal(self, literal: Literal, environment: URIRef):
        """Find facet IRI for a literal."""
        if literal.datatype is not None:
            yield FindFacetByLiteralDatatype(
                ldflex=self.ldflex,
                node=literal,
                environment=environment,
            )

        yield FindFacetByType(
            ldflex=self.ldflex,
            node=literal,
            environment=environment,
            instance_type=RDFS.Literal,
        )

        yield FindFacetByEnvironment(
            ldflex=self.ldflex,
            node=literal,
            environment=environment,
        )

    def find_instance_types(self, node: URIRef) -> List[URIRef]:
        """Find types for particular node."""
        rows = self.ldflex.query(
            query_text='''
            SELECT ?type WHERE {
                $node rdf:type ?type .
            }
            ''',
            node=node,
        )

        return list(
            map(
                operator.itemgetter('type'),
                rows,
            ),
        )
