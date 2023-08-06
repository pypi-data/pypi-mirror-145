# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Utilities-TUW is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Utilities for the CLI commands."""

import json

from invenio_db import db
from invenio_pidstore.errors import PIDAlreadyExists
from invenio_pidstore.models import PersistentIdentifier

from ..utils import get_record_service


def read_metadata(metadata_file_path):
    """Read the record metadata from the specified JSON file."""
    metadata = None
    with open(metadata_file_path, "r") as metadata_file:
        metadata = json.load(metadata_file)

    if metadata is None:
        raise TypeError(f"not a valid json file: {metadata_file_path}")

    return metadata


def create_record_from_metadata(
    metadata, identity, vanity_pid=None, vanity_pid_type="recid"
):
    """Create a draft from the specified metadata."""
    service = get_record_service()

    if vanity_pid is not None:
        # check if the vanity PID is already taken, before doing anything stupid
        count = PersistentIdentifier.query.filter_by(
            pid_value=vanity_pid, pid_type=vanity_pid_type
        ).count()

        if count > 0:
            raise PIDAlreadyExists(pid_type=vanity_pid_type, pid_value=vanity_pid)

    draft = service.create(identity=identity, data=metadata)._record

    if vanity_pid:
        # service.update_draft() is called to update the IDs in the record's metadata
        # (via record.commit()), re-index the record, and commit the db session
        if service.indexer:
            service.indexer.delete(draft)

        draft.pid.pid_value = vanity_pid
        db.session.commit()

        draft = service.update_draft(
            vanity_pid, identity=identity, data=metadata
        )._record

    return draft


def patch_metadata(metadata: dict, patch: dict) -> dict:
    """Replace the fields mentioned in the patch, while leaving others as is.

    The first argument's content will be changed during the process.
    """
    for key in patch.keys():
        val = patch[key]
        if isinstance(val, dict):
            patch_metadata(metadata[key], val)
        else:
            metadata[key] = val

    return metadata


def get_object_uuid(pid_value, pid_type):
    """Fetch the UUID of the referenced object."""
    uuid = (
        PersistentIdentifier.query.filter_by(pid_value=pid_value, pid_type=pid_type)
        .first()
        .object_uuid
    )

    return uuid


def convert_to_recid(pid_value, pid_type):
    """Fetch the recid of the referenced object."""
    if pid_type != "recid":
        object_uuid = get_object_uuid(pid_value=pid_value, pid_type=pid_type)
        query = PersistentIdentifier.query.filter_by(
            object_uuid=object_uuid,
            pid_type="recid",
        )
        pid_value = query.first().pid_value

    return pid_value


def set_record_owners(record, owners, commit=True):
    """Set the record's owners, assuming an RDMRecord-like record object."""
    parent = record.parent

    parent.access.owners.clear()
    for owner in owners:
        parent.access.owners.add(owner)

    if commit:
        parent.commit()
        db.session.commit()
