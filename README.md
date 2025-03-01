# Career Journal AI

Career Journal AI is a professional growth tracking application designed to help you log your career journey and gain actionable insights through AI-powered summarization.

## Overview

The application is divided into two primary features:

1. **Professional Logging**: Record your career milestones, journal entries, project details, and technical skills.

   - Leverage a robust backend that manages journal entries, project data, and technology tracking. See [backend/database/models.py](backend/database/models.py) for detailed data model definitions.

2. **AI Insights**: An intelligent AI agent summarizes your journal entries to provide monthly to yearly insights.
   - Gain insights and recommendations based on your documented professional journey.

## Key Features

- **Journal Logging**: Capture your daily work experiences, projects, and skill development.
- **Privacy Controls**: Manage visibility of your entries with privacy settings.
- **Project & Technology Association**: Link your journal entries to specific projects and technologies.
- **AI Summarization**: Automatically generate summaries and insights from your journal over various time frames.
- [**Admin Portal**](https://github.com/jowilf/starlette-admin): Secure administrative interface for managing entities:
  - Journal Entries: View, edit, and manage all journal entries
  - Projects: Track and organize professional projects
  - Technologies: Maintain a catalog of technical skills and tools
  - Access Control: Protected by environment-based authentication

## Admin Portal Setup

To access the admin portal:

1. Set up environment variables in `.env`:

   ```
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   ```

2. Access the portal at `/admin` endpoint
3. Log in with your configured credentials
4. Manage your data through the user-friendly interface

The admin portal provides a comprehensive dashboard for managing all aspects of your career journal data, built with Starlette Admin for a clean and intuitive interface.

## Architecture

- **Backend**: Hosts the API and core logic. Explore the [backend](backend) directory for more details.
- **Frontend**: Vue.js-based user interface with TypeScript support. Located in the [frontend](frontend) directory.
- **Database Models**: The foundation of data management is detailed in [backend/database/models.py](backend/database/models.py), including models for Journal Entries, Projects, and Technologies.
- **AI Agent**: Processes journal entries to extract actionable insights and trends.

## Technology

This project leverages the following technologies:

### Backend

- [**Python**](https://www.python.org/): The core programming language used for the backend development.
- [**Poetry**](https://python-poetry.org/): Dependency management and packaging tool.
- [**FastAPI**](https://fastapi.tiangolo.com/): Modern, fast (high-performance) web framework for building APIs.
- [**SQLModel**](https://sqlmodel.tiangolo.com/): SQL databases in Python, designed for simplicity and compatibility with Pydantic and SQLAlchemy.

### Frontend

- [**Vue.js**](https://vuejs.org/): Progressive JavaScript framework for building user interfaces.
- [**TypeScript**](https://www.typescriptlang.org/): Typed superset of JavaScript that compiles to plain JavaScript.
- [**Vite**](https://vitejs.dev/): Next generation frontend tooling for faster development.
- [**Tailwind CSS**](https://tailwindcss.com/): A utility-first CSS framework for rapid UI development.
- [**Shadcn Vue**](https://shadcn-vue.com/): Vue port of shadcn/ui.
