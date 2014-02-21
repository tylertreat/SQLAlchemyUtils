from datetime import datetime
from datetime import timedelta
import json

import sqlalchemy as sa


class SerializeMixin(object):

    def to_dict(self, follow_rels=False):
        return self._to_dict_rec(self, dict(), set(), follow_rels)

    def to_json(self, follow_rels=False):
        # TODO: Make encoder pluggable.
        return json.dumps(self.to_dict(follow_rels), cls=DateTimeEncoder)

    def _to_dict_rec(self, obj, data, visited, follow_rels):
        visited.add(obj)

        for prop in sa.orm.object_mapper(obj).iterate_properties:
            if not isinstance(prop, sa.orm.properties.RelationshipProperty):
                data[prop.key] = getattr(obj, prop.key)

            elif follow_rels:
                relationship = getattr(obj, prop.key)

                if prop.uselist:
                    if not relationship:
                        data[prop.key] = []

                    elif visited & set(relationship):
                        continue

                    else:
                        data[prop.key] = [self._to_dict_rec(
                            related, dict(), visited, follow_rels)
                            for related in relationship]

                elif relationship not in visited:
                    if not relationship:
                        data[prop.key] = None

                    else:
                        data[prop.key] = self._to_dict_rec(
                            relationship, dict(), visited, follow_rels)

        return data


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime, timedelta)):
            return str(obj)

        return json.JSONEncoder.default(self, obj)

