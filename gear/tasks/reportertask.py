from pathlib import Path
from typing import Any
from gear.tasks.taskexceptions import ReporterTaskException

import luigi

from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.base.basetask import BaseTask

from gear.tasks.transformertask import TransformerTask


class ReporterTask(BaseTask):
    def __init__(self, input_filename, config, *args, **kwargs):
        BaseTask.__init__(
             self,
             input_filename=input_filename,
             config=config,
             plugin_section="reporters",
        )

    def run(self):
        # get plugins
        plugins = self.plugins

        for data in self.load():
            for plugin in plugins:
                # get required transformer plugins
                required_transformer_plugins = set(
                    map(str.strip, plugin.argconfig["requires"].split(","))
                )

                # check for missing ones that are required as input
                missing_plugins = (
                    required_transformer_plugins - set(data.keys())
                )
                if len(missing_plugins) > 0:
                    # missing extractor plugin input
                    raise ReporterTaskException(
                        f"The reporter plugin '{plugin.metadata.name}' "
                        f"requires the following transformer plugins: "
                        f"{', '.join(missing_plugins)}"
                    )

                # apply to input data
                plugin.apply(
                    value={
                        required_plugin: data[required_plugin]
                        for required_plugin in required_transformer_plugins
                    }
                )

            # collect overall result from plugins' results
            res = {
                plugin.metadata.name: plugin._res
                for plugin in plugins
            }

            # dump plugin results
            self.dump(res)

    def requires(self):
        return [
            TransformerTask(
                input_filename=self.input_filename,
                config=self.config
            )
        ]
