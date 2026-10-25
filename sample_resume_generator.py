"""
Script: sample_resume_generator.py
Purpose: Generates diverse sample resumes in PDF format to thoroughly test:
         - Complete match (Rohan Sharma)
         - Partial match (Priya Patel)
         - Non-match / unrelated profile (Amit Verma)
         - Blank / unreadable PDF
Uses pure Python standard PDF 1.4 byte generation (no external PDF library required).
"""

def make_pdf(filename: str, title: str, lines: list[str]):
    """Generates a standard compliant PDF file with given title and text lines."""
    header_cmd = f"BT\n/F1 15 Tf\n50 750 Td\n({title}) Tj\nET\n"
    body_cmd = "BT\n/F2 9.5 Tf\n"
    y = 728
    
    for line in lines:
        sanitized = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if any(line.startswith(h) for h in ["CAREER", "EDUCATION", "TECHNICAL", "PROJECTS", "SKILLS", "EXPERIENCE", "PROFILE"]):
            body_cmd += f"ET\nBT\n/F1 11 Tf\n50 {y} Td\n({sanitized}) Tj\nET\nBT\n/F2 9.5 Tf\n"
        else:
            body_cmd += f"50 {y} Td\n({sanitized}) Tj\n-50 -{y} Td\n"
        y -= 13.5
    body_cmd += "ET\n"

    stream_bytes = (header_cmd + body_cmd).encode("latin1")
    length = len(stream_bytes)

    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n",
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
        f"6 0 obj\n<< /Length {length} >>\nstream\n".encode("latin1") + stream_bytes + b"\nendstream\nendobj\n"
    ]

    body = b"".join(objects)
    offsets = [0]
    cur = len(b"%PDF-1.4\n")
    for obj in objects:
        offsets.append(cur)
        cur += len(obj)

    xref = f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("latin1")
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n".encode("latin1")

    trailer = f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{cur}\n%%EOF\n".encode("latin1")

    with open(filename, "wb") as f:
        f.write(b"%PDF-1.4\n" + body + xref + trailer)
    print(f"Generated: {filename}")


def make_blank_pdf(filename: str):
    """Generates an empty PDF page with 0 text content."""
    stream_bytes = b""
    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Length 0 >>\nstream\n\nendstream\nendobj\n"
    ]
    body = b"".join(objects)
    offsets = [0]
    cur = len(b"%PDF-1.4\n")
    for obj in objects:
        offsets.append(cur)
        cur += len(obj)
    xref = f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("latin1")
    for off in offsets[1:]:
        xref += f"{off:010d} 00000 n \n".encode("latin1")
    trailer = f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{cur}\n%%EOF\n".encode("latin1")
    with open(filename, "wb") as f:
        f.write(b"%PDF-1.4\n" + body + xref + trailer)
    print(f"Generated: {filename} (Empty)")


def generate_all_samples():
    # 1. Full Match Resume (Rohan Sharma -> matches Python Developer)
    rohan_lines = [
        "Email: rohan.dev@example.com | Phone: +91 98765 43210 | Location: New Delhi, India",
        "LinkedIn: linkedin.com/in/rohan-dev | GitHub: github.com/rohan-dev",
        "",
        "CAREER OBJECTIVE",
        "Enthusiastic BCA student seeking an entry-level Python Developer role to apply technical knowledge.",
        "",
        "EDUCATION",
        "- Bachelor of Computer Applications (BCA) | XYZ University (2021-2024) | CGPA: 8.4 / 10",
        "- Class XII (CBSE) | ABC School (2021) | 85%",
        "",
        "TECHNICAL SKILLS",
        "- Programming Languages: Python, C++",
        "- Web & Backend: REST APIs, FastAPI, HTML5, CSS3",
        "- Databases: MySQL, SQL, SQLite",
        "- Developer Tools: Git, GitHub, VS Code, Linux terminal basics",
        "- Core Concepts: Object-Oriented Programming (OOP), Data Structures, Unit Testing with Pytest",
        "",
        "PROJECTS",
        "1. Student Management API (Python, FastAPI, SQLite)",
        "   - Designed RESTful endpoints for student attendance and marks tracking.",
        "   - Implemented unit testing using Pytest ensuring 90% test coverage.",
        "",
        "2. Database Query Tool (Python, SQL)",
        "   - Created a CLI tool for executing relational queries and generating CSV reports.",
        "   - Applied OOP design principles with clean inheritance and encapsulation."
    ]
    make_pdf("sample_resume_match.pdf", "ROHAN SHARMA - RESUME", rohan_lines)

    # 2. Partial Match Resume (Priya Patel -> matches some skills, missing REST APIs, Git, Unit Testing)
    priya_lines = [
        "Email: priya.analytics@example.com | Phone: +91 91234 56789 | Location: Pune, India",
        "",
        "CAREER OBJECTIVE",
        "Motivated computer science student with a passion for database administration and data insights.",
        "",
        "EDUCATION",
        "- Bachelor of Computer Applications (BCA) | Pune College (2021-2024) | 78%",
        "",
        "TECHNICAL SKILLS",
        "- Languages: Python, SQL",
        "- Data Tools: Pandas, NumPy, Excel",
        "- Concepts: Database normalization, Basic statistical analysis",
        "",
        "PROJECTS",
        "1. Sales Analysis Spreadsheet (Excel, Python)",
        "   - Computed quarterly sales metrics and identified revenue trends.",
        "2. Customer Record Manager (Python, MySQL)",
        "   - Built a basic console application to store client records in MySQL database."
    ]
    make_pdf("sample_resume_partial.pdf", "PRIYA PATEL - RESUME", priya_lines)

    # 3. Non-Match Resume (Amit Verma -> Graphic Designer, 0 tech skills)
    amit_lines = [
        "Email: amit.creative@example.com | Phone: +91 99887 76655 | Location: Mumbai, India",
        "",
        "CAREER OBJECTIVE",
        "Creative graphic designer and digital illustrator seeking visual branding assignments.",
        "",
        "EDUCATION",
        "- Bachelor of Arts (Fine Arts) | Mumbai Arts Academy (2020-2023)",
        "",
        "CREATIVE SKILLS",
        "- Adobe Photoshop, Adobe Illustrator, Canva, Figma",
        "- Typography, Color Palette Selection, Logo Design, Banner Illustration",
        "",
        "EXPERIENCE",
        "- Freelance Poster & Brochure Designer for campus events and local business campaigns."
    ]
    make_pdf("sample_resume_nonmatch.pdf", "AMIT VERMA - CREATIVE RESUME", amit_lines)

    # 4. Blank PDF
    make_blank_pdf("sample_resume_blank.pdf")


if __name__ == "__main__":
    generate_all_samples()
