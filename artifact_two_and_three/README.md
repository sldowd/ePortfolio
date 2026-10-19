# Grazioso Salvare Animal Shelter Dashboard

A full-stack web application for managing and visualizing animal shelter data to identify rescue dog training candidates. Built with Python, MongoDB, and Plotly Dash to provide interactive data exploration, filtering, and geolocation capabilities.

## Table of Contents
- [Project Overview](#project-overview)
- [Dashboard Demo](#dashboard-demo)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
  - [Why This Tech Stack?](#why-this-tech-stack)
- [Features](#features)
  - [CRUD Operations Module (`animal_shelter.py`)](#crud-operations-module-animal_shelterpy)
  - [Interactive Dashboard](#interactive-dashboard)
  - [Query Implementation](#query-implementation)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Configuration](#environment-configuration)
  - [Database Setup](#database-setup)
  - [Running the Application](#running-the-application)
- [Usage Guide](#usage-guide)
  - [Starting the Dashboard](#starting-the-dashboard)
  - [Using Filters](#using-filters)
  - [Interacting with the Map](#interacting-with-the-map)
  - [Exporting Data](#exporting-data)
- [Development Status](#development-status)
- [Testing](#testing)
  - [CRUD Module Tests](#crud-module-tests)
  - [Dashboard Testing Checklist](#dashboard-testing-checklist)
- [Challenges and Solutions](#challenges-and-solutions)
  - [Challenge 1: Filter Reset Not Updating Selected Row](#challenge-1-filter-reset-not-updating-selected-row)
  - [Challenge 2: Pie Chart Overcrowding with Unfiltered Data](#challenge-2-pie-chart-overcrowding-with-unfiltered-data)
  - [Challenge 3: Radio Button Styling](#challenge-3-radio-button-styling)
  - [Challenge 4: Snake Case Column Headers](#challenge-4-snake-case-column-headers)
  - [Challenge 5: Adding Chart Selection Without Breaking Layout](#challenge-5-adding-chart-selection-without-breaking-layout)
- [Performance Considerations](#performance-considerations)
- [Enhancement: Weighted Fit Scoring](#enhancement-weighted-fit-scoring-cs-499-enhancement-two)
- [Reflection on Software Development and Computer Science](#reflection-on-software-development-and-computer-science)
  - [Writing Maintainable, Readable, and Adaptable Programs](#writing-maintainable-readable-and-adaptable-programs)
  - [Approaching Problems as a Computer Scientist](#approaching-problems-as-a-computer-scientist)
  - [The Role and Impact of Computer Scientists](#the-role-and-impact-of-computer-scientists)
- [Acknowledgments](#acknowledgments)
- [Contact](#contact)

## Project Overview

This application provides a comprehensive dashboard interface for Grazioso Salvare, an international rescue animal training company, enabling users to:
- View and filter animal shelter outcome data from Austin-area shelters
- Identify dogs suitable for specific rescue training programs (Water, Mountain/Wilderness, Disaster/Individual Tracking)
- Visualize breed distribution through interactive pie charts
- Explore animal locations via geolocation mapping
- Perform CRUD operations on the shelter database

## Dashboard Demo

[![Dashboard Demo](https://img.youtube.com/vi/OsMyzGyEvUA/0.jpg)](https://youtu.be/OsMyzGyEvUA)

## Tech Stack

- **Backend:** Python 3.11+, MongoDB 5.0+
- **Frontend Framework:** Plotly Dash 2.x, Dash Bootstrap Components
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly Express, Dash Leaflet
- **Database Driver:** PyMongo
- **Styling:** Bootstrap (UNITED theme)

## Architecture

The application follows the **MVC (Model-View-Controller)** design pattern:

- **Model:** MongoDB database (`aac.animals` collection) with custom Python CRUD module for data operations
- **View:** Dash components including interactive data tables, pie charts, and Leaflet maps
- **Controller:** Python callback functions managing real-time component interactions and data flow

### Why This Tech Stack?

**MongoDB**
- Flexible NoSQL schema accommodates varying animal data structures
- Built-in geospatial indexing and query support for location-based features
- Scalable architecture supports growing shelter data
- Document model aligns naturally with shelter record structure

**Plotly Dash**
- Python-native framework eliminates need for separate JavaScript development
- Reactive components enable real-time dashboard updates
- Built-in callback system simplifies complex user interactions
- Rapid prototyping accelerates development cycle

**PyMongo**
- Official MongoDB Python driver with robust error handling
- Connection pooling for improved performance
- Well-documented API with active community support
- Seamless integration with Pandas for data analysis

**Dash Bootstrap Components**
- Professional UI components without custom CSS overhead
- Responsive grid system for mobile compatibility
- Consistent theming across application
- Accessibility features built-in

## Features

### CRUD Operations Module (`animal_shelter.py`)

Custom Python class providing full database operations:

**Create**
- Inserts one document after checking its fields and types against an allow-list
- Required fields must be present
- Returns acknowledgment status

**Read**
- Accepts only allowed fields and operators (`$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`, `$and`, `$or`); `$where` and `$regex` are rejected
- `{}` returns every record
- Raises an error on database failure instead of returning an empty list

**Update**
- `$set` on matching documents, using exact-match filters only (`$eq`, `$in`)
- Refuses an empty filter unless `allow_all=True` is passed
- `animal_id` and `rec_num` cannot be changed
- Returns count of modified documents

**Delete**
- Removes matching documents, using exact-match filters only
- Refuses an empty filter unless `allow_all=True` is passed
- Logs the number of documents deleted
- Returns count of deleted documents

**Connection Management**
- Environment variable configuration for secure credential storage
- Connection verified with a ping at startup
- Manual close method for cleanup

### Interactive Dashboard

**Welcome Section**
- Branded header with Grazioso Salvare logo
- Mission statement and usage instructions
- Responsive card layout with professional styling

**Data Table**
- Displays all animal records with sortable columns
- Pagination (10 records per page)
- Single-row selection for detail viewing
- Column headers auto-formatted from snake_case to Title Case
- Horizontal scroll for overflow data
- Custom styling matching brand colors

**Filter System**
- Dropdown menu with four filter options:
  - **Water Rescue:** Labrador Retriever Mix, Chesapeake Bay Retriever, Newfoundland (Intact Female, 26-156 weeks)
  - **Mountain/Wilderness Rescue:** German Shepherd, Alaskan Malamute, Old English Sheepdog, Siberian Husky, Rottweiler (Intact Male, 26-156 weeks)
  - **Disaster/Individual Tracking:** Doberman Pinscher, German Shepherd, Golden Retriever, Bloodhound, Rottweiler (Intact Male, 20-300 weeks)
  - **Reset:** Returns to unfiltered view
- Dogs are scored by breed (40), sex (30), and age (30). Only dogs scoring 70 or higher appear, ranked by Fit Score (see Enhancement Two)
- Real-time table updates on filter selection
- Automatic first-row selection after filtering

**Visualization Charts**
- Dropdown selector to choose between two chart types:
  - **Breed Distribution:** Interactive pie chart showing top 8 breeds in filtered dataset
  - **Age Distribution:** Bar chart showing animals grouped by age ranges
- Custom hover tooltips with detailed data
- White borders for visual clarity
- Responsive to filter changes

**Geolocation Map**
- Interactive Leaflet map centered on selected animal's location
- Marker shows animal position in Austin, TX area
- Tooltip displays breed on hover
- Popup shows animal name on click
- Zoom level 10 for neighborhood-scale view
- Dynamic centering based on selected record

**CSV Export**
- Custom "Export to CSV" button in filter card
- Exports currently filtered/viewed table data
- Maintains data integrity with proper index handling
- Downloads as `shelter_data.csv`
- Implemented via custom callback for consistent styling (vs built-in DataTable export)

### Query Implementation

The dashboard reads all records with an empty query (`db.read({})`) and scores each dog against the selected rescue profile in `scoring_algorithm.py`. The scoring rules are in Enhancement Two below.

Queries reach MongoDB only after validation: field names, value types, and operators must be on the allow-list (see Enhancement Three). An example of a query the module accepts, using the Water Rescue criteria:

```python
{
    'breed': {'$in': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']},
    'sex_upon_outcome': 'Intact Female',
    'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}
}
```

## Project Structure

```
GraziosoSilvare/
├── venv/                              # Virtual environment (not in repo)
├── .env                               # Environment variables (not in repo)
├── .gitignore                         # Git ignore configuration
├── requirements.txt                   # Python dependencies
├── animal_shelter.py                  # Validated, access-controlled MongoDB module
├── scoring_algorithm.py               # Enhancement Two: weighted fit scoring
├── dashboard.py                       # Main dashboard application
├── setup_db_users.js                  # Creates least-privilege database users
├── Grazioso Salvare Logo.png          # Brand logo image
├── animals.json                       # Dataset for mongoimport
├── README.md                          # This file
├── STYLE_GUIDE.md                     # Frontend design documentation
├── docs/
│   ├── flowchart.md                   # Mermaid flowchart source (Enhancement Two)
│   └── enhancement-two-flowchart.png  # Flowchart image
├── original_code/                     # Code before enhancements, for comparison
└── tests/
    ├── test_animal_shelter.py         # Enhancement Three tests (unittest, no server needed)
    ├── test_scoring.py                # Enhancement Two tests (unittest)
    └── test_crud.ipynb                # Original notebook tests (requires a live database)
```

## Database Schema

**Collection:** `aac.animals`

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `_id` | ObjectId | MongoDB unique identifier |
| `animal_id` | String | Shelter's animal ID (e.g., A721199) |
| `animal_type` | String | Species (Dog, Cat, Bird, etc.) |
| `breed` | String | Specific breed or mix |
| `name` | String | Animal's name |
| `age_upon_outcome_in_weeks` | Integer | Age in weeks at outcome |
| `sex_upon_outcome` | String | Sex classification (Intact Male, Intact Female, etc.) |
| `outcome_type` | String | Outcome category (Adoption, Transfer, Return to Owner, etc.) |
| `location_lat` | Float | Latitude coordinate for shelter location |
| `location_long` | Float | Longitude coordinate for shelter location |
| `date_of_birth` | String | Birth date (YYYY-MM-DD format) |
| `datetime` | String | Outcome datetime timestamp |
| `color` | String | Animal's color description |

**Index Considerations:**
- Primary index on `_id` (automatic)
- The dashboard reads every record and scores in Python, so an index on these fields does not speed up the dashboard. It would only help future exact-match queries.
- Geospatial index on `location_lat` and `location_long` for map queries

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- MongoDB 5.0 or higher
- pip package manager
- 10,000+ records from Austin Animal Center Outcomes dataset

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/sldowd/grazioso-salvare-dashboard.git
cd grazioso-salvare-dashboard
```

**2. Set up virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**Required packages:**
listed in requirements.txt

**4. Import dataset into MongoDB**
```bash
# From project root directory
mongoimport --db aac --collection animals --file animals.json
```

**5. Create the database users**
```bash
# With MongoDB running, from the project folder
mongosh setup_db_users.js
```
The script prompts for two passwords and creates:
- `aac_reader` (read-only): used by the dashboard
- `aac_writer` (read/write): used only for maintenance scripts

Then restart MongoDB with authentication turned on (see Enabling database-level protection below).

**6. Configure environment variables**

Copy `.env.example` to `.env` in the project root, then edit it:
```env
MONGO_USER=aac_reader
MONGO_PASSWORD=your_reader_password
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DATABASE=aac
MONGO_COLLECTION=animals
```

**Security Note:** Never commit `.env` file to version control. It's included in `.gitignore`.

### Running the Application

**Method 1: Python Script (Recommended)**
```bash
# Ensure virtual environment is activated
python dashboard.py
```

Access dashboard at: `http://localhost:8050`


**Stopping the Application:**
- Press `Ctrl+C` in the terminal

**Debug mode** is off by default. To turn it on for development:
```bash
DASH_DEBUG=1 python3 dashboard.py
```

## Usage Guide

### Filtering Animals by Rescue Type

1. Locate the **"Filter by Rescue Type"** dropdown near the top of the dashboard
2. Click the dropdown to reveal filter options:
   - Water Rescue
   - Mountain Rescue
   - Disaster Rescue
   - Reset
3. Select desired rescue type
4. Data table automatically updates to show only matching animals
5. Pie chart refreshes to show breed distribution of filtered results
6. First row auto-selects to display animal location on map

### Viewing Animal Details

1. **In Data Table:** Click any row to select an animal
2. **On Map:** 
   - Marker appears at animal's shelter location
   - **Hover** over marker to see breed in tooltip
   - **Click** marker to open popup with animal name
3. **In Pie Chart:** Hover over slice to see breed count and percentage

### Sorting Data

- Click any column header to sort ascending
- Click again to sort descending
- Click third time to remove sort

### Navigating Large Datasets

- Use pagination controls at bottom of table
- Table displays 10 records per page
- Current page indicator shows position in dataset
- Jump to specific page using page number buttons

### Resetting View

Select "Reset" from filter dropdown to return to unfiltered view of all 10,000+ shelter animals.

## Development Status

### ✅ Completed (Project One - Database Foundation)
- [x] MongoDB database setup and configuration
- [x] User authentication with role-based permissions
- [x] CRUD Python module with all four operations
- [x] Test script validating CRUD functionality
- [x] Error handling and input validation
- [x] Environment variable configuration for security

### ✅ Completed (Project Two - Dashboard Implementation)
- [x] Full dashboard layout with responsive design
- [x] Interactive data table with sorting and pagination
- [x] Dropdown filter with three rescue type queries + reset
- [x] MongoDB query integration for filtering
- [x] Pie chart visualization for breed distribution
- [x] Geolocation map with Leaflet integration
- [x] Real-time component updates via callbacks
- [x] Logo and branding integration
- [x] Custom styling with Bootstrap UNITED theme
- [x] Professional color palette and typography
- [x] Mobile-responsive grid layout
- [x] Row highlighting for selected table records
- [x] Additional chart types (bar chart for age distribution)
- [x] Export filtered results to CSV

### ✅ Completed (CS-499 Enhancements)
- [x] Weighted fit scoring with unit tests (Enhancement Two)
- [x] Database validation, access control, and unit tests (Enhancement Three)

### 🔄 In Progress
- [ ] Custom map markers with brand colors

### 📋 Planned Enhancements
- [ ] User authentication UI for dashboard access
- [ ] Role-based dashboard permissions
- [ ] Real-time data refresh from MongoDB change streams
- [ ] Advanced search with multi-field filtering
- [ ] Dashboard analytics and usage metrics
- [ ] Printable report generation
- [ ] Dark mode theme option
- [ ] Docker containerization for deployment
- [ ] CI/CD pipeline configuration

## Testing

### Automated Tests

Run from the project folder. No MongoDB server is needed:

```bash
python3 -m unittest discover -s tests -v
```

This runs 34 tests in two files:
- `tests/test_animal_shelter.py`: validation, access control, read-only mode, error handling, and connection settings for the database module. It uses an in-memory fake collection, so it also checks that rejected input never reaches the database.
- `tests/test_scoring.py`: scoring rules, the 70-point cutoff, age boundaries, and rescue profile weights.

`tests/test_crud.ipynb` is the original notebook test. It needs a live database and is kept for reference.

### Dashboard Testing Checklist

**Filter Functionality:**
- [ ] Water Rescue filter returns correct breeds
- [ ] Mountain Rescue filter returns correct breeds
- [ ] Disaster Rescue filter returns correct breeds
- [ ] Reset filter shows all records
- [ ] First row auto-selects after filter change

**Data Table:**
- [ ] All columns display correctly
- [ ] Sorting works on each column
- [ ] Pagination navigates through records
- [ ] Row selection updates map

**Visualizations:**
- [ ] Pie chart displays top 8 breeds
- [ ] Chart updates when filter changes
- [ ] Hover tooltips show correct data
- [ ] Map centers on selected animal
- [ ] Map marker shows correct location
- [ ] Tooltip displays breed
- [ ] Popup shows animal name

**Responsive Design:**
- [ ] Layout adapts to mobile screens
- [ ] All elements remain accessible
- [ ] Text remains readable at all sizes

## Challenges and Solutions

### Challenge 1: Filter Reset Not Updating Selected Row
**Problem:** When applying new filter, first row wasn't auto-selecting, causing map to show stale data.

**Solution:** Modified `update_table` callback to return both filtered data AND `[0]` for selected_rows, ensuring first row is always selected after filter application.

```python
@app.callback(
    Output('shelter-table', 'data'),
    Output('shelter-table', 'selected_rows'),  # Added second output
    Input('dropdown-filter', 'value')
)
def update_table(dropdown_filter):
    # ... filter logic ...
    return filtered_df.to_dict('records'), [0]  # Always select first row
```

### Challenge 2: Pie Chart Overcrowding with Unfiltered Data
**Problem:** With 10,000+ records, pie chart displayed 100+ breeds, making it unreadable.

**Solution:** Implemented top-8 breed filtering using Pandas value_counts() to show only most common breeds in current dataset.

```python
top_breeds = chart_df['breed'].value_counts().head(8).reset_index()
```

### Challenge 3: Radio Button Styling
**Problem:** Default radio buttons didn't match brand colors and were difficult to see.

**Solution:** Applied inline CSS accent-color property via DataTable's css parameter to customize radio button color to brand red (#c9341b).

### Challenge 4: Snake Case Column Headers
**Problem:** Database field names like `age_upon_outcome_in_weeks` appeared as-is in table headers.

**Solution:** Transformed column names during DataTable initialization using Python string methods.

```python
columns=[{
    'name': i.replace('_', ' ').title(),  # Display name
    'id': i                                 # Original field name
} for i in df.columns]
```
### Challenge 5: Adding Chart Selection Without Breaking Layout
**Problem:** Wanted to add age distribution chart but didn't want two separate graph areas taking up space.

**Solution:** Implemented dropdown selector that toggles between chart types using the same graph container, with conditional rendering in the callback based on selector value.
```python
@app.callback(
    Output('chart-holder', 'figure'),
    [Input('shelter-table', 'derived_virtual_data'),
     Input('chart-selector', 'value')]
)
def update_chart(viewData, chart_selector):
    if chart_selector == 'Breed Distribution':
        # ... return pie chart
    elif chart_selector == 'Age Distribution':
        # ... return bar chart
```

## Performance Considerations

- **Initial Load:** ~2-3 seconds for 10,000 records on standard broadband
- **Filter Application:** <500ms for query execution and table update
- **Map Rendering:** ~1 second for Leaflet initialization
- **Chart Updates:** Real-time (<100ms) due to client-side Pandas operations

**Optimization Opportunities:**
- Implement server-side pagination for datasets >50,000 records
- Score in MongoDB, or cache the full dataset instead of re-reading it on each selection
- Lazy-load map tiles to reduce initial bandwidth

## Enhancement: Weighted Fit Scoring (CS-499, Enhancement Two)

The original dashboard matched dogs to each rescue profile with exact-match MongoDB queries, so a dog missing any single criterion was excluded. The dashboard now fetches all records and scores each dog against the selected profile in `scoring_algorithm.py`:

| Criterion | Weight | Scoring |
|---|---|---|
| Breed | 40 | Full points if on the profile's preferred list, otherwise 0 |
| Sex | 30 | Full points if it matches the profile's preferred sex, otherwise 0 |
| Age | 30 | Full points inside the age range; outside it, lose 1 point per week from the nearest bound (minimum 0) |

Animals scoring below `MIN_SCORE` (70) are hidden; the rest are ranked by a new **Fit Score** column, highest first. A score of 70+ requires a preferred breed plus at least one other criterion, so near-matches (e.g., preferred breed, wrong sex) now appear instead of being silently dropped.

**Trade-off:** scoring runs in the application (O(n) to score, O(m log m) to sort the m animals above the cutoff) instead of inside MongoDB, and all records are fetched on each selection. At roughly 10,000 records this is negligible.

**Files:** flowchart source in [`docs/flowchart.md`](docs/flowchart.md), flowchart image in `docs/enhancement-two-flowchart.png`, tests in `tests/test_scoring.py`.

## Enhancement: Database Security Layer (CS-499, Enhancement Three)

The original `animal_shelter.py` passed whatever it received straight to MongoDB. The dashboard has no free-text input today, but the module is a reusable data-access layer, and any future caller (an API, a search box, a script) could send it a hostile query. This enhancement adds validation and access control inside the module.

| Problem in the original | Enhancement |
|---|---|
| Queries went to MongoDB unchecked, so `{"$where": ...}` or `{"breed": {"$ne": None}}` would run | Queries are checked against an allow-list of fields, value types, and operators (`$eq $ne $gt $gte $lt $lte $in $nin $and $or`). `$where`, `$regex`, `$expr`, and unknown fields are rejected before reaching the database |
| Documents could contain any fields or types | `create()` and `update()` validate field names, types, string length, and required fields. `animal_id` and `rec_num` cannot be changed |
| `delete({})` or `update({}, ...)` affected every record | Empty filters are refused unless `allow_all=True` is passed. Update and delete accept exact-match operators only (`$eq`, `$in`), because `$ne`/`$gt` could match nearly everything |
| Errors were printed, then turned into `[]`, `0`, or `False`, so failures looked like empty results | Exceptions are raised: `ValidationError`, `DatabaseError`, `PermissionError`. Callers can tell "no results" from "something broke" |
| Connection `try/except` never fired because `MongoClient` connects lazily; credentials were put in the URI unescaped | The connection is verified with a ping at startup and fails with a clear message that never includes the password. Credentials are URL-escaped, and missing or malformed settings fail fast |
| The dashboard connected with a read/write account | `AnimalShelter(read_only=True)` blocks writes in the application, and `setup_db_users.js` creates a database-level read-only user (least privilege) |

**Behavior change:** invalid input now raises an exception instead of returning `False`, `0`, or `[]`. The dashboard and notebook tests only send valid input, so they are unaffected.

### Enabling database-level protection

```bash
# 1. With MongoDB running, create the reader and writer users (prompts for passwords)
mongosh setup_db_users.js

# 2. Restart MongoDB with authentication required
mongod --auth --dbpath /path/to/data

# 3. Put the READER credentials in .env for the dashboard (see .env.example)
```

Use the writer account only for maintenance scripts: `AnimalShelter(username="aac_writer", password=...)`.

### Tests

`tests/test_animal_shelter.py` runs without a MongoDB server by using an in-memory stand-in collection, so it can also prove rejected input never reached the database:

```bash
python -m unittest discover -s tests -v
```

**Verification scope:** the tests above use a fake collection. They have not been run against a live MongoDB server, so the `setup_db_users.js` steps and authentication settings are untested in this repository.

**Limits:** the allow-list must be updated if the dataset gains fields. Validation protects this module only, so MongoDB should still run with authentication and a network-restricted `bindIp`.

## Reflection on Software Development and Computer Science

### Writing Maintainable, Readable, and Adaptable Programs

Throughout this project, I prioritized code quality through modular design, comprehensive documentation, and industry-standard best practices. The CRUD Python module from Project One exemplifies this approach—by encapsulating all database operations in a single, reusable class, I created a clean interface between the application logic and the database layer. This separation of concerns meant that when building the dashboard in Project Two, I could focus on visualization and user interaction without worrying about low-level database connection details.

The advantages of this modular approach became immediately apparent during dashboard development. When I needed to filter animals by rescue type, I simply called the existing `read()` method with appropriate query parameters rather than rewriting database logic. The module's consistent error handling and logging meant debugging was straightforward, and the use of environment variables for credentials ensured security without hardcoding sensitive information.

Looking forward, this CRUD module has broad applicability beyond the Grazioso Salvare dashboard. It could serve as the foundation for a mobile application allowing shelter staff to update animal records in the field, a batch processing system for importing data from multiple shelters, or an API backend for integration with veterinary clinic systems. The module's design makes it adaptable to any application requiring animal shelter data management—whether that's analytics tools, reporting systems, or third-party integrations. By investing in clean, well-documented code upfront, I created a versatile tool that can evolve with changing requirements.

### Approaching Problems as a Computer Scientist

Computer scientists approach problems systematically, breaking complex requirements into manageable components and designing solutions that balance functionality, performance, and maintainability. For the Grazioso Salvare project, I began by thoroughly analyzing the client's needs: identifying rescue dog candidates based on specific breed, age, and sex criteria. Rather than jumping directly into implementation, I mapped out the data flow from MongoDB queries through the CRUD module to dashboard visualizations, identifying potential bottlenecks and edge cases early.

This project differed significantly from previous coursework in its emphasis on real-world constraints and user-centered design. Unlike assignments with predetermined solutions, Grazioso Salvare's requirements demanded creative problem-solving—such as designing queries that balance precision (finding dogs meeting exact training criteria) with usability (presenting results clearly to non-technical staff). I had to consider not just whether the code worked, but whether the interface would actually help trainers make faster, better decisions about rescue dog candidates.

Several strategies proved valuable and will guide my future database projects. First, I learned to prototype queries in the MongoDB shell before implementing them in Python, which accelerated development and reduced debugging time. Second, I found that starting with the data model—understanding what information exists and how it relates—provides crucial context for designing effective queries and interfaces. Finally, I recognized the importance of iterative testing with realistic data; edge cases like empty filter results only became apparent when working with the full 10,000-record dataset rather than toy examples.

For future client projects, I would employ a similar iterative approach: requirements analysis, data modeling, incremental development with continuous testing, and regular stakeholder feedback. I would also prioritize documentation from day one, as clear technical documentation proved essential when revisiting code weeks later during Project Two development.

### The Role and Impact of Computer Scientists

Computer scientists solve problems through computational thinking, transforming real-world challenges into systems that leverage data, algorithms, and automation. We design solutions that don't just work today but can scale, adapt, and integrate with evolving technology ecosystems. Our work matters because we create tools that amplify human capabilities—enabling people to process information faster, identify patterns that would be invisible to manual analysis, and make data-driven decisions with confidence.

For Grazioso Salvare, this dashboard project directly enhances their operational efficiency and mission effectiveness. Before this system, trainers likely spent hours manually reviewing spreadsheets, filtering records by hand, and cross-referencing breed characteristics with training requirements. The dashboard automates this tedious work, instantly identifying candidates matching any rescue type criteria. The geolocation feature helps trainers plan efficient pickup routes, while the breed distribution visualizations reveal trends in available animals that inform recruitment strategies.

Beyond time savings, the dashboard improves decision quality. By consistently applying the same breed/age/sex criteria across all searches, it eliminates human error and bias that could result in overlooking qualified dogs or selecting poor candidates. The ability to export filtered results enables trainers to share candidate lists with partners, track success rates across rescue types, and maintain consistent documentation. Perhaps most importantly, by accelerating the dog identification process, the dashboard helps Grazioso Salvare train more rescue animals—ultimately saving more human lives in disaster and emergency situations.

This project demonstrates how thoughtful software engineering creates measurable value: reducing manual labor, improving accuracy, enabling data-driven insights, and ultimately advancing an organization's core mission. That's why computer science matters—we don't just write code; we design tools that empower people to do their most important work more effectively.

## Acknowledgments

- **Austin Animal Center** for providing the shelter outcomes dataset
- **Grazioso Salvare** (fictional client) for project requirements and specifications
- **MongoDB** documentation and community support
- **Plotly Dash** documentation and example galleries
- **Southern New Hampshire University** CS-340 course materials and instruction
- **Bootstrap** and **Dash Bootstrap Components** for UI framework

## Contact

**Sarah Dowd**
- Email: sarah.dowd1@snhu.edu
- GitHub: [@sldowd](https://github.com/sldowd)