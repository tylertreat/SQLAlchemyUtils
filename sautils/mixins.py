import json

from sqlalchemy import inspect
from sqlalchemy.orm.relationships import RelationshipProperty

from sautils.encoders import DateTimeEncoder


class SerializeMixin(object):
    """This mixin allows arbitrary SQLAlchemy models to be serialized to dicts
    and subsequently to JSON (and potentially other formats).
    """

    def to_dict(self, follow_rels=False, force_serialization=False):
        """Convert the model to a dict.

        Args:
            follow_rels: boolean indicating if related models should included
                         in the dict. If True, the object graph will be
                         recursively traversed but cycles will be avoided. If
                         False, only non-relationship properties will be
                         included in the dict.
            force_serialization: boolean indicating if every model property
                                 should be included, regardless of whether or
                                 not it has serialize set to False.

        Returns:
            dict representation of the model.
        """
        return _to_dict_rec(self, {}, set(), follow_rels, force_serialization)

    def to_json(self, follow_rels=False, force_serialization=False,
                encoder=DateTimeEncoder):
        """Convert the model to a JSON string.

        Args:
            follow_rels: boolean indicating if related models should be
                         included in the JSON. If True, the object graph will
                         be recursively traversed but cycles will be avoided.
                         If False, only non-relationship properties will be
                         included in the JSON.
            force_serialization: boolean indicating if every model property
                                 should be serialized, regardless of whether
                                 or not it has serialize set to False.
            encoder: the JSONEncoder type to use.

        Returns:
            JSON representation of the model.
        """
        return json.dumps(
            self.to_dict(follow_rels=follow_rels,
                         force_serialization=force_serialization), cls=encoder)


def _to_dict_rec(obj, data, visited, follow_rels, force_serialization):
    """Transform the model to a dict, recursing on related models if necessary.
    """

    visited.add(obj)

    for prop in inspect(obj.__class__).iterate_properties:
        if not isinstance(prop, RelationshipProperty):
            data[prop.key.lstrip('_')] = getattr(obj, prop.key)

        elif follow_rels and (prop.info.get('serialize', True) or
                              force_serialization):
            relationship = getattr(obj, prop.key)

            if prop.uselist:
                if not relationship:
                    data[prop.key.lstrip('_')] = []

                elif visited & set(relationship):
                    continue

                else:
                    data[prop.key.lstrip('_')] = [_to_dict_rec(
                        related, dict(), visited, follow_rels,
                        force_serialization)
                        for related in relationship]

            elif relationship not in visited:
                if not relationship:
                    data[prop.key.lstrip('_')] = None

                else:
                    data[prop.key.lstrip('_')] = _to_dict_rec(
                        relationship, dict(), visited, follow_rels,
                        force_serialization)

    return data

