from database import init_db, db_session
from models import Leader, Project, Collaborator, Content

def seed_database():
    init_db()

    # Create sample leaders
    leader1 = Leader(name="Rahul Sharma", company="TechInnovate", bio="Experienced product leader with a passion for AI")
    leader2 = Leader(name="Priya Patel", company="DataWise", bio="Data-driven product manager focused on user experience")

    db_session.add(leader1)
    db_session.add(leader2)
    db_session.commit()

    # Add projects
    project1 = Project(name="AI Assistant", description="Developing an AI-powered personal assistant", leader=leader1)
    project2 = Project(name="Data Visualization Platform", description="Creating intuitive data visualization tools", leader=leader2)

    db_session.add(project1)
    db_session.add(project2)

    # Add collaborators
    collaborator1 = Collaborator(name="Amit Kumar", role="Senior Developer", leader=leader1)
    collaborator2 = Collaborator(name="Neha Gupta", role="UX Designer", leader=leader2)

    db_session.add(collaborator1)
    db_session.add(collaborator2)

    # Add content
    content1 = Content(title="AI in Product Management", type="free", url="https://example.com/ai-product-management", leader=leader1)
    content2 = Content(title="Data-Driven Decision Making", type="paid", url="https://example.com/data-driven-decisions", leader=leader2)

    db_session.add(content1)
    db_session.add(content2)

    db_session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
