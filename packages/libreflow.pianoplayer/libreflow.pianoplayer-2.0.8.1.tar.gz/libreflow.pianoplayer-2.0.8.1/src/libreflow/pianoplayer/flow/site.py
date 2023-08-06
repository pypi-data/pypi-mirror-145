from kabaret import flow
from libreflow.baseflow.site import WorkingSite as BaseWorkingSite
from libreflow.utils.flow import SiteActionView


class WorkingSite(BaseWorkingSite):

    actions = flow.Child(SiteActionView)

    package_source_dir = flow.Param()
    package_target_dir = flow.Param()
    package_layout_dir = flow.Param()
    package_clean_dir  = flow.Param()
    package_color_dir  = flow.Param()
    package_line_dir   = flow.Param()
    target_sites       = flow.OrderedStringSetParam()
