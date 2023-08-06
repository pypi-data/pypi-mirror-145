from NotionPy.notionpy import NotionClient

inst = NotionClient("Your integration token")
# inst.create.page(
#     database_id="the id of database of choice",
#     data=[  # List of tuples
#         ("Name", "title", "kareem"),
#         ("price", "number", 254),
#         ("to-do", "checkbox", False),
#     ],
#     # Optional
#     icon="🔥",
#     # Optional
#     cover="https://images.unsplash.com/photo-1523867574998-1a336b6ded04?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y292ZXJ8ZW58MHx8MHx8&w=1000&q=80",
# )

# inst.create.db(
#     "cc39932a53da46be8472fdfc4c55966e",
#     "kareem's db",
#     [("Name", "title"), ("num", "number")],
#     "🌟",
# )
inst.query.db(
    "04cd159d03a64f98bdcba4cb45014d30", in_json=True, json_indent=2, print_data=True
)

# secret_LYxhmvMw0RoQncukgmKNjLkPHduLBLgELz5HE9id5MW
#
# inst.create.page(
#     "04cd159d03a64f98bdcba4cb45014d30",
#     data=[("Name", "title", "kareem"), ("number", "phone", "01006007952")],
# )
# inst.update.page(
#     "d6ee44d9d4ef4a8a85cb7d0a1c69364d",
#     [("Name", "title", "ahmed"), ("number", "phone", "56748625452")],
#     # archived=True,
#     icon="🦴",
# )
# inst.update.db(
#     "04cd159d03a64f98bdcba4cb45014d30",
#     # title="Grocery list",
#     data=[("Name", "title", "ahmed")],
#     icon="📌",
# )
