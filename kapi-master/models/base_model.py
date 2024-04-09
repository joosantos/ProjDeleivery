from sql_app import Base
from sqlalchemy.orm.attributes import QueryableAttribute
import json


class BaseModel(Base):
    __abstract__ = True

    def to_json(self, _hide=None, _path=None, _deep=None):
        """Return a dictionary representation of this model."""

        _hide = _hide or []
        _deep = _deep or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        _deep_hidden = (
            self._deep_hidden_fields if hasattr(self, "_deep_hidden_fields") else []
        )
        _deep_hidden = _deep_hidden + _deep

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}
        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            cont = False
            for deep_hided in _deep_hidden:
                if deep_hided in check:
                    cont = True
            if cont:
                continue
            # print(check)

            _hide.append(check)
            is_list = self.__mapper__.relationships[key].uselist
            if is_list:
                items = getattr(self, key)
                if self.__mapper__.relationships[key].query_class is not None:
                    if hasattr(items, "all"):
                        items = items.all()
                ret_data[key] = []
                for item in items:
                    ret_data[key].append(
                        item.to_json(
                            _hide=list(_hide),
                            _path=("%s.%s" % (_path, key.lower())),
                            _deep=_deep_hidden,
                        )
                    )
            else:
                if (
                    self.__mapper__.relationships[key].query_class is not None
                    or self.__mapper__.relationships[key].instrument_class is not None
                ):
                    item = getattr(self, key)
                    if item is not None:
                        ret_data[key] = item.to_json(
                            _hide=list(_hide),
                            _path=("%s.%s" % (_path, key.lower())),
                            _deep=_deep_hidden,
                        )
                    else:
                        ret_data[key] = None
                else:
                    ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            val = getattr(self, key)
            if hasattr(val, "to_json"):
                ret_data[key] = val.to_json(
                    _hide=list(_hide),
                    _path=("%s.%s" % (_path, key.lower())),
                    _deep=_deep_hidden,
                )
            else:
                try:
                    ret_data[key] = json.loads(json.dumps(val))
                except:
                    pass

        return ret_data
