from dataclasses import dataclass
from functools import cached_property
from typing import Optional, cast

from iolanta.facets.base import FacetSearchAttempt
from more_itertools import first
from rdflib.term import URIRef


@dataclass
class FindFacetByType(FacetSearchAttempt):
    """
    Find facet by node type.

    Look for such `?facet` that `{self.instance_type}` `iolanta:instanceFacet`
    `?facet`, whereas `?facet` `iolanta:supports` `{self.environment}`.
    """

    instance_type: URIRef

    @cached_property
    def facet(self) -> Optional[URIRef]:
        """Find facet."""
        rows = self.ldflex.query(
            '''
            SELECT ?facet WHERE {
                $instance_type iolanta:instanceFacet ?facet .
                ?facet iolanta:supports $env .
            }
            ''',
            instance_type=self.instance_type,
            env=self.environment,
        )

        try:
            return cast(URIRef, first(rows)['facet'])
        except (ValueError, TypeError):
            return None
