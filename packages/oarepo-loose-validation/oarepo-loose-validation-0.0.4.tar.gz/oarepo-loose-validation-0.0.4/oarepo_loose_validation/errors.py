"""Validation classes for various types of data."""
from __future__ import annotations

import typing

from marshmallow.validate import Length as MaLength
from marshmallow.validate import Equal as MaEqual
from marshmallow.validate import Regexp as MaRegexp
from marshmallow.validate import Predicate as MaPredicate
from marshmallow.validate import NoneOf as MaNoneOf
from marshmallow.validate import OneOf as MaOneOf
from marshmallow.validate import ContainsNoneOf as MaContainsNoneOf
from marshmallow.validate import And as MaAnd
from marshmallow.validate import URL as MaURL
from marshmallow.validate import Email as MaEmail
from marshmallow.validate import Range as MaRange

class OarepoError(str):
    def __init__(self, content, struct= True):
        self.s = content
        self.struct = struct
        self.params = {}

    def __new__(cls, content, *args, **kwargs ):
        return str.__new__(cls, content)

    def format(self, *args, **kwargs):  # known special case of str.format
        self.params = kwargs
        return self

_T = typing.TypeVar("_T")

class Length(MaLength):


    message_min = OarepoError('Shorter than minimum length.', struct=False)
    message_max = OarepoError('Longer than maximum length.', struct=False)
    message_all = OarepoError('Length must be between parameters.', struct=False)
    message_equal = OarepoError('Length must be equal to parameter.', struct=False)

class Equal(MaEqual):

    default_message =  OarepoError('Must be equal to parameter.', struct=False)

class Regexp(MaRegexp):

    default_message = OarepoError("String does not match expected pattern.", struct=False)




class Predicate(MaPredicate):

    default_message = OarepoError("Invalid input.", struct=False)



class NoneOf(MaNoneOf):

    default_message = OarepoError("Invalid input.", struct=False)



class OneOf(MaOneOf):

    default_message = OarepoError("Must be one of parameters.", struct=False)


class ContainsOnly(OneOf):

    default_message = OarepoError("One or more of the choices you made was not in parameters.", struct=False)


class ContainsNoneOf(MaContainsNoneOf):

    default_message = OarepoError("One or more of the choices you made was in parameters.", struct=False)


class And(MaAnd):

    default_error_message = OarepoError("Invalid value.", struct=False)



class URL(MaURL):

    default_message = OarepoError("Not a valid URL.", struct=False)



class Email(MaEmail):

    default_message = OarepoError("Not a valid email address.", struct=False)



class Range(MaRange):


    message_min = OarepoError("Not in defined range.", struct=False)
    message_max = OarepoError("Not in defined range.", struct=False)
    message_all = OarepoError("Not in defined range.", struct=False)
