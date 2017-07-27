#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from com.xebialabs.deployit.plugin.api.reflect import Type
from xlr_xldeploy.XLDeployClientUtil import XLDeployClientUtil

xld_client = XLDeployClientUtil.create_xldeploy_client(xldeployServer, username, password)
throwOnFail = not continueIfStepFails

app_check = xld_client.check_ci_exist(application_folder)
env_check = xld_client.check_ci_exist(environment)

if throwOnFail:
    if not app_check or not env_check:
        raise ValueError("Check existence of " + environment + " and " + application_folder)

package_ids = xld_client.get_all_package_version(application_folder,recurse)

if throwOnFail and len(package_ids) == 0:
    raise ValueError(application_folder + " exists but has no versions")

def create_undeploy_task(phaseId,title,precondition, propertyMap):

    parenttaskType = Type.valueOf("xlrelease.CustomScriptTask")
    parentTask = parenttaskType.descriptor.newInstance("nonamerequired")
    parentTask.setTitle(title)
    childTaskType = Type.valueOf("xldeploy.UndeployTask")
    childTask = childTaskType.descriptor.newInstance("nonamerequired")
    for item in propertyMap:
        childTask.setProperty(item,propertyMap[item])
    parentTask.setPythonScript(childTask)
    parentTask.setPrecondition(precondition)
    taskApi.addTask(phaseId,parentTask)

def create_container_task(phaseId,title,precondition,propertyMap,containerType):
    containertaskType = Type.valueOf("xlrelease."+containerType+"Group")
    containertask = containertaskType.descriptor.newInstance("nonamerequired")
    containertask.setTitle(title)
    containertask.setPrecondition(precondition)
    taskApi.addTask(phaseId,containertask)
    return containertask.id

needed = True
for package_id in package_ids:
    package_name = package_id.split("/")[-1]
    package = environment +"/"+ package_name
    if xld_client.check_ci_exist(package):
        if needed:
            new_task = create_container_task(phase.id,task.title,None,{},containerType)
            needed = False
        print(package_name + " is deployed on "+ environment +"\n")
        create_undeploy_task(new_task,package_name,None,{'username':username,'password':password,'deployedApplication':package_name,'environment':environment,'deployedApplicationProperties':deployedApplicationProperties,'orchestrators':orchestrators,'failOnPause':failOnPause,'rollbackOnError':rollbackOnError,'cancelOnError':cancelOnError})
    else:
        print(package_name + " is not deployed on "+ environment +"\n")
