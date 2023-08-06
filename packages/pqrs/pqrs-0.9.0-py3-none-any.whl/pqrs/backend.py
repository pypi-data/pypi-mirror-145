"""
Implements backend-related functionality.
"""

from contextlib import contextmanager
import dataclasses
import itertools
import json
import os
import pathlib
from typing import Optional, Any

import ansible_runner
import datafiles.formats
import rich.prompt
import temppathlib
import yaml
from plumbum import local, FG, BG
from plumbum.commands.processes import ProcessExecutionError

from pqrs import paths
from pqrs.config import config
from pqrs.version import Version


@dataclasses.dataclass
class Role:
    """
    A collection of metadata related to a single ansible role.
    """

    name: str
    collection: str
    description: list[str]
    dependencies: list[str]
    variables: dict[str, Any]
    available_version: Version
    installed_version: Optional[Version] = None
    selected: bool = False
    hidden: bool = False  # A hidden role performs no changes on the system, i.e. 'facts' collection role

    @classmethod
    def from_path(cls, path, collection):
        # type: (pathlib.Path, str) -> Role
        """
        Construct a Role object from a given filesystem path. The information
        about the role is loaded from the meta/pqrs.yml file.
        """

        name = path.stem

        metadata = {}

        # Load PQRS metadata file
        pqrs_metadata_path = path / 'meta/pqrs.yml'

        if pqrs_metadata_path.exists():
            hidden = False
            with open(pqrs_metadata_path) as f:
                metadata = yaml.safe_load(f)
        else:
            hidden = True

        description = metadata.get('description', '')
        available = Version(metadata.get('version', '0.0.0'))
        installed = (config.channels[collection]['roles'] or {}).get(name)
        config_vars = metadata.get('config', {})
        dependencies = metadata.get('dependencies', [])

        return cls(
            name,
            collection,
            [line.strip() for line in description.splitlines()],
            [d for d in dependencies if d is not None],
            config_vars,
            available,
            Version(installed) if installed else None,
            False,  # By default nothing is selected. This has to be toggled later.
            hidden
        )

    @property
    def is_outdated(self):
        # type: () -> bool
        """
        Returns True if role should be run.
        """

        return self.installed_version is None or self.available_version > self.installed_version


def discover_roles(hidden=False):
    # type: (bool) -> dict[str, list[Role]]
    """
    Discovers PQRS-enabled roles on the filesystem.
    """

    # Discover the PQRS-enabled collections
    pqrs_collections = {
        f"{path.parent.parent.stem}.{path.parent.stem}": path.parent
        for path in paths.COLLECTIONS.glob('*/*/MANIFEST.json')
        if len(list(path.parent.glob('roles/*/meta/pqrs.yml'))) > 0
    }

    # Locate the roles for each collection
    return {
        collection: [
            Role.from_path(p, collection)
            for p in path.glob('roles/*')
            if hidden or (p / 'meta/pqrs.yml').exists()
        ]
        for collection, path in pqrs_collections.items()
    }

def bump_role_version(role, version=None):
    """
    Bumps the version of the role in the config to the given version. Defaults
    to latest.
    """

    # Default to the bump to the last version
    version = version or role.available_version

    # Create role dict if it does not exist
    if not config.channels[role.collection].get("roles"):
        config.channels[role.collection]["roles"] = {}

    config.channels[role.collection]["roles"][role.name] = version


def is_sudo_password_valid(password):
    """
    Returns True if the sudo password is valid, False otherwise.
    """

    sudo = local.cmd.sudo

    try:
        # The -k option ensures we don't use cached credentials
        command = local.cmd.sudo["--stdin", "-k", "echo", "1"] << password
        command()
        return True
    except ProcessExecutionError:
        return False


def is_sudo_passwordless():
    """
    Attempts to escalate to superuser privileges to determine whether a
    password is required for doing so.
    """

    try:
        # The -k option ensures we don't use cached credentials
        local.cmd.sudo["--non-interactive", "-k", "echo", "1"]()
        return True
    except ProcessExecutionError:
        return False


def execute_roles(roles_to_run, status, stderr, become_password=None, assume_yes=False, verbosity=0):
    """
    Executes the given roles using ansible-runner.
    """
    # Execute the playbook, using private role vars switch to ensure
    # role_version variables are not overwriting each other
    os.environ["ANSIBLE_PRIVATE_ROLE_VARS"] = "True"

    # Supress colorful output (and cows) in the stdout
    os.environ["ANSIBLE_NOCOLOR"] = "True"
    os.environ["ANSIBLE_NOCOWS"] = "True"

    role_paths = [
        str(paths.COLLECTIONS / f"{collection.replace('.', '/')}/roles")
        for collection in roles_to_run
    ]

    current_role = None
    roles_by_name = {role.name: role for role in itertools.chain(*discover_roles(hidden=True).values())}
    roles_success = {}

    def ensure_role_header(role_name):
        nonlocal current_role
        if role_name == current_role or role_name is None:
            return

        current_role = role_name
        role = roles_by_name.get(role_name)
        if role is not None:
            stderr.print(f"\n[magenta]{role_name}:[/] {role.installed_version or '0.0.0'} -> {role.available_version}")

    def check_event_handler(data, **kwargs):
        event_type = data.get("event")

        if event_type.startswith("runner_on_"):
            event_type = event_type.removeprefix("runner_on_")

            role = data["event_data"].get("role", "")
            task = data["event_data"].get("task", "")
            changed = data["event_data"].get("res", {}).get("changed")

            # Do not print a line for built-in fact collection
            if task == "Gathering Facts":
                return

            # Do not provide any feedback for a hidden role
            if role and roles_by_name[role].hidden:
                return

            # Supress pqrs-meta: tasks
            if task.startswith("pqrs-meta:"):
                return

            if event_type == "start":
                # Start of the task
                ensure_role_header(role)
                status.update(f"{task} [dim](analyzing..)[/]")
            elif event_type == "ok":
                # End of the task
                if changed or verbosity > 0:
                    ensure_role_header(role)
                    stderr.print(f"[yellow]-[/] {task}")
            elif event_type == "skipped":
                # Do not print anything for skipped tasks
                pass

    def event_handler(data, **kwargs):
        event_type = data.get("event")

        if event_type == "verbose":
            # Supress verbose messages for now
            pass
        elif event_type.startswith("playbook_on"):
            # Playbook events don't contain interesting information
            pass
        elif event_type.startswith("runner_on"):
            role = data["event_data"].get("role", "")
            task = data["event_data"].get("task", "")
            changed = data["event_data"].get("res", {}).get("changed")

            # Record success / failure from "pqrs-meta: Termination guard"(s)
            if task.startswith("pqrs-meta: Termination guard") and event_type == "runner_on_ok":
                # The termination guard(s) are not a part of the role, so
                # we have to extract the relevant role (and completion
                # status) from the debug message of the guard
                reported_role, reported_status = data["event_data"]["res"]["msg"].split()

                if not roles_by_name[reported_role].hidden:
                    success = (reported_status == "success")
                    roles_success[reported_role] = success
                    if success:
                        bump_role_version(roles_by_name[reported_role])

            # Supress pqrs-meta: tasks
            if task.startswith("pqrs-meta:"):
                return

            # Do not print a line for built-in fact collection
            if task == "Gathering Facts":
                return

            # Do not provide any feedback for a hidden role
            if role and roles_by_name[role].hidden:
                return

            ensure_role_header(role)

            if event_type == "runner_on_start":
                # Start of the task
                status.update(f"{task} [dim](executing..)[/]")
            elif event_type == "runner_on_ok":
                # End of the task
                symbol = "[green]✔[/]" if changed else "[blue]↻[/]"
                if changed or verbosity > 0:
                    stderr.print(f"{symbol} {task}")
            elif event_type == "runner_on_failed":
                ignore_errors = data["event_data"].get("ignore_errors", False)
                if ignore_errors:
                    stderr.print(f"[yellow]![/] {task} [dim](ignoring allowed error...)[/]")
                else:
                    stderr.print(f"[red][bold]✗[/] {task}")

    if not assume_yes:
        with _prepare_execution_environment(roles_to_run, become_password) as tmpdir:
            # Collect all the tasks to execute and await confirmation
            stderr.print("[bold]Analyzing system for applicable updates[/]")
            runner = ansible_runner.interface.run(
                private_data_dir=str(tmpdir.path),
                project_dir=str(tmpdir.path),
                roles_path=role_paths,
                playbook="play.yml",
                event_handler=check_event_handler,
                cmdline="--check",
                quiet=True
            )

        current_role = None

        status.stop()
        if not rich.prompt.Confirm.ask("Do you wish to apply the updates?"):
            return

        # A spacer between the check phase and the execution phase
        stderr.print("\n\n")

    status.update("Comitting current PQRS configuration...")
    local.cmd.git["-C", str(paths.PQRS_LOCATION), "add", "."] & BG
    local.cmd.git["-C", str(paths.PQRS_LOCATION), "commit", "-a", "-m", "PQRS: Pre-update commit"] & BG

    status.update("Applying configuration updates...")
    status.start()

    with _prepare_execution_environment(roles_to_run, become_password) as tmpdir:
        stderr.print("[bold]Applying configuration updates[/]")
        runner = ansible_runner.interface.run(
            private_data_dir=str(tmpdir.path),
            project_dir=str(tmpdir.path),
            roles_path=role_paths,
            playbook="play.yml",
            event_handler=event_handler,
            quiet=True
        )

    # Prepare summary
    successes = [roles_by_name[role] for role, status in roles_success.items() if status is True]
    failures = [roles_by_name[role] for role, status in roles_success.items() if status is False]

    success_msg = failure_msg = None

    if successes:
        success_msg = (
            f"Successfully applied {len(successes)} role{'s' if len(successes) > 1 else ''}: " +
            ", ".join([f'{role.name} ({role.available_version})' for role in successes])
        )
    if failures:
        failure_msg = (
            f"The following {len(failures)} role{'s' if len(failures) > 1 else ''} failed: " +
            ", ".join([f'{role.name} ({role.available_version})' for role in failures])
        )

    status.update("Comitting updated PQRS configuration...")
    local.cmd.git["-C", str(paths.PQRS_LOCATION), "add", "."] & BG
    commit_message = (
        "-m", "PQRS: Post-update commit",
        *(["-m", success_msg] if successes else []),
        *(["-m", failure_msg] if failures else [])
    )
    local.cmd.git[("-C", str(paths.PQRS_LOCATION), "commit", "-a", *commit_message)] & BG

    if successes or failures:
        stderr.print("\n\n[bold]Summary[/]")

    if successes:
        stderr.print(success_msg)
    if failures:
        stderr.print(failure_msg)
        stdout_path = list(tmpdir.path.glob("artifacts/*/stdout"))
        if stdout_path:
            stderr.print(f"For more details, please refer to the log file: '{stdout_path[0]}'.")

@contextmanager
def _prepare_execution_environment(roles_to_run, become_password=None):
    try:
        if become_password:
            os.environ["PQRS_BECOME"] = become_password
        with temppathlib.TemporaryDirectory(prefix="pqrs-", dont_delete=True) as tmpdir:
            # Dump the configuration values into a temp file
            with open(tmpdir.path / "vars.yml", "w") as f:
                # We need to use datafiles serializer directly to turn just one
                # attribute of the class into yaml
                content = datafiles.formats.YAML.serialize(config.variables)
                if become_password:
                    content += '''\nansible_become_password: "{{ lookup('env', 'PQRS_BECOME') }}"'''
                f.write(content)

            # Prepare the playbook. The playbook consists of a single play, which
            # configures all roles that need to be executed (=the ones that have
            # new tasks to be applied).

            # First we need to order roles by their dependencies, ensuring roles
            # that depend on a different role have that role run first
            def order_by_dependencies_and_inject(collection, roles):
                """
                Orders the roles in the order of dependencies - ensuring any
                role's dependencies are run before the role itself.

                Additionally injects any roles that are dependencies, are
                available, and were not part of the execution plan.
                """

                available_roles = {
                    r.name: r
                    for r in discover_roles(hidden=True)[collection]
                }

                yielded_roles = set()
                required_roles = {r.name for r in roles}

                while not required_roles.issubset(yielded_roles):
                    for role in roles:
                        if role.name in yielded_roles:
                            continue

                        if all(dependency in yielded_roles for dependency in role.dependencies):
                            yield role
                            yielded_roles.add(role.name)
                            break
                    else:
                        # We did not find a role that can be yielded, attempt to inject a dependency role
                        unreachable_roles = [r for r in roles if r.name not in yielded_roles]
                        their_dependencies = set(sum((role.dependencies for role in unreachable_roles), []))

                        for dependency_name in their_dependencies:
                            if dependency_role := available_roles.get(dependency_name):
                                if not all(dependency in yielded_roles for dependency in dependency_role.dependencies):
                                    # If this dependency has unsatisfied dependencies, skip it
                                    continue

                                yield dependency_role
                                yielded_roles.add(dependency_name)
                                break
                        else:
                            raise ValueError(
                                f"The following roles are unreachable: \"{', '.join(r.name for r in unreachable_roles)}\", "
                                f"because their dependencies are unreachable: \"{', '.join(their_dependencies)}\""
                            )

            # The role application is performed via the 'include_role' task
            # (instead of the simpler 'role:' play parameter), because this allows
            # us to create a try-except analogue, the "block-rescue", which will ensure
            # that subsequent roles continue executing even if the given role errors out.
            playbook = [{
                'hosts': 'localhost',
                'tasks': [
                    {
                        'name': f"pqrs-meta: Wrapper for {role.name}",
                        'block': [
                            {
                                'name': f"pqrs-meta: Execute {role.name}",
                                'include_role': {'name': role.name},
                                'vars': {'role_version': role.installed_version or '0.0.0'}
                            },
                            {
                                # Use 'debug' task as a signal for us that the role successfully completed
                                'name': f"pqrs-meta: Termination guard for {role.name} - success",
                                'debug': {'msg': f"{role.name} success"},
                            },
                        ],
                        'rescue': [
                            {
                                # Use 'debug' task as a signal for us that the role failed
                                'name': f"pqrs-meta: Termination guard for {role.name} - failure",
                                'debug': {'msg': f"{role.name} failure"},
                            }
                        ]
                    }
                    for role in itertools.chain(*[
                        order_by_dependencies_and_inject(collection, roles)
                        for collection, roles in roles_to_run.items()  # fmt: skip
                    ])
                ],
                'vars_files': str(tmpdir.path / "vars.yml")
            }]

            with open(tmpdir.path / "play.yml", "w") as f:
                content = datafiles.formats.YAML.serialize(playbook)
                f.write(content)

            yield tmpdir
    finally:
        os.environ["PQRS_BECOME"] = ""
