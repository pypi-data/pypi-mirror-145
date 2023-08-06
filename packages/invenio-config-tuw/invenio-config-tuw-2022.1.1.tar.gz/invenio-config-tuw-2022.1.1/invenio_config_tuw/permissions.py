# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

from flask_login import current_user
from flask_principal import RoleNeed, UserNeed
from invenio_rdm_records.services import RDMRecordPermissionPolicy
from invenio_rdm_records.services.generators import (
    IfRestricted,
    RecordOwners,
    SecretLinks,
)
from invenio_records_permissions.generators import (
    Admin,
    AnyUser,
    AuthenticatedUser,
    Disable,
    Generator,
    SuperUser,
    SystemProcess,
)
from invenio_requests.services.permissions import (
    PermissionPolicy as RequestsPermissionPolicy,
)


class TrustedUsers(Generator):
    """Allows users with the "trusted-user" role."""

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        return [RoleNeed("trusted-user")]


class RecordOwnersWithRole(Generator):
    """Allows record owners with a given role."""

    def __init__(self, role_name, exclude=True):
        """Constructor."""
        super().__init__()
        self.role_name = role_name
        self.exclude = exclude

    def needs(self, record=None, **kwargs):
        """Enabling Needs."""
        if record is None:
            if (
                bool(current_user)
                and not current_user.is_anonymous
                and current_user.has_role(self.role_name)
            ):
                return [UserNeed(current_user.id)]
            else:
                return []

        return [
            UserNeed(owner.owner_id)
            for owner in record.parent.access.owners
            if owner.resolve().has_role(self.role_name)
        ]

    def excludes(self, **kwargs):
        """Explicit excludes."""
        if not self.exclude:
            return super().excludes(**kwargs)

        elif (
            bool(current_user)
            and not current_user.is_anonymous
            and not current_user.has_role(self.role_name)
        ):
            return [UserNeed(current_user.id)]

        return []


def TrustedRecordOwners(exclude=False):
    """Allows record owners with the "trusted-user" role."""
    return RecordOwnersWithRole("trusted-user", exclude=exclude)


def TrustedPublisherRecordOwners(exclude=False):
    """Allows record owners with the "trusted-publisher" role."""
    return RecordOwnersWithRole("trusted-publisher", exclude=exclude)


secret_links = {
    "edit": [SecretLinks("edit")],
    "view": [SecretLinks("edit"), SecretLinks("view")],
    "view_record": [SecretLinks("edit"), SecretLinks("view"), SecretLinks("record")],
    "view_files": [SecretLinks("edit"), SecretLinks("view"), SecretLinks("files")],
    "preview": [SecretLinks("edit"), SecretLinks("preview")],
}

owner_if_restricted_record = IfRestricted(
    "record", then_=[RecordOwners()], else_=[AnyUser()]
)

owner_if_restricted_files = IfRestricted(
    "files", then_=[RecordOwners()], else_=[AnyUser()]
)


# TODO add review-related permissions to the once we allow requests
# -> CommunityCurator, SubmissionReviewer
# (c.f. changes since rdm-records v0.32.5)
class TUWRecordPermissionPolicy(RDMRecordPermissionPolicy):
    """Record permission policy of TU Wien."""

    # note: edit := create a draft from a record (i.e. putting it in edit mode),
    #               which does not imply the permission to save the edits
    # note: can_search_* is the permission for the search in general, the records
    #       (drafts) will be filtered as per can_read_* permissions
    # fmt: off
    # high-level permissions
    can_manage             = [RecordOwners(),                 Admin(), SuperUser(), SystemProcess()]                                # noqa
    can_curate             = [TrustedRecordOwners(),          Admin(), SuperUser(), SystemProcess()] + secret_links["edit"]         # noqa
    can_preview            = [RecordOwners(),                 Admin(), SuperUser(), SystemProcess()] + secret_links["preview"]      # noqa
    can_view               = [RecordOwners(),                 Admin(), SuperUser(), SystemProcess()] + secret_links["view"]         # noqa

    # records
    can_search             = [AnyUser(),                      Admin(), SuperUser(), SystemProcess()]                                # noqa
    can_read               = [owner_if_restricted_record,     Admin(), SuperUser(), SystemProcess()] + secret_links["view_record"]  # noqa
    can_read_files         = [owner_if_restricted_files,      Admin(), SuperUser(), SystemProcess()] + secret_links["view_files"]   # noqa
    can_create             = [TrustedUsers(),                 Admin(), SuperUser(), SystemProcess()]                                # noqa

    # drafts
    can_search_drafts      = [AuthenticatedUser(),            Admin(), SuperUser(), SystemProcess()]                                # noqa
    can_read_draft         = [                            *can_preview                             ]                                # noqa
    can_update_draft       = [                            *can_curate                              ]                                # noqa
    can_draft_read_files   = [                            *can_preview                             ]                                # noqa
    can_draft_create_files = [                            *can_curate                              ]                                # noqa
    can_draft_update_files = [                            *can_curate                              ]                                # noqa
    can_draft_delete_files = [                            *can_curate                              ]                                # noqa

    # PIDs
    can_pid_reserve        = [                            *can_curate                              ]                                # noqa
    can_pid_delete         = [                            *can_curate                              ]                                # noqa

    # actions
    can_edit               = [RecordOwners(),             *can_curate                              ]                                # noqa
    can_delete_draft       = [                            *can_curate                              ]                                # noqa
    can_new_version        = [                            *can_curate                              ]                                # noqa
    can_lift_embargo       = [                            *can_manage                              ]                                # noqa
    can_publish            = [TrustedPublisherRecordOwners(), Admin(), SuperUser(), SystemProcess()]                                # noqa

    # disabled (record management in InvenioRDM goes through drafts)
    can_update             = [                             Disable()                               ]                                # noqa
    can_delete             = [                             Disable()                               ]                                # noqa
    can_create_files       = [                             Disable()                               ]                                # noqa
    can_update_files       = [                             Disable()                               ]                                # noqa
    can_delete_files       = [                             Disable()                               ]                                # noqa
    # fmt: on


# TODO allow requests once the requests are more stable
class TUWRequestsPermissionPolicy(RequestsPermissionPolicy):
    """Requests permission policy of TU Wien."""

    # fmt: off
    # Requests: Management
    can_create = [Disable()]
    can_search = [Disable()]
    can_read   = [Disable()]
    can_update = [Disable()]
    can_delete = [Disable()]

    # Actions: Submit/Cancel/Accept/Decline/Expire
    can_action_submit  = [Disable()]
    can_action_cancel  = [Disable()]
    can_action_accept  = [Disable()]
    can_action_decline = [Disable()]
    can_action_expire  = [Disable()]

    # Request Events: Comments
    can_create_comment = [Disable()]
    can_update_comment = [Disable()]
    can_delete_comment = [Disable()]

    # Request Events: All other events
    can_create_event = [Disable()]
    can_read_event   = [Disable()]
    can_update_event = [Disable()]
    can_delete_event = [Disable()]
    can_search_event = [Disable()]
    # fmt: on
