import type { Project } from "./projects";
import type { Technology } from "./technology";

export type JournalEntry = {
    id: string;
    content: string;
    date: string;
    isPrivate: boolean;
    technologies: Technology[];
    project: Project | null;
    userId: string;
}