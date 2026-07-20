"""
graph.py
Directed graph logic for course prerequisites.
Solves: enrollment mistakes (checks eligibility before allowing enrollment).

This module is intentionally "pure" - it doesn't read or write any JSON files
itself. Whoever calls these functions (admin_service.py / student_service.py)
is responsible for loading course_require.json and Enrollment.json first,
then passing the data in.
"""


def build_graph(course_require):
    """
    Build an adjacency structure from the course_require data.

    course_require: list of dicts like
        {"course_id": 2, "requires_course_id": 1}

    Returns: dict like
        {2: [1], 4: [3], 5: [2], 6: [5], 7: [6], 8: [7]}
    Meaning: graph[course_id] = list of courses it directly requires.
    """
    graph = {}
    for row in course_require:
        course_id = row["course_id"]
        requires_id = row["requires_course_id"]
        graph.setdefault(course_id, []).append(requires_id)
    return graph


def get_direct_requirements(graph, course_id):
    """
    Return only the immediate prerequisite(s) for a course - one step back.

    Example: get_direct_requirements(graph, 8) -> [7]   (APL-402 needs APL-401)
    """
    return graph.get(course_id, [])


def get_full_chain(graph, course_id):
    """
    Return the FULL chain of prerequisites needed to reach a course,
    ordered from earliest to latest (does not include course_id itself).

    Uses DFS, walking backward through the graph.

    Example: get_full_chain(graph, 8)
        -> [1, 2, 5, 6, 7]
        meaning: DS-101, DS-102, DB-301, DB-302, APL-401
        (the entire path needed before APL-402)
    """
    chain = []
    visited = set()

    def dfs(current_id):
        for required_id in get_direct_requirements(graph, current_id):
            if required_id not in visited:
                visited.add(required_id)
                dfs(required_id)
                chain.append(required_id)

    dfs(course_id)
    return chain


def can_enroll(graph, completed_course_ids, course_id):
    """
    Check if a student can enroll in a course, based on DIRECT requirements
    only (not the full chain - if a student completed a course, they must
    have already satisfied everything behind it at the time they took it).

    completed_course_ids: a set/list of course_ids the student has finished
                           (grade is not None in Enrollment.json)

    Returns: {"eligible": True/False, "missing_courses": [...]}
    """
    required = get_direct_requirements(graph, course_id)
    missing = [c for c in required if c not in completed_course_ids]
    return {
        "eligible": len(missing) == 0,
        "missing_courses": missing,
    }


def add_requirement(graph, course_id, requires_course_id):
    """
    Add a new prerequisite edge to the in-memory graph (used when an admin
    adds a new course_require rule). The caller is still responsible for
    also appending this to course_require.json so it persists.
    """
    graph.setdefault(course_id, []).append(requires_course_id)
    return graph