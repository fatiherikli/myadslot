from django.utils import simplejson
from django.utils.translation import ugettext as _
from adserver.helpers import detect_browser
from adserver.utils import jsonify


def build_statistic_data(sql, columns):
    """
        return stringify json for charts...
    """
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql)
    result = []
    for item in  cursor.fetchall():
        result.append(map(jsonify, list(item))) # make list from tuple and jsonify list
    return simplejson.dumps({
        "rows" : result,
        "columns" : list(columns)
    })


def advertisement_month_visits(advertisement_id):
    """
    result example:
        [["2011-12-18", 11, 2], ["2011-12-21", 2, 1], ["2011-12-25", 11, 1]]
    """
    columns = (
        ('string', _("Date")),
        ('number', _("View Counts")),
        ('number', _("Unique Visits")),
        )
    return build_statistic_data("""
        SELECT
        Date(adserver_visitor.last_visit_date) AS date,
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits
        FROM adserver_visitor
        WHERE advertisement_id = %s
        GROUP BY date;
        """ % advertisement_id, columns)

def slot_month_visits(slot_id):
    """
    result example:
        [["2011-12-18", 11, 2], ["2011-12-21", 2, 1], ["2011-12-25", 11, 1]]
    """
    columns = (
        ('string', _("Date")),
        ('number', _("View Counts")),
        ('number', _("Unique Visits")),
        )
    return build_statistic_data("""
        SELECT
        Date(adserver_visitor.last_visit_date) AS date,
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits
        FROM adserver_visitor
        INNER JOIN  adserver_advertisement ON adserver_visitor.advertisement_id = adserver_advertisement.id
        WHERE adserver_advertisement.adslot_id = %s
        GROUP BY date;
        """ % slot_id, columns)


def slot_month_hours(slot_id):
    """
    result example:
        [["2011-12-18", 11, 2], ["2011-12-21", 2, 1], ["2011-12-25", 11, 1]]
    """
    columns = (
        ('string', _("Hour")),
        ('number', _("View Counts")),
        ('number', _("Unique Visits")),
        )
    return build_statistic_data("""
        SELECT
        CONCAT(hour(adserver_visitor.last_visit_date),':00') AS date,
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits
        FROM adserver_visitor
        INNER JOIN  adserver_advertisement ON adserver_visitor.advertisement_id = adserver_advertisement.id
        WHERE adserver_advertisement.adslot_id = %s
        GROUP BY date;
        """ % slot_id, columns)


def stats_slot_advertisements(slot_id):
    """
    result example:
        [["2011-12-18", 11, 2], ["2011-12-21", 2, 1], ["2011-12-25", 11, 1]]
    """
    columns = (
        ('string', _("Advertisement")),
        ('number', _("View Counts")),
        ('number', _("Unique Visits")),
        )
    return build_statistic_data("""
        SELECT
        adserver_advertisement.title,
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits

        FROM adserver_visitor
        INNER JOIN  adserver_advertisement ON adserver_visitor.advertisement_id = adserver_advertisement.id
        WHERE adserver_advertisement.adslot_id = %s
        GROUP BY adserver_visitor.advertisement_id;
        """ % slot_id, columns)


def stats_browser(slot_id):
    columns = (
        ('string', _("User Agent")),
        ('number', _("Count")),
        )
    sql ="""
        SELECT
        adserver_visitor.user_agent AS user_agent,
        Sum(adserver_visitor.visit_count) AS browser_count
        FROM adserver_visitor
        INNER JOIN  adserver_advertisement ON adserver_visitor.advertisement_id = adserver_advertisement.id
        WHERE adserver_advertisement.adslot_id = %s
        GROUP BY user_agent;
        """ % slot_id

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql)
    result = []
    for user_agent, count in  cursor.fetchall():
        result.append([detect_browser(user_agent), jsonify(count)])

    return simplejson.dumps({
        "rows" : result,
        "columns" : list(columns)
    })