from typing import Optional

def get_chunking_pattern(language: str = "python", framework: Optional[str] = None) -> Optional[str]:
    """
    Returns a regex pattern for chunking based on language and framework.
    """
    if framework == "react":
        return r"(?=^\s*(function|class|export\s+(default\s+)?(function|class|const|let|var)))"
    elif framework == "angular":
        return r"(?=^\s*@Component|@Injectable|@Directive|export\s+class)"
    elif language == "python":
        return r"(?=^\s*(def|class)\s)"
    elif language == "java":
        return r"(?=^\s*(public\s+(class|interface|enum)|private|protected|void)\s)"
    elif language in ("javascript", "nodejs"):
        return r"(?=^\s*(function|class|module\.exports|export)\s)"
    else:
        return None