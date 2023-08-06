from fury.ui import UI

class Disk2D(UI):
    """A 2D disk UI component."""

    def __init__(self, outer_radius, inner_radius=0, center=(0, 0),
                 color=(1, 1, 1), opacity=1.0):
        """Initialize a 2D Disk.

        Parameters
        ----------
        outer_radius : int
            Outer radius of the disk.
        inner_radius : int, optional
            Inner radius of the disk. A value > 0, makes a ring.
        center : (float, float), optional
            Coordinates (x, y) of the center of the disk.
        color : (float, float, float), optional
            Must take values in [0, 1].
        opacity : float, optional
            Must take values in [0, 1].

        """
        super(Disk2D, self).__init__()
        self.outer_radius = outer_radius
        self.inner_radius = inner_radius
        self.color = color
        self.opacity = opacity
        self.center = center

    def _setup(self):
        """Setup this UI component.

        Creating the disk actor used internally.

        """
        # Setting up disk actor.
        self._disk = DiskSource()
        self._disk.SetRadialResolution(10)
        self._disk.SetCircumferentialResolution(50)
        self._disk.Update()

        # Mapper
        mapper = PolyDataMapper2D()
        mapper = set_input(mapper, self._disk.GetOutputPort())

        # Actor
        self.actor = Actor2D()
        self.actor.SetMapper(mapper)

        # Add default events listener to the VTK actor.
        self.handle_events(self.actor)

    def _get_actors(self):
        """Get the actors composing this UI component."""
        return [self.actor]

    def _add_to_scene(self, scene):
        """Add all subcomponents or VTK props that compose this UI component.

        Parameters
        ----------
        scene : scene

        """
        scene.add(self.actor)

    def _get_size(self):
        diameter = 2 * self.outer_radius
        size = (diameter, diameter)
        return size

    def _set_position(self, coords):
        """Set the lower-left corner position of this UI bounding box.

        Parameters
        ----------
        coords: (float, float)
            Absolute pixel coordinates (x, y).
        """
        # Disk actor are positioned with respect to their center.
        self.actor.SetPosition(*coords + self.outer_radius)

    @property
    def color(self):
        """Get the color of this UI component."""
        color = self.actor.GetProperty().GetColor()
        return np.asarray(color)

    @color.setter
    def color(self, color):
        """Set the color of this UI component.

        Parameters
        ----------
        color : (float, float, float)
            RGB. Must take values in [0, 1].

        """
        self.actor.GetProperty().SetColor(*color)

    @property
    def opacity(self):
        """Get the opacity of this UI component."""
        return self.actor.GetProperty().GetOpacity()

    @opacity.setter
    def opacity(self, opacity):
        """Set the opacity of this UI component.

        Parameters
        ----------
        opacity : float
            Degree of transparency. Must be between [0, 1].

        """
        self.actor.GetProperty().SetOpacity(opacity)

    @property
    def inner_radius(self):
        return self._disk.GetInnerRadius()

    @inner_radius.setter
    def inner_radius(self, radius):
        self._disk.SetInnerRadius(radius)
        self._disk.Update()

    @property
    def outer_radius(self):
        return self._disk.GetOuterRadius()

    @outer_radius.setter
    def outer_radius(self, radius):
        self._disk.SetOuterRadius(radius)
        self._disk.Update()

