export type Project = {
    id: number;
    name: string;
    description: string;
    link?: string | null;
    technologies: string[];
    updatedAt: string;
}