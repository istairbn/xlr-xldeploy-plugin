#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#Worked before
#from com.xebialabs.xlrelease.domain import *

import xml.etree.ElementTree as ET
from xlr_xldeploy.XLDeployClientUtil import XLDeployClientUtil

xld_client = XLDeployClientUtil.create_xldeploy_client(xldeployServer, username, password)

test = xld_client.check_ci_exist(ci_id)

def get_application_checklist(ci_xml):

    root = ET.fromstring(ci_xml)
    variableDict = {}

    for child in root:
        if "satisfies" in child.tag:
            variableDict[child.tag] = child.text

    return variableDict

if not test:
    raise Exception(ci_id + " does not exist")

elif "Applications" not in ci_id:
    raise Exception(ci_id + "is not an application")
else:
    ci_xml = xld_client.get_ci(ci_id,"xml")

variableDict = get_application_checklist(ci_xml)

if createReleaseVariables:
    existingVariables = releaseApi.getVariables(release.id)
    existingkeys = {}
    for existing in existingVariables:
        existingkeys[existing.key] = existing

    root = ET.fromstring(ci_xml)
    applicationName = root.attrib["id"].split("/")[-2] + "_" + root.attrib["id"].split("/")[-1]

    for variable in variableDict:
        if unique:
            varName = applicationName + "_" + variable
        else:
            varName = variable

        newVar = Variable(varName,None,False)

        if variableDict[variable] == "true" or variableDict[variable] == "false":

            newVar.setType("xlrelease.BooleanVariable")
            if variableDict[variable] == "true":
                newVar.setValue(True)
            else:
                newVar.setValue(False)
        else:
            newVar.setValue(variableDict[variable])

        if varName in existingkeys:
            print("%s already exists, removing and replacing" % (varName))
            releaseApi.deleteVariable(str(existingkeys[varName]))

        releaseApi.createVariable(release.id,newVar)
