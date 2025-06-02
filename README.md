# Data Science Table Animation Visualizer 📊

This project is a **Manim-powered animation program** for visualizing common **table transformations**, covered in UC Berkeley's Introductory Data Science course, Data 8. It was built to generate short, animated clips that help students intuitively understand how generalized data science operations such as filtering, grouping, sorting, and selecting are carried out row by row and column by column.

## YouTube Demo
Check out some of the currently supported animations created using this tool on YouTube! -> https://www.youtube.com/playlist?list=PL6EoNR2zLle9yqCGA9fecoFuYJ5fjvB1X

## 🚀 Features

- Animates **row-level operations** such as filtering (`where`), reordering (`sort`), and grouping (`group`).
- Visualizes **column selections** and highlights cell-level changes.
- Highlights rows, columns, and cells dynamically with support for custom colors and transitions.
- Shows table transformations with clear side-by-side comparisons and smooth object tracking.
- Uses **Manim** (the animation engine behind 3Blue1Brown) for educational clarity and expressiveness.

## 🧠 Why It Exists

For the last two semesters I have been an **Undergraduate Student Instructor for UC Berkeley's Data 8, Introduction to Data Science**. For many of my students, this course was their first college-level exposure to data science and programming. This project aims to:
- Ease students into **conceptual understanding** through visual learning.
- Help instructors and TAs produce animated demos for their students.
- Increase **classroom engagement** in data science topics and presentations.

## 📦 Technologies Used

- [Manim](https://docs.manim.community/en/stable/) (Community Edition)
- Python 3.10+
- Jupyter / VS Code for development
- Data 8’s `Table` object model from `datascience` package

## 📁 Currently Supported Animations

- `.where()`: Highlights and keeps rows that match a filter condition.
- `.group()`: Highlights grouped rows by color and aggregates them.
- `.sort()`: Reorders and animates rows into sorted positions.
- `.drop()`: Drops specific column(s) to create a new table.
- `.select()`: Moves specific column(s) into a new table.
- `.take()`: Transfers selected rows by index into a new table.

## 📺 Animation Guide

1) Use the `datascience` library package to create your before and after tables.
2) Create a `TableAnimation` object (`GroupAnimation`, `SelectAnimation`, `SortAnimation`,etc.)
3) Call the `animate()` method of your `TableAnimation` object to animate rows moving from your before table to your after table.


## 🔧 To be Implemented
- All remaining table fucntions from the `datascience` library
- Interactive UI for creating animations.
- Support for DataFrame animations using the `pandas` library
