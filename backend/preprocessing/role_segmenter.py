import re


class RoleSegmenter:
    KEYWORDS = ("engineer", "developer", "analyst", "architect", "manager")

    def segment(self, jd_text: str) -> list[str]:
        lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
        segments: list[list[str]] = [[]]
        for line in lines:
            is_heading = (
                line.isupper()
                or line.endswith(":")
                or bool(re.match(r"^(role|position|job title)\b", line, flags=re.IGNORECASE))
                or any(keyword in line.lower() for keyword in self.KEYWORDS)
            )
            if is_heading and segments[-1]:
                segments.append([line])
            else:
                segments[-1].append(line)

        result = ["\n".join(chunk).strip() for chunk in segments if chunk]
        return result if result else [jd_text]
