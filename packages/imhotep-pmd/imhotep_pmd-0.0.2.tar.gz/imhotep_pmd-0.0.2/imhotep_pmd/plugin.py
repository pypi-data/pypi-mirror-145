import json
import logging
import os
import shutil
from collections import defaultdict

import jsonschema
import requests
import toml
from imhotep.tools import Tool


class PmdLinter(Tool):
    """
    An Imhotep tool for linting code with PMD.
    """

    logger = logging.getLogger(__name__)

    default_pmd_command = "~/bin/pmd-bin-6.44.0/bin/run.sh pmd"

    def get_configs(self):
        """
        You can create a `imhotep_pmd.toml` at the root of your repo to configure `imhotep_pmd`.

        Currently, only one property is supported:
        - `pmd_command`: The command to use for invoking `pmd` binary. Typically, it looks like `"~/bin/pmd-bin-6.44.0/bin/run.sh pmd"`.
        """
        return ("imhotep_pmd.toml",)

    def invoke(self, dirname, filenames=set(), **kwargs):
        """
        Parameters:
        - `list_file` is a list of relative paths.
        - `dirname` is the directory path to the **temporary** repo.
        """

        # determine the command to run.
        configurations = dict()
        if "linter_configs" in kwargs:
            for configuration_path in kwargs["linter_configs"]:
                self.logger.info(f"Reading configurations from `{configuration_path}`")
                these_configurations = toml.load(configuration_path)
                configurations.update(these_configurations)
        if "pmd_command" in configurations:
            pmd_command = configurations["pmd_command"]
            self.logger.info(f"Overriding `pmd_command` to `{pmd_command}`.")
        else:
            pmd_command = self.default_pmd_command
            self.logger.info(f"Using default value for `pmd_command`: `{pmd_command}`.")

        # Invoke `pmd`.
        cmd = f'{pmd_command} --rulesets rulesets/java/quickstart.xml --format sarif --dir "{dirname}"'
        output = self.executor(cmd)

        filepaths_absolute = {os.path.join(dirname, filename) for filename in filenames}
        # Parse the Static Analysis Results Interchange Format (sarif) results.
        results = json.loads(output)
        retval = defaultdict(lambda: defaultdict(list))
        try:
            for run_id, run in enumerate(results["runs"]):
                for invocation_id, invocation in enumerate(run["invocations"]):
                    assert invocation[
                        "executionSuccessful"
                    ], f"Invocation #{invocation_id} in Run #{run_id} failed."
                for result in run["results"]:
                    message = f"Rule No. {result['ruleIndex']} - {result['ruleId']}: {result['message']['text']}"
                    for location in result["locations"]:
                        filepath_absolute = location["physicalLocation"][
                            "artifactLocation"
                        ]["uri"]
                        # Oddly, PMD prepends `/private` when running on macOS. Why?
                        filepath_absolute = filepath_absolute.removeprefix("/private")
                        if filepath_absolute not in filepaths_absolute:
                            continue
                        filepath_relative = os.path.relpath(filepath_absolute, dirname)
                        region = location["physicalLocation"]["region"]
                        location_message = f'L{region["startLine"]}:{region["startColumn"]}-L{region["endLine"]}:{region["endColumn"]}'
                        this_message = f"{location_message}: {message}"
                        line_number = region["startLine"]
                        retval[filepath_relative][str(line_number)].append(this_message)
        except KeyError as e:
            logger.error(f"Error happened: {e}. Validating JSON schema.")
            # TODO: As of 04/03/2022, the URL to the schema provided by PMD's results are giving a 404.
            schema_response = requests.get(results["$schema"])
            schema = schema_response.json()
            jsonschema.validate(results)
        return retval
