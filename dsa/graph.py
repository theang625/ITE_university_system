"""
graph.py
Directed graph logic for course prerequisites, as a class - matching the
same style as HashTable in hash_table.py.

Solves: enrollment mistakes (checks eligibility before allowing enrollment).

This class is "pure" - it doesn't read or write any JSON files itself.
Whoever uses it (admin_service.py / student_service.py) is responsible for
loading course_require.json first, then calling build() with that data.
"""


class Graph:
    def __init__(self):
        self.adjacency = {}

    def build(self, course_require):
        """
        Build the adjacency structure from course_require data.

        course_require: list of dicts like
            {"course_id": 2, "requires_course_id": 1}

        Fills self.adjacency like:
            {2: [1], 4: [3], 5: [2], 6: [5], 7: [6], 8: [7]}
        Meaning: adjacency[course_id] = list of courses it directly requires.
        """
        for row in course_require:
            course_id = row["course_id"]
            requires_id = row["requires_course_id"]
            self.adjacency.setdefault(course_id, []).append(requires_id)
        return self.adjacency

    def get_direct_requirements(self, course_id):
        """
        Return only the immediate prerequisite(s) for a course - one step back.

        Example: get_direct_requirements(8) -> [7]   (APL-402 needs APL-401)
        """
        return self.adjacency.get(course_id, [])

    def get_full_chain(self, course_id):
        """
        Return the FULL chain of prerequisites needed to reach a course,
        ordered from earliest to latest (does not include course_id itself).

        Uses DFS, walking backward through the graph.

        Example: get_full_chain(8) -> [1, 2, 5, 6, 7]
            meaning: DS-101, DS-102, DB-301, DB-302, APL-401
        """
        chain = []
        visited = set()

        def dfs(current_id):
            for required_id in self.get_direct_requirements(current_id):
                if required_id not in visited:
                    visited.add(required_id)
                    dfs(required_id)
                    chain.append(required_id)

        dfs(course_id)
        return chain

    def can_enroll(self, completed_course_ids, course_id):
        """
        Check if a student can enroll, based on DIRECT requirements only.

        completed_course_ids: set/list of course_ids the student has
                               finished (grade is not None in Enrollment.json)

        Returns: {"eligible": True/False, "missing_courses": [...]}
        """
        required = self.get_direct_requirements(course_id)
        missing = [c for c in required if c not in completed_course_ids]
        return {
            "eligible": len(missing) == 0,
            "missing_courses": missing,
        }

    def add_requirement(self, course_id, requires_course_id):
        """
        Add a new prerequisite edge (used when an admin adds a new
        course_require rule). Caller is still responsible for also
        appending this to course_require.json so it persists.
        """
        self.adjacency.setdefault(course_id, []).append(requires_course_id)
        return self.adjacency