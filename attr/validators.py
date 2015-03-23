"""
Commonly useful validators.
"""

from __future__ import absolute_import, division, print_function

from ._make import attr, attributes


@attributes(repr=False)
class _InstanceOfValidator(object):
    type = attr()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if not isinstance(value, self.type):
            raise TypeError(
                "'{name}' must be {type!r} (got {value!r} that is a "
                "{actual!r})."
                .format(name=attr.name, type=self.type,
                        actual=value.__class__, value=value),
                attr, self.type, value,
            )

    def __repr__(self):
        return (
            "<instance_of validator for type {type!r}>"
            .format(type=self.type)
        )


def instance_of(type):
    """
    A validator that raises a :exc:`TypeError` if the initializer is called
    with a wrong type for this particular attribute (checks are perfomed using
    :func:`isinstance`).

    :param type: The type to check for.
    :type type: type

    The :exc:`TypeError` is raised with a human readable error message, the
    attribute (of type :class:`attr.Attribute`), the expected type and the
    value it got.
    """
    return _InstanceOfValidator(type)


@attributes(repr=False)
class _ProvidesValidator(object):
    interface = attr()

    def __call__(self, inst, attr, value):
        """
        We use a callable class to be able to change the ``__repr__``.
        """
        if not self.interface.providedBy(value):
            raise TypeError(
                "'{name}' must provide {interface!r} which {value!r} "
                "doesn't."
                .format(name=attr.name, interface=self.interface, value=value),
                attr, self.interface, value,
            )

    def __repr__(self):
        return (
            "<provides validator for interface {interface!r}>"
            .format(interface=self.interface)
        )


def provides(interface):
    """
    A validator that raises a :exc:`TypeError` if the initializer is called
    with an object that does not provide the requested *interface* (checks are
    perfomed using ``value.providedBy(interface)`` (see `zope.interface
    <http://docs.zope.org/zope.interface/>`_).

    :param interface: The interface to check for.
    :type interface: zope.interface.Interface

    The :exc:`TypeError` is raised with a human readable error message, the
    attribute (of type :class:`attr.Attribute`), the expected interface, and
    the value it got.
    """
    return _ProvidesValidator(interface)
