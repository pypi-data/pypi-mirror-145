from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.feature_create import FeatureCreate
from ..types import UNSET, Unset

T = TypeVar("T", bound="FeatureBulkCreate")


@attr.s(auto_attribs=True, repr=False)
class FeatureBulkCreate:
    """ Inputs for bulk creating a new feature """

    _features: Union[Unset, List[FeatureCreate]] = UNSET

    def __repr__(self):
        fields = []
        fields.append("features={}".format(repr(self._features)))
        return "FeatureBulkCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        features: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._features, Unset):
            features = []
            for features_item_data in self._features:
                features_item = features_item_data.to_dict()

                features.append(features_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if features is not UNSET:
            field_dict["features"] = features

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def get_features() -> Union[Unset, List[FeatureCreate]]:
            features = []
            _features = d.pop("features")
            for features_item_data in _features or []:
                features_item = FeatureCreate.from_dict(features_item_data)

                features.append(features_item)

            return features

        features = get_features() if "features" in d else cast(Union[Unset, List[FeatureCreate]], UNSET)

        feature_bulk_create = cls(
            features=features,
        )

        return feature_bulk_create

    @property
    def features(self) -> List[FeatureCreate]:
        if isinstance(self._features, Unset):
            raise NotPresentError(self, "features")
        return self._features

    @features.setter
    def features(self, value: List[FeatureCreate]) -> None:
        self._features = value

    @features.deleter
    def features(self) -> None:
        self._features = UNSET
