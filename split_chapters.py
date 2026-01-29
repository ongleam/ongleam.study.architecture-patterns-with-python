#!/usr/bin/env python3
"""Split Architecture Patterns with Python markdown into separate chapter files."""

from pathlib import Path

# Chapter definitions: (start_line, end_line, filename, title)
# Lines are 1-indexed to match the file
CHAPTERS = [
    # Skip TOC (lines 1-561)
    (562, 641, "00-frontmatter.md", "Front Matter"),
    (642, 1076, "00-preface.md", "Preface"),
    (1077, 1371, "00-introduction.md", "Introduction"),
    (1372, 1447, "part1-intro.md", "Part I. Building an Architecture to Support Domain Modeling"),
    (1448, 2285, "ch01-domain-modeling.md", "Chapter 1. Domain Modeling"),
    (2286, 3134, "ch02-repository-pattern.md", "Chapter 2. Repository Pattern"),
    (3135, 3807, "ch03-coupling-and-abstractions.md", "Chapter 3. A Brief Interlude: On Coupling and Abstractions"),
    (3808, 4565, "ch04-flask-api-service-layer.md", "Chapter 4. Our First Use Case: Flask API and Service Layer"),
    (4566, 5019, "ch05-tdd-high-low-gear.md", "Chapter 5. TDD in High Gear and Low Gear"),
    (5020, 5657, "ch06-unit-of-work.md", "Chapter 6. Unit of Work Pattern"),
    (5658, 6552, "ch07-aggregates.md", "Chapter 7. Aggregates and Consistency Boundaries"),
    (6553, 6610, "part2-intro.md", "Part II. Event-Driven Architecture"),
    (6611, 7404, "ch08-events-message-bus.md", "Chapter 8. Events and the Message Bus"),
    (7405, 8255, "ch09-going-to-town-message-bus.md", "Chapter 9. Going to Town on the Message Bus"),
    (8256, 8819, "ch10-commands-command-handler.md", "Chapter 10. Commands and Command Handler"),
    (8820, 9301, "ch11-event-driven-microservices.md", "Chapter 11. Event-Driven Architecture: Using Events to Integrate Microservices"),
    (9302, 10100, "ch12-cqrs.md", "Chapter 12. Command-Query Responsibility Segregation (CQRS)"),
    (10101, 11001, "ch13-dependency-injection.md", "Chapter 13. Dependency Injection (and Bootstrapping)"),
    (11002, 11717, "epilogue.md", "Epilogue"),
    (11718, 11855, "appendix-a-summary.md", "Appendix A. Summary Diagram and Table"),
    (11856, 12255, "appendix-b-project-structure.md", "Appendix B. A Template Project Structure"),
    (12256, 12522, "appendix-c-csv-infrastructure.md", "Appendix C. Swapping Out the Infrastructure: Do Everything with CSVs"),
    (12523, 12960, "appendix-d-django.md", "Appendix D. Repository and Unit of Work Patterns with Django"),
    (12961, 13439, "appendix-e-validation.md", "Appendix E. Validation"),
    (13440, None, "index.md", "Index"),
]


def split_markdown(input_file: Path, output_dir: Path) -> None:
    """Split the markdown file into separate chapter files."""
    # Read all lines
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    output_dir.mkdir(exist_ok=True)

    for start, end, filename, title in CHAPTERS:
        # Convert to 0-indexed
        start_idx = start - 1
        end_idx = (end - 1) if end else total_lines

        # Extract chapter content
        chapter_lines = lines[start_idx:end_idx]

        # Clean up form feed characters at line starts
        cleaned_lines = []
        for line in chapter_lines:
            if line.startswith('\x0c'):  # Form feed character
                line = line[1:]
            cleaned_lines.append(line)

        # Write to file
        output_path = output_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            # Don't add header if the first line already contains the title
            first_line = cleaned_lines[0].strip() if cleaned_lines else ""
            if title not in first_line:
                f.write(f"# {title}\n\n")
            f.writelines(cleaned_lines)

        print(f"Created: {filename} ({len(cleaned_lines)} lines)")


if __name__ == "__main__":
    input_file = Path("Architecture-Patterns-with-Python.md")
    output_dir = Path("chapters")

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        exit(1)

    split_markdown(input_file, output_dir)
    print(f"\nDone! Created {len(CHAPTERS)} files in {output_dir}/")
