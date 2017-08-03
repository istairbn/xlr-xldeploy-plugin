#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from xlr_xldeploy.XLDeployClientUtil import XLDeployClientUtil

def create_path(path):
    parent = path.rpartition('/')[0]
    if parent and not xld_destination_client.check_ci_exist(parent):
        create_path(parent)
    xld_destination_client.create_directory(path)

def get_username():
    if username:
        return username
    return xldeployServer['username']

def get_password():
    if username:
        return password
    return xldeployServer['password']

xld_source_client = XLDeployClientUtil.create_xldeploy_client(xldeployServer, username, password)
xld_destination_client = XLDeployClientUtil.create_xldeploy_client(destinationXLDeployServer, destinationUsername, destinationPassword)

app_path = deploymentPackage.rpartition('/')[0]
app_version = deploymentPackage.rpartition('/')[2]
app_name = app_path.rpartition('/')[2]
app_folder = app_path.rpartition('/')[0]
application_exists_on_destination = False
destination_package = ""

if xld_destination_client.check_ci_exist(app_path):
    print("%s exists on destination server" % (app_path) )
    application_exists_on_destination = True
    destination_package = deploymentPackage

else:
    destination_applications = xld_destination_client.get_all_package_version("Applications",True)

    for application in destination_applications:
        if app_name == application.rpartition('/')[2]:
            application_exists_on_destination = True
            destination_package = "%s/%s" % (application,app_version)

if not application_exists_on_destination:

    if autoCreatePath:

        if xld_destination_client.check_ci_exist(app_folder):
            print("%s exists on destination server, but no application named %s is present" % app_folder,app_name)
            xld_destination_client.create_application(app_path)

        else:
            print("One or more containing folders missing from %s" % (app_folder) )
            xld_destination_client.create_folder_tree(app_folder, "Applications")
            xld_destination_client.create_application(app_path)

    else:
        raise Exception("%s not found on the destination server. Please create and try again" % (app_name) )


if xld_destination_client.check_ci_exist(destination_package):
    if idempotent:
        xld_destination_client.delete_ci(destination_package)
    else:
        raise Exception("[%s] already exists on destination server!" % (destination_package) )

package_uuid = xld_source_client.get_download_uuid(deploymentPackage)
fetch_url = xldeployServer['url'] + '/deployit/internal/download/' + package_uuid
print(fetch_url)
xld_destination_client.fetch_package2(fetch_url, get_username(), get_password())
