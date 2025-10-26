import sqlite3

conn = sqlite3.connect("hackathon.db")
cursor = conn.cursor()

query = """
SELECT 
    t.name AS team_name,
    t.leader_name,
    t.contact,
    GROUP_CONCAT(tm.name, ', ') AS members,
    p.title AS selected_problem
FROM teams t
LEFT JOIN team_members tm ON t.id = tm.team_id
LEFT JOIN problems p ON t.problem_id = p.id
GROUP BY t.id
"""

cursor.execute(query)
teams = cursor.fetchall()

print(f"{'Team Name':20} {'Leader':15} {'Members':30} {'Selected Problem'}")
print("-" * 90)
for team in teams:
    team_name, leader_name, contact, members, problem = team
    members = members if members else ""
    problem = problem if problem else "Not selected"
    print(f"{team_name:20} {leader_name:15} {members:30} {problem}")

conn.close()
