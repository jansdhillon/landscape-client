# Copyright 2017 Canonical Limited.  All rights reserved.
from .message import Message
from landscape.lib.schema import Any
from landscape.lib.schema import Bool
from landscape.lib.schema import Bytes
from landscape.lib.schema import Constant
from landscape.lib.schema import Dict
from landscape.lib.schema import Float
from landscape.lib.schema import Int
from landscape.lib.schema import KeyDict
from landscape.lib.schema import List
from landscape.lib.schema import Tuple
from landscape.lib.schema import Unicode


__all__ = [
    "ACTIVE_PROCESS_INFO",
    "CLOUD_INIT",
    "OPERATION_RESULT",
    "COMPUTER_INFO",
    "DISTRIBUTION_INFO",
    "HARDWARE_INFO",
    "LOAD_AVERAGE",
    "MEMORY_INFO",
    "RESYNCHRONIZE",
    "MOUNT_ACTIVITY",
    "MOUNT_INFO",
    "FREE_SPACE",
    "REGISTER",
    "REGISTER_3_3",
    "TEMPERATURE",
    "PROCESSOR_INFO",
    "USERS",
    "PACKAGES",
    "PACKAGE_LOCKS",
    "CHANGE_PACKAGES_RESULT",
    "UNKNOWN_PACKAGE_HASHES",
    "ADD_PACKAGES",
    "PACKAGE_REPORTER_RESULT",
    "TEXT_MESSAGE",
    "TEST",
    "CUSTOM_GRAPH",
    "REBOOT_REQUIRED",
    "APT_PREFERENCES",
    "NETWORK_DEVICE",
    "NETWORK_ACTIVITY",
    "REBOOT_REQUIRED_INFO",
    "UPDATE_MANAGER_INFO",
    "CPU_USAGE",
    "CEPH_USAGE",
    "SWIFT_USAGE",
    "SWIFT_DEVICE_INFO",
    "KEYSTONE_TOKEN",
    "JUJU_UNITS_INFO",
    "CLOUD_METADATA",
    "COMPUTER_TAGS",
    "UBUNTU_PRO_INFO",
    "LIVEPATCH",
    "UBUNTU_PRO_REBOOT_REQUIRED",
    "USG_AUDIT",
    "SNAPS",
    "SNAP_INFO",
]


# When adding a new schema, which deprecates an older schema, the recommended
# naming convention, is to name it SCHEMA_NAME_ and the last API version that
# the schema works with.
#
# i.e. if I have USERS and I'm deprecating it, in API 2.2, then USERS becomes
# USERS_2_1


process_info = KeyDict(
    {
        "pid": Int(),
        "name": Unicode(),
        "state": Bytes(),
        "sleep-average": Int(),
        "uid": Int(),
        "gid": Int(),
        "vm-size": Int(),
        "start-time": Int(),
        "percent-cpu": Float(),
    },
    # Optional for backwards compatibility
    optional=["vm-size", "sleep-average", "percent-cpu"],
)

ACTIVE_PROCESS_INFO = Message(
    "active-process-info",
    {
        "kill-processes": List(Int()),
        "kill-all-processes": Bool(),
        "add-processes": List(process_info),
        "update-processes": List(process_info),
    },
    # XXX Really we don't want all three of these keys to be optional:
    # we always want _something_...
    optional=[
        "add-processes",
        "update-processes",
        "kill-processes",
        "kill-all-processes",
    ],
)

OPERATION_RESULT = Message(
    "operation-result",
    {
        "operation-id": Int(),
        "status": Int(),
        "result-code": Int(),
        "result-text": Unicode(),
    },
    optional=["result-code", "result-text"],
)

COMPUTER_INFO = Message(
    "computer-info",
    {
        "hostname": Unicode(),
        "total-memory": Int(),
        "total-swap": Int(),
        "annotations": Dict(Unicode(), Unicode()),
        "machine-id": Unicode(),
    },
    # Not sure why these are all optional, but it's explicitly tested
    # in the server
    optional=[
        "hostname",
        "total-memory",
        "total-swap",
        "annotations",
        "machine-id",
    ],
)

DISTRIBUTION_INFO = Message(
    "distribution-info",
    {
        "distributor-id": Unicode(),
        "description": Unicode(),
        "release": Unicode(),
        "code-name": Unicode(),
    },
    # all optional because the lsb-release file may not have all data.
    optional=["distributor-id", "description", "release", "code-name"],
)

CLOUD_METADATA = Message(
    "cloud-instance-metadata",
    {
        "instance-id": Unicode(),
        "ami-id": Unicode(),
        "instance-type": Unicode(),
    },
)

SNAP_INFO = Message(
    "snap-info",
    {
        "brand": Unicode(),
        "model": Unicode(),
        "serial": Unicode(),
    },
)

HARDWARE_INFO = Message("hardware-info", {"data": Unicode()})

juju_data = {
    "environment-uuid": Unicode(),
    "api-addresses": List(Unicode()),
    "unit-name": Unicode(),
    "private-address": Unicode(),
}

# The copy of juju_data is needed because Message mutates the dictionary
JUJU_UNITS_INFO = Message(
    "juju-units-info",
    {
        "juju-info-list": List(
            KeyDict(juju_data.copy(), optional=["private-address"]),
        ),
    },
)

LOAD_AVERAGE = Message(
    "load-average",
    {
        "load-averages": List(Tuple(Int(), Float())),
    },
)

CPU_USAGE = Message(
    "cpu-usage",
    {
        "cpu-usages": List(Tuple(Int(), Float())),
    },
)

CEPH_USAGE = Message(
    "ceph-usage",
    {
        "ring-id": Unicode(),
        # Usage data points in the form (timestamp, size, avail, used)
        "data-points": List(Tuple(Int(), Int(), Int(), Int())),
        # Unused now, for backwards compatibility
        "ceph-usages": List(None),
    },
)

SWIFT_DEVICE_INFO = Message(
    "swift-device-info",
    {
        "swift-device-info": List(
            KeyDict({"device": Unicode(), "mounted": Bool()}),
        ),
    },
)

SWIFT_USAGE = Message(
    "swift-usage",
    {
        # Usage data points in the form (timestamp, device, size, avail, used)
        "data-points": List(Tuple(Int(), Unicode(), Int(), Int(), Int())),
    },
)

KEYSTONE_TOKEN = Message(
    "keystone-token",
    {"data": Any(Bytes(), Constant(None))},
)

MEMORY_INFO = Message(
    "memory-info",
    {
        "memory-info": List(Tuple(Float(), Int(), Int())),
    },
)

RESYNCHRONIZE = Message(
    "resynchronize",
    {"operation-id": Int()},
    # operation-id is only there if it's a response to a server-initiated
    # resynchronize.
    optional=["operation-id"],
)

MOUNT_ACTIVITY = Message(
    "mount-activity",
    {"activities": List(Tuple(Float(), Unicode(), Bool()))},
)


MOUNT_INFO = Message(
    "mount-info",
    {
        "mount-info": List(
            Tuple(
                Float(),
                KeyDict(
                    {
                        "mount-point": Unicode(),
                        "device": Unicode(),
                        "filesystem": Unicode(),
                        "total-space": Int(),
                    },
                ),
            ),
        ),
    },
)

FREE_SPACE = Message(
    "free-space",
    {"free-space": List(Tuple(Float(), Unicode(), Int()))},
)


REGISTER = Message(
    "register",
    # The term used in the UI is actually 'registration_key', but we keep
    # the message schema field as 'registration_password' in case a new
    # client contacts an older server.
    {
        "registration_password": Any(Unicode(), Constant(None)),
        "computer_title": Unicode(),
        "hostname": Unicode(),
        "account_name": Unicode(),
        "tags": Any(Unicode(), Constant(None)),
        "vm-info": Bytes(),
        "container-info": Unicode(),
        "access_group": Unicode(),
    },
    optional=[
        "registration_password",
        "hostname",
        "tags",
        "vm-info",
        "container-info",
        "access_group",
    ],
)


REGISTER_3_3 = Message(
    "register",
    # The term used in the UI is actually 'registration_key', but we keep
    # the message schema field as 'registration_password' in case a new
    # client contacts an older server.
    {
        "registration_password": Any(Unicode(), Constant(None)),
        "computer_title": Unicode(),
        "hostname": Unicode(),
        "account_name": Unicode(),
        "tags": Any(Unicode(), Constant(None)),
        "vm-info": Bytes(),
        "container-info": Unicode(),
        "juju-info": KeyDict(
            {
                "environment-uuid": Unicode(),
                "api-addresses": List(Unicode()),
                "machine-id": Unicode(),
            },
        ),
        "access_group": Unicode(),
        "clone_secure_id": Any(Unicode(), Constant(None)),
        "ubuntu_pro_info": Unicode(),
        "hostagent_uid": Unicode(),
        "installation_request_id": Unicode(),
        "authenticated_attach_code": Unicode(),
        "machine_id": Unicode(),
    },
    api=b"3.3",
    optional=[
        "registration_password",
        "hostname",
        "tags",
        "vm-info",
        "container-info",
        "access_group",
        "juju-info",
        "clone_secure_id",
        "ubuntu_pro_info",
        "hostagent_uid",
        "installation_request_id",
        "authenticated_attach_code",
        "machine_id",
    ],
)

TEMPERATURE = Message(
    "temperature",
    {
        "thermal-zone": Unicode(),
        "temperatures": List(Tuple(Int(), Float())),
    },
)

PROCESSOR_INFO = Message(
    "processor-info",
    {
        "processors": List(
            KeyDict(
                {
                    "processor-id": Int(),
                    "vendor": Unicode(),
                    "model": Unicode(),
                    "cache-size": Int(),
                },
                optional=["vendor", "cache-size"],
            ),
        ),
    },
)

user_data = KeyDict(
    {
        "uid": Int(),
        "username": Unicode(),
        "name": Any(Unicode(), Constant(None)),
        "enabled": Bool(),
        "location": Any(Unicode(), Constant(None)),
        "home-phone": Any(Unicode(), Constant(None)),
        "work-phone": Any(Unicode(), Constant(None)),
        "primary-gid": Any(Int(), Constant(None)),
        "primary-groupname": Unicode(),
    },
    optional=["primary-groupname", "primary-gid"],
)

group_data = KeyDict({"gid": Int(), "name": Unicode()})

USERS = Message(
    "users",
    {
        "operation-id": Int(),
        "create-users": List(user_data),
        "update-users": List(user_data),
        "delete-users": List(Unicode()),
        "create-groups": List(group_data),
        "update-groups": List(group_data),
        "delete-groups": List(Unicode()),
        "create-group-members": Dict(Unicode(), List(Unicode())),
        "delete-group-members": Dict(Unicode(), List(Unicode())),
    },
    # operation-id is only there for responses, and all other are
    # optional as long as one of them is there (no way to say that yet)
    optional=[
        "operation-id",
        "create-users",
        "update-users",
        "delete-users",
        "create-groups",
        "update-groups",
        "delete-groups",
        "create-group-members",
        "delete-group-members",
    ],
)

package_ids_or_ranges = List(Any(Tuple(Int(), Int()), Int()))
PACKAGES = Message(
    "packages",
    {
        "installed": package_ids_or_ranges,
        "available": package_ids_or_ranges,
        "available-upgrades": package_ids_or_ranges,
        "locked": package_ids_or_ranges,
        "autoremovable": package_ids_or_ranges,
        "not-autoremovable": package_ids_or_ranges,
        "security": package_ids_or_ranges,
        "not-installed": package_ids_or_ranges,
        "not-available": package_ids_or_ranges,
        "not-available-upgrades": package_ids_or_ranges,
        "not-locked": package_ids_or_ranges,
        "not-security": package_ids_or_ranges,
    },
    optional=[
        "installed",
        "available",
        "available-upgrades",
        "locked",
        "not-available",
        "not-installed",
        "not-available-upgrades",
        "not-locked",
        "autoremovable",
        "not-autoremovable",
        "security",
        "not-security",
    ],
)

package_locks = List(Tuple(Unicode(), Unicode(), Unicode()))
PACKAGE_LOCKS = Message(
    "package-locks",
    {"created": package_locks, "deleted": package_locks},
    optional=["created", "deleted"],
)

CHANGE_PACKAGE_HOLDS = Message(
    "change-package-holds",
    {"created": List(Unicode()), "deleted": List(Unicode())},
    optional=["created", "deleted"],
)

CHANGE_PACKAGES_RESULT = Message(
    "change-packages-result",
    {
        "operation-id": Int(),
        "must-install": List(Any(Int(), Constant(None))),
        "must-remove": List(Any(Int(), Constant(None))),
        "result-code": Int(),
        "result-text": Unicode(),
    },
    optional=["result-text", "must-install", "must-remove"],
)

UNKNOWN_PACKAGE_HASHES = Message(
    "unknown-package-hashes",
    {
        "hashes": List(Bytes()),
        "request-id": Int(),
    },
)

PACKAGE_REPORTER_RESULT = Message(
    "package-reporter-result",
    {"report-timestamp": Float(), "code": Int(), "err": Unicode()},
    optional=["report-timestamp"],
)

ADD_PACKAGES = Message(
    "add-packages",
    {
        "packages": List(
            KeyDict(
                {
                    "name": Unicode(),
                    "description": Unicode(),
                    "section": Unicode(),
                    "relations": List(Tuple(Int(), Unicode())),
                    "summary": Unicode(),
                    "installed-size": Any(Int(), Constant(None)),
                    "size": Any(Int(), Constant(None)),
                    "version": Unicode(),
                    "type": Int(),
                },
            ),
        ),
        "request-id": Int(),
    },
)

TEXT_MESSAGE = Message("text-message", {"message": Unicode()})

TEST = Message(
    "test",
    {
        "greeting": Bytes(),
        "consistency-error": Bool(),
        "echo": Bytes(),
        "sequence": Int(),
    },
    optional=["greeting", "consistency-error", "echo", "sequence"],
)

# The tuples are timestamp, value
GRAPH_DATA = KeyDict(
    {
        "values": List(Tuple(Float(), Float())),
        "error": Unicode(),
        "script-hash": Bytes(),
    },
)

CUSTOM_GRAPH = Message("custom-graph", {"data": Dict(Int(), GRAPH_DATA)})

# XXX This is kept for backward compatibility, it can eventually be removed
# when all clients will support REBOOT_REQUIRED_INFO
REBOOT_REQUIRED = Message("reboot-required", {"flag": Bool()})

REBOOT_REQUIRED_INFO = Message(
    "reboot-required-info",
    {"flag": Bool(), "packages": List(Unicode())},
    optional=["flag", "packages"],
)

APT_PREFERENCES = Message(
    "apt-preferences",
    {"data": Any(Dict(Unicode(), Unicode()), Constant(None))},
)

# The network-device message is split in two top level keys because we don't
# support adding sub-keys in a backwards-compatible way (only top-level keys).
# New servers will see an optional device-speeds key, and old servers will
# simply ignore the extra info..
NETWORK_DEVICE = Message(
    "network-device",
    {
        "devices": List(
            KeyDict(
                {
                    "interface": Bytes(),
                    "ip_address": Bytes(),
                    "mac_address": Bytes(),
                    "broadcast_address": Bytes(),
                    "netmask": Bytes(),
                    "flags": Int(),
                },
            ),
        ),
        "device-speeds": List(
            KeyDict({"interface": Bytes(), "speed": Int(), "duplex": Bool()}),
        ),
    },
    optional=["device-speeds"],
)

NETWORK_ACTIVITY = Message(
    "network-activity",
    # Dict maps interfaces to their network activity. The network activity of
    # an interface a is a list of 3-tuples (step, in, out), where 'step' is the
    # time interval and 'in'/'out' are number of bytes received/sent over the
    # interval.
    {"activities": Dict(Bytes(), List(Tuple(Int(), Int(), Int())))},
)

UPDATE_MANAGER_INFO = Message("update-manager-info", {"prompt": Unicode()})

COMPUTER_TAGS = Message(
    "computer-tags",
    {"tags": Any(Unicode(), Constant(None))},
)

UBUNTU_PRO_INFO = Message("ubuntu-pro-info", {"ubuntu-pro-info": Unicode()})

LIVEPATCH = Message("livepatch", {"livepatch": Unicode()})

UBUNTU_PRO_REBOOT_REQUIRED = Message(
    "ubuntu-pro-reboot-required",
    {"ubuntu-pro-reboot-required": Unicode()},
)

CLOUD_INIT = Message(
    "cloud-init",
    {"cloud-init": Unicode()},
)

SNAPS = Message(
    "snaps",
    {
        "snaps": KeyDict(
            {
                "installed": List(
                    KeyDict(
                        {
                            "id": Unicode(),
                            "name": Unicode(),
                            "version": Unicode(),
                            "revision": Unicode(),
                            "tracking-channel": Unicode(),
                            "hold": Unicode(),
                            "publisher": KeyDict(
                                {
                                    "username": Unicode(),
                                    "validation": Unicode(),
                                },
                                strict=False,
                            ),
                            "confinement": Unicode(),
                            "summary": Unicode(),
                            "config": Unicode(),
                        },
                        strict=False,
                        optional=[
                            "hold",
                            "summary",
                            "publisher",
                            "tracking-channel",
                            "config",
                        ],
                    ),
                ),
            },
        ),
    },
)

SNAP_SERVICES = Message(
    "snap-services",
    {
        "services": KeyDict(
            {
                "running": List(
                    KeyDict(
                        {
                            "name": Unicode(),
                            "snap": Unicode(),
                            "desktop-file": Unicode(),
                            "daemon": Unicode(),
                            "daemon-scope": Unicode(),
                            "enabled": Bool(),
                            "active": Bool(),
                            "activators": List(
                                Dict(Unicode(), Any(Unicode(), Bool())),
                            ),
                        },
                        strict=False,
                        optional=[
                            "snap",
                            "desktop-file",
                            "daemon",
                            "daemon-scope",
                            "enabled",
                            "active",
                            "activators",
                        ],
                    ),
                ),
            },
            strict=False,
        ),
    },
)

USG_AUDIT = Message(
    "usg-audit",
    {
        "report": Bytes(),
        "operation-id": Int(),
        "run-id": Unicode(),
    },
)

message_schemas = (
    ACTIVE_PROCESS_INFO,
    CLOUD_INIT,
    OPERATION_RESULT,
    COMPUTER_INFO,
    DISTRIBUTION_INFO,
    HARDWARE_INFO,
    LOAD_AVERAGE,
    MEMORY_INFO,
    RESYNCHRONIZE,
    MOUNT_ACTIVITY,
    MOUNT_INFO,
    FREE_SPACE,
    REGISTER,
    REGISTER_3_3,
    TEMPERATURE,
    PROCESSOR_INFO,
    USERS,
    PACKAGES,
    PACKAGE_LOCKS,
    CHANGE_PACKAGES_RESULT,
    UNKNOWN_PACKAGE_HASHES,
    ADD_PACKAGES,
    PACKAGE_REPORTER_RESULT,
    TEXT_MESSAGE,
    TEST,
    CUSTOM_GRAPH,
    REBOOT_REQUIRED,
    APT_PREFERENCES,
    NETWORK_DEVICE,
    NETWORK_ACTIVITY,
    REBOOT_REQUIRED_INFO,
    UPDATE_MANAGER_INFO,
    CPU_USAGE,
    CEPH_USAGE,
    SWIFT_USAGE,
    SWIFT_DEVICE_INFO,
    KEYSTONE_TOKEN,
    JUJU_UNITS_INFO,
    CLOUD_METADATA,
    COMPUTER_TAGS,
    UBUNTU_PRO_INFO,
    LIVEPATCH,
    UBUNTU_PRO_REBOOT_REQUIRED,
    USG_AUDIT,
    SNAPS,
    SNAP_INFO,
    SNAP_SERVICES,
)
