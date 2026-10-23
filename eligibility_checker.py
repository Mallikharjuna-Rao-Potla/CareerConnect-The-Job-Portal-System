# eligibility_checker.py
import re


def _skill_tokens(skill):
    """Split a skill into normalized words while keeping common skill punctuation."""
    return re.findall(r"[\w+#.]+", skill.casefold())

def clean_skills(skill_string):
    """Converts a comma-separated string of skills into a clean list of lowercase skills."""
    if not skill_string:
        return []
    # Split by comma, strip whitespace, and convert to lowercase
    return [skill.strip().lower() for skill in skill_string.split(",") if skill.strip()]

def calculate_match(candidate_skills_str, required_skills_str):
    """
    Compares candidate skills against required skills and returns matching info.
    """
    candidate_skills = set(clean_skills(candidate_skills_str))
    required_skills = set(clean_skills(required_skills_str))

    # If the job doesn't require any specific skills
    if not required_skills:
        return {
            "matching_skills": list(candidate_skills),
            "missing_skills": [],
            "match_percentage": 100.0
        }

    # Single-word requirements can match a complete word in a longer candidate skill,
    # while multi-word requirements must match as a complete phrase.
    matching_skills = set()
    missing_skills = set()
    for required_skill in required_skills:
        required_tokens = _skill_tokens(required_skill)
        matched = any(
            (
                required_tokens == candidate_tokens
                or (
                    len(required_tokens) == 1
                    and required_tokens[0] in candidate_tokens
                )
            )
            for candidate_tokens in (
                _skill_tokens(candidate_skill)
                for candidate_skill in candidate_skills
            )
        )
        (matching_skills if matched else missing_skills).add(required_skill)

    # Calculate percentage
    match_percentage = (len(matching_skills) / len(required_skills)) * 100

    return {
        # Title() capitalizes the first letter for display purposes
        "matching_skills": [skill.title() for skill in matching_skills],
        "missing_skills": [skill.title() for skill in missing_skills],
        "match_percentage": round(match_percentage, 2)
    }