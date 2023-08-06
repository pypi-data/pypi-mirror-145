# copyright 2016-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-jsonb automatic tests


uncomment code below if you want to activate automatic test for your cube:

.. sourcecode:: python

    from cubicweb.devtools.testlib import AutomaticWebTest

    class AutomaticWebTest(AutomaticWebTest):
        '''provides `to_test_etypes` and/or `list_startup_views` implementation
        to limit test scope
        '''

        def to_test_etypes(self):
            '''only test views for entities of the returned types'''
            return set(('My', 'Cube', 'Entity', 'Types'))

        def list_startup_views(self):
            '''only test startup views of the returned identifiers'''
            return ('some', 'startup', 'views')
"""

from six import string_types
import json

from cubicweb.devtools import (
    testlib,
    startpgcluster,
    stoppgcluster,
    PostgresApptestConfiguration,
)
from logilab.common.testlib import unittest_main


def setUpModule():
    startpgcluster(__file__)


def tearDownModule():
    stoppgcluster(__file__)


# taken adapted from: https://stackoverflow.com/a/2213199
QUERY_INDEXED_COLUMN_TMPL = """
SELECT
    i.relname as index_name,
    array_to_string(array_agg(a.attname), ', ') as column_names
FROM
    pg_class t,
    pg_class i,
    pg_index ix,
    pg_attribute a
WHERE
    t.oid = ix.indrelid
    and i.oid = ix.indexrelid
    and a.attrelid = t.oid
    and a.attnum = ANY(ix.indkey)
    and t.relkind = 'r'
    and t.relname = '{table_name}'
GROUP BY
    t.relname,
    i.relname;
"""


class JsonbGetSetTC(testlib.CubicWebTC):
    """Functional get/set tests for the jsonb type."""

    configcls = PostgresApptestConfiguration

    def test_indexed_field(self):
        """Check that indexed are correctly added"""
        etype = "Named"
        table_name = f"cw_{etype.lower()}"
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.system_sql(
                QUERY_INDEXED_COLUMN_TMPL.format(table_name=table_name)
            )
            index_and_col_names = rset.fetchall()

        for relation_name in ("other_names", "named_by"):
            relation_def = self.schema.get(relation_name).rdef(etype, "Jsonb")
            sql_relation_name = f"cw_{relation_name}"
            if relation_def.indexed:
                idxname = "{0}_{1}_idx".format(table_name, relation_name)
                self.assertIn((idxname, sql_relation_name), index_and_col_names)
            else:
                self.assertNotIn(
                    sql_relation_name, {col for _, col in index_and_col_names}
                )

    def test_get_set_dict(self):
        """Check that we can set jsonb attribute from a dict and get the dict back."""
        tls_other_names = {"occitan": "Tolosa", "latin": "Tolosa"}
        with self.admin_access.repo_cnx() as cnx:
            tls = cnx.create_entity(
                "Named", name="Toulouse", other_names=tls_other_names
            )
            cnx.commit()
            tls = cnx.entity_from_eid(tls.eid)
            self.assertEqual(tls.other_names, tls_other_names)

    def test_get_set_str(self):
        """Check that we can set jsonb attribute from a JSON string and get back a dict."""
        with self.admin_access.repo_cnx() as cnx:
            tls = cnx.create_entity(
                "Named",
                name="Toulouse",
                other_names='{"occitan": "Tolosa", "latin": "Tolosa"}',
            )
            cnx.commit()
            tls = cnx.entity_from_eid(tls.eid)
            self.assertEqual(tls.other_names, {"occitan": "Tolosa", "latin": "Tolosa"})

    def test_set_invalid_str(self):
        """Check that we can't set jsonb attribute from an invalid JSON string."""
        with self.admin_access.repo_cnx() as cnx:
            with self.assertRaises(ValueError) as err:
                cnx.create_entity("Named", name="Toulouse", other_names='{1: "a"}')
                cnx.commit()
            self.assertIn("Invalid JSON value", str(err.exception))


class JsonbQueryTC(testlib.CubicWebTC):
    """Functional query tests for the jsonb type."""

    configcls = PostgresApptestConfiguration

    def test_jsonb_contains_query(self):
        """Check that we can query a jsonb attribute for containing a value."""
        tls_other_names = {"occitan": "Tolosa", "latin": "Tolosa"}
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity("Named", name="Toulouse", other_names=tls_other_names)
            cnx.commit()
            tls = cnx.execute(
                "Any X WHERE X other_names ON "
                "HAVING JSONB_CONTAINS(ON, %(json)s)=True",
                {"json": json.dumps({"occitan": "Tolosa"})},
            ).one()
            self.assertEqual(tls.other_names, tls_other_names)
            empty_rset = cnx.execute(
                "Any X WHERE X other_names ON "
                "HAVING JSONB_CONTAINS(ON, %(json)s)=True",
                {"json": json.dumps({"occitan": "Toulouse"})},
            )
            self.assertFalse(empty_rset)

    def test_jsonb_exists_query(self):
        """Check that we can query a jsonb attribute for key existence."""
        tls_other_names = {"occitan": "Tolosa", "latin": "Tolosa"}
        tarbes_other_names = {"occitan": "Tarba", "latin": "Turba"}
        aurillac_other_names = {"occitan": "Orlhac"}
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity("Named", name="Toulouse", other_names=tls_other_names)
            cnx.create_entity("Named", name="Tarbes", other_names=tarbes_other_names)
            cnx.create_entity(
                "Named", name="Aurillac", other_names=aurillac_other_names
            )
            cnx.commit()
            occ_rset = cnx.execute(
                "Any X WHERE X other_names ON " "HAVING JSONB_EXISTS(ON, %(key)s)=True",
                {"key": "occitan"},
            )
            self.assertEqual(len(occ_rset), 3)
            self.assertCountEqual(
                [entity.other_names for entity in occ_rset.entities()],
                [tls_other_names, tarbes_other_names, aurillac_other_names],
            )
            lat_rset = cnx.execute(
                "Any X WHERE X other_names ON " "HAVING JSONB_EXISTS(ON, %(key)s)=True",
                {"key": "latin"},
            )
            self.assertEqual(len(lat_rset), 2)
            self.assertCountEqual(
                [entity.other_names for entity in lat_rset.entities()],
                [tls_other_names, tarbes_other_names],
            )
            empty_rset = cnx.execute(
                "Any X WHERE X other_names ON " "HAVING JSONB_EXISTS(ON, %(key)s)=True",
                {"key": "french"},
            )
            self.assertFalse(empty_rset)

    def test_jsonb_get_query(self):
        """Check that we can query a jsonb attribute for value from a key."""
        tls_occname = "Tolosa"
        tarbes_occname = "Tarba"
        aurillac_occname = "Orlhac"
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity(
                "Named",
                name="Toulouse",
                other_names={"occitan": tls_occname, "latin": "Tolosa"},
            )
            cnx.create_entity(
                "Named",
                name="Tarbes",
                other_names={"occitan": tarbes_occname, "latin": "Turba"},
            )
            cnx.create_entity(
                "Named", name="Aurillac", other_names={"occitan": aurillac_occname}
            )
            cnx.commit()
            rset = cnx.execute(
                "Any JSONB_GET(ON, %(key)s) WHERE X other_names ON", {"key": "occitan"}
            )
            self.assertEqual(len(rset), 3)
            self.assertEqual(
                set(row[0] for row in rset),
                set([tls_occname, tarbes_occname, aurillac_occname]),
            )
            rset = cnx.execute(
                "Any JSONB_GET(ON, %(key)s) WHERE X other_names ON "
                "HAVING JSONB_CONTAINS(ON, %(json)s)=True",
                {"key": "occitan", "json": json.dumps({"latin": tls_occname})},
            )
            self.assertEqual(len(rset), 1)
            self.assertEqual(rset[0][0], tls_occname)
            rset = cnx.execute(
                "Any JSONB_GET(ON, %(key)s) WHERE X other_names ON "
                "HAVING JSONB_CONTAINS(ON, %(json)s)=True",
                {"key": "latin", "json": json.dumps({"occitan": aurillac_occname})},
            )
            self.assertEqual(len(rset), 1)
            self.assertIsNone(rset[0][0])
            rset = cnx.execute(
                "Any JSONB_GET(ON, %(key)s) WHERE X other_names ON "
                "HAVING JSONB_CONTAINS(ON, %(json)s)=True",
                {"key": "occitan", "json": json.dumps({"latin": "Lugdunum"})},
            )
            self.assertFalse(rset)

    def test_jsonb_get_query_non_str(self):
        """Check that querying in RQL a jsonb attribute for a key always returns a string."""
        tls_occname = "Tolosa"
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity(
                "Named",
                name="Toulouse",
                other_names={"names": {"occitan": tls_occname}},
            )
            cnx.commit()
            rset = cnx.execute(
                "Any JSONB_GET(ON, %(key)s) WHERE X other_names ON", {"key": "names"}
            )
            self.assertEqual(len(rset), 1)
            json_str = rset[0][0]
            self.assertTrue(isinstance(json_str, string_types))
            self.assertEqual(json.loads(json_str)["occitan"], tls_occname)

    def test_jsonb_array_elements(self):
        """Check that we can retrieve each element in a jsonb attribute consisting of an array."""
        author_occname_tuples = [("me", "Tolosa"), ("flu", "Tolocha")]
        with self.admin_access.repo_cnx() as cnx:
            # other_names equals to:
            #     [{'author': u'me', 'occitan': u'Tolosa'},
            #      {'author': u'flu', 'occitan': u'Tolocha'}]
            cnx.create_entity(
                "Named",
                name="Toulouse",
                other_names=[
                    {"author": author, "occitan": occname}
                    for author, occname in author_occname_tuples
                ],
            )
            cnx.commit()
            dict_rset = cnx.execute(
                "Any JSONB_ARRAY_ELEMENTS(ON) WHERE X other_names ON"
            )
            self.assertCountEqual(
                [(row[0]["author"], row[0]["occitan"]) for row in dict_rset],
                author_occname_tuples,
            )
            # Mix get and array_elements
            names_rset = cnx.execute(
                "Any JSONB_GET(JSONB_ARRAY_ELEMENTS(ON), %(key)s) "
                "WHERE X other_names ON",
                {"key": "author"},
            )
            self.assertEqual(
                set(row[0] for row in names_rset),
                set(author for author, _ in author_occname_tuples),
            )


if __name__ == "__main__":
    unittest_main()
