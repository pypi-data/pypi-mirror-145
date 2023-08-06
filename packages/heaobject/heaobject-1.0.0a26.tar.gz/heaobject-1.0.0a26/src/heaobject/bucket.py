import json
import typing
from typing import Optional, Union, List, Dict
from . import root
from .data import DataObject, SameMimeType
from abc import ABC

from .root import Tag


class Bucket(DataObject, ABC):
    """
    Abstract base class for user accounts.
    """
    pass


class AWSBucket(Bucket, SameMimeType):
    """
    Represents an AWS Bucket in the HEA desktop. Contains functions that allow access and setting of the value.
    """

    def __init__(self):
        super().__init__()
        self.__arn: Optional[str] = None
        self.__s3_uri: Optional[str] = None
        self.__encrypted: Optional[bool] = None
        self.__versioned: Optional[bool] = None
        self.__locked: Optional[bool] = None
        self.__region: Optional[str] = None
        self.__size: Optional[float] = None
        self.__object_count: Optional[int] = None
        self.__tags: List[Tag] = []
        self.__permission_policy: Optional[str] = None

    @classmethod
    def get_mime_type(cls) -> str:
        """
        Returns the mime type for AWSBucket objects.

        :return: application/x.awsbucket
        """
        return 'application/x.awsbucket'

    @property
    def mime_type(self) -> str:
        """Read-only. The mime type for AWSBucket objects, application/x.awsbucket."""
        return type(self).get_mime_type()

    @property
    def arn(self) -> Optional[str]:
        """Returns the aws arn str for identifying resources on aws"""
        return self.__arn

    @arn.setter
    def arn(self, arn: Optional[str]) -> None:
        """Sets the numerical account identifier"""
        self.__arn = str(arn) if arn is not None else None

    @property
    def s3_uri(self) -> Optional[str]:
        """the aws arn str for identifying resources on aws"""
        return self.__s3_uri

    @s3_uri.setter
    def s3_uri(self, s3_uri: Optional[str]) -> None:
        """Sets the aws s3 uri str"""
        self.__s3_uri = str(s3_uri) if s3_uri is not None else None

    @property
    def encrypted(self) -> Optional[bool]:
        """Returns the is encrypted flag for bucket"""
        return self.__encrypted

    @encrypted.setter
    def encrypted(self, is_encrypted: Optional[bool]) -> None:
        """Sets the is encrypted flag for bucket"""
        if type(is_encrypted) is not None and type(is_encrypted) is not bool:
            raise TypeError("is_encrypted is a boolean")
        self.__encrypted = is_encrypted

    @property
    def versioned(self) -> Optional[bool]:
        """Returns the is versioned flag for bucket"""
        return self.__versioned

    @versioned.setter
    def versioned(self, is_versioned: Optional[bool]) -> None:
        """Sets the is versioned flag for bucket"""
        if type(is_versioned) is not None and type(is_versioned) is not bool:
            raise TypeError("is_version is a boolean")
        self.__versioned = is_versioned

    @property
    def locked(self) -> Optional[bool]:
        """Returns the  flag that objects are 'locked' for bucket"""
        return self.__locked

    @locked.setter
    def locked(self, is_locked: Optional[bool]) -> None:
        """Sets the flag that objects are 'locked'"""
        if type(is_locked) is not None and type(is_locked) is not bool:
            raise TypeError("is_locked is a boolean")
        self.__locked = is_locked

    @property
    def region(self) -> Optional[str]:
        """Returns the bucket region"""
        return self.__region

    @region.setter
    def region(self, region: Optional[str]) -> None:
        """Sets the bucket region"""
        self.__region = str(region) if region is not None else None

    @property
    def size(self) -> Optional[float]:
        """Returns the bucket size"""
        return self.__size

    @size.setter
    def size(self, size: float) -> None:
        """Sets the bucket size"""
        self.__size = float(size) if size is not None else None

    @property
    def object_count(self) -> Optional[int]:
        """Returns the number of objects in the bucket"""
        return self.__object_count

    @object_count.setter
    def object_count(self, object_count: int) -> None:
        """Sets the number of objects in the bucket"""
        self.__object_count = int(object_count) if object_count is not None else None

    @property
    def tags(self) -> List[Tag]:
        """Returns the bucket tags"""
        return self.__tags

    @tags.setter
    def tags(self, tags: List[Tag]) -> None:
        """Sets the bucket tags"""
        if tags is not None and type(tags) is not list:
            raise ValueError("This format is not correct for tags, type should be list")
        if len(tags) > 0 and not isinstance(tags[0], Tag):
            raise ValueError("This format is not correct list must contain tags")
        self.__tags = tags if tags is not None else []

    @property
    def permission_policy(self) -> str:
        """Returns the permission policy as string representation of json"""
        return self.__permission_policy

    @permission_policy.setter
    def permission_policy(self, permission_policy: Optional[str] = None) -> None:
        """Sets the permission policy as json str"""

        if permission_policy is not None and type(permission_policy) is not str:
            """testing if valid json str"""
            raise ValueError("not valid permission policy json, type should be str.")

        self.__permission_policy = permission_policy if permission_policy is not None else None
