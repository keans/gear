from pathlib import Path
from typing import Any
from gear.tasks.taskexceptions import TransformerTaskException

import luigi

from gear.utils.config import OUTPUT_DIR, PLUGIN_DIR
from gear.base.basetask import BaseTask

from gear.tasks.extractortask import ExtractorTask


class TransformerTask(BaseTask):
    def __init__(self, input_filename, config, *args, **kwargs):
        BaseTask.__init__(
             self,
             input_filename=input_filename,
             config=config,
             plugin_section="transformers",
        )

    def run(self):
        # get plugins
        plugins = self.plugins

        for data in self.load():
            for plugin in plugins:
                # get required extractor plugins
                required_extractor_plugins = set(
                    map(str.strip, plugin.argconfig["requires"].split(","))
                )

                # check for missing ones that are required as input
                missing_plugins = required_extractor_plugins - set(data.keys())
                if len(missing_plugins) > 0:
                    # missing extractor plugin input
                    raise TransformerTaskException(
                        f"The transformer plugin '{plugin.metadata.name}' "
                        f"requires the following extractor plugins: "
                        f"{', '.join(missing_plugins)}"
                    )

                # apply to input data
                plugin.apply(
                    value={
                        required_plugin: data[required_plugin]
                        for required_plugin in required_extractor_plugins
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
            ExtractorTask(
                input_filename=self.input_filename,
                config=self.config
            )
        ]
