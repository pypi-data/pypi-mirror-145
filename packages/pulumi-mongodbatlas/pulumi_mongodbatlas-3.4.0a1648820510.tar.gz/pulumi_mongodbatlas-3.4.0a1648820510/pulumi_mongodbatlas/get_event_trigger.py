# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'GetEventTriggerResult',
    'AwaitableGetEventTriggerResult',
    'get_event_trigger',
    'get_event_trigger_output',
]

@pulumi.output_type
class GetEventTriggerResult:
    """
    A collection of values returned by getEventTrigger.
    """
    def __init__(__self__, app_id=None, config_collection=None, config_database=None, config_full_document=None, config_full_document_before=None, config_match=None, config_operation_type=None, config_operation_types=None, config_project=None, config_providers=None, config_schedule=None, config_schedule_type=None, config_service_id=None, disabled=None, event_processors=None, function_id=None, function_name=None, id=None, name=None, project_id=None, trigger_id=None, type=None):
        if app_id and not isinstance(app_id, str):
            raise TypeError("Expected argument 'app_id' to be a str")
        pulumi.set(__self__, "app_id", app_id)
        if config_collection and not isinstance(config_collection, str):
            raise TypeError("Expected argument 'config_collection' to be a str")
        pulumi.set(__self__, "config_collection", config_collection)
        if config_database and not isinstance(config_database, str):
            raise TypeError("Expected argument 'config_database' to be a str")
        pulumi.set(__self__, "config_database", config_database)
        if config_full_document and not isinstance(config_full_document, bool):
            raise TypeError("Expected argument 'config_full_document' to be a bool")
        pulumi.set(__self__, "config_full_document", config_full_document)
        if config_full_document_before and not isinstance(config_full_document_before, bool):
            raise TypeError("Expected argument 'config_full_document_before' to be a bool")
        pulumi.set(__self__, "config_full_document_before", config_full_document_before)
        if config_match and not isinstance(config_match, str):
            raise TypeError("Expected argument 'config_match' to be a str")
        pulumi.set(__self__, "config_match", config_match)
        if config_operation_type and not isinstance(config_operation_type, str):
            raise TypeError("Expected argument 'config_operation_type' to be a str")
        pulumi.set(__self__, "config_operation_type", config_operation_type)
        if config_operation_types and not isinstance(config_operation_types, list):
            raise TypeError("Expected argument 'config_operation_types' to be a list")
        pulumi.set(__self__, "config_operation_types", config_operation_types)
        if config_project and not isinstance(config_project, str):
            raise TypeError("Expected argument 'config_project' to be a str")
        pulumi.set(__self__, "config_project", config_project)
        if config_providers and not isinstance(config_providers, list):
            raise TypeError("Expected argument 'config_providers' to be a list")
        pulumi.set(__self__, "config_providers", config_providers)
        if config_schedule and not isinstance(config_schedule, str):
            raise TypeError("Expected argument 'config_schedule' to be a str")
        pulumi.set(__self__, "config_schedule", config_schedule)
        if config_schedule_type and not isinstance(config_schedule_type, str):
            raise TypeError("Expected argument 'config_schedule_type' to be a str")
        pulumi.set(__self__, "config_schedule_type", config_schedule_type)
        if config_service_id and not isinstance(config_service_id, str):
            raise TypeError("Expected argument 'config_service_id' to be a str")
        pulumi.set(__self__, "config_service_id", config_service_id)
        if disabled and not isinstance(disabled, bool):
            raise TypeError("Expected argument 'disabled' to be a bool")
        pulumi.set(__self__, "disabled", disabled)
        if event_processors and not isinstance(event_processors, list):
            raise TypeError("Expected argument 'event_processors' to be a list")
        pulumi.set(__self__, "event_processors", event_processors)
        if function_id and not isinstance(function_id, str):
            raise TypeError("Expected argument 'function_id' to be a str")
        pulumi.set(__self__, "function_id", function_id)
        if function_name and not isinstance(function_name, str):
            raise TypeError("Expected argument 'function_name' to be a str")
        pulumi.set(__self__, "function_name", function_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if trigger_id and not isinstance(trigger_id, str):
            raise TypeError("Expected argument 'trigger_id' to be a str")
        pulumi.set(__self__, "trigger_id", trigger_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> str:
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="configCollection")
    def config_collection(self) -> str:
        """
        The name of the MongoDB collection that the trigger watches for change events.
        """
        return pulumi.get(self, "config_collection")

    @property
    @pulumi.getter(name="configDatabase")
    def config_database(self) -> str:
        """
        The name of the MongoDB database that contains the watched collection.
        """
        return pulumi.get(self, "config_database")

    @property
    @pulumi.getter(name="configFullDocument")
    def config_full_document(self) -> bool:
        """
        If true, indicates that `UPDATE` change events should include the most current [majority-committed](https://docs.mongodb.com/manual/reference/read-concern-majority/) version of the modified document in the fullDocument field.
        """
        return pulumi.get(self, "config_full_document")

    @property
    @pulumi.getter(name="configFullDocumentBefore")
    def config_full_document_before(self) -> bool:
        return pulumi.get(self, "config_full_document_before")

    @property
    @pulumi.getter(name="configMatch")
    def config_match(self) -> str:
        """
        A [$match](https://docs.mongodb.com/manual/reference/operator/aggregation/match/) expression document that MongoDB Realm includes in the underlying change stream pipeline for the trigger.
        """
        return pulumi.get(self, "config_match")

    @property
    @pulumi.getter(name="configOperationType")
    def config_operation_type(self) -> str:
        """
        The [authentication operation type](https://docs.mongodb.com/realm/triggers/authentication-triggers/#std-label-authentication-event-operation-types) to listen for.
        """
        return pulumi.get(self, "config_operation_type")

    @property
    @pulumi.getter(name="configOperationTypes")
    def config_operation_types(self) -> Sequence[str]:
        """
        The [database event operation types](https://docs.mongodb.com/realm/triggers/database-triggers/#std-label-database-events) to listen for.
        """
        return pulumi.get(self, "config_operation_types")

    @property
    @pulumi.getter(name="configProject")
    def config_project(self) -> str:
        """
        A [$project](https://docs.mongodb.com/manual/reference/operator/aggregation/project/) expression document that Realm uses to filter the fields that appear in change event objects.
        """
        return pulumi.get(self, "config_project")

    @property
    @pulumi.getter(name="configProviders")
    def config_providers(self) -> Sequence[str]:
        """
        A list of one or more [authentication provider](https://docs.mongodb.com/realm/authentication/providers/) id values. The trigger will only listen for authentication events produced by these providers.
        """
        return pulumi.get(self, "config_providers")

    @property
    @pulumi.getter(name="configSchedule")
    def config_schedule(self) -> str:
        """
        A [cron expression](https://docs.mongodb.com/realm/triggers/cron-expressions/) that defines the trigger schedule.
        """
        return pulumi.get(self, "config_schedule")

    @property
    @pulumi.getter(name="configScheduleType")
    def config_schedule_type(self) -> str:
        return pulumi.get(self, "config_schedule_type")

    @property
    @pulumi.getter(name="configServiceId")
    def config_service_id(self) -> str:
        """
        The ID of the MongoDB Service associated with the trigger.
        """
        return pulumi.get(self, "config_service_id")

    @property
    @pulumi.getter
    def disabled(self) -> bool:
        """
        Status of a trigger.
        """
        return pulumi.get(self, "disabled")

    @property
    @pulumi.getter(name="eventProcessors")
    def event_processors(self) -> Sequence['outputs.GetEventTriggerEventProcessorResult']:
        """
        An object where each field name is an event processor ID and each value is an object that configures its corresponding event processor.
        * `event_processors.0.aws_eventbridge.config_account_id` - AWS Account ID.
        * `event_processors.0.aws_eventbridge.config_region` - Region of AWS Account.
        """
        return pulumi.get(self, "event_processors")

    @property
    @pulumi.getter(name="functionId")
    def function_id(self) -> str:
        """
        The ID of the function associated with the trigger.
        """
        return pulumi.get(self, "function_id")

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> str:
        """
        The name of the function associated with the trigger.
        """
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the trigger.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter(name="triggerId")
    def trigger_id(self) -> str:
        return pulumi.get(self, "trigger_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the trigger.
        """
        return pulumi.get(self, "type")


class AwaitableGetEventTriggerResult(GetEventTriggerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventTriggerResult(
            app_id=self.app_id,
            config_collection=self.config_collection,
            config_database=self.config_database,
            config_full_document=self.config_full_document,
            config_full_document_before=self.config_full_document_before,
            config_match=self.config_match,
            config_operation_type=self.config_operation_type,
            config_operation_types=self.config_operation_types,
            config_project=self.config_project,
            config_providers=self.config_providers,
            config_schedule=self.config_schedule,
            config_schedule_type=self.config_schedule_type,
            config_service_id=self.config_service_id,
            disabled=self.disabled,
            event_processors=self.event_processors,
            function_id=self.function_id,
            function_name=self.function_name,
            id=self.id,
            name=self.name,
            project_id=self.project_id,
            trigger_id=self.trigger_id,
            type=self.type)


def get_event_trigger(app_id: Optional[str] = None,
                      project_id: Optional[str] = None,
                      trigger_id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventTriggerResult:
    """
    `EventTrigger` describe an Event Trigger.


    :param str app_id: The ObjectID of your application.
    :param str project_id: The unique ID for the project to create the trigger.
    :param str trigger_id: The unique ID of the trigger.
    """
    __args__ = dict()
    __args__['appId'] = app_id
    __args__['projectId'] = project_id
    __args__['triggerId'] = trigger_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('mongodbatlas:index/getEventTrigger:getEventTrigger', __args__, opts=opts, typ=GetEventTriggerResult).value

    return AwaitableGetEventTriggerResult(
        app_id=__ret__.app_id,
        config_collection=__ret__.config_collection,
        config_database=__ret__.config_database,
        config_full_document=__ret__.config_full_document,
        config_full_document_before=__ret__.config_full_document_before,
        config_match=__ret__.config_match,
        config_operation_type=__ret__.config_operation_type,
        config_operation_types=__ret__.config_operation_types,
        config_project=__ret__.config_project,
        config_providers=__ret__.config_providers,
        config_schedule=__ret__.config_schedule,
        config_schedule_type=__ret__.config_schedule_type,
        config_service_id=__ret__.config_service_id,
        disabled=__ret__.disabled,
        event_processors=__ret__.event_processors,
        function_id=__ret__.function_id,
        function_name=__ret__.function_name,
        id=__ret__.id,
        name=__ret__.name,
        project_id=__ret__.project_id,
        trigger_id=__ret__.trigger_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_event_trigger)
def get_event_trigger_output(app_id: Optional[pulumi.Input[str]] = None,
                             project_id: Optional[pulumi.Input[str]] = None,
                             trigger_id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventTriggerResult]:
    """
    `EventTrigger` describe an Event Trigger.


    :param str app_id: The ObjectID of your application.
    :param str project_id: The unique ID for the project to create the trigger.
    :param str trigger_id: The unique ID of the trigger.
    """
    ...
