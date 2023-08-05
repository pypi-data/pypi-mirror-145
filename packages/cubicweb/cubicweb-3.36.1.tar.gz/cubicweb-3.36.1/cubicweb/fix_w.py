from redbaron import RedBaron


files = [
    "utils.py",
    "view.py",
    "ext/tal.py",
    "web/component.py",
    "web/htmlwidgets.py",
    "sobjects/supervising.py",
    "sobjects/notification.py",
    "web/views/schema.py",
    "web/views/plots.py",
    "web/views/navigation.py",
    "web/views/vcard.py",
    "web/views/pyviews.py",
    "web/views/basetemplates.py",
    "web/views/bookmark.py",
    "web/views/baseviews.py",
    "web/views/editviews.py",
    "web/views/rdf.py",
    "web/views/startup.py",
    "web/views/treeview.py",
    "web/views/basecomponents.py",
    "web/views/wdoc.py",
    "web/views/emailaddress.py",
    "web/views/undohistory.py",
    "web/views/json.py",
    "web/views/cwproperties.py",
    "web/views/xmlrss.py",
    "web/views/calendar.py",
    "web/views/debug.py",
    "web/views/tableview.py",
    "web/views/ibreadcrumbs.py",
    "web/views/xbel.py",
    "web/views/cwsources.py",
    "web/views/cwuser.py",
    "web/views/timetable.py",
    "web/views/ajaxedit.py",
    "web/views/idownloadable.py",
    "web/views/owl.py",
    "web/views/reledit.py",
    "web/views/management.py",
    "web/views/tabs.py",
    "web/views/error.py",
    "web/views/workflow.py",
    "web/views/sparql.py",
    "web/views/dotgraphview.py",
    "web/views/editforms.py",
    "devtools/test/data/views.py",
    "web/views/primary.py",
    "web/views/autoform.py",
]

for f in files:
    print(f)
    try:
        red = RedBaron(open(f).read())
    except Exception:
        print(f"failed on {f}")
        continue

    for z in red.find_all(
        "atomtrailers",
        lambda x: x[0].dumps() == "self"
        and x[1].dumps() == "w"
        and x.call
        and x.call.binary_operator,
    ):
        first = z.call.binary_operator.first
        second = z.call.binary_operator.second

        if second.type in ("associative_parenthesis", "tuple"):
            second = second.value

        z.call.value = "%s, %s" % (first.dumps(), second.dumps())

    open(f, "w").write(red.dumps())
