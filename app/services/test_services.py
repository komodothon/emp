"""app/services/test_services.py"""

import json    

def build_department_tree():
    tree = {}

    departments = [
        # Level 1 (Top-level)
        {"id": 1, "name": "Head Office", "parent_id": None},

        # Level 2
        {"id": 2, "name": "HR Department", "parent_id": 1},
        {"id": 3, "name": "IT Department", "parent_id": 1},

        # Level 3
        {"id": 4, "name": "Recruitment", "parent_id": 2},
        {"id": 5, "name": "Training", "parent_id": 2},
        {"id": 6, "name": "Infrastructure", "parent_id": 3},
        {"id": 7, "name": "Development", "parent_id": 3},

        # Level 4
        {"id": 8, "name": "University Relations", "parent_id": 4},
        {"id": 9, "name": "Onboarding", "parent_id": 5},
        {"id": 10, "name": "Server Maintenance", "parent_id": 6},
        {"id": 11, "name": "Frontend Team", "parent_id": 7},
        {"id": 12, "name": "Backend Team", "parent_id": 7},
    ]


    # Create a lookup dictionary with empty children list
    lookup = {
        dept["id"]:{
            "name": dept["name"],
            "children": [],
        } for dept in departments
    }

    
    # print(json.dumps(lookup, indent=4))

    # build the tree
    for dept in departments:
        if dept["parent_id"]:
            lookup[dept["parent_id"]]["children"].append(lookup[dept["id"]])
        else:
            tree[dept["id"]] = lookup[dept["id"]]
    
    # print(json.dumps(tree, indent=4))

    return tree

