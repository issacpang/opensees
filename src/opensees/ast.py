
def _to_list(val, fmt):
    if isinstance(val, (int,float)):
        return val
    elif isinstance(val, (Int,Num)):
        return val.to_str(fmt)
    elif isinstance(val,list) or hasattr(val,"__array__"):
        return None

class Parameter:
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ
    def __repr__(self):
        return f"${self.name}"

class Arg:
    __slots__ = ["name", "flag", "value", "field", "default", "type", "reqd"]
    def __init__(self,
        name = None,
        help = None,
        flag = None,
        reqd = True,
        type = None,
        field= None,
        about= "",
        default = None,
        **kwds
    ):
        self.name  = name
        self.flag  = [flag] if flag is not None else []
        self.value = None
        self.field = field if field is not None  else name
        self.type  = type
        self.reqd  = reqd
        self.default = default
        self.kwds = kwds
        self.about = about
        self.init()

    def __repr__(self):
        return self.__class__.__name__ + f"<{self.value}>"

    def init(self): pass

    def c_decl(self): pass

    def c_test_argv(self, argidx):
        return f"""(strcmp(argv[{argidx}], "{self.flag}") == 0)"""

    def c_read_argv(self, struct, argidx):
        return f"{struct}->{self.field} = argv[++{argidx}];\n"
    
    def get_value(self, parent, fmt):
        val = getattr(parent, self.field, None)
        if isinstance(val,bool):
            return str(val).lower()
        else:
            return val

    def _get_value(self, parent, value=None):
        value = self.value if value is None else value
        if value is None:
            value = self.default
        return value

    def as_tcl_list(self, value=None)->list:
        value = self._get_value(None, value)
        if isinstance(value, (type(None), )):
            if not self.reqd:
                return []
            else:
                value = f"${self.name}"
        elif isinstance(value, (Arg,)):
            if not self.reqd:
                return []
            else:
                value = f"${value.name}"
        return self.flag + [value] 

    def m_src(self, value=None):
        value = self._get_value(None,value)
        if isinstance(value,bool):
            return str(value).lower()

class Flg(Arg):
    "A `Flg` is a flag-like argument"
    def init(self):
        if "enum" in self.kwds:
            self.enum = self.kwds["enum"]
            if self.type is None:
                self.type = str

        self.default = False
        if "-" in self.name:
            if self.field == self.name:
                self.field = self.name[1:]
            self.flag = self.name
            self.name = self.name[1:]
    
    def c_read_argv(self, struct, argidx):
        return f"{struct}->{self.field} = true;\n"

    def as_tcl_list(self, value=None): 
        value = self.value if value is None else value
        return [self.flag] if value else []

class Num(Arg): 
    def init(self): self.type = float
    
    def c_read_argv(self, struct, argidx):
        return f"{struct}->{self.field} = argv[++{argidx}];\n"

class Int(Arg): 
    def init(self): self.type = int

class Str(Arg): 
    def init(self): self.type = str

class Chr(Arg): 
    def init(self): self.type = chr

class Ref(Arg):
    """A `Ref` is a reference to another object.

    ## Extra parameters

    `attr="name"`: referenced attribute

    """
    def init(self):
        if "attr" not in self.kwds: self.kwds["attr"] = "name"
        self.__name__ = f"Ref({self.type.__class__.__name__})"

    def __call__(self, *args,**kwds):
        return Ref(*args, type=self.type, attr=self.kwds["attr"], **kwds)

    def _get_value(self, parent, value=None):
        value = self.value if value is None else value
        if not isinstance(value, (str,int,float,type(None))):
            return getattr(value, self.kwds["attr"])
        else:
            return value
    
    def as_tcl_list(self, value=None): 
        value = self._get_value(None, value)
        try:
            value = getattr(value, self.kwds["attr"])
        except:
            pass
        return self.flag + [value]

class Ary(Arg): pass

class Sub(Arg): pass

class Map(Arg):
    def  init(self):
        self.key_type = self.kwds["key"]
        self.val_type = self.kwds["val"]
        self.tcl_rev_kv = self.kwds.get("tcl_rev_kv", False)
        #self.__name__ = f"Map({self.key_type.__class__.__name__} : {self.val_type.__class__.__name__})"
        self.__name__ = f"{{{self.key_type.name} : {self.val_type.name} ...}}"

    def as_tcl_list(self, value=None):
        value = self._get_value(None,value)
        if value is None:
            if self.reqd:
                value = [None]*self.num
            else:
                return []
        vals = []
        i, j = (1, 0) if self.tcl_rev_kv else (0, 1)
        for arg, kv in zip(arg,value.items()):
            kv = kv[0], arg.as_tcl_list(kv[1])
            vals = vals + [kv[i], kv[j]]
        return self.flag + vals

class Grp(Arg):
    """Argument grouping"""
    def init(self):
        num = self.kwds.get("num", self.kwds.get("min", None))
        if num:
            self.args = [
                self.type(f"{self.name}{i+1}") for i in range(num)
            ]
        else:
            assert isinstance(self.kwds["args"],list)
            self.args = self.kwds["args"]
        self.num = len(self.args)

    def as_tcl_list(self, value=None):
        value = self._get_value(None,value)
        if value is None:
            if self.reqd:
                value = [None]*self.num
            else:
                return []
        return self.flag + [a for arg,v in zip(self.args,value) for a in arg.as_tcl_list(v)]

class One(Arg): pass

class Blk(Grp):
    def init(self):
        self.args = []

    def as_tcl_list(self, value=None):
        value = self.value if value is None else value
        if value is None:
            value = [None]
        return self.flag + [[v.get_cmd() for v in value]]

class Tag(Int):
    def init(self):
        super().init()
        self.name = "name"
        self.field = "name"
        type = int

