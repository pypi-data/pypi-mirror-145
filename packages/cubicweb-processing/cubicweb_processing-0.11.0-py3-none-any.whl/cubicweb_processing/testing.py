# copyright 2012-2022 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""tools helping cubicweb-processing client to test their code"""

from random import random, randint, choice
from json import loads, dumps
from six import text_type

from logilab.common.shellutils import generate_password

from cubicweb import Binary
from cubicweb.devtools.fill import ValueGenerator


class MyValueGenerator(ValueGenerator):
    def generate_Any_json(self, entity, index):
        return text_type(dumps({"modules": ()}))

    def generate_Executable_python_code(self, entity, index):
        return "1"


def generate_param_value(value_type, req):
    if value_type == "Int":
        return randint(-1000, 1000)
    if value_type == "Float":
        return random() * 1000
    if value_type == "String":
        return text_type(generate_password())
    if value_type == "File":
        data_name = "toto." + choice(["py", "txt", "xls", "dat"])
        bpassword = generate_password().encode("utf-8")
        return req.create_entity("File", data_name=data_name, data=Binary(bpassword))


def generate_io(tc, cnx):
    with cnx.allow_all_hooks_but("integrity", "processing.test"):
        for exe in cnx.execute("Executable X").entities():
            for vtype in ("Int", "Float", "String", "File"):
                exe.add_input("i" + vtype, vtype)
                exe.add_output("o" + vtype, vtype)
            for run in exe.reverse_executable:
                for vtype in ("Int", "Float", "String", "File"):
                    run["i" + vtype] = generate_param_value(vtype, cnx)


class ProcessingTCMixin(object):
    def setup_database(self):
        super(ProcessingTCMixin, self).setup_database()
        with self.admin_access.repo_cnx() as cnx:
            self.exeeid = cnx.create_entity("Executable", name="some executable").eid
            cnx.commit()

    def assertExcMsg(self, ctm, expected):
        if not str(ctm.exception).endswith(expected):
            self.fail("did not get error %r but %s" % (expected, ctm.exception))

    def new_run(self, cnx, **kwargs):
        return cnx.create_entity("Run", **kwargs)

    def new_file_pval(self, cnx, pdef, run, with_value=True):
        ce = cnx.create_entity
        pval = ce("ParameterValueFile", param_def=pdef, value_of_run=run)
        if with_value:
            ce(
                "File",
                data_name="file.txt",
                data=Binary("content"),
                data_format="text/plain",
                reverse_value_file=pval,
            )
        return pval

    def runchain_wlang_def(self, runchain):
        if runchain.wlang:
            runchain.wlang[0].cw_clear_all_caches()
            return loads(runchain.wlang[0].json)

    def wlang_fields_by_module(self, wlang):
        fields = []
        for mod in wlang["modules"]:
            fields.append(
                (
                    mod["name"],
                    sorted(
                        [
                            (f["inputParams"]["name"], f["type"])
                            for f in mod["container"]["fields"]
                        ]
                    ),
                )
            )
        return fields

    def _add_iset_1(self, exe):
        exe.add_input("i11", "Float")
        exe.add_input("i12", "String")

    def _add_oset_1(self, exe):
        exe.add_output("o11", "Float")
        exe.add_output("o12", "String")
        exe.add_output("o13", "Float")

    def _add_iset_2(self, exe):
        exe.add_input("i21", "Float")
        exe.add_input("i22", "Float")
        exe.add_input("i23", "String")

    def _add_oset_2(self, exe):
        exe.add_output("o21", "String")
        exe.add_output("o22", "Float")


class ChainingTestMixin(ProcessingTCMixin):
    def setup_database(self):
        super(ChainingTestMixin, self).setup_database()
        with self.admin_access.repo_cnx() as cnx:
            ce = cnx.create_entity
            exe0 = ce("Executable", name="e0")
            self.exe0eid = exe0.eid
            self.odef0_feid = exe0.add_output("f", "Float").eid
            self.odef0_seid = exe0.add_output("s", "String").eid
            exe1 = ce("Executable", name="e1")
            self.exe1eid = exe1.eid
            self.idef1_feid = exe1.add_input("f", "Float").eid
            cnx.commit()

    def chaining_setup(self, cnx):
        ce = cnx.create_entity
        run0 = ce("Run", executable=self.exe0eid)
        run1 = ce("Run", executable=self.exe1eid)
        pval = ce(
            "ParameterValueFloat",
            param_def=self.idef1_feid,
            value_of_run=run1,
            from_run=run0,
            from_output=self.odef0_feid,
        )
        cnx.commit()
        return pval


class RunChainTCMixin(ProcessingTCMixin):
    def setup_database(self):
        super(RunChainTCMixin, self).setup_database()
        with self.admin_access.repo_cnx() as cnx:
            ce = cnx.create_entity
            # add a new run with files
            exe0 = ce("Executable", name="e0")
            self.exe0eid = exe0.eid
            idef1 = exe0.add_input("i1", "File")
            idef2 = exe0.add_input("i2", "Float")
            exe0.add_output("o1", "File")
            exe0.add_output("o2", "Float")
            cnx.commit()
            run = ce("Run", executable=exe0)
            pv1 = self.new_file_pval(cnx, idef1, run, with_value=True)
            idef2.create_value(1.0, run)
            cnx.commit()
            self.exe1eid = self.exeeid
            exe1 = cnx.entity_from_eid(self.exe1eid)
            self._add_iset_1(exe1)
            self._add_oset_1(exe1)
            exe2 = ce("Executable", name="e2")
            self.exe2eid = exe2.eid
            self._add_iset_2(exe2)
            self._add_oset_2(exe2)
            runchain = ce("RunChain", uses_executable=(exe0, exe1, exe2))
            self.runchaineid = runchain.eid
            cnx.commit()
            exe = cnx.entity_from_eid(self.exeeid)
            descr = {
                "modules": [
                    {
                        "config": {"position": [167, 71]},
                        "name": exe.dc_title(),
                        "eid": self.exeeid,
                        "value": {
                            "o11": "[wired]",
                            "o12": "",
                            # do not rely on '[wired]' value, also test None:
                            "o13": None,
                            "i11": 1.1,
                            "i12": "1.2",
                        },
                    },
                    {
                        "config": {"position": [634, 161]},
                        "name": exe2.dc_title(),
                        "eid": self.exe2eid,
                        "value": {
                            "o21": "",
                            "o22": "",
                            "i21": "[wired]",
                            "i22": "[wired]",
                            "i23": "i23 value",
                        },
                    },
                    {
                        "config": {"position": [2, 40]},
                        "name": exe0.dc_title(),
                        "eid": self.exe0eid,
                        "value": {
                            "o1": "",
                            "o2": "",
                            "i1": "%s" % pv1.value_file[0].eid,
                            "i2": "1.0",
                        },
                    },
                ],
                "properties": None,
                "wires": [
                    {
                        "src": {"moduleId": 0, "terminal": "o11"},
                        "tgt": {"moduleId": 1, "terminal": "i21"},
                    },
                    {
                        "src": {"moduleId": 0, "terminal": "o13"},
                        "tgt": {"moduleId": 1, "terminal": "i22"},
                    },
                ],
            }
            ce(
                "Wiring",
                name="test",
                json=text_type(dumps(descr)),
                reverse_wiring=runchain,
                language=runchain.wlang[0],
            )
            cnx.commit()
