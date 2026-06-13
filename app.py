from datetime import date
from typing import List, Optional
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

# ==========================================
# 1. DATABASE MODELS (THE ARCHITECTURE)
# ==========================================

class GameSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Warhammer 40k"
    
    # Relationship link to child Factions
    factions: List["Faction"] = Relationship(back_populates="system")


class Faction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Ossiarch Bonereapers"
    
    # Foreign Key linking to GameSystem
    system_id: int = Field(foreign_key="gamesystem.id")
    system: GameSystem = Relationship(back_populates="factions")
    
    # Relationship link to child MasterUnits
    master_units: List["MasterUnit"] = Relationship(back_populates="faction")


class MasterUnit(SQLModel, table=True):
    """The generic blueprint of a unit sold by a retailer."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Mortek Guard"
    
    # Scope Creep Protection: Generic slot for System-Specific Roles 
    # (e.g., "Battleline", "HQ", "Operative")
    classification: Optional[str] = Field(default=None) 
    
    # Foreign Key linking to Faction
    faction_id: int = Field(foreign_key="faction.id")
    faction: Faction = Relationship(back_populates="master_units")


# --- The Collection Superclass Concept ---
# In SQLModel/Pydantic, we use a base class (not table=True) for shared fields.
class InventoryItemBase(SQLModel):
    purchase_date: date = Field(default_factory=date.today)
    state: str = "NIB"  # NIB, Built, Painted
    is_damaged: bool = False
    notes: Optional[str] = None


class UserInventoryItem(InventoryItemBase, table=True):
    """The actual physical miniature instance sitting on your shelf."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key linking back to the Master Unit list
    master_unit_id: int = Field(foreign_key="masterunit.id")


# ==========================================
# 2. DATABASE CONFIGURATION
# ==========================================
# Creates a local file named 'minis.db' right in your project folder
sqlite_file_name = "minis.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False) # Change echo=True to see raw SQL commands


def create_db_and_tables():
    """Generates the database file and constructs the tables."""
    SQLModel.metadata.create_all(engine)


# ==========================================
# 3. SEED DATA FUNCTION
# ==========================================
def seed_database():
    """Populates the database with the initial wargaming catalog."""
    with Session(engine) as session:
        # Check if we've already seeded to avoid duplicates
        if session.exec(select(GameSystem)).first():
            print("Database already contains data. Skipping seeding.")
            return

        print("Seeding wargaming data...")

        # --- 1. Define Systems ---
        w40k = GameSystem(name="Warhammer 40k")
        aos = GameSystem(name="Age of Sigmar")

        # --- 2. Define Factions & Units ---
        # 40k Factions
        necrons = Faction(name="Necrons", system=w40k)
        aeldari = Faction(name="Aeldari", system=w40k)
        votann = Faction(name="Leagues of Votann", system=w40k)

        # 40k Units (With classification tags ready)
        necrons.master_units = [
            MasterUnit(name="Necron Warriors", classification="Troops"),
            MasterUnit(name="Overlord", classification="HQ")
        ]
        aeldari.master_units = [
            MasterUnit(name="Guardian Defenders", classification="Troops"),
            MasterUnit(name="Avatar of Khaine", classification="Epic Hero")
        ]
        votann.master_units = [
            MasterUnit(name="Hearthkyn Warriors", classification="Battleline"),
            MasterUnit(name="Einhyr Hearthguard", classification="Infantry")
        ]

        # AoS Factions
        obr = Faction(name="Ossiarch Bonereapers", system=aos)
        fyreslayers = Faction(name="Fyreslayers", system=aos)
        idoneth = Faction(name="Idoneth Deepkin", system=aos)

        # AoS Units
        obr.master_units = [
            MasterUnit(name="Mortek Guard", classification="Battleline"),
            MasterUnit(name="Katakros", classification="Leader")
        ]
        fyreslayers.master_units = [
            MasterUnit(name="Vulkite Berzerkers", classification="Battleline"),
            MasterUnit(name="Auric Runefather", classification="Leader")
        ]
        idoneth.master_units = [
            MasterUnit(name="Namarti Thralls", classification="Battleline"),
            MasterUnit(name="Akhelian Ishlaen Guard", classification="Sub-Commander")
        ]

        # Save everything to the database file
        session.add(w40k)
        session.add(aos)
        session.commit()
        print("Seeding complete!")


# ==========================================
# 4. RUN TIME EXECUTION
# ==========================================
if __name__ == "__main__":
    # Create the file and tables
    create_db_and_tables()
    # Populates your data
    seed_database()
    
    print("\n--- Project initialized successfully! ---")