# MyMiniCollection

A dedicated, full-stack collection tracker and backlog management web application tailored for tabletop wargamers and hobbyists. **MyMiniCollection** allows users to catalog their miniatures across distinct game systems and factions, tracking the granular state of their inventory from box to fully painted.

## 🚀 Features

- **Multi-System Hierarchies:** Clear separation of collections by game type (e.g., Warhammer 40k, Age of Sigmar, Star Wars Legion) and sub-factions.
- **Aggregated Dashboard:** High-level line-item views showing total counts of identical units owned, with expandable dropdowns to view individual unit details.
- **Granular State Tracking:** Track physical states (New in Box, Built, Painted) and operational flags (Damaged) for every item.
- **Metadata Management:** Record historical data including purchase dates and custom notes for distinct models/squads.

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI (REST API framework)
- **Database:** SQLite (Local development), PostgreSQL via SQLAlchemy ORM
- **Frontend:** Streamlit / HTML5 UI

## 📋 Database Architecture

The application relies on a relational database schema to eliminate redundant data entry:

1. **GameSystem:** High-level game category.
2. **Faction:** Specific armies or forces tied to a GameSystem.
3. **MasterUnit:** A public directory of official retail units.
4. **UserInventoryItem:** Individual instances of units owned by the user, storing unique states and dates.

## 🔧 Getting Started

### Prerequisites
- Python 3.10+
- VS Code (with SQLite Viewer extension recommended)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/MyMiniCollection.git](https://github.com/YOUR_USERNAME/MyMiniCollection.git)
   cd MyMiniCollection
