# Job AI Assistant

Job AI Assistant is a professional growth tracking application designed to help you log your career journey and gain actionable insights through AI-powered summarization.

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

## Architecture

- **Backend**: Hosts the API and core logic. Explore the [backend](backend) directory for more details.
- **Database Models**: The foundation of data management is detailed in [backend/database/models.py](backend/database/models.py), including models for Journal Entries, Projects, and Technologies.
- **AI Agent**: Processes journal entries to extract actionable insights and trends.

