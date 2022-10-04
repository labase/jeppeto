from browser import window

from .vector import vec


class paths:
    ...


class shapes:
    ...


class ShapeInit:
    def __init__(self):
        s = window.shapes
        p = window.paths

        shapes_ = ['rectangle', 'circle', 'ellipse', 'arc', 'line', 'triangle',
                   'pentagon', 'hexagon', 'octagon', 'ngon', 'star', 'trapezoid',
                   'cross', 'points', 'gear', 'rackgear']
        shdic_ = dict(rectangle=s.rectangle, circle=s.circle, ellipse=s.ellipse, arc=s.arc, line=s.line,
                      triangle=s.triangle,
                      pentagon=s.pentagon, hexagon=s.hexagon, octagon=s.octagon, ngon=s.ngon, star=s.star,
                      trapezoid=s.trapezoid, cross=s.cross, points=s.points, gear=s.gear, rackgear=s.rackgear
                      )

        phdic_ = dict(rectangle=p.rectangle, circle=p.circle, ellipse=p.ellipse, arc=p.arc, line=p.line,
                      triangle=p.triangle,
                      pentagon=p.pentagon, hexagon=p.hexagon, octagon=p.octagon, ngon=p.ngon, star=p.star,
                      trapezoid=p.trapezoid, cross=p.cross
                      )

        def _paths_call(classname):
            def __paths_call(_, **kwargs):
                return phdic_[classname](kwargs)

            return __paths_call

        def _shapes_call(classname):
            def _shapes_init(_, **kwargs):
                return shdic_[classname](kwargs)

            return _shapes_init

        _ = [setattr(paths, classname, type(classname, (), dict(
            __call__=_paths_call(classname)))()) for classname in shapes_]

        _ = [setattr(shapes, classname, type(classname, (), dict(
            __call__=_shapes_call(classname)))()) for classname in shapes_]


# window.glowscript = window.glowscript
class primitive:
    def __init__(self, prim, **kwargs):
        for _key in kwargs.keys():
            if isinstance(kwargs[_key], tuple):
                kwargs[_key] = vec(*kwargs[_key])._vec
            if isinstance(kwargs[_key], vec):
                kwargs[_key] = kwargs[_key]._vec
        if "compound" in kwargs:
            # print(kwargs["compound"])
            # self._prim=prim(kwargs["compound"])
            self._prim = window.glowscript.compound(kwargs.pop("compound"), kwargs)
            return
        self._prim = prim(kwargs)

    def rotate(self, **kwargs):
        if 'axis' in kwargs:
            # for now lets assume axis is a vector
            kwargs['axis'] = kwargs['axis']._vec

        self._prim.rotate(kwargs)

    @property
    def prim(self):
        return self._prim

    @property
    def pos(self):
        _v = vec()
        _v._set_vec(self._prim.pos)
        return _v

    @pos.setter
    def pos(self, value):
        if isinstance(value, vec):
            self._prim.pos = value._vec
        elif isinstance(value, tuple):
            self._prim.pos = vec(*value)._vec
        else:
            print("Error! pos must be a vector")

    @property
    def color(self):
        _v = vec()
        _v._set_vec(self._prim.color)
        return _v

    @color.setter
    def color(self, value):
        if isinstance(value, vec):
            self._prim.color = value._vec
        elif isinstance(value, tuple):
            self._prim.color = vec(*value)._vec
        else:
            print("Error! color must be a vec")

    @property
    def axis(self):
        _v = vec()
        _v._set_vec(self._prim.axis)
        return _v

    @axis.setter
    def axis(self, value):
        if isinstance(value, vec):
            self._prim.axis = value._vec
        elif isinstance(value, tuple):
            self._prim.axis = vec(*value)._vec
        else:
            print("Error! axis must be a vec")

    @property
    def size(self):
        _v = vec()
        _v._set_vec(self._prim.size)
        return _v

    @size.setter
    def size(self, value):
        if isinstance(value, vec):
            self._prim.size = value._vec
        elif isinstance(value, tuple):
            self._prim.size = vec(*value)._vec
        else:
            print("Error! axis must be a vec")

    @property
    def up(self):
        _v = vec()
        _v._set_vec(self._prim.up)
        return _v

    @up.setter
    def up(self, value):
        if isinstance(value, vec):
            self._prim.up = value._vec
        elif isinstance(value, tuple):
            self._prim.up = vec(*value)._vec
        else:
            print("Error! up must be a vec")

    @property
    def opacity(self):
        return self._prim.opacity

    @opacity.setter
    def opacity(self, value):
        self._prim.opacity = value

    @property
    def shininess(self):
        return self._prim.shininess

    @shininess.setter
    def shininess(self, value):
        self._prim.shininess = value

    @property
    def emissive(self):
        return self._prim.emissive

    @emissive.setter
    def emissive(self, value):
        self._prim.emissive = value

    @property
    def texture(self):
        return self._prim.texture

    @texture.setter
    def texture(self, **kwargs):
        self._prim.texture = kwargs

    @property
    def visible(self):
        return self._prim.visible

    @visible.setter
    def visible(self, flag):
        assert isinstance(flag, bool)

        self._prim.visible = flag


class arrow(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.arrow, **kwargs)


class box(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.box, **kwargs)


class cone(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.cone, **kwargs)


class curve(primitive):
    def __init__(self, *args):
        primitive.__init__(self, window.glowscript.curve)
        self._prim = window.glowscript.curve(args)

    def push(self, v):
        if isinstance(v, vec):
            self._prim.push(v._vec)
        elif isinstance(v, tuple):
            self._prim.push(vec(*v)._vec)
        elif isinstance(v, dict):
            for _key in v.keys():
                if isinstance(_key, vec):
                    v[_key] = v[_key]._vec

            self._prim.push(v)
        else:
            print("Error! push must get a vec or keywords")

    def append(self, v):
        self.push(v)


class cylinder(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.cylinder, **kwargs)


class helix(cylinder):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.helix, **kwargs)


# shapes = window.glowscript.shapes


class extrusion(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.extrusion, **kwargs)


class text(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.text, **kwargs)


class ellipsoid(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.sphere, **kwargs)


class pyramid(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.pyramid, **kwargs)


# class ring(curve):

class ring(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.ring, **kwargs)


class sphere(primitive):
    def __init__(self, **kwargs):
        primitive.__init__(self, window.glowscript.sphere, **kwargs)


# triangle
# class triangle:
#  def __init__(self, **kwargs):
#      self._tri = window.glowscript.triangle.new()(kwargs)

# vertex
# class vertex:
#  def __init__(self, **kwargs):
#      self._ver = window.glowscript.vertex.new()(kwargs)


# quad

# compound
class compound(primitive):
    def __init__(self, comps, **kwargs):
        primitive.__init__(self, window.glowscript.compound, compound=[c.prim for c in comps], **kwargs)


# I'm not sure if the declarations below are correct.  Will fix later.

class distinct_light:
    def __init__(self, **kwargs):
        self._dl = window.glowscript.distant_light.new()(kwargs)


class local_light:
    def __init__(self, **kwargs):
        self._ll = window.glowscript.local_light.new()(kwargs)


class draw:
    def __init__(self, **kwargs):
        self._draw = window.glowscript.draw.new()(kwargs)


class label:
    def __init__(self, **kwargs):
        self._label = window.glowscript.label.new()(kwargs)


def attach_trail(object, **kwargs):
    if isinstance(object, primitive):
        window.glowscript.attach_trail(object._prim, kwargs)
    else:
        window.glowscript.attach_trail(object, kwargs)
