# {
#     "name": "Sports Facility Operational ERP",
#     "depends": ["base"],
#     "application": True,
#     "data": [
#         "security/ir.model.access.csv",
#         "views/sports_facility_views.xml",
#         "views/sports_facility_court_views.xml",
#         "views/sports_menus.xml",
#         "views/sports_facility_booking_views.xml",
#     ]
# }

# -*- coding: utf-8 -*-
{
    "name": "TOdooSports",
    "depends": ["base"],
    "application": True,
    "data": [
        "data/sequences.xml",
        "security/ir.model.access.csv",
        "views/sports_type_views.xml",
        "views/sports_amenity_views.xml",
        "views/sports_facility_views.xml",
        "views/sports_facility_court_views.xml",
        "views/sports_equipment_views.xml",
        "views/sports_coach_views.xml",
        "views/sports_locker_views.xml",
        "views/sports_pricing_rule_views.xml",
        "views/sports_facility_booking_views.xml",
        "views/sports_membership_views.xml",
        "views/sports_menus.xml",
    ]
}