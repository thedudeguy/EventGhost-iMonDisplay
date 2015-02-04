from ctypes import c_int

class EnumMember(object):
    """
    A storage structure class that represents a single
    Enum Member, containing all relavent information about the enum

    Instance of this class are generally instantiated in the ImonEnum class.

    Notes
    -----
    All attributes can not be modified after being set

    Attributes
    ----------
    name : string
        The name of the Enum Member
    value : int
        The value of the Enum Member

    """

    def __init__(self, name, value):
        """
        Constructor

        Parameters
        ----------
        name : string
            The name of this enum
        value : int
            the value of this enum

        """
        self.__dict__['name'] = name
        self.__dict__['value'] = value

    def __setattr__(self, name, value):
        """Prevents any modifications from being made the attributes."""
        raise AttributeError, "Attributes can not be modified"


    def __repr__(self):
        """Machine Readable Output"""
        return "(" + str(self.name) + ", " + str(self.value) + ")"

    def __str__(self):
        """Human Readable Output"""
        return self.__class__.__name__ + " " + str(self.name) + " (" + str(self.value) + ")"

    def __eq__(self, other):
        """Comparative / Sorting"""
        return ((self.name, self.value) == (other.name, other.value))

    def __ne__(self, other):
        """Comparative / Sorting"""
        return not self == other

    def __gt__(self, other):
        """Comparative / Sorting"""
        return (self.name, self.version) > (other.name, other.value)

    def __lt__(self, other):
        """Comparative / Sorting"""
        return (self.name, self.version) < (other.name, other.value)

    def __ge__(self, other):
        """Comparative / Sorting"""
        return (self > other) or (self == other)

    def __le__(self, other):
        """Comparative / Sorting"""
        return (self < other) or (self == other)

class ImonEnum(object):
    """
    Created Enum type objects.
    This was specifically created to be used with the IMON API.

    Notes
    -----
    All attributes can not be modified after being set.
    The class instance itself can be called as a function in order to perform a
    reverse lookup, returning an Enum by value, instead of name

    Attributes
    ----------
    members : dict
        This dictionary holds all the defined Enum Members

    Example
    -------
    >>> MyEnum = ImonEnum(("ENUM1", 0), ("ENUM2",), ("ENUM3", 10), ("ENUM4",))
    >>> MyEnum.ENUM1
    (ENUM1, 0)
    >>> MyEnum.ENUM4.value
    11
    >>> MyEnum(1)
    (ENUM2, 1)
    >>> MyEnum.ENUM3 == MyEnum(10)
    True

    """

    _nextAutoVal = 0

    def __init__(self, *enums):
        """
        Constructor

        Notes
        -----
        Each item passed in should be a key-value tuple. A tuple
        can be only a name, with no value, and the value will be
        generated, by incrementing the previous item's value by 1.

        These Tuples will be created automatically into an EnumMember instance

        Parameters
        ----------
        *enums :
            Variable length argument list, each arg passed should
            be a tuple key-value pair.
        value : int
            the value of this enum

        """
        #set up the members
        self.__dict__['members'] = {}

        #add items to the members dict
        for enum in enums:
            # first should always be the name
            name = enum[0]
            # second value, if it exists, is the value, or use the autoval
            value = c_int(enum[1]).value if len(enum)>1 else ImonEnum._nextAutoVal
            ImonEnum._nextAutoVal = value + 1
            self.__dict__['members'][name] = EnumMember(name, value)

    def __str__(self):
        """Human Readable Output"""
        sb = ""
        for name, enum in self.members.iteritems():
            sb = sb + str(enum) + "\n"
        return self.__class__.__name__ + "\n" + sb

    def __setattr__(self, name, value):
        """Prevents any changes from being made to the enum"""
        raise AttributeError, "Attributes can not be modified"

    def __getattr__ (self, attribute):
        """
        Allows for attributes to be called and mapped to any existing enums
        such as:

            MyEnum.SOMEENOMENAME

        Raises
        ------
        AttributeError
            Raised if no matching enums were found with the matching attribute name

        Return
        ------
        EnumMember
            The enum that matches the attribute

        """
        if attribute in self.members:
            return self.members[attribute]
        raise AttributeError

    def __call__(self, byValue):
        """
        Allows for a reverse lookup of an enum by its value, such as:

            MyEnum(10)

        Raises
        ------
        LookupError
            Raised if either there were no entries found that matched the value,
            or if there were too many entries found, such as 2 enums with the same value
            which would have an ambiguous result.

        Parameters
        ----------
        byValue :
            The value of the enum to search for.

        Returns
        -------
        EnumMember
            The enum that matches the Value provided

        """
        byValue = c_int(byValue).value
        found = []
        for name, enum in self.members.iteritems():
            if enum.value == byValue:
                found.append(enum)
        if len(found) > 1:
            raise LookupError, "Too many results found with a matching value"
        if len(found) < 1:
            raise LookupError, "No matching items with a matching value"
        return found[0]
