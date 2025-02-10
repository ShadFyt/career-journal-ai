from database.models import Technology
from enums import Language


TECHNOLOGY_SEED_DATA: list[Technology] = [
    {
        "name": "HTML",
        "description": "A markup language for structuring and presenting\
        content on the World Wide Web.",
        "language": Language.HTML,
    },
    {
        "name": "CSS",
        "description": "A style sheet language used\
        for describing the presentation of a document written in a\
        markup language such as HTML.",
        "language": Language.CSS,
    },
    {
        "name": "Python",
        "description": "A versatile programming language.",
        "language": Language.PYTHON,
    },
    {
        "name": "SQLModel",
        "description": "A library for interacting with SQL databases from\
        Python code, with Python objects. It is designed to be intuitive,\
        easy to use, highly compatible, and robust.",
        "language": Language.PYTHON,
    },
    {
        "name": "FastAPI",
        "description": "A modern, fast (high-performance), web framework\
        for building APIs with Python based on standard Python type hints.",
        "language": Language.PYTHON,
    },
    {
        "name": "JavaScript",
        "description": "A scripting language, that enables you to create\
        control multimedia, animate images, and pretty much everything else",
        "language": Language.JAVASCRIPT,
    },
    {
        "name": "TypeScript",
        "description": "A typed superset of JavaScript that compiles\
        to plain JavaScript. It offers classes, modules,\
        and interfaces to help you build robust components.",
        "language": Language.TYPESCRIPT,
    },
    {
        "name": "NestJS",
        "description": "A progressive Node.js framework for building efficient\
        reliable and scalable server-side applications.",
        "language": Language.NODEJS,
    },
    {
        "name": "TypeORM",
        "description": "A traditional ORM which maps tables to model classes",
        "language": Language.NODEJS,
    },
    {
        "name": "Prisma",
        "description": "A Node.js and TypeScript ORM with an intuitive data\
        model, automated migrations, type-safety, and auto-completion",
        "language": Language.NODEJS,
    },
    {
        "name": "React",
        "description": "React lets you build user interfaces out of individual\
        pieces called components. Create your own React components",
        "language": Language.JAVASCRIPT,
    },
    {
        "name": "TanStack Query",
        "description": "A powerful asynchronous state management for TS/JS",
        "language": Language.TYPESCRIPT,
    },
    {
        "name": "Tailwind CSS",
        "description": "A utility-first CSS framework packed with classes\
        that can be composed to build any design.",
        "language": Language.CSS,
    },
    {
        "name": "Go",
        "description": "A statically typed programming language.",
        "language": Language.GO,
    },
    {
        "name": "Docker",
        "description": "Docker is a platform for developing, testing, and\
        deploying containerized applications.",
        "language": Language.GO,
    },
]
