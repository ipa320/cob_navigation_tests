"""autogenerated by genmsg_py from Status.msg. Do not edit."""
import roslib.message
import struct

import navigation_helper.msg
import std_msgs.msg

class Status(roslib.message.Message):
  _md5sum = "b64ede49ee77a346ac5741a00a9fa384"
  _type = "navigation_helper/Status"
  _has_header = True #flag to mark the presence of a Header object
  _full_text = """Header header
float64 localtime
int32 waypointId
float64 waypointX
float64 waypointY
float64 waypointTheta
string info
Setting setting

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.secs: seconds (stamp_secs) since epoch
# * stamp.nsecs: nanoseconds since stamp_secs
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: navigation_helper/Setting
string navigation
string robot
string scenario
string repository

"""
  __slots__ = ['header','localtime','waypointId','waypointX','waypointY','waypointTheta','info','setting']
  _slot_types = ['Header','float64','int32','float64','float64','float64','string','navigation_helper/Setting']

  def __init__(self, *args, **kwds):
    """
    Constructor. Any message fields that are implicitly/explicitly
    set to None will be assigned a default value. The recommend
    use is keyword arguments as this is more robust to future message
    changes.  You cannot mix in-order arguments and keyword arguments.
    
    The available fields are:
       header,localtime,waypointId,waypointX,waypointY,waypointTheta,info,setting
    
    @param args: complete set of field values, in .msg order
    @param kwds: use keyword arguments corresponding to message field names
    to set specific fields. 
    """
    if args or kwds:
      super(Status, self).__init__(*args, **kwds)
      #message fields cannot be None, assign default values for those that are
      if self.header is None:
        self.header = std_msgs.msg._Header.Header()
      if self.localtime is None:
        self.localtime = 0.
      if self.waypointId is None:
        self.waypointId = 0
      if self.waypointX is None:
        self.waypointX = 0.
      if self.waypointY is None:
        self.waypointY = 0.
      if self.waypointTheta is None:
        self.waypointTheta = 0.
      if self.info is None:
        self.info = ''
      if self.setting is None:
        self.setting = navigation_helper.msg.Setting()
    else:
      self.header = std_msgs.msg._Header.Header()
      self.localtime = 0.
      self.waypointId = 0
      self.waypointX = 0.
      self.waypointY = 0.
      self.waypointTheta = 0.
      self.info = ''
      self.setting = navigation_helper.msg.Setting()

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
      _x = self
      buff.write(_struct_3I.pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_di3d.pack(_x.localtime, _x.waypointId, _x.waypointX, _x.waypointY, _x.waypointTheta))
      _x = self.info
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.navigation
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.robot
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.scenario
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.repository
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
      if self.header is None:
        self.header = std_msgs.msg._Header.Header()
      if self.setting is None:
        self.setting = navigation_helper.msg.Setting()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _struct_3I.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 36
      (_x.localtime, _x.waypointId, _x.waypointX, _x.waypointY, _x.waypointTheta,) = _struct_di3d.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.info = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.navigation = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.robot = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.scenario = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.repository = str[start:end]
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
      _x = self
      buff.write(_struct_3I.pack(_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs))
      _x = self.header.frame_id
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self
      buff.write(_struct_di3d.pack(_x.localtime, _x.waypointId, _x.waypointX, _x.waypointY, _x.waypointTheta))
      _x = self.info
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.navigation
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.robot
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.scenario
      length = len(_x)
      buff.write(struct.pack('<I%ss'%length, length, _x))
      _x = self.setting.repository
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
      if self.header is None:
        self.header = std_msgs.msg._Header.Header()
      if self.setting is None:
        self.setting = navigation_helper.msg.Setting()
      end = 0
      _x = self
      start = end
      end += 12
      (_x.header.seq, _x.header.stamp.secs, _x.header.stamp.nsecs,) = _struct_3I.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.header.frame_id = str[start:end]
      _x = self
      start = end
      end += 36
      (_x.localtime, _x.waypointId, _x.waypointX, _x.waypointY, _x.waypointTheta,) = _struct_di3d.unpack(str[start:end])
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.info = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.navigation = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.robot = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.scenario = str[start:end]
      start = end
      end += 4
      (length,) = _struct_I.unpack(str[start:end])
      start = end
      end += length
      self.setting.repository = str[start:end]
      return self
    except struct.error as e:
      raise roslib.message.DeserializationError(e) #most likely buffer underfill

_struct_I = roslib.message.struct_I
_struct_3I = struct.Struct("<3I")
_struct_di3d = struct.Struct("<di3d")
