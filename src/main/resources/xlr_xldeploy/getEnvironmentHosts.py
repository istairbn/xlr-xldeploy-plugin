#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
from xlr_xldeploy.XLDeployClientUtil import XLDeployClientUtil

xld_client = XLDeployClientUtil.create_xldeploy_client(xldeployServer, username, password)

test = xld_client.check_ci_exist(ciID)

if not test:
    raise Exception(ciID + " does not exist")

else:
    environmentJson = xld_client.get_ci(ciID,'json')

environment = json.loads(environmentJson)

if not environment["type"] == "udm.Environment":
    raise Exception("%s is not udm.Environment, it is %s. Please select an Environment" % (ciID,environment["type"]))

members = environment["members"]
host_dict = {}
host_list = []

for member_id in members:
    print member_id
    memberJson = xld_client.get_ci(member_id,'json')
    memberJson = memberJson.replace("\\", "//")
    member = json.loads(memberJson)
    valid_host = False

    if "Host" in member["type"]:
        if not tags_to_check:
            valid_host = True
        else:
            for tag in tags_to_check:
                if tag in member["tags"]:
                    print("%s tag applied to %s" % (tag,member_id) )
                    valid_host = True
                else:
                    print("%s tag not applied to %s" % (tag,member_id) )

        if valid_host:
            print("%s is a valid host" % (member_id))
            host_dict[member_id] = member["address"]
            host_list.append(member["address"])

        else:
            print("%s is not a valid host" % (member_id))

    else:
        print("%s is not a host" % (member_id))


print(host_dict)
print(host_list)
