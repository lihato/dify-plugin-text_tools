import re
from typing import Any, Generator

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class RegexExtractTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the regex extraction tool.
        """

        # Extract tool parameters
        input_text1 = tool_parameters.get("input_text1", "")
        if not input_text1:
            yield self.create_text_message("Invalid input_text1")
        input_text2 = tool_parameters.get("input_text2", "")
        if not input_text2:
            yield self.create_text_message("Invalid input_text2")
        regex_pattern = tool_parameters.get("regex_pattern", "")
        # json_path = tool_parameters.get("json_path", "")
        # if not json_path and not regex_pattern:
        #    yield self.create_text_message("Invalid regex_pattern or json_path")
        if not regex_pattern:
            yield self.create_text_message("Invalid regex_pattern")
        regex_ignorecase = tool_parameters.get("regex_ignorecase", False)
        regex_multiline = tool_parameters.get("regex_multiline", False)
        regex_dotall = tool_parameters.get("regex_dotall", False)
        regex_ascii = tool_parameters.get("regex_ascii", False)

        try:
            # Set flags based on parameters
            flags = 0
            if regex_ignorecase:
                flags |= re.IGNORECASE
            if regex_multiline:
                flags |= re.MULTILINE
            if regex_dotall:
                flags |= re.DOTALL
            if regex_ascii:
                flags |= re.ASCII

            if regex_pattern:
                # Perform regex search
                matches1 = re.findall(regex_pattern, input_text1, flags=flags)
                matches2 = re.findall(regex_pattern, input_text2, flags=flags)
                if matches1 and matches2:
                    # 计算matches1相对于matches2的差异（matches1有而matches2没有的元素）
                    diff = [item for item in matches1 if item not in matches2]
                    if len(diff) ==0:
                        yield self.create_text_message(str("no difference"))
                        yield self.create_json_message({"result": "no difference"})
                    else:
                        yield self.create_text_message(str(diff))
                        yield self.create_json_message({"all_matches": diff})
                else:
                    yield self.create_text_message("input_text1 or input_text2 No matches found.")
            else:
                #if json_path:
                yield self.create_text_message("No regex_pattern found.")
        except Exception as e:
            yield self.create_text_message(f"Failed to find diffrence extract matches, error: {str(e)}")
