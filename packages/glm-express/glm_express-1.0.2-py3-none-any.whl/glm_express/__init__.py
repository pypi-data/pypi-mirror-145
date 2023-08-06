#!/bin/python3

"""
GLM Express is a lightweight, object-oriented approach
to first- and second-level modeling of functional neuroimaging data.
For a primer and demo, see github.com/IanRFerguson/glm-express
"""

__version__ = "1.0.2"

from aggregator.aggregator import Aggregator
from group_level.group import GroupLevel
from subject.subject import Subject

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
