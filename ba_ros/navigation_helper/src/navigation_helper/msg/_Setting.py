"""autogenerated by genmsg_py from Setting.msg. Do not edit."""
import roslib.message
import struct


class Setting(roslib.message.Message):
  _md5sum = "e3da676ea304d6234e6e8b89e57f6e22"
  _type = "navigation_helper/Setting"
  _has_header = False #flag to mark the presence of a Header object
  _full_text = """string navigation
string robot
string scenario
string repository

"""
  __slots__ = ['navigation','robot','scenario','repository']
  _slot_types = ['string','string','string','string']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.
    
    The available fields are:
       navigation,robot,scenario,repository
    
    @param args: complete set of field values, in .msg order
    @param kwds: use keyword arguments corresponding to message field names
    to set specific fields. 
    """
    if args or kwds:
      super(Setting, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.navigation is None:
        self.navigation = ''
      if self.robot is None:
        self.robot = ''
      if self.scenario is None:
        self.scenario = ''
      if self.repository is None:
        self.repository = ''
    else:
      self.navigation = ''
      self.robot = ''
      self.scenario = ''
      self.repository = ''

  def _get_types(self):
    """
    internal API method
    """
    return self._slot_types

  def serialize(self, buff):
    """
    serialize message into buffer
    @param buff: buffer
    @type  buff: StringIO
    """
    try:
      _x = self.navigation
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.robot
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.scenario
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.repository
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize(self, str):
    """
    unpack serialized message in str into this message instance
    @param str: byte array of serialized message
    @type  str: str
    """
    try:
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.navigation = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.robot = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.scenario = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.repository = str[start:end]
      return self
    except struct.error as e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill


  def serialize_numpy(self, buff, numpy):
    """
    serialize message with numpy array types into buffer
    @param buff: buffer
    @type  buff: StringIO
    @param numpy: numpy python module
    @type  numpy module
    """
    try:
      _x = self.navigation
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.robot
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.scenario
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.repository
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
    except struct.error as se: self._check_types(se)
    except TypeError as te: self._check_types(te)

  def deserialize_numpy(self, str, numpy):
    """
    unpack serialized message in str into this message instance using numpy for array types
    @param str: byte array of serialized message
    @type  str: str
    @param numpy: numpy python module
    @type  numpy: module
    """
    try:
      end = 0
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.navigation = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.robot = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.scenario = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.repository = str[start:end]
      return self
    except struct.error as e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill

_struct_I = roslib.message.struct_I