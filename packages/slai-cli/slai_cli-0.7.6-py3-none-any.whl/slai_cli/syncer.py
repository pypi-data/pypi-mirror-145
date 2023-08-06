import sys
import time
import logging
import os
import yaml
from pathlib import Path
import hashlib
import json
from datetime import datetime
import click
from functools import partial


class SandboxSyncer:
    def __init__(self, client, sandbox, path, test=False):
        self.client = client
        self.sandbox = sandbox
        self.path = path
        self.local_files = {}
        self._client_deletions = []
        self._sandbox_deletions = []
        self.slai_dir = os.path.join(self.path, "slai")
        if not test:
            # tests don't use OpPerformer and eliminate all the noisy console output
            self.op_performer = OpPerformer(self.client, self.sandbox["id"], self.slai_dir)
        self.ignore_paths = ["breakpoints", "settings", "data"]

    def _initialize_project(self):
        if os.path.exists(os.path.join(self.path, "slai")):
            click.echo(click.style("Project alredy intialized.", "white"))
            return

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        for filename, content in self.sandbox["sandbox_data"].items():
            filepath = os.path.join(self.path, "slai", filename)
            directory = os.path.dirname(filepath)
            Path(directory).mkdir(parents=True, exist_ok=True)
            if filename not in self.ignore_paths:
                with open(filepath, "w") as f:
                    f.write(content)

        yml_path = os.path.join(self.path, "slai.yml")
        with open(yml_path, "w") as f:
            f.write(
                yaml.dump({"sandbox_url": f"{self.client.base_url}/sandbox/{self.sandbox['id']}"})
            )

        requirements_path = os.path.join(self.path, "requirements.txt")
        with open(requirements_path, "w") as f:
            f.write("slai==0.1.62\n")

        self._update_local_files()

    # TODO rename to reflect new responsability
    def _new_file_ops(self):
        # discover new sandbox files
        new_sandbox_files = [
            f
            for f in self.sandbox["sandbox_data"].keys()
            if f not in self.local_files
            and f not in self._local_deletions
            and f not in self.ignore_paths
        ]
        # for each new sandbox file create op to create new local file
        ops = [
            {"op": "new_local_file", "path": f, "content": self.sandbox["sandbox_data"][f]}
            for f in new_sandbox_files
        ]
        # discover new local files
        new_local_files = [
            f
            for f in self.local_files.keys()
            if f not in self.sandbox["sandbox_data"] and f not in self._sandbox_deletions
        ]
        # for each new local file create op to create new sandbox file
        ops = ops + [
            {"op": "new_sandbox_file", "path": f, "content": self.local_files[f]}
            for f in new_local_files
        ]

        # create ops for deletions
        ops = ops + [
            {"op": "delete_sandbox_file", "path": f}
            for f in self._local_deletions
            if f not in ["model/train.py", "test/test.py", "handler/handler.py"]
        ]

        ops = ops + [{"op": "delete_local_file", "path": f} for f in self._sandbox_deletions]

        return ops

    def _generate_sync_ops(self):
        sandbox_updated = datetime.fromisoformat(self.sandbox["updated"].replace("Z", "+00:00"))

        sandbox_updated_seconds = sandbox_updated.timestamp()
        slai_dir = os.path.join(self.path, "slai")
        ops = []
        for file in self.local_files:
            filepath = os.path.join(slai_dir, file)
            modified_time = os.path.getmtime(filepath)
            with open(filepath, "r") as f:
                file_content = f.read()
                if file not in self.sandbox["sandbox_data"]:
                    continue
                if file_content != self.sandbox["sandbox_data"][file]:
                    if modified_time > sandbox_updated_seconds:
                        ops.append({"op": "update_server", "path": file, "content": file_content})
                    else:
                        ops.append(
                            {
                                "op": "update_client",
                                "path": file,
                                "content": self.sandbox["sandbox_data"][file],
                            }
                        )
        ops += self._new_file_ops()
        ops = [op for op in ops if op["path"] not in self.ignore_paths]
        return ops

    def _update_local_files(self):
        slai_dir = os.path.join(self.path, "slai")
        local_files = {}
        for root, subdir, files in os.walk(slai_dir):
            for filename in files:
                full_filename_path = os.path.join(root, filename)
                with open(full_filename_path) as f:
                    key = os.path.relpath(full_filename_path, slai_dir)
                    local_files[key] = f.read()
        self._local_deletions = [f for f in self.local_files.keys() if f not in local_files]

        # should store a last synced date somewhere, this could help
        # distinguish between deletions and sandbox additions
        # sometimes
        self.local_files = local_files

    def _update_sandbox(self, sandbox):
        self._sandbox_deletions = [
            f for f in self.sandbox["sandbox_data"].keys() if f not in sandbox["sandbox_data"]
        ]
        if len(self._sandbox_deletions) > 0:
            pass
            # print("deletions found", self._sandbox_deletions)
        self.sandbox = sandbox

    def _differ(self, local_files, remote_summary):
        local_hashes = {
            k: hashlib.md5(local_files[k].encode("utf-8")).hexdigest() for k in local_files
        }
        remote_hashes = remote_summary["sandbox_data_hashes"]
        remote_hashes = {k: v for k, v in remote_hashes.items() if k not in self.ignore_paths}
        return local_hashes != remote_hashes

    def start(self):
        # does the path exist? if not then create it
        self._initialize_project()
        click.echo("Starting syncing")
        while True:
            time.sleep(1)
            self._update_local_files()
            summary = self.client.get_sandbox_summary(self.sandbox["id"])
            if self._differ(self.local_files, summary):
                print("\n")  # new line to break up the syncer timer
                sandbox = self.client.get_sandbox(self.sandbox["id"])
                self._update_sandbox(sandbox)
                for op in self._generate_sync_ops():
                    self.op_performer.perform_op(op)
            else:
                now = datetime.now().strftime("%H:%M:%S")
                click.echo(
                    f"\rProject in sync at {now}",
                    nl=False,
                )


class OpPerformer:
    def __init__(self, slai_client, sandbox_id, slai_dir):
        self.slai_client = slai_client
        self.sandbox_id = sandbox_id
        self.slai_dir = slai_dir
        self.show_blurb()

    def show_blurb(self):
        green = partial(click.style, fg="green")
        click.echo(
            click.style(
                """
                            ..         
                          .:..:        
                         :.  ::.         SLAI SYNCER
  :^^~:.....  .........:^. .^:.:.      
   .^^^.   .::.        :  ::  :.:      - First time using Slai? Check out our
    .^^:^. :.         .: ^.   :.:         docs at https://docs.slai.io
      :^:^^:            ..   ::^.      
       .::~.                 ..:.      - Slai syncer is in beta. Please let us
         .^:         ..         :.       know if you run into anything. Email
          ^:^^^    :^:^          :       mike@slai.io
          :^:^^   :~::.       .: :.    
           :.^.     ....  .....  :.    - Find Slai starter projects at slai.io/launchpad
           .:.    .:...         .:     
       .....   .... .^...........      - Happy coding! May the fox be with you.
     .^:~..........~!:..               
     .^:........::..                                   
""",
                fg="yellow",
            )
        )
        click.echo(
            f"""
{green("Syncer started")}
--------------
Local dir:    {self.slai_dir}
Slai sandbox: {self.slai_client.base_url}/sandbox/{self.sandbox_id}
"""
        )

    def perform_op(self, op):
        # print(op)
        operation = op.pop("op")
        getattr(self, operation)(**op)

    def update_server(self, path, content):
        self.slai_client.update_sandbox_file(self.sandbox_id, path, content)
        click.echo(
            click.style(
                f"Updated sandbox {path} with local modifications.",
                fg="green",
            )
        )

    def update_client(self, path, content):
        with open(os.path.join(self.slai_dir, path), "w") as f:
            f.write(content)
        click.echo(
            click.style(
                f"Updated {os.path.join(self.slai_dir, path)} with sandbox modifications.",
                fg="green",
            )
        )

    def new_local_file(self, path, content):
        with open(os.path.join(self.slai_dir, path), "w") as f:
            f.write(content)
        click.echo(
            click.style(
                f"New file {os.path.join(self.slai_dir, path)} synced from sandbox.", fg="green"
            )
        )

    def new_sandbox_file(self, path, content):
        self.slai_client.create_sandbox_file(self.sandbox_id, path, content)
        click.echo(click.style(f"New file {path} synced to sandbox.", fg="green"))

    def delete_sandbox_file(self, path):
        self.slai_client.delete_sandbox_file(self.sandbox_id, path)
        click.echo(click.style(f"Deleted file {path} from sandbox.", fg="red"))

    def delete_local_file(self, path):
        os.remove(os.path.join(self.sandbox_id, self.slai_dir, path))
        click.echo(
            click.style(
                f"Deleted file {os.path.join(self.slai_dir, path)} based on sandbox removal.",
                fg="red",
            )
        )
