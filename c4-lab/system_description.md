## ICT To Do List System Description

ICT To Do List is a task management system for the ICT e-learning environment, supporting both a web-based application and a mobile application. Its purpose is to help students track personal tasks and automatically track course work by syncing assignments and submission status from MyCourses.

### Key Features
- **Manual and Imported Tasks:** Users can create tasks manually, and the system can also create tasks from MyCourses assignments. Each task has a title, optional description, due date, status, and a source flag (manual or imported). Imported tasks store the MyCourses assignment ID to support updates and deduplication.
- **Task Operations:** Users can view, update, delete, and mark tasks as done. Imported tasks are updated automatically during sync if the assignment changes in MyCourses.
- **Sync with MyCourses:** The system connects to MyCourses (an external ICT e-learning system) to retrieve active courses, assignments, and submission status for authenticated users. MyCourses exposes web services returning JSON payloads. The integration supports:
	- Retrieving the list of active courses for the user
	- Retrieving assignments for a selected course (title, due date, assignment ID)
	- Retrieving submission status for each assignment (submitted/not submitted, timestamp)
- **Source of Truth:** MyCourses is the source of truth for imported assignments and submission status.

### User Roles
- **Student:** Manages their own task list, views assignments, and tracks submission status. Student tasks are private.
- **Instructor:** May view their own teaching-related tasks and monitor assignment deadlines for their courses, but cannot see student private tasks.
- **System Administrator:** Manages system configuration, user accounts, and monitors sync health via a separate admin interface.

### Architecture and Technology
- **Web App:** Browser-based UI implemented as a single page application using React.
- **Mobile App:** Cross-platform mobile app using Flutter (iOS and Android).
- **Web API:** Backend service implemented with Python FastAPI, exposing REST endpoints (JSON over HTTPS).
- **Database:** PostgreSQL for user profiles, tasks, sync settings, and sync history.
- **MyCourses Connector:** Integration module (service) within the backend, implemented as a separate service module. It calls MyCourses web services, parses JSON, and maps external data into internal task records.
- **Communication:** All client requests (Web App, Mobile App) go to the Web API over HTTPS. The Web API uses SQLAlchemy ORM for PostgreSQL access and calls the MyCourses Connector via internal interface (function call or internal HTTP if deployed separately). The MyCourses Connector communicates with MyCourses over HTTPS and exchanges JSON.
- **Authentication:** Uses university single sign-on (SSO) when available. If MyCourses supports OAuth2/OpenID Connect, ICT To Do List uses it; otherwise, it uses its own account system, storing only the minimum link needed to call MyCourses on behalf of the user.

### Main User Flows
1. **Sign In:** Student signs in via Web App or Mobile App.
2. **View Tasks:** Client requests current task list from Web API.
3. **Create/Edit/Delete Task:** Student creates, edits, or deletes a manual task via the Web API, which validates and stores the task.
4. **Mark Task as Done:** Student marks a task as done, updating its status in the database.
5. **Sync MyCourses:** Student initiates a sync; the Web API calls the MyCourses Connector, which retrieves courses, assignments, and submission status. The Web API creates/updates imported tasks as needed. Submitted assignments can be marked as done or with a submitted status.
6. **Refresh Task List:** User refreshes to see updated items.

### Key Rules
- Each user can access only their own task list.
- Student tasks are private; not visible to instructors or other students.
- Imported tasks must be linked to MyCourses assignment ID for updates and deduplication.
- Sync must not delete manual tasks.
- Sync failures must not corrupt existing tasks.
- System must handle MyCourses downtime gracefully, returning clear errors and recording failures in sync history.
- All network communication uses HTTPS.
- Store only the minimum MyCourses data needed (course name, assignment title, due date, submission status).
- Keep a sync log with timestamp, result, and error message for troubleshooting.
- Admin can view sync health and manage system-wide settings (MyCourses endpoint, default sync frequency).

### C4 Component Level (Web API)
Within the Web API, the internal design is decomposed into major components:
- **Authentication and Authorization Component:** Handles login, token validation, and access control.
- **Task Management Component:** Handles CRUD for manual and imported tasks.
- **MyCourses Sync Orchestrator Component:** Manages sync workflow, decides when to call external services, and updates tasks.
- **MyCourses Client Component:** Calls MyCourses web services, handles HTTPS requests and JSON parsing (may be inside the MyCourses Connector).
- **Mapping Component:** Converts MyCourses assignment/submission data into the internal task model.
- **Sync History Component:** Records sync outcomes and provides data for admin monitoring.
- **Data Access Component:** Provides repository functions for PostgreSQL access, ensuring controlled transactions.
