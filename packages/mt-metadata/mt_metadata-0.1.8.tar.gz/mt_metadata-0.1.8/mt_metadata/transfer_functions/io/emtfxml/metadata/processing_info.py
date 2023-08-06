# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from .standards import SCHEMA_FN_PATHS
from . import Software, RemoteRef

# =============================================================================
attr_dict = get_schema("processing_info", SCHEMA_FN_PATHS)
attr_dict.add_dict(Software()._attr_dict, "processing_software")
attr_dict.add_dict(RemoteRef()._attr_dict, "remote_ref")
# =============================================================================


class ProcessingInfo(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):

        self.remote_ref = RemoteRef()
        self.processing_software = Software()

        super().__init__(attr_dict=attr_dict, **kwargs)
